import datetime
import json
import logging
import requests
from typing import Optional
from minio import Minio
import io
<<<<<<< HEAD
=======
from functools import reduce
import pytz
>>>>>>> sleep-information
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

def get_overview_stats(api: Garmin, date: datetime.datetime) -> dict:
    stats = api.get_stats(date.isoformat())
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
    wanted_stats = [ 'totalKilocalories'
            ,'activeKilocalories'
            ,'totalDistanceMeters'
            ,'dailyStepGoal'
            ,'activeSeconds'
            ,'sedentarySeconds'
            ,'sleepingSeconds'
            ,'floorsAscendedInMeters'
            ,'floorsDescendedInMeters'
            ,'intensityMinutesGoal'
            ,'minHeartRate'
            ,'maxHeartRate'
            ,'restingHeartRate'
            ,'maxStressLevel'
            ,'averageStressLevel'
            ,'totalSteps'
            ,'sleepingSeconds'
            ,'stressPercentage'
            ,'bodyBatteryChargedValue'
            ,'bodyBatteryDrainedValue'
            ,'bodyBatteryHighestValue'
            ,'bodyBatteryLowestValue'
            ,'stressQualifier'
        ]
    stats = {stat: data[stat] for stat in wanted_stats}
    logger.info(format_json(stats))
    return stats

def transform_daily_activities(data: dict) -> dict:
    wanted_stats = [
        'activityName'
        ,'sportTypeId'
        ,'startTimeLocal'
        ,'activityType'
        ,'distance'
        ,'duration'
        ,'elapsedDuration'
        ,'movingDuration'
        ,'averageSpeed'
        ,'maxSpeed'
        ,'calories'
        ,'bmrCalories'
        ,'averageHR'
        ,'maxHR'
        ,'steps'
        ,'strokes'
        ,'waterEstimated'
        ,'averageRunningCadenceInStepsPerMinute'
        ,'maxRunningCadenceInStepsPerMinute'
        ,'averageSwimCadenceInStrokesPerMinute'
        ,'maxSwimCadenceInStrokesPerMinute'
    ]
    stats = { 'activities':
                         [{stat: activity[stat] for stat in wanted_stats} for activity in data]
                        }

    logger.info(format_json(stats))
    return stats

def transform_overview_stats(data: dict) -> dict:
    wanted_stats = [ 'totalKilocalories'
            ,'activeKilocalories'
            ,'totalDistanceMeters'
            ,'dailyStepGoal'
            ,'activeSeconds'
            ,'sedentarySeconds'
            ,'sleepingSeconds'
            ,'floorsAscendedInMeters'
            ,'floorsDescendedInMeters'
            ,'intensityMinutesGoal'
            ,'minHeartRate'
            ,'maxHeartRate'
            ,'restingHeartRate'
            ,'maxStressLevel'
            ,'averageStressLevel'
            ,'totalSteps'
            ,'sleepingSeconds'
            ,'stressPercentage'
            ,'bodyBatteryChargedValue'
            ,'bodyBatteryDrainedValue'
            ,'bodyBatteryHighestValue'
            ,'bodyBatteryLowestValue'
            ,'stressQualifier'
        ]
    stats = {stat: data[stat] for stat in wanted_stats}
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
        'sleepTimeSeconds'
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
        , 'avgSleepStress'
        , 'ageGroup'
        , 'sleepScoreFeedback'
        , 'sleepStartTimestampGMT'
        , 'sleepEndTimestampGMT'
    ]

    def timestamp_to_datetime(stamp: str) -> datetime.datetime:
        dt = (datetime.datetime.utcfromtimestamp(stamp / 1000))
        return pytz.utc.localize(dt, is_dst=None).astimezone(pytz.timezone('America/Mexico_City'))

    stats = dict([(stat,data[stat]) for stat in data.keys() if stat not in unwanted_stats])
    wellness_stats = {stat: stats[sleep_key][stat] for stat in wanted_sleep_stats }
    restless_stats = {restless_key: stats[restless_key]}
    wellness_stats['sleepStartDatetime'] = str(timestamp_to_datetime(wellness_stats['sleepStartTimestampGMT']))
    wellness_stats['sleepEndDatetime'] = str(timestamp_to_datetime(wellness_stats['sleepEndTimestampGMT']))
    del wellness_stats['sleepStartTimestampGMT']
    del wellness_stats['sleepEndTimestampGMT']
    sleep_stats = wellness_stats |  restless_stats

    logger.info(format_json(sleep_stats))
    return sleep_stats

def prepare_json(*data) -> dict:
    concat = dict(reduce(lambda a,b: a | b, data))
    logger.info(format_json(concat))
    return concat

<<<<<<< HEAD
def save_json(data: dict, date: datetime.datetime, con:Optional[Minio], bucket:str="") -> None:
=======
def save_json(data: dict, date: datetime.datetime, con:Optional[Minio]=None, bucket:str="") -> None:
>>>>>>> sleep-information
    data = json.dumps(data, separators=(',', ':'))
    if con is None:
        filename = f"{date.isoformat()}_overview.json"
        with open(filename, 'w') as f:
            json.dump(data, f, separators=(',',':'))
        logger.info(f"Saved data to {filename}")
    else:
        try:
            path = f"/garmin/{date}/overview.json"
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
