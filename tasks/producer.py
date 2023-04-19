import re
import datetime
import json
import logging
from minio import Minio
from .models import (
    Base
    , OverviewFact
    , SleepFact
    , ActivityFact
)
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine import URL

logger = logging.getLogger(__name__)

def to_snake_case(camel: str) -> str:
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    snake = pattern.sub('_', camel).lower()
    return snake

def get_minio_data(con: Minio, bucket:str, api_type: str, date:str, grouping:str) -> dict:
    try:
        response = con.get_object(bucket, f"/{api_type}/{date}/{grouping}.json")
        data = json.loads(response.data.decode('utf8'))
        logger.info(json.dumps(data, indent=2))
        return data
    except:
        msg = f"Error querying for {api_type}/{date}/{grouping} in {bucket}"
        logger.error(msg)
        raise ValueError(msg)
    finally:
        response.close()
        response.release_conn()

def convert_raw_to_db(raw: dict, date: datetime.datetime, grouping: str):
    if grouping == 'overview':
        return [overview_raw_to_db(raw, date)]
    elif grouping == 'sleep':
        return [sleep_raw_to_db(raw, date)]
    elif grouping == 'activities':
        return list(map(
            lambda act: activity_raw_to_db(act),
            raw['activities'])
        )
    else:
        raise ValueError('Grouping provided is unknown')

def compact_for_db(*trans):
    return [db_row for t in trans for db_row in t]

def save_to_db(url: URL, to_add):
    db = create_engine(url)
    Base.metadata.create_all(db)
    with Session(db) as session:
        for obj in to_add:
            try:
                session.add(obj)
                session.commit()
            except Exception as e:
                logger.error(f"SQL Error inserting {obj}")
                logger.error(e)
                pass

def overview_raw_to_db(raw: dict, date: datetime.datetime) -> OverviewFact:
    def get_value(key: str):
        if key in raw:
            return raw[key]
        else:
            return None

    return OverviewFact(
         user_profile_id= get_value('userProfileId')
         , timestamp = date
         , user_fullname = get_value('userFullname')
         , total_kilocalories= get_value('totalKilocalories')
         , active_kilocalories= get_value('activeKilocalories')
         , bmr_kilocalories= get_value('bmrKilocalories')
         , wellness_kilocalories= get_value('wellnessKilocalories')
         , total_steps= get_value('totalSteps')
         , total_distance_meters= get_value('totalDistanceMeters')
         , wellness_distance_meters= get_value('wellnessDistanceMeters')
         , wellness_active_kilocalories= get_value('wellnessActiveKilocalories')
         , daily_step_goal= get_value('dailyStepGoal')
         , highly_active_seconds= get_value('highlyActiveSeconds')
         , active_seconds= get_value('activeSeconds')
         , sedentary_seconds= get_value('sedentarySeconds')
         , sleeping_seconds= get_value('sleepingSeconds')
         , moderate_intensity_minutes= get_value('moderateIntensityMinutes')
         , vigorous_intensity_minutes= get_value('vigorousIntensityMinutes')
         , floors_ascended_in_meters= get_value('floorsAscendedInMeters')
         , floors_descended_in_meters= get_value('floorsDescendedInMeters')
         , intensity_minutes_goal= get_value('intensityMinutesGoal')
         , min_heart_rate= get_value('minHeartRate')
         , max_heart_rate= get_value('maxHeartRate')
         , resting_heart_rate= get_value('restingHeartRate')
         , max_stress_level= get_value('maxStressLevel')
         , average_stress_level= get_value('averageStressLevel')
         , stress_duration= get_value('stressDuration')
         , rest_stress_duration= get_value('restStressDuration')
         , activity_stress_duration= get_value('activityStressDuration')
         , uncategorized_stress_duration= get_value('uncategorizedStressDuration')
         , total_stress_duration= get_value('totalStressDuration')
         , low_stress_duration= get_value('lowStressDuration')
         , medium_stress_duration= get_value('mediumStressDuration')
         , high_stress_duration= get_value('highStressDuration')
         , stress_qualifier= get_value('stressQualifier')
         , body_battery_charged_value= get_value('bodyBatteryChargedValue')
         , body_battery_drained_value= get_value('bodyBatteryDrainedValue')
         , body_battery_highest_value= get_value('bodyBatteryHighestValue')
         , body_battery_lowest_value= get_value('bodyBatteryLowestValue')
         , average_spo2= get_value('averageSpo2')
         , lowest_spo2= get_value('lowestSpo2')
         , avg_waking_respiration_value= get_value('avgWakingRespirationValue')
         , highest_respiration_value= get_value('highestRespirationValue')
         , lowest_respiration_value= get_value('lowestRespirationValue')
         , weight= get_value('weight')
         , bmi= get_value('bmi')
         , metabolic_age= get_value('metabolicAge')
    )

