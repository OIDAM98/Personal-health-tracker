import datetime
import json
import logging
import requests
from typing import Optional
from minio import Minio
import io
from functools import reduce
import pytz
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError
)

logger = logging.getLogger(__name__)

def format_json(data: dict, lvl:int=2) -> dict:
    return json.dumps(data, indent=lvl)

def init_api(email: str,password: str) -> Garmin:
    try:
        with open('cached_session.json') as f:
            saved =  json.load(f)

            logger.info('Login to Garmin Connect using cached session...')

            api = Garmin(session_data=saved)
            api.login()
    except (FileNotFoundError, GarminConnectAuthenticationError):
        logger.info(
            'No saved credentials.',
            'Session cookies will be sotred in cached_session.json'
        )

        try:
            api = Garmin(email, password)
            api.login()

            with open('cached_session.json', 'w', encoding='utf-8') as f:
                json.dump(api.session_data, f, ensure_ascii=False, indent=2)

        except(
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
            requests.exceptions.HTTPError
        ) as err:
            logger.error('Error ocurred during Garmin Connect comm %s', err)
            return None

    return api

def get_full_name(api: Garmin) -> dict:
    name = { 'username': api.get_full_name() }
    logger.info(format_json(name))
    return name

def get_overview_stats(api: Garmin, date: datetime.datetime) -> dict:
    stats = api.get_stats_and_body(date.isoformat())
    logger.info(format_json(stats))
    return stats

def get_sleep_stats(api: Garmin, date: datetime.datetime) -> dict:
    stats = api.get_sleep_data(date.isoformat())
    logger.info(format_json(stats))
    return stats

def get_daily_activities(api: Garmin, date:datetime.datetime) -> dict:
    activities = api.get_activities_by_date(date.isoformat(), date.isoformat())
    logger.info(format_json(activities))
    return activities


def transform_overview_stats(data: dict) -> dict:
    overview_stats = [
        'userProfileId'
        , 'totalKilocalories'
        , 'activeKilocalories'
        , 'bmrKilocalories'
        , 'wellnessKilocalories'
        , 'totalSteps'
        , 'totalDistanceMeters'
        , 'wellnessDistanceMeters'
        , 'wellnessActiveKilocalories'
        , 'dailyStepGoal'
        , 'highlyActiveSeconds'
        , 'activeSeconds'
        , 'sedentarySeconds'
        , 'sleepingSeconds'
        , 'moderateIntensityMinutes'
        , 'vigorousIntensityMinutes'
        , 'floorsAscendedInMeters'
        , 'floorsDescendedInMeters'
        , 'intensityMinutesGoal'
        , 'minHeartRate'
        , 'maxHeartRate'
        , 'restingHeartRate'
        , 'maxStressLevel'
        , 'averageStressLevel'
        , 'maxStressLevel'
        , 'stressDuration'
        , 'restStressDuration'
        , 'activityStressDuration'
        , 'uncategorizedStressDuration'
        , 'totalStressDuration'
        , 'lowStressDuration'
        , 'mediumStressDuration'
        , 'highStressDuration'
        , 'sleepingSeconds'
        , 'stressQualifier'
        , 'bodyBatteryChargedValue'
        , 'bodyBatteryDrainedValue'
        , 'bodyBatteryHighestValue'
        , 'bodyBatteryLowestValue'
        , 'averageSpo2'
        , 'lowestSpo2'
        , 'avgWakingRespirationValue'
        , 'highestRespirationValue'
        , 'lowestRespirationValue'
        , 'weight'
        , 'bmi'
        , 'metabolicAge'
    ]
    stats = {stat: data[stat] for stat in overview_stats}
    logger.info(format_json(stats))
    return stats

