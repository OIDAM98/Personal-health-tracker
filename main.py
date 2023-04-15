import datetime
import json
import logging
import sys
import os
from dotenv import load_dotenv

import requests

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError
)


def format_json(data: dict, lvl:int=2) -> dict:
    return json.dumps(data, indent=lvl)

def init_api(email,password):
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

def get_today_stats(api):
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
    today_stats = api.get_stats(today.isoformat())
    stats = {stat: today_stats[stat] for stat in wanted_stats}
    stats = format_json(stats)
    logger.info('Overview Data')
    logger.info(stats)
    return stats

def get_daily_activities(api):
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
    activities = api.get_activities_by_date(today.isoformat(), today.isoformat())
    activities_stats = { 'activities':
                         [{stat: activity[stat] for stat in wanted_stats} for activity in activities]
                        }
    stats = format_json(activities_stats)
    logger.info('Activities data')
    logger.info(stats)
    return stats

if __name__=='__main__':
    FORMAT = "[%(asctime)s - %(levelname)s - %(funcName)s] %(message)s"
    DATEFORMAT = "%Y-%m-%d %I:%M:%S %p"
    logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFORMAT)
    logger = logging.getLogger(__name__)


    load_dotenv()

    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    api = None

    today = datetime.date.today()
    logger.info(f"Getting data for: {today.isoformat()}")
    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    api = init_api(email, password)
    get_today_stats(api)
    get_daily_activities(api)
