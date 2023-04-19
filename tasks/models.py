
import datetime
from typing import (
    List
    , Optional
)
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase
    , Mapped
    , mapped_column
    , relationship
)
from sqlalchemy import (
    Column
    , String
    , MetaData
    , Integer
    , DateTime
    , Boolean
    , Float
)

class Base(DeclarativeBase):
    pass

class OverviewFact(Base):
    __tablename__ = 'raw_overview_facts'

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, unique=True)

    user_profile_id: Mapped[int]
    user_fullname: Mapped[str]
    total_kilocalories: Mapped[Optional[float]]
    active_kilocalories: Mapped[Optional[float]]
    bmr_kilocalories: Mapped[Optional[float]]
    wellness_kilocalories: Mapped[Optional[float]]
    total_steps: Mapped[Optional[int]]
    total_distance_meters: Mapped[Optional[int]]
    wellness_distance_meters: Mapped[Optional[int]]
    wellness_active_kilocalories: Mapped[Optional[float]]
    daily_step_goal: Mapped[Optional[int]]
    highly_active_seconds: Mapped[Optional[int]]
    active_seconds: Mapped[Optional[int]]
    sedentary_seconds: Mapped[Optional[int]]
    sleeping_seconds: Mapped[Optional[int]]
    moderate_intensity_minutes: Mapped[Optional[int]]
    vigorous_intensity_minutes: Mapped[Optional[int]]
    floors_ascended_in_meters: Mapped[Optional[float]]
    floors_descended_in_meters: Mapped[Optional[float]]
    intensity_minutes_goal: Mapped[Optional[int]]
    min_heart_rate: Mapped[Optional[int]]
    max_heart_rate: Mapped[Optional[int]]
    resting_heart_rate: Mapped[Optional[int]]
    max_stress_level: Mapped[Optional[int]]
    average_stress_level: Mapped[Optional[int]]
    stress_duration: Mapped[Optional[int]]
    rest_stress_duration: Mapped[Optional[int]]
    activity_stress_duration: Mapped[Optional[int]]
    uncategorized_stress_duration: Mapped[Optional[int]]
    total_stress_duration: Mapped[Optional[int]]
    low_stress_duration: Mapped[Optional[int]]
    medium_stress_duration: Mapped[Optional[int]]
    high_stress_duration: Mapped[Optional[int]]
    stress_qualifier: Mapped[Optional[str]]
    body_battery_charged_value: Mapped[Optional[int]]
    body_battery_drained_value: Mapped[Optional[int]]
    body_battery_highest_value: Mapped[Optional[int]]
    body_battery_lowest_value: Mapped[Optional[int]]
    average_spo2: Mapped[Optional[float]]
    lowest_spo2: Mapped[Optional[int]]
    avg_waking_respiration_value: Mapped[Optional[float]]
    highest_respiration_value: Mapped[Optional[float]]
    lowest_respiration_value: Mapped[Optional[float]]
    weight: Mapped[Optional[float]]
    bmi: Mapped[Optional[float]]
    metabolic_age: Mapped[Optional[int]]

    def __repr__(self) -> str:
        return f"""
        OverviewFact(
            id={self.id}
            timestamp={self.timestamp}
            user_profile_id={self.user_profile_id}
            user_fullname={self.user_fullname}
            total_kilocalories={self.total_kilocalories}
            active_kilocalories={self.active_kilocalories}
            bmr_kilocalories={self.bmr_kilocalories}
            wellness_kilocalories={self.wellness_kilocalories}
            total_steps={self.total_steps}
            total_distance_meters={self.total_distance_meters}
            wellness_distance_meters={self.wellness_distance_meters}
            wellness_active_kilocalories={self.wellness_active_kilocalories}
            daily_step_goal={self.daily_step_goal}
            highly_active_seconds={self.highly_active_seconds}
            active_seconds={self.active_seconds}
            sedentary_seconds={self.sedentary_seconds}
            sleeping_seconds={self.sleeping_seconds}
            moderate_intensity_minutes={self.moderate_intensity_minutes}
            vigorous_intensity_minutes={self.vigorous_intensity_minutes}
            floors_ascended_in_meters={self.floors_ascended_in_meters}
            floors_descended_in_meters={self.floors_descended_in_meters}
            intensity_minutes_goal={self.intensity_minutes_goal}
            min_heart_rate={self.min_heart_rate}
            max_heart_rate={self.max_heart_rate}
            resting_heart_rate={self.resting_heart_rate}
            max_stress_level={self.max_stress_level}
            average_stress_level={self.average_stress_level}
            stress_duration={self.stress_duration}
            rest_stress_duration={self.rest_stress_duration}
            activity_stress_duration={self.activity_stress_duration}
            uncategorized_stress_duration={self.uncategorized_stress_duration}
            total_stress_duration={self.total_stress_duration}
            low_stress_duration={self.low_stress_duration}
            medium_stress_duration={self.medium_stress_duration}
            high_stress_duration={self.high_stress_duration}
            stress_qualifier={self.stress_qualifier}
            body_battery_charged_value={self.body_battery_charged_value}
            body_battery_drained_value={self.body_battery_drained_value}
            body_battery_highest_value={self.body_battery_highest_value}
            body_battery_lowest_value={self.body_battery_lowest_value}
            average_spo2={self.average_spo2}
            lowest_spo2={self.lowest_spo2}
            avg_waking_respiration_value={self.avg_waking_respiration_value}
            highest_respiration_value={self.highest_respiration_value}
            lowest_respiration_value={self.lowest_respiration_value}
            weight={self.weight}
            bmi={self.bmi}
            metabolic_age={self.metabolic_age}
        )
        """