def sleep_raw_to_db(raw: dict, date: datetime.datetime) -> SleepFact:
    def get_value(key: str):
        if key in raw:
            return raw[key]
        else:
            return None

    return SleepFact(
        timestamp = date
        , user_profile_p_k=get_value('userProfilePK')
        , sleep_time_seconds=get_value('sleepTimeSeconds')
        , nap_time_seconds=get_value('napTimeSeconds')
        , unmeasurable_sleep_seconds=get_value('unmeasurableSleepSeconds')
        , deep_sleep_seconds=get_value('deepSleepSeconds')
        , light_sleep_seconds=get_value('lightSleepSeconds')
        , rem_sleep_seconds=get_value('remSleepSeconds')
        , awake_sleep_seconds=get_value('awakeSleepSeconds')
        , average_sp_o2_value=get_value('averageSpO2Value')
        , lowest_sp_o2_value=get_value('lowestSpO2Value')
        , highest_sp_o2_value=get_value('highestSpO2Value')
        , average_sp_o2_h_r_sleep=get_value('averageSpO2HRSleep')
        , average_respiration_value=get_value('averageRespirationValue')
        , lowest_respiration_value=get_value('lowestRespirationValue')
        , highest_respiration_value=get_value('highestRespirationValue')
        , awake_count=get_value('awakeCount')
        , avg_sleep_stress=get_value('avgSleepStress')
        , age_group=get_value('ageGroup')
        , sleep_score_feedback=get_value('sleepScoreFeedback')
        , sleep_start_datetime=get_value('sleepStartDatetime')
        , sleep_end_datetime=get_value('sleepEndDatetime')
        , restless_moments_count=get_value('restlessMomentsCount')
    )

def activity_raw_to_db(raw: dict) -> SleepFact:
    def get_value(key: str):
        if key in raw:
            return raw[key]
        else:
            return None

    return ActivityFact(
        activity_name=get_value('activityName')
        , owner_id=get_value('ownerId')
        , sport_type_id=get_value('sportTypeId')
        , start_time_local=get_value('startTimeLocal')
        , distance=get_value('distance')
        , duration=get_value('duration')
        , elapsed_duration=get_value('elapsedDuration')
        , moving_duration=get_value('movingDuration')
        , average_speed=get_value('averageSpeed')
        , max_speed=get_value('maxSpeed')
        , calories=get_value('calories')
        , bmr_calories=get_value('bmrCalories')
        , average_h_r=get_value('averageHR')
        , max_h_r=get_value('maxHR')
        , steps=get_value('steps')
        , strokes=get_value('strokes')
        , water_estimated=get_value('waterEstimated')
        , average_running_cadence_in_steps_per_minute=get_value('averageRunningCadenceInStepsPerMinute')
        , max_running_cadence_in_steps_per_minute=get_value('maxRunningCadenceInStepsPerMinute')
        , average_swim_cadence_in_strokes_per_minute=get_value('averageSwimCadenceInStrokesPerMinute')
        , max_swim_cadence_in_strokes_per_minute=get_value('maxSwimCadenceInStrokesPerMinute')
        , average_swolf=get_value('averageSwolf')
        , active_lengths=get_value('activeLengths')
        , pool_length=get_value('poolLength')
        , avg_strokes=get_value('avgStrokes')
        , min_strokes=get_value('minStrokes')
        , moderate_intensity_minutes=get_value('moderateIntensityMinutes')
        , vigorous_intensity_minutes=get_value('vigorousIntensityMinutes')
        , type_id=get_value('typeId')
        , type_key=get_value('typeKey')
    )
