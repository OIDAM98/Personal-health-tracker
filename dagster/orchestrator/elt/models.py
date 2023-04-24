
import datetime
from typing import (
    List
    , Optional
)
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    declarative_base
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

Base = declarative_base()

class OverviewFact(Base):
    __tablename__ = 'raw_overview_facts'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)

    user_profile_id = Column(Integer)
    user_fullname = Column(String)
    total_kilocalories = Column(Float, nullable=True)
    active_kilocalories = Column(Float, nullable=True)
    bmr_kilocalories = Column(Float, nullable=True)
    wellness_kilocalories = Column(Float, nullable=True)
    total_steps = Column(Integer, nullable=True)
    total_distance_meters = Column(Integer, nullable=True)
    wellness_distance_meters = Column(Integer, nullable=True)
    wellness_active_kilocalories = Column(Float, nullable=True)
    daily_step_goal = Column(Integer, nullable=True)
    highly_active_seconds = Column(Integer, nullable=True)
    active_seconds = Column(Integer, nullable=True)
    sedentary_seconds = Column(Integer, nullable=True)
    sleeping_seconds = Column(Integer, nullable=True)
    moderate_intensity_minutes = Column(Integer, nullable=True)
    vigorous_intensity_minutes = Column(Integer, nullable=True)
    floors_ascended_in_meters = Column(Float, nullable=True)
    floors_descended_in_meters = Column(Float, nullable=True)
    intensity_minutes_goal = Column(Integer, nullable=True)
    min_heart_rate = Column(Integer, nullable=True)
    max_heart_rate = Column(Integer, nullable=True)
    resting_heart_rate = Column(Integer, nullable=True)
    max_stress_level = Column(Integer, nullable=True)
    average_stress_level = Column(Integer, nullable=True)
    stress_duration = Column(Integer, nullable=True)
    rest_stress_duration = Column(Integer, nullable=True)
    activity_stress_duration = Column(Integer, nullable=True)
    uncategorized_stress_duration = Column(Integer, nullable=True)
    total_stress_duration = Column(Integer, nullable=True)
    low_stress_duration = Column(Integer, nullable=True)
    medium_stress_duration = Column(Integer, nullable=True)
    high_stress_duration = Column(Integer, nullable=True)
    stress_qualifier = Column(Integer, nullable=True)
    body_battery_charged_value = Column(Integer, nullable=True)
    body_battery_drained_value = Column(Integer, nullable=True)
    body_battery_highest_value = Column(Integer, nullable=True)
    body_battery_lowest_value = Column(Integer, nullable=True)
    average_spo2 = Column(Float, nullable=True)
    lowest_spo2 = Column(Integer, nullable=True)
    avg_waking_respiration_value = Column(Float, nullable=True)
    highest_respiration_value = Column(Float, nullable=True)
    lowest_respiration_value = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    bmi = Column(Float, nullable=True)
    metabolic_age = Column(Integer, nullable=True)

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

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, unique=True)
    user_profile_p_k = Column(Integer)
    sleep_time_seconds = Column(Integer, nullable=True)
    nap_time_seconds = Column(Integer, nullable=True)
    unmeasurable_sleep_seconds = Column(Integer, nullable=True)
    deep_sleep_seconds = Column(Integer, nullable=True)
    light_sleep_seconds = Column(Integer, nullable=True)
    rem_sleep_seconds = Column(Integer, nullable=True)
    awake_sleep_seconds = Column(Integer, nullable=True)
    average_sp_o2_value = Column(Float, nullable=True)
    lowest_sp_o2_value = Column(Integer, nullable=True)
    highest_sp_o2_value = Column(Integer, nullable=True)
    average_sp_o2_h_r_sleep = Column(Float, nullable=True)
    average_respiration_value = Column(Float, nullable=True)
    lowest_respiration_value = Column(Float, nullable=True)
    highest_respiration_value = Column(Float, nullable=True)
    awake_count = Column(Integer, nullable=True)
    avg_sleep_stress = Column(Float, nullable=True)
    age_group = Column(String, nullable=True)
    sleep_score_feedback = Column(String, nullable=True)
    sleep_start_datetime = Column(DateTime, nullable=True)
    sleep_end_datetime = Column(DateTime, nullable=True)
    restless_moments_count = Column(Integer, nullable=True)

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

    id = Column(Integer, primary_key=True)

    activity_name = Column(String, nullable=True)
    owner_id = Column(Integer, nullable=True)
    sport_type_id = Column(Integer, nullable=True)
    start_time_local = Column(DateTime, nullable=True)
    distance = Column(Float, nullable=True)
    duration = Column(Float, nullable=True)
    elapsed_duration = Column(Float, nullable=True)
    moving_duration = Column(Float, nullable=True)
    average_speed = Column(Float, nullable=True)
    max_speed = Column(Float, nullable=True)
    calories = Column(Float, nullable=True)
    bmr_calories = Column(Float, nullable=True)
    average_h_r = Column(Float, nullable=True)
    max_h_r = Column(Float, nullable=True)
    steps = Column(Integer, nullable=True)
    strokes = Column(Float, nullable=True)
    water_estimated = Column(Float, nullable=True)
    average_running_cadence_in_steps_per_minute = Column(Float, nullable=True)
    max_running_cadence_in_steps_per_minute = Column(Integer, nullable=True)
    average_swim_cadence_in_strokes_per_minute = Column(Float, nullable=True)
    max_swim_cadence_in_strokes_per_minute = Column(Integer, nullable=True)
    average_swolf = Column(Float, nullable=True)
    active_lengths = Column(Integer, nullable=True)
    pool_length = Column(Float, nullable=True)
    avg_strokes = Column(Float, nullable=True)
    min_strokes = Column(Integer, nullable=True)
    moderate_intensity_minutes = Column(Integer, nullable=True)
    vigorous_intensity_minutes = Column(Integer, nullable=True)
    type_id = Column(Integer, nullable=True)
    type_key = Column(String, nullable=True)

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