class SleepFact(Base):
    __tablename__ = 'raw_sleep_facts'

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, unique=True)
    user_profile_p_k: Mapped[int]
    sleep_time_seconds: Mapped[Optional[int]]
    nap_time_seconds: Mapped[Optional[int]]
    unmeasurable_sleep_seconds: Mapped[Optional[int]]
    deep_sleep_seconds: Mapped[Optional[int]]
    light_sleep_seconds: Mapped[Optional[int]]
    rem_sleep_seconds: Mapped[Optional[int]]
    awake_sleep_seconds: Mapped[Optional[int]]
    average_sp_o2_value: Mapped[Optional[float]]
    lowest_sp_o2_value: Mapped[Optional[int]]
    highest_sp_o2_value: Mapped[Optional[int]]
    average_sp_o2_h_r_sleep: Mapped[Optional[float]]
    average_respiration_value: Mapped[Optional[float]]
    lowest_respiration_value: Mapped[Optional[float]]
    highest_respiration_value: Mapped[Optional[float]]
    awake_count: Mapped[Optional[int]]
    avg_sleep_stress: Mapped[Optional[float]]
    age_group: Mapped[Optional[str]]
    sleep_score_feedback: Mapped[Optional[str]]
    sleep_start_datetime: Mapped[Optional[datetime.datetime]]
    sleep_end_datetime: Mapped[Optional[datetime.datetime]]
    restless_moments_count: Mapped[Optional[int]]

    def __repr__(self) -> str:
        return f"""
        SleepFact(
            timestamp={self.timestamp}
            user_profile_p_k={self.user_profile_p_k}
            sleep_time_seconds={self.sleep_time_seconds}
            nap_time_seconds={self.nap_time_seconds}
            unmeasurable_sleep_seconds={self.unmeasurable_sleep_seconds}
            deep_sleep_seconds={self.deep_sleep_seconds}
            light_sleep_seconds={self.light_sleep_seconds}
            rem_sleep_seconds={self.rem_sleep_seconds}
            awake_sleep_seconds={self.awake_sleep_seconds}
            average_sp_o2_value={self.average_sp_o2_value}
            lowest_sp_o2_value={self.lowest_sp_o2_value}
            highest_sp_o2_value={self.highest_sp_o2_value}
            average_sp_o2_h_r_sleep={self.average_sp_o2_h_r_sleep}
            average_respiration_value={self.average_respiration_value}
            lowest_respiration_value={self.lowest_respiration_value}
            highest_respiration_value={self.highest_respiration_value}
            awake_count={self.awake_count}
            avg_sleep_stress={self.avg_sleep_stress}
            age_group={self.age_group}
            sleep_score_feedback={self.sleep_score_feedback}
            sleep_start_datetime={self.sleep_start_datetime}
            sleep_end_datetime={self.sleep_end_datetime}
            restless_moments_count={self.restless_moments_count}
        )
        """