def transform_daily_activities(data: dict) -> dict:
    exercise_stats = [
        'activityName'
        , 'ownerId'
        , 'sportTypeId'
        , 'startTimeLocal'
        , 'activityType'
        , 'distance'
        , 'duration'
        , 'elapsedDuration'
        , 'movingDuration'
        , 'averageSpeed'
        , 'maxSpeed'
        , 'calories'
        , 'bmrCalories'
        , 'averageHR'
        , 'maxHR'
        , 'steps'
        , 'strokes'
        , 'waterEstimated'
        , 'averageRunningCadenceInStepsPerMinute'
        , 'maxRunningCadenceInStepsPerMinute'
        , 'averageSwimCadenceInStrokesPerMinute'
        , 'maxSwimCadenceInStrokesPerMinute'
        , 'averageSwolf'
        , 'activeLengths'
        , 'poolLength'
        , 'avgStrokes'
        , 'minStrokes'
        , 'moderateIntensityMinutes'
        , 'vigorousIntensityMinutes'
    ]
    stats = { 'activities':
                         [{stat: activity[stat] for stat in exercise_stats} for activity in data]
                        }
    for stat in stats['activities']:
        act_type = stat['activityType']
        stat['typeId'] = act_type['typeId']
        stat['typeKey'] = act_type['typeKey']
        del stat['activityType']


    logger.info(format_json(stats))
    return stats

def transform_sleep_stats(data: dict) -> dict:
    unwanted_stats = [
        'wellnessEpochRespirationDataDTOList'
        ,'wellnessEpochSPO2DataDTOList'
        , 'sleepStress'
        , 'sleepRestlessMoments'
        , 'sleepLevels'
        , 'sleepMovement'
        , 'remSleepData'
    ]
    restless_key = 'restlessMomentsCount'
    sleep_key = 'dailySleepDTO'
    wanted_sleep_stats = [
        'userProfilePK'
        , 'sleepTimeSeconds'
        , 'napTimeSeconds'
        , 'unmeasurableSleepSeconds'
        , 'deepSleepSeconds'
        , 'lightSleepSeconds'
        , 'remSleepSeconds'
        , 'awakeSleepSeconds'
        , 'averageSpO2Value'
        , 'lowestSpO2Value'
        , 'highestSpO2Value'
        , 'averageSpO2HRSleep'
        , 'averageRespirationValue'
        , 'lowestRespirationValue'
        , 'highestRespirationValue'
        , 'awakeCount'
        , 'avgSleepStress'
        , 'ageGroup'
        , 'sleepScoreFeedback'
        , 'sleepStartTimestampGMT'
        , 'sleepEndTimestampGMT'
    ]

    def timestamp_to_datetime(stamp: str) -> datetime.datetime:
        if stamp is None:
            return None
        dt = (datetime.datetime.utcfromtimestamp(stamp / 1000))
        return str(pytz.utc.localize(dt, is_dst=None).astimezone(pytz.timezone('America/Mexico_City')))

    stats = dict([(stat,data[stat]) for stat in data.keys() if stat not in unwanted_stats])
    logger.info(stats[sleep_key].keys())
    wellness_stats = dict([ (stat,stats[sleep_key][stat]) for stat in wanted_sleep_stats if stat in stats[sleep_key].keys() ])
    if restless_key in stats:
        restless_stats = {restless_key: stats[restless_key]}
    else:
        restless_stats= { restless_key: None }
    if 'sleepStartTimestampGMT' in wellness_stats and 'sleepEndTimestampGMT' in wellness_stats:
        wellness_stats['sleepStartDatetime'] = timestamp_to_datetime(wellness_stats['sleepStartTimestampGMT'])
        wellness_stats['sleepEndDatetime'] = timestamp_to_datetime(wellness_stats['sleepEndTimestampGMT'])
        del wellness_stats['sleepStartTimestampGMT']
        del wellness_stats['sleepEndTimestampGMT']
    sleep_stats = wellness_stats |  restless_stats

    logger.info(format_json(sleep_stats))
    return sleep_stats

def prepare_json(*data) -> dict:
    concat = dict(reduce(lambda a,b: a | b, data))
    logger.info(format_json(concat))
    return concat

def save_json(data: dict, date: datetime.datetime, filename: str, con:Optional[Minio]=None, bucket:str="") -> None:
    data = json.dumps(data, separators=(',', ':'))
    if con is None:
        f_name = f"{date.isoformat()}_{filename}.json"
        with open(f_name, 'w') as f:
            json.dump(data, f, separators=(',',':'))
        logger.info(f"Saved data to {filename}")
    else:
        try:
            path = f"/garmin/{date}/{filename}.json"
            con.put_object(
                bucket,
                path,
                io.BytesIO(bytes(data, 'utf-8')),
                len(data),
                content_type='application/json'
            )
            logger.info(f"Saved data in Minio as {bucket}:{path}")
        except:
            logger.error(f"Error saving to Minio")
