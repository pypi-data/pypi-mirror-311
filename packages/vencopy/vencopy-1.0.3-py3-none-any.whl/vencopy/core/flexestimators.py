__maintainer__ = "Niklas Wulff, Fabia Miorelli"
__license__ = "BSD-3-Clause"

import math
import logging

from pathlib import Path
from typing import Union

import pandas as pd

from ..utils.metadata import read_metadata_config, write_out_metadata
from ..utils.utils import create_file_name, write_out, calculate_daily_seasonal_factor


class FlexEstimator:
    def __init__(self, configs: dict, data: pd.DataFrame):
        """
        In the Flexestimator, the previously defined activities are calculated
        one after the other. A further iteration loop is executed in the outer
        iteration cycle iterative_battrey_calculation. In the inner iteration
        loop, each activity id is processed one after the other. Firstly in a
        maximum consideration, which implies that as much as possible is
        always charged according to the usage profile. The minimum profile
        is then determined, which simulates a utilisation profile in which
        only as much is charged as is needed for the next planned trips.
        The two profiles and the resulting difference in battery level serve
        as a prerequisite for starting the next outer iteration loop and
        calling up the maximum and minimum profile with adjustment of the
        start variables. The __get_delta function is used to calculate both
        a max_delta and a min_delta depending on the start/end line of the
        min/max_battery_leve_start/end. As soon as the two delta values are
        below the selected epsilon value, the iteration is interrupted.
        Finally, the auxilliary_fuel_need is calculated in the flexestimator
        from the residual_need calculated for each trip and an output
        is generated.
        More detailed information on the different functions can be found in
        the documentation.

        Args:
            configs (dict): A dictionary containing a user_config_dictionary
            and a dev_config_dictionary
            activities (pd.DataFrame): a dataframe containing all trip and
            parking activities
        """
        self.dataset = configs["user_config"]["global"]["dataset"]
        self.user_config = configs["user_config"]
        self.dev_config = configs["dev_config"]
        self.electric_consumption = self.user_config[
            "flexestimators"]["electric_consumption"]["general"]
        self.season = self.user_config[
            "global"][
                "consider_temperature_cycle_dependency"]['season']
        self.seasons = ["winter", "spring", "summer", "fall"]
        self.temperature_factors = self.user_config[
            "global"][
                "consider_temperature_cycle_dependency"]["day_night_factors"]
        self.upper_battery_level = (
            self.user_config["flexestimators"]["battery_capacity"]
            * self.user_config["flexestimators"]["maximum_soc"]
        )
        self.lower_battery_level = (
            self.user_config["flexestimators"]["battery_capacity"]
            * self.user_config["flexestimators"]["minimum_soc"]
        )
        self.CCCV = self.user_config["flexestimators"]["CCCV_limit"]
        self.data = data
        self.activities = data['activities'].copy()
        self.is_trip = ~self.activities["trip_id"].isna()
        self.is_park = ~self.activities["park_id"].isna()
        self.is_first_activity = (
            self.activities["is_first_activity"].fillna(0).astype(bool)
        )
        self.is_last_activity = (
            self.activities["is_last_activity"].fillna(0).astype(bool)
        )
        self.activities[
            [
                "max_battery_level_start",
                "max_battery_level_end",
                "min_battery_level_start",
                "min_battery_level_end",
                "max_battery_level_end_unlimited",
                "uncontrolled_charging",
                "timestamp_end_uncontrolled_charging_unlimited",
                "timestamp_end_uncontrolled_charging",
                "min_battery_level_end_unlimited",
                "max_residual_need",
                "min_residual_need",
                "max_overshoot",
                "min_undershoot",
                "max_auxiliary_fuel_need",
                "min_auxiliary_fuel_need",
                "electric_consumption"
            ]
        ] = None
        self.activities_without_residual = None

    def _drain(self):
        """
        This function calculates the electric consumption first based on the
        seasonal factor and after that the drain of a specific trip according
        to its length based on the season (if enabled).
        """
        if self.user_config[
                "global"][
                "consider_temperature_cycle_dependency"][
                "annual"] & (self.season != 'None'):
            if self.user_config[
                    "global"][
                        "consider_temperature_cycle_dependency"]["daily"]:
                self.activities[
                    'electric_consumption'] = self.activities.apply(
                    lambda row:
                    self.electric_consumption *
                    (1 + self.user_config[
                        "flexestimators"]["electric_consumption"].get(
                        row['season'] + "_factor") *
                        calculate_daily_seasonal_factor(
                            self.user_config,
                            row['season'],
                            self.user_config[
                                "flexestimators"]["electric_consumption"],
                            row['trip_start_hour']
                            )),
                    axis=1
                )
            else:
                self.activities['electric_consumption'] = self.activities[
                    'season'].apply(
                    lambda season:
                    self.electric_consumption * (
                        1 + self.user_config[
                            "flexestimators"]["electric_consumption"].get(
                            season + "_factor"
                            ))
                       )
        elif (self.user_config["global"]["consider_temperature_cycle_dependency"]["season"] in self.seasons):
            if self.user_config[
                    "global"][
                        "consider_temperature_cycle_dependency"]["daily"]:
                self.activities[
                    'electric_consumption'] = self.activities.apply(
                    lambda row:
                    self.electric_consumption *
                    (1 + self.user_config[
                        "flexestimators"]["electric_consumption"].get(
                        row['season'] + "_factor") *
                        calculate_daily_seasonal_factor(
                            self.user_config,
                            self.season,
                            self.user_config[
                                "flexestimators"]["electric_consumption"],
                            row['trip_start_hour']
                            )),
                    axis=1
                )
            else:
                self.activities[
                    'electric_consumption'] = self.electric_consumption * (
                            1 + self.user_config[
                                "flexestimators"]["electric_consumption"].get(
                                self.season + "_factor"
                                ))
        else:
            self.activities['electric_consumption'] = self.electric_consumption

        self.activities["drain"] = (
            self.activities['trip_distance']
            * self.activities['electric_consumption'] / 100
            )

    def _max_charge_volume_first_parking_activity(self, first_park_activities):
        """
        Filters for the first parking activity and assigns a maximum charge
        volume based on the start soc

        Args:
            first_park_activities (dataframe): all rows of the dataframe that
            are first parking activities

        Returns:
            dataframe: dataframe wtith first activities
        """
        first_park_activities[
            "max_charge_volume"] = first_park_activities.apply(
                lambda row: self._max_charge_volume_per_parking_activity(
                            self.CCCV,
                            self.user_config["flexestimators"]["start_soc"],
                            self.user_config[
                                "flexestimators"]["battery_capacity"],
                            row["available_power"],
                            row["time_delta"],
                            self.user_config["flexestimators"]["time_steps"]),
                axis=1
                )

        return first_park_activities

    def _min_charge_volume_last_parking_activity(self, last_park_activities):
        """
        Filters for the last activities and calculates the min_charge_volume,
        based on the minimum soc,
        that would be the soc when arriving home with the min charge
        profile behaviour

        Args:
            last_park_activities (dataframe):  all rows of the dataframe that
            are last parking activities

        Returns:
            dataframe: dataframe wtith last activities
        """
        # NOTE: macht eigentlich keinen Sinn, weil erster charge vorgang immer
        # Laden ist und für den ersten Trip nicht zwei mal geladen werden muss
        last_park_activities["min_charge_volume"] = last_park_activities.apply(
                lambda row: self._min_charge_volume_per_parking_activity(
                            self.CCCV,
                            self.user_config["flexestimators"]["minimum_soc"],
                            self.user_config["flexestimators"]["minimum_soc"],
                            self.user_config[
                                "flexestimators"]["battery_capacity"],
                            row["available_power"],
                            row["time_delta"],
                            self.user_config["flexestimators"]["time_steps"]),
                axis=1
                )

        return last_park_activities

    @staticmethod
    def _max_charge_volume_per_parking_activity(CCCV,
                                                soc,
                                                battery_size,
                                                available_power,
                                                time,
                                                time_steps):
        """
        Calculates the max charge volume, related to the start_soc.
        If the soc_start is above 0.75, charging takes place slower

        Args:
            soc (tuple): start_soc (based on previous_trip_soc_end)
            available_power (_type_): available power from grid
            time (_type_): time delta for charging

        Returns:
            max_cahrge_volume: biggest possible charging_volume based on the
            charging time and available power
        """

        time_step = time / pd.Timedelta("1 hour")/time_steps

        if available_power == 0.0:
            max_charge_volume = 0
            return max_charge_volume

        elif soc < CCCV:
            # Calculate t, when soc = soc,cccv
            soc_CC = CCCV - soc
            time_switch = soc_CC * (
                battery_size / available_power
                ) * pd.Timedelta("1 hour")
            if time_switch < time:
                max_charge_volume = (
                    available_power
                    * time_switch
                    / pd.Timedelta("1 hour")
                ) + FlexEstimator._max_charge_volume_per_parking_activity(
                    CCCV, CCCV,
                    battery_size, available_power,
                    time-time_switch, time_steps)
            else:
                max_charge_volume = (
                    available_power
                    * time
                    / pd.Timedelta("1 hour")
                )

        elif soc >= CCCV:

            # to give a start max_charge_volume:
            max_charge_volume = 0
            for i in range(0, time_steps):

                soc = soc + (
                    available_power *
                    (-4 * soc + 4) * time_step
                ) / battery_size

                # to catch very long parking ttrips that are overestimated
                # with soc above 100% after first iteration
                # max_charging_volume will be the maximum possible charge
                # volume if soc = 1 so iteration can end
                if soc > 1:
                    soc = 1
                    max_charge_volume = battery_size * (1-CCCV)
                    break
                max_charge_volume = max_charge_volume + (
                    available_power *
                    (-4 * soc + 4) * time_step
                )
            # NOTE: charging above 100% no longer possible
            # -> no unlimited charge_volume
            
        return max_charge_volume

    @staticmethod
    def _min_charge_volume_per_parking_activity(CCCV,
                                                soc_min,
                                                soc_end,
                                                battery_size,
                                                available_power,
                                                time,
                                                time_steps):
        """
        Calculates a "minimum" charge volume based on the min_soc_start from
        the the next trip. min_soc_start_trip becomes soc_end of the parking
        activity. Because soc_start of a parking activity is only
        related to known values, it can be calculated to assign a slower
        or faster charge behaviour.

        Args:
            soc_min (_type_): minimum_soc (based on user_config)
            soc_end (_type_): soc on the end of previous trip activity
            available_power (_type_): available power from grid
            time (_type_): time delta for charging

        Returns:
            min_cahrge_volume: smallest possible charging_volume based on the
            next trip needed charging
        """
        if available_power == 0.0 or soc_end == soc_min:
            min_charge_volume = 0
            return min_charge_volume

        elif round(
                (soc_end - ((time / pd.Timedelta("1 hour")
                             ) * available_power / battery_size)), 2) < CCCV:
            soc_start = soc_end - (
                time / pd.Timedelta("1 hour") * available_power / battery_size)

            if soc_start < soc_min:
                soc_start = soc_min

            # switching from CC to CV happening within the parking time
            # calculate switching point
            soc_CC = CCCV - soc_start
            time_switch = soc_CC * (
                battery_size / available_power
                ) * pd.Timedelta("1 hour")

            if time_switch < time and soc_end > CCCV:
                CV_time = time - time_switch
                # switching happens within the given time
                min_charge_volume = (
                        available_power
                        * time_switch
                        / pd.Timedelta("1 hour")
                    ) + FlexEstimator._min_charge_volume_per_parking_activity(
                        CCCV, soc_min, soc_end,
                        battery_size, available_power,
                        CV_time, time_steps)
            else:
                min_charge_volume = (
                        available_power
                        * time
                        / pd.Timedelta("1 hour")
                    )

        else:
            time_step = time / pd.Timedelta("1 hour")/time_steps

            for i in range(0, time_steps):
                soc_start = (
                    soc_end - 4 * time_step * available_power / battery_size
                    ) / (-4 * time_step * available_power / battery_size + 1)
                soc_end = soc_start

            # to give a start min_charge_volume:
            min_charge_volume = 0
            for i in range(0, time_steps):
                soc_start = soc_start + (
                    available_power *
                    (-4 * soc_start + 4) * time_step
                    ) / battery_size

                min_charge_volume = min_charge_volume + (
                    available_power *
                    (-4 * soc_start + 4) * time_step
                    )

        return min_charge_volume

    def __battery_level_max(self, start_level: float) -> pd.Series:
        """
        Calculate the maximum battery level at the beginning and end of each
        activity. This represents the case of vehicle users always connecting
        when charging is available and charging as soon as possible as fast as
        possible until the maximum battery capacity is reached. act_temp is the
        overall collector for each activity's park and trip results, that will
        then get written to self.activities at the very end.

        Args:
            start_level (float): Battery start level for first activity of the
            activity chain

        Returns:
            pd.Series: activities dataframe with updated values
            for battery levels
        """
        logging.info("Starting maximum battery level calculation.")
        logging.info("Calculating maximum battery level for first activities.")

        act_temp = self.__first_activities(start_level=start_level)

        # Start and end for all trips and parkings in between
        set_acts = range(1, int(self.activities["park_id"].max()) + 1)
        subset_trip_activities = pd.DataFrame()  # Redundant?
        for act in set_acts:  # implementable via groupby with
            # actIDs as groups?
            logging.info(f"Calculating maximum battery level for act {act}.")
            trip_rows = (self.activities["trip_id"] == act) & (
                ~self.activities["is_first_activity"]
            )
            park_rows = (self.activities["park_id"] == act) & (
                ~self.activities["is_first_activity"]
            )
            trip_activities = self.activities.loc[trip_rows, :]
            park_activities = self.activities.loc[park_rows, :]
            # Filtering for the previous park activites that have the current
            # activity as next activity
            previous_park_activities = act_temp.loc[
                (act_temp["next_activity_id"] == act) & (
                    ~act_temp["park_id"].isna()), :
            ]

            subset_trip_activities = self.__calculate_max_battery_level_trip(
                activity_id=act,
                trip_activities=trip_activities,
                previous_park_activities=previous_park_activities,
            )

            act_temp = pd.concat([act_temp, subset_trip_activities],
                                 ignore_index=True)
            previous_trip_activities = act_temp.loc[
                (act_temp["next_activity_id"] == act) & (
                    ~act_temp["trip_id"].isna()), :
            ]
            subset_park_activities = self.__calculate_max_battery_level_park(
                activity_id=act,
                park_activities=park_activities,
                previous_trip_activities=previous_trip_activities,
            )

            act_temp = pd.concat([act_temp, subset_park_activities],
                                 ignore_index=True)
            # previous_trip_activities = subset_trip_activities  # Redundant?
        self.activities = act_temp.sort_values(
            by=["unique_id", "activity_id", "trip_id"]
        )
        return self.activities.loc[
            self.activities["is_last_activity"], [
                "unique_id", "max_battery_level_end"]
        ].set_index("unique_id")

    def __battery_level_min(self, end_level: pd.Series) -> pd.Series:
        """
        Calculate the minimum battery level at the beginning and end of each
        activity. This represents the case of vehicles just being charged for
        the energy required for the next trip and as late as possible. The loop
        works exactly inverted to the batteryLevelMax() function since later
        trips influence the energy that has to be charged in parking activities
        before. Thus, activities are looped over from the last activity to
        first.

        Args:
            end_level (pd.Series): A series containing the battery_end levels
            to start the battery_level_min

        Returns:
            pd.Series: The activities dataframe with updated
            batter_level_min_end/start values
        """
        logging.info("Starting minimum battery level calculation.")
        logging.info("Calculate minimum battery level for last activities.")
        last_activities = self.__last_activities(end_level=end_level)
        act_temp = last_activities
        # Start and end for all trips and parkings starting from the last
        # activities, then looping to earlier activities
        n_act = int(self.activities["park_id"].max())
        for act in range(n_act, -1, -1):
            logging.info(f"Calculate minimum battery level for act {act}.")
            trip_rows = (self.activities["trip_id"] == act) & (
                ~self.activities["is_last_activity"]
            )
            park_rows = (self.activities["park_id"] == act) & (
                ~self.activities["is_last_activity"]
            )
            trip_activities = self.activities.loc[trip_rows, :]
            park_activities = self.activities.loc[park_rows, :]

            next_trip_activities = act_temp.loc[
                (act_temp["previous_activity_id"] == act)
                & (~act_temp["trip_id"].isna()),
                :,
            ].copy()
            if act != n_act:
                next_trip_activities[
                    "park_activity_index"] = park_activities.index
                next_trip_activities = next_trip_activities.set_index(
                    "park_activity_index")
                next_trip_activities["soc_min_start"] = next_trip_activities[
                    "min_battery_level_start"] / self.user_config[
                        "flexestimators"]["battery_capacity"]

                if park_activities.empty == False:  # noqa: E712
                    subset_park_activities = self.__calculate_min_battery_level_park(
                        activity_id=act,
                        park_activities=park_activities,
                        next_trip_activities=next_trip_activities
                    )
                    act_temp = pd.concat(
                        [act_temp, subset_park_activities], ignore_index=True)

            next_park_activities = act_temp.loc[
                (act_temp["previous_activity_id"] == act)
                & (~act_temp["park_id"].isna()),
                :,
            ]
            subset_trip_activities = self.__calculate_min_battery_level_trip(
                activity_id=act,
                trip_activities=trip_activities,
                next_park_activities=next_park_activities,
            )
            act_temp = pd.concat(
                [act_temp, subset_trip_activities], ignore_index=True)
        self.activities = act_temp.sort_values(
            by=["unique_id", "activity_id", "trip_id"], ignore_index=True
        )
        return self.activities.loc[
            self.activities["is_first_activity"],
            ["unique_id", "min_battery_level_start"],
        ].set_index("unique_id")

    def __first_activities(
            self,
            start_level: Union[float, pd.Series]
            ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        This function filters for all first activities and calls the
        _calculate_max_battery_level_first_activity function, that handels all
        first activities, parking as well as trips. If over_night_spliiting is
        activated there is an additional calculation of the battery level for
        parking activities that do not have the activity_id= 0. But due to
        overnight splitting they are first activities.

        Args:
            start_level (Union[float, pd.Series]): A float or Series that
            contains battery_levels used to start the activity calculation

        Returns:
            pd.DataFrame: updated dataframe that contains all handeld first
            activities
        """
        first_activities = self._calculate_max_battery_level_first_activity(
            start_level=start_level)
        first_parking_activities = first_activities.loc[
            ~first_activities["park_id"].isna(), :]
        first_trip_activities = first_activities.loc[(
            ~first_activities["trip_id"].isna()), :]
        first_park_activities_overnight = self.activities.loc[
                (self.activities['is_first_park_activity']) & ~(
                    self.activities['is_first_activity'])].copy()

        if self.user_config[
            'dataparsers'][
                'split_overnight_trips'
                ] & first_park_activities_overnight.empty is False:
            # Treat parking activities after morning split trips.
            # They have activitiy_id==0 but are the second activity.
            first_park_activities_overnight = self.__calculate_max_battery_level_park(
                activity_id=0,
                park_activities=first_park_activities_overnight,
                previous_trip_activities=first_trip_activities,
            )
            return pd.concat(
                [
                    first_parking_activities,
                    first_trip_activities,
                    first_park_activities_overnight,
                ]
            )
        else:
            return pd.concat([first_parking_activities, first_trip_activities])

    def _calculate_max_battery_level_first_activity(
        self, start_level: Union[float, pd.Series]
    ) -> pd.DataFrame:
        """
        Calculate maximum battery levels at beginning and end of the first
        activities. This includes first park
        activities (inferred) before first MiD trips as well as morning splits
        first trip activities. Parking activities
        after morning split trips are treated later in [ELSEWHERE].

        Args:
            start_level (Union[float, pd.Series]): Start battery level at
            beginning of simulation (MON, 00:00). Defaults
            to self.upper_battery_level, the maximum battery level.
            In iterations, this is a pandas Series with the
            respective unique_ids in the index.

        Returns:
            pd.DataFrame: First activities with all battery level columns as
            anchor for the consecutive calculation of maximum charge
        """
        # First activities - parking and trips
        first_activities = self.activities.loc[
            self.activities["is_first_activity"], :
        ].copy()

        # Needed for setting start_level at correct unique_id in iterations
        first_activities = first_activities.set_index("unique_id")
        first_activities["max_battery_level_start"] = start_level
        first_activities = first_activities.reset_index()
        first_trip_activities = self.__calc_first_trip_activities(
            first_trip_activities=first_activities.loc[
                ~first_activities["trip_id"].isna(), :].copy())

        first_activities = self._max_charge_volume_first_parking_activity(
            first_park_activities=first_activities.loc[
                ~first_activities["park_id"].isna()].copy())

        first_park_activities = self.__calc_first_park_activities(
            first_park_activities=first_activities.loc[
                ~first_activities["park_id"].isna()].copy())

        first_activities = pd.concat(
            [first_park_activities, first_trip_activities])
        return first_activities.sort_values(
            by=["unique_id"]
        )  # Only one activity per unique_id exists

    def __calc_first_park_activities(
        self, first_park_activities: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Function to handle all first parking activities. Calculates
        max_battery_level_end of this parking activity by adding the
        max_charge_volume, and the max_battery_level_end_unlimited by
        ignoring the maximum battery capycity.

        Args:
            first_park_activities (pd.DataFrame): A dataframe containing only
            first park activities from the activities dataframe

        Returns:
            pd.DataFrame: dataframe containing only first park activities with
            new updated max_battery_levels
        """
        first_park_activities.loc[:, "max_battery_level_end_unlimited"] = (
            first_park_activities["max_battery_level_start"]
            + first_park_activities["max_charge_volume"]
        )
        first_park_activities.loc[
            :, "max_battery_level_end"
        ] = first_park_activities.loc[
            :, "max_battery_level_end_unlimited"].where(
            first_park_activities.loc[:, "max_battery_level_end_unlimited"]
            <= self.upper_battery_level,
            other=self.upper_battery_level,
        )
        first_park_activities.loc[:, "max_overshoot"] = (
            first_park_activities["max_battery_level_end_unlimited"]
            - first_park_activities["max_battery_level_end"]
        )

        return first_park_activities

    def __calc_first_trip_activities(
        self, first_trip_activities: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Function that handles all first activities being a trip
        (only happening with over night splitting). Function substracts the
        drain from every max_battery_level_start of the trip and calculates
        the max_battery_level_end as well as max_battery_level_end_unlimited
        if the drain exceeds the battery capacity and there fore residual
        need will result.

        Args:
            first_trip_activities (pd.DataFrame): dataframe containing only
            first trip activities

        Returns:
            pd.DataFrame: dataframe containing only first trip activities with
            new calculated max_battery_level_end
        """
        first_trip_activities.loc[:, "max_battery_level_end_unlimited"] = (
            first_trip_activities.loc[:, "max_battery_level_start"]
            - first_trip_activities.loc[:, "drain"]
        )
        first_trip_activities.loc[
            :, "max_battery_level_end"
        ] = first_trip_activities.loc[
            :, "max_battery_level_end_unlimited"].where(
            first_trip_activities.loc[:, "max_battery_level_end_unlimited"]
            >= self.lower_battery_level,
            other=self.lower_battery_level,
        )
        res = (
            first_trip_activities.loc[:, "max_battery_level_end"]
            - first_trip_activities.loc[:, "max_battery_level_end_unlimited"]
        )
        first_trip_activities.loc[:, "max_residual_need"] = res.where(
            first_trip_activities.loc[:, "max_battery_level_end_unlimited"]
            < self.lower_battery_level,
            other=0,
        )

        return first_trip_activities

    def __last_activities(self, end_level: pd.Series) -> pd.DataFrame:
        """
        Calculate the minimum battery levels for the last activity in the
        dataset determined by the maximum activity
        ID.

        Args:
            end_level (float or pd.Series): End battery level at end of
            simulation time (last_bin). Defaults to
            self.lower_battery_level, the minimum battery level. Can be either
            of type float (in first iteration) or
            pd.Series with respective unique_id in the index.

        Returns:
            pd.DataFrame: Activity data set with the battery variables set for
            all last activities of the activity chains
        """
        # Last activities - parking and trips
        last_activities_in = self.activities.loc[
            self.activities["is_last_activity"], :
        ].copy()
        is_trip = ~last_activities_in["trip_id"].isna()

        indeces_last_activities = last_activities_in.set_index("unique_id")
        indeces_last_activities["min_battery_level_end"] = end_level
        indeces_last_activities.loc[
            indeces_last_activities["trip_id"].isna(),
            "min_battery_level_start"
        ] = end_level  # For park activities

        self._min_charge_volume_last_parking_activity(
            indeces_last_activities.loc[
                indeces_last_activities["trip_id"].isna()])

        last_activities = indeces_last_activities.reset_index("unique_id")
        last_activities.index = last_activities_in.index

        last_activities.loc[is_trip, "min_battery_level_start_unlimited"] = (
            last_activities.loc[is_trip, "min_battery_level_end"]
            + last_activities.loc[is_trip, "drain"]
        )
        last_activities.loc[
            is_trip, "min_battery_level_start"] = last_activities.loc[
            is_trip, "min_battery_level_start_unlimited"
        ].where(
            last_activities.loc[is_trip, "min_battery_level_start_unlimited"]
            <= self.upper_battery_level,
            other=self.upper_battery_level,
        )
        residual_need = (
            last_activities.loc[is_trip, "min_battery_level_start_unlimited"]
            - self.upper_battery_level
        )
        last_activities.loc[
            is_trip, "min_residual_need"] = residual_need.where(
            residual_need >= 0, other=0
        ).astype(float)
        return last_activities

    def __calculate_max_battery_level_trip(
        self,
        activity_id: int,
        trip_activities: pd.DataFrame,
        previous_park_activities: pd.DataFrame = None,
    ) -> pd.DataFrame:
        """
        Function that handles activities with current trip_id= act. Function
        substracts the drain from every max_battery_level_start that is based
        on the previous parking (charging) activity of the trip and calculates
        the max_battery_level_end as well as max_battery_level_end_unlimited
        if the drain exceeds the battery capacity and there fore residual need
        will result.

        Args:
            activity_id (int): the current id of activity that is handeld
            trip_activities (pd.DataFrame): dataframe that contains all trips
            with trip_id = current act
            previous_park_activities (pd.DataFrame, optional):
            dataframe that stores all previous park activities that have
            same act_id as the current trip_id

        Returns:
            pd.DataFrame: _description_
        """
        # Index setting of trip activities to be updated
        active_unique_ids = trip_activities.loc[:, "unique_id"]
        multi_index_trip = [
            (id, activity_id, None) for id in active_unique_ids]
        indeces_trip_activities = trip_activities.set_index(
            ["unique_id", "trip_id", "park_id"]
        )
        # Index setting of previous park activities as basis for the update
        previous_park_ids = trip_activities.loc[:, "previous_activity_id"]
        multi_index_park = [
            (id, None, act) for id, act in zip(
                active_unique_ids, previous_park_ids)
        ]
        indeces_previous_park_activities = previous_park_activities.set_index(
            ["unique_id", "trip_id", "park_id"]
        )
        # Calculation of battery level at start and end of trip
        indeces_trip_activities.loc[
            multi_index_trip, "max_battery_level_start"] = (
            indeces_previous_park_activities.loc[
                multi_index_park, "max_battery_level_end"
            ].values
        )
        indeces_trip_activities.loc[
            multi_index_trip, "max_battery_level_end_unlimited"
        ] = (
            indeces_trip_activities.loc[
                multi_index_trip, "max_battery_level_start"]
            - indeces_trip_activities.loc[multi_index_trip, "drain"]
        )
        indeces_trip_activities.loc[
            multi_index_trip, "max_battery_level_end"
        ] = indeces_trip_activities.loc[
            multi_index_trip, "max_battery_level_end_unlimited"
        ].where(
            indeces_trip_activities.loc[
                multi_index_trip, "max_battery_level_end_unlimited"
            ]
            >= self.lower_battery_level,
            other=self.lower_battery_level,
        )
        res = (
            indeces_trip_activities.loc[
                multi_index_trip, "max_battery_level_end"]
            - indeces_trip_activities.loc[
                multi_index_trip, "max_battery_level_end_unlimited"
            ]
        )
        indeces_trip_activities.loc[
            multi_index_trip, "max_residual_need"] = res.where(
            indeces_trip_activities.loc[
                multi_index_trip, "max_battery_level_end_unlimited"
            ]
            < self.lower_battery_level,
            other=0,
        )
        return indeces_trip_activities.reset_index()

    def __calculate_min_battery_level_trip(
        self,
        activity_id: int,
        trip_activities: pd.DataFrame,
        next_park_activities: pd.DataFrame = None,
    ) -> pd.DataFrame:
        """
        Function that handles activities with current trip_id= act. Function
        adds the drain from on every min_battery_level_end, based on the
        min_battery_level_start of the next parking activity of the trip
        and calculates the min_battery_level_start as well as
        min_battery_level_start_unlimited if the drain exceeds the battery
        capacity and therefore residual need will result.

        Args:
            activity_id (int): _description_
            trip_activities (pd.DataFrame): _description_
            next_park_activities (pd.DataFrame, optional): _description_.
            Defaults to None.

        Returns:
            pd.DataFrame: _description_
        """
        active_unique_ids = trip_activities.loc[:, "unique_id"]
        multi_index_trip = [
            (id, activity_id, None) for id in active_unique_ids]
        indeces_trip_activities = trip_activities.set_index(
            ["unique_id", "trip_id", "park_id"]
        )

        next_park_ids = trip_activities.loc[:, "next_activity_id"]
        multi_index_park = [
            (id, None, act) for id, act in zip(
                active_unique_ids, next_park_ids)
        ]
        indeces_next_park_activities = next_park_activities.set_index(
            ["unique_id", "trip_id", "park_id"]
        )
        indeces_trip_activities.loc[
            multi_index_trip, "min_battery_level_end"] = (
            indeces_next_park_activities.loc[
                multi_index_park, "min_battery_level_start"
            ].values
        )

        # Setting minimum battery end level for trip
        indeces_trip_activities.loc[
            multi_index_trip, "min_battery_level_start_unlimited"
        ] = (
            indeces_trip_activities.loc[
                multi_index_trip, "min_battery_level_end"]
            + indeces_trip_activities.loc[multi_index_trip, "drain"]
        )
        indeces_trip_activities.loc[
            multi_index_trip, "min_battery_level_start"
        ] = indeces_trip_activities.loc[
            multi_index_trip, "min_battery_level_start_unlimited"
        ].where(
            indeces_trip_activities.loc[
                multi_index_trip, "min_battery_level_start_unlimited"
            ]
            <= self.upper_battery_level,
            other=self.upper_battery_level,
        )
        residual_need = (
            indeces_trip_activities.loc[
                multi_index_trip, "min_battery_level_start_unlimited"
            ]
            - self.upper_battery_level
        )
        indeces_trip_activities.loc[multi_index_trip, "min_residual_need"] = (
            residual_need.where(residual_need >= 0, other=0)
        )
        return indeces_trip_activities.reset_index()

    def __calculate_max_battery_level_park(
        self,
        activity_id: int,
        park_activities: pd.DataFrame,
        previous_trip_activities: pd.DataFrame = None,
    ) -> pd.DataFrame:
        """
        Calculate the maximum battery level of the given
        parking activities for the activity ID given by activity_id.
        Previous trip activities are used as boundary for
        max_battery_level_start. This function is called multiple
        times once per activity ID. It is then applied to all activities
        with the given activity ID in a vectorized
        manner.

        Args:
            activity_id (int): Activity ID in current loop
            park_activities (pd.DataFrame): _description_
            previous_trip_activities (pd.DataFrame, optional): _description_.
            Defaults to None.

        Returns:
            pd.DataFrame: Park activities with maximum battery level columns.
        """

        park_activities = park_activities.set_index(["unique_id"])
        indeces_previous_trip_activities = previous_trip_activities.set_index(
            ["unique_id"])
        park_activities["soc_max_start"] = indeces_previous_trip_activities[
            "max_battery_level_end"] / self.upper_battery_level
        park_activities["max_charge_volume"] = park_activities.apply(
                lambda row: self._max_charge_volume_per_parking_activity(
                        self.CCCV,
                        row["soc_max_start"],
                        self.upper_battery_level,
                        row["available_power"],
                        row["time_delta"],
                        self.user_config["flexestimators"]["time_steps"]
                        ), axis=1
                )

        park_activities = park_activities.reset_index()
        # Index setting of park activities to be updated
        active_unique_ids = park_activities.loc[:, "unique_id"]
        multi_index_park = [
            (id, None, activity_id) for id in active_unique_ids]
        indeces_park_activities = park_activities.set_index(
            ["unique_id", "trip_id", "park_id"]
        )

        # Index setting of previous trip activities used to update
        previous_trip_ids = park_activities.loc[:, "previous_activity_id"]
        multi_index_trip = [
            (id, act, None) for id, act in zip(active_unique_ids,
                                               previous_trip_ids)
        ]
        indeces_previous_trip_activities = previous_trip_activities.set_index(
            ["unique_id", "trip_id", "park_id"]
        )

        # Calculation of battery level at start and end of park activity
        indeces_park_activities.loc[
            multi_index_park, "max_battery_level_start"] = (
            indeces_previous_trip_activities.loc[
                multi_index_trip, "max_battery_level_end"
            ].values
        )
        indeces_park_activities["max_battery_level_end_unlimited"] = (
            indeces_park_activities.loc[
                multi_index_park, "max_battery_level_start"]
            + indeces_park_activities.loc[
                multi_index_park, "max_charge_volume"]
        )
        indeces_park_activities.loc[
            multi_index_park, "max_battery_level_end"
        ] = indeces_park_activities["max_battery_level_end_unlimited"].where(
            indeces_park_activities["max_battery_level_end_unlimited"]
            <= self.upper_battery_level,
            other=self.upper_battery_level,
        )
        temporary_overshoot = (
            indeces_park_activities["max_battery_level_end_unlimited"]
            - self.upper_battery_level
        )
        indeces_park_activities["max_overshoot"] = temporary_overshoot.where(
            temporary_overshoot >= 0, other=0
        )
        return indeces_park_activities.reset_index()

    def __calculate_min_battery_level_park(
        self,
        activity_id: int,
        park_activities: pd.DataFrame,
        next_trip_activities: pd.DataFrame = None,
    ) -> pd.DataFrame:
        """
        Calculate minimum battery levels for given parking activities based on
        the given next trip activities.
        The calculated battery levels only suffice for the trips and thus
        describe a technical lower level for
        each activity. This function is called looping through the parking
        activities from largest to smallest.
        The column "minOvershoot" describes electricity volume that can be
        charged beyond the given batterycapacity.

        Args:
            activity_id (int): _description_
            park_activities (pd.DataFrame): _description_
            next_trip_activities (pd.DataFrame, optional): _description_.
            Defaults to None.

        Returns:
            _type_: _description_
        """
        # match next_trip_index unique_id with park_activities index unique_id
        park_activities = park_activities.set_index(["unique_id"])
        next_trip_activities = next_trip_activities.set_index(["unique_id"])

        park_activities["soc_min_end"] = next_trip_activities[
            "min_battery_level_start"]/self.upper_battery_level
        park_activities["min_charge_volume"] = park_activities.apply(
                lambda row: self._min_charge_volume_per_parking_activity(
                        self.CCCV,
                        self.user_config["flexestimators"]["minimum_soc"],
                        row["soc_min_end"],
                        self.upper_battery_level,
                        row["available_power"],
                        row["time_delta"],
                        self.user_config["flexestimators"]["time_steps"]
                        ), axis=1
            )

        park_activities = park_activities.reset_index()
        next_trip_activities = next_trip_activities.reset_index()
        # Composing park activity index to be set
        active_unique_ids = park_activities.loc[:, "unique_id"]
        multi_index_park = [
            (id, None, activity_id) for id in active_unique_ids]
        indeces_park_activities = park_activities.set_index(
            ["unique_id", "trip_id", "park_id"]
        )
        # Composing trip activity index to get battery level from
        next_trip_ids = park_activities.loc[:, "next_activity_id"]
        multi_index_trip = [
            (id, act, None) for id, act in zip(
                active_unique_ids,
                next_trip_ids
                )
        ]
        indeces_next_trip_activities = next_trip_activities.set_index(
            ["unique_id", "trip_id", "park_id"]
        )

        indeces_park_activities.loc[
            multi_index_park,
            "min_battery_level_end"] = (
            indeces_next_trip_activities.loc[
                multi_index_trip, "min_battery_level_start"
            ].values
        )
        indeces_park_activities["min_battery_level_start_unlimited"] = (
                indeces_park_activities.loc[
                    multi_index_park,
                    "min_battery_level_end"]
                - indeces_park_activities.loc[
                    multi_index_park,
                    "min_charge_volume"]
        )
        indeces_park_activities.loc[
            multi_index_park, "min_battery_level_start"
        ] = indeces_park_activities["min_battery_level_start_unlimited"].where(
            indeces_park_activities["min_battery_level_start_unlimited"]
            >= self.lower_battery_level,
            other=self.lower_battery_level,
        )
        temporary_undershoot = (
            indeces_park_activities["min_battery_level_start_unlimited"]
            - self.lower_battery_level
        )
        indeces_park_activities["min_undershoot"] = temporary_undershoot.where(
            temporary_undershoot >= 0, other=0
        )
        return indeces_park_activities.reset_index()

    def _uncontrolled_charging(self):
        """
        calculates the difference between the start and end level of a battery
        resuting in the realistic value of energy
        that was charged into the battery
        """
        park_activities = self.activities.loc[
            self.activities["trip_id"].isna(), :
        ].copy()
        park_activities["uncontrolled_charging"] = (
            park_activities["max_battery_level_end"]
            - park_activities["max_battery_level_start"]
        )
        # Calculate timestamp at which charging ends disregarding parking end
        park_activities[
            "timestamp_end_uncontrolled_charging_unlimited"
            ] = park_activities.apply(
            lambda x: self._calculate_charging_end_timestamp(
                start_timestamp=x["timestamp_start"],
                start_battery_level=x["max_battery_level_start"],
                power=x["available_power"],
            ),
            axis=1,
        )

        # Take into account possible earlier disconnection due
        # to end of parking
        park_activities[
            "timestamp_end_uncontrolled_charging"
            ] = park_activities[
            "timestamp_end_uncontrolled_charging_unlimited"
        ].where(
            park_activities["timestamp_end_uncontrolled_charging_unlimited"]
            <= park_activities["timestamp_end"],
            other=park_activities["timestamp_end"],
        )

        self.activities.loc[
            self.activities["trip_id"].isna(), :] = park_activities

    def _calculate_charging_end_timestamp(
        self,
        start_timestamp: pd.Timestamp,
        start_battery_level: float,
        power: float
    ) -> pd.Timestamp:
        """
        Function calculates an end_timp_stamp where the realistic charging has
        stopped for the specific parking act. This can be due to the battery
        being full or the vehcile taking its next trip and is therefore being
        plugged off the grid.

        Args:
            start_timestamp (pd.Timestamp): timestamp where the charging
            process begins
            start_battery_level (float): battery level at te start timestamp
            power (float): available power for the individual parking activity
            based on the grid

        Returns:
            pd.Timestamp: dataframe containing all end timestamps for each
            charging activity
        """
        #TODO: check if correct
        if power == 0:
            return pd.NA
        else:
            delta_battery_level = self.upper_battery_level-start_battery_level

            if start_battery_level/self.user_config["flexestimators"][
                    "battery_capacity"] < self.CCCV:
                time_for_charge = delta_battery_level / power  # in hours
            else:
                time_for_charge = delta_battery_level / (
                    power * (
                        -4 * (
                            start_battery_level/self.user_config[
                                "flexestimators"]["battery_capacity"]
                                ) + 4
                                )
                            )
            return start_timestamp + pd.Timedelta(value=time_for_charge,
                                                  unit="h").round(freq="s")

    def _auxiliary_fuel_need(self):
        """
        Function calculates the auxiliary fuel needed for the trips that
        cannot be fulfilled purely by energy stored in
        the battery. E.g. if the sum of all trips requires 55 kWh and there
        is no charging available but the battery
        capacity is set to 50 kWh, 5 kWh will be required from auxiliary fuel.
        The difference between the variables
        max_auxiliary_fuel_need and min_auxiliary_fuel_need is negligible and
        occurs in edge cases with very specific
        chains of charging availabilities and trips. If the option
        "filter_fuel_need" is set to True in the
        flexestimator section of the user_config, both variables are used in
        FlexEstimator._filter_residual_need()
        to drop trips where auxiliary fuel is needed.
        """
        self.activities["max_auxiliary_fuel_need"] = (
            self.activities["max_residual_need"]
            * self.user_config["flexestimators"]["fuel_consumption"]
            / self.activities["electric_consumption"]
        )

        self.activities["min_auxiliary_fuel_need"] = (
            self.activities["min_residual_need"]
            * self.user_config["flexestimators"]["fuel_consumption"]
            / self.activities["electric_consumption"]
        )

    def _filter_residual_need(
        self, activities: pd.DataFrame, index_columns: list
    ) -> pd.DataFrame:
        """
        Filter out days (uniqueIDs) that require additional fuel, i.e. for
        which the trip distance cannot be
        completely be fulfilled with the available charging power.
        Since additional fuel for a single trip motivates
        filtering out the whole vehicle, index_columns defines the columns
        that make up one vehicle. If index_columns is
        ['unique_id'], all uniqueIDs that have at least one trip requiring
        fuel are disregarded. If index_columns is
        ['category_id', 'week_id'] each unique combination of category_id and
        week_id (each "week") for which fuel is
        required in at least one trip is disregarded.

        Args:
            activities (pd.DataFrame): Activities data set containing at least
            the columns 'unique_id' and
                'max_residual_need'
            index_columns (list): Columns that define a "day", i.e. all unique
            combinations where at least one activity
                requires residual fuel are disregarded.
        """
        indeces_activities = activities.set_index(index_columns)
        indeces_out = (~indeces_activities["max_residual_need"].isin([None, 0]
                                                                     )) | (
            ~indeces_activities["min_residual_need"].isin([None, 0])
        )

        if len(index_columns) == 1:
            category_week_ids_out = indeces_activities.index[indeces_out]
            activities_filter = indeces_activities.loc[
                ~indeces_activities.index.isin(category_week_ids_out)
            ]
        else:
            category_week_ids_out = activities.loc[indeces_out.values,
                                                   index_columns]
            filter = category_week_ids_out.apply(
                lambda x: tuple(x), axis=1).unique()
            activities_filter = indeces_activities.loc[
                ~indeces_activities.index.isin(filter), :
            ]
        return activities_filter.reset_index()

    def __write_output(self):
        """
        Writes the output of the flexestimator calculation to the specified
        disk path
        """
        if self.user_config["global"]["write_output_to_disk"]["flex_output"]:
            root = Path(self.user_config[
                "global"]["absolute_path"]["vencopy_root"])
            folder = self.dev_config["global"]["relative_path"]["flex_output"]
            file_name = create_file_name(
                user_config=self.user_config,
                dev_config=self.dev_config,
                file_name_id="output_flexestimator",
                dataset=self.dataset,
            )
            write_out(data=self.activities, path=root / folder / file_name)
            self._write_metadata(file_name=root / folder / file_name)

    def generate_metadata(self, metadata_config, file_name):
        metadata_config["name"] = file_name
        metadata_config["title"] = "National Travel Survey activities dataframe"
        metadata_config["description"] = "Trips and parking activities from venco.py including profiles representing the available charging power, an uncontrolled charging profile, the battery drain, and the maximum and minum battery level."
        metadata_config["sources"] = [f for f in metadata_config["sources"] if f["title"] in self.dataset]
        reference_resource = metadata_config["resources"][0]
        this_resource = reference_resource.copy()
        this_resource["name"] = file_name.rstrip(".csv")
        this_resource["path"] = file_name
        these_fields = [f for f in reference_resource["schema"][self.dataset]["fields"]["flexestimators"] if f["name"] in self.activities.columns]
        this_resource["schema"] = {"fields": these_fields}
        metadata_config["resources"].pop()
        metadata_config["resources"].append(this_resource)
        return metadata_config

    def _write_metadata(self, file_name):
        metadata_config = read_metadata_config()
        class_metadata = self.generate_metadata(metadata_config=metadata_config, file_name=file_name.name)
        write_out_metadata(metadata_yaml=class_metadata, file_name=file_name.as_posix().replace(".csv", ".metadata.yaml"))

    def __iterative_battery_level_calculation(
        self,
        max_iteration: int,
        epsilon: float,
        battery_capacity: float,
        number_vehicles: int,
    ):
        """
        A single iteration of calculation maximum battery levels, uncontrolled charging and minimum battery levels
        for each trip. Initial battery level for first iteration loop per unique_id in index. Start battery level will
        be set to end battery level consecutively. Function operates on class attribute self.activities.

        Args:
            max_iteration (int): Maximum iteration limit if epsilon threshold is never reached.
            epsilon (float): Share of total aggregated battery fleet capacity (e.g. 0.01 for 1% would relate to a
                threshold of 100 Wh per car for a 10 kWh battery capacity.)
            battery_capacity (float): Average nominal battery capacity per vehicle in kWh.
            number_vehicles (int): Number of vehicles in the empiric mobility pattern data set.
        """
        max_battery_level_end = (
            self.upper_battery_level * self.user_config["flexestimators"]["start_soc"]
        )
        min_battery_level_start = self.lower_battery_level
        absolute_epsilon = int(
            self.__absolute_epsilon(
                epsilon=epsilon,
                battery_capacity=battery_capacity,
                number_vehicles=number_vehicles,
            )
        )

        max_battery_level_end = self.__battery_level_max(
            start_level=max_battery_level_end
        )
        self._uncontrolled_charging()
        min_battery_level_start = self.__battery_level_min(
            end_level=min_battery_level_start
        )

        max_delta = self.__get_delta(
            start_column="max_battery_level_start", end_column="max_battery_level_end"
        )
        min_delta = self.__get_delta(
            start_column="min_battery_level_start", end_column="min_battery_level_end"
        )

        logging.info(
            f"Finished iteration {1} / {max_iteration}. Delta max battery level is {int(max_delta)}, delta min "
            f"battery level is {int(min_delta)} and threshold epsilon is {absolute_epsilon}."
        )

        for i in range(1, max_iteration + 1):
            if max_delta < absolute_epsilon and min_delta < absolute_epsilon:
                break

            elif max_delta >= absolute_epsilon:
                max_battery_level_end = self.__battery_level_max(
                    start_level=max_battery_level_end
                )
                self._uncontrolled_charging()
                max_delta = self.__get_delta(
                    start_column="max_battery_level_start",
                    end_column="max_battery_level_end",
                )

            else:
                min_battery_level_start = self.__battery_level_min(
                    end_level=min_battery_level_start
                )
                min_delta = self.__get_delta(
                    start_column="min_battery_level_start",
                    end_column="min_battery_level_end",
                )

            logging.info(
                f"Finished iteration {i} / {max_iteration}. Delta max battery level is {int(max_delta)}, delta min "
                f"battery level is {int(min_delta)} and threshold epsilon is {absolute_epsilon}."
            )

    def __absolute_epsilon(
        self, epsilon: float, battery_capacity: float, number_vehicles: int
    ) -> float:
        """
        Calculates the absolute threshold of battery level deviatiation (delta in kWh for the whole fleet)
        used for interrupting the battery level calculation iterations.

        Args:
            epsilon (float): Share of total aggregated battery fleet capacity (e.g. 0.01 for 1% would relate to a
                threshold of 100 Wh per car for a 10 kWh battery capacity.)
            batteryCapacity (float): Average battery capacity per car
            number_vehicles (int): Number of vehicles

        Returns:
            float: Absolute iteration threshold in kWh of fleet battery
        """
        return epsilon * battery_capacity * number_vehicles

    def __get_delta(self, start_column: str, end_column: str) -> float:
        """
        Function calculates an absolute delta from the column max/min_battery_level_end of all last activies and the column max/min_battery_level_start of all first activities.

        Args:
            start_column (str): name of start_column to call (max/min_battery_level_start) 
            end_column (str): name of end column to call (max/min_battery_level_end)

        Returns:
            float: absolute delta
        """
        delta = abs(
            self.activities.loc[self.activities["is_last_activity"], end_column].values
            - self.activities.loc[
                self.activities["is_first_activity"], start_column
            ].values
        ).sum()
        return delta

    def estimate_technical_flexibility_no_boundary_constraints(self) -> pd.DataFrame:
        """
        Main run function for the class WeekFlexEstimator. Calculates uncontrolled charging as well as technical
        boundary constraints for controlled charging and feeding electricity back into the grid on an indvidiual vehicle
        basis. If filter_fuel_need is True, only electrifiable days are considered.

        Returns:
            pd.DataFrame: Activities data set comprising uncontrolled charging and flexible charging constraints for
            each car.
        """
        self._drain()
        self.__battery_level_max(start_level=self.upper_battery_level * self.user_config["flexestimators"]["start_soc"])
        self._uncontrolled_charging()
        self.__battery_level_min()
        self._auxiliary_fuel_need()
        if self.user_config["flexestimators"]["filter_fuel_need"]:
            self.activities = self._filter_residual_need(
                activities=self.activities, index_columns=["unique_id"]
            )
        if self.user_config["global"]["write_output_to_disk"]["flex_output"]:
            self.__write_output()
        logging.info("Technical flexibility estimation ended.")
        return self.activities

    @staticmethod
    def _cleanup_dataset(activities):
        activities.drop(
            columns=['max_battery_level_end',
                     'min_battery_level_start',
                     'max_battery_level_end_unlimited',
                     'max_battery_level_end_unlimited',
                     'timestamp_end_uncontrolled_charging_unlimited',
                     'min_battery_level_end_unlimited',
                     'min_battery_level_end_unlimited',
                     'max_residual_need',
                     'min_residual_need',
                     'max_overshoot',
                     'min_undershoot',
                     # 'auxiliary_fuel_need',
                     'max_charge_volume',
                     'min_battery_level_start_unlimited'], inplace=True)
        return activities

    def estimate_technical_flexibility_through_iteration(self) -> pd.DataFrame:
        """
        Main run function for the class WeekFlexEstimator. Calculates uncontrolled charging as well as technical
        boundary constraints for controlled charging and feeding electricity back into the grid on an indvidiual vehicle
        basis. If filter_fuel_need is True, only electrifiable days are considered.

        Returns:
            pd.DataFrame: Activities data set comprising uncontrolled charging and flexible charging constraints for
            each car.
        """
        self._drain()
        self.__iterative_battery_level_calculation(
            max_iteration=self.user_config["flexestimators"]["max_iterations"],
            epsilon=self.user_config["flexestimators"]["epsilon_battery_level"],
            battery_capacity=self.upper_battery_level,
            number_vehicles=len(self.activities["unique_id"].unique()),
        )
        self._auxiliary_fuel_need()
        if self.user_config["flexestimators"]["filter_fuel_need"]:
            self.activities = self._filter_residual_need(activities=self.activities, index_columns=["unique_id"])
        self.activities = self._cleanup_dataset(activities=self.activities)
        if self.user_config["global"]["write_output_to_disk"]["flex_output"]:
            self.__write_output()
        logging.info("Technical flexibility estimation ended.")
        self.data['activities'] = self.activities
        return self.data