class ActivityFact(Base):
    __tablename__ = 'raw_activities_facts'

    id: Mapped[int] = mapped_column(primary_key=True)

    activity_name: Mapped[Optional[str]]
    owner_id: Mapped[Optional[int]]
    sport_type_id: Mapped[Optional[int]]
    start_time_local: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, unique=True)
    distance: Mapped[Optional[float]]
    duration: Mapped[Optional[float]]
    elapsed_duration: Mapped[Optional[float]]
    moving_duration: Mapped[Optional[float]]
    average_speed: Mapped[Optional[float]]
    max_speed: Mapped[Optional[float]]
    calories: Mapped[Optional[float]]
    bmr_calories: Mapped[Optional[float]]
    average_h_r: Mapped[Optional[float]]
    max_h_r: Mapped[Optional[float]]
    steps: Mapped[Optional[int]]
    strokes: Mapped[Optional[float]]
    water_estimated: Mapped[Optional[str]]
    average_running_cadence_in_steps_per_minute: Mapped[Optional[float]]
    max_running_cadence_in_steps_per_minute: Mapped[Optional[int]]
    average_swim_cadence_in_strokes_per_minute: Mapped[Optional[float]]
    max_swim_cadence_in_strokes_per_minute: Mapped[Optional[int]]
    average_swolf: Mapped[Optional[float]]
    active_lengths: Mapped[Optional[int]]
    pool_length: Mapped[Optional[float]]
    avg_strokes: Mapped[Optional[float]]
    min_strokes: Mapped[Optional[int]]
    moderate_intensity_minutes: Mapped[Optional[int]]
    vigorous_intensity_minutes: Mapped[Optional[int]]
    type_id: Mapped[Optional[int]]
    type_key: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"""
        ActivityFact(
             id={self.id}
             activity_name={self.activity_name}
             owner_id={self.owner_id}
             sport_type_id={self.sport_type_id}
             start_time_local={self.start_time_local}
             distance={self.distance}
             duration={self.duration}
             elapsed_duration={self.elapsed_duration}
             moving_duration={self.moving_duration}
             average_speed={self.average_speed}
             max_speed={self.max_speed}
             calories={self.calories}
             bmr_calories={self.bmr_calories}
             average_h_r={self.average_h_r}
             max_h_r={self.max_h_r}
             steps={self.steps}
             strokes={self.strokes}
             water_estimated={self.water_estimated}
             average_running_cadence_in_steps_per_minute={self.average_running_cadence_in_steps_per_minute}
             max_running_cadence_in_steps_per_minute={self.max_running_cadence_in_steps_per_minute}
             average_swim_cadence_in_strokes_per_minute={self.average_swim_cadence_in_strokes_per_minute}
             max_swim_cadence_in_strokes_per_minute={self.max_swim_cadence_in_strokes_per_minute}
             average_swolf={self.average_swolf}
             active_lengths={self.active_lengths}
             pool_length={self.pool_length}
             avg_strokes={self.avg_strokes}
             min_strokes={self.min_strokes}
             moderate_intensity_minutes={self.moderate_intensity_minutes}
             vigorous_intensity_minutes={self.vigorous_intensity_minutes}
             type_id={self.type_id}
             type_key={self.type_key}
        )
        """
