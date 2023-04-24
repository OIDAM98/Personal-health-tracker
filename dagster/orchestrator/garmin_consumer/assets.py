from dagster import asset, job, Definitions, define_asset_job, op
from datetime import date, timedelta
import os

@asset
def date_query() -> date:
    return date.today() - timedelta(days=2)

@asset(required_resource_keys={'garmin_api'})
def raw_overall_stats(context, date_query: date) -> dict:
    stats = context.resources.garmin_api.get_stats_and_body(date.isoformat())
    return stats

@asset(required_resource_keys={'garmin_api'})
def full_name(context) -> dict:
    return { 'username': context.resources.garmin_api.get_full_name() }

@asset(required_resource_keys={'garmin_api'})
def raw_sleep_stats(context, date_query: date) -> dict:
    stats = context.resources.garmin_api.get_sleep_data(date.isoformat())
    return stats

@asset(required_resource_keys={'garmin_api'})
def raw_activities(context, date_query:date) -> dict:
    activities = context.resources.garmin_api.get_activities_by_date(date.isoformat(), date.isoformat())
    return activities

@asset
def overall_stats(raw_overall_stats: dict) -> dict:
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
    stats = dict(
        [
            (stat, raw_overall_stats[stat])
            for stat in raw_overall_stats.keys() if stat in overview_stats
        ]
    )
    return stats

@asset
def activities(raw_activities: dict) -> dict:
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
                         [
                             {stat: activity[stat] for stat in exercise_stats}
                             for activity in raw_activities
                         ]
             }
    for stat in stats['activities']:
        act_type = stat['activityType']
        stat['typeId'] = act_type['typeId']
        stat['typeKey'] = act_type['typeKey']
        del stat['activityType']

    return stats

@asset
def sleep_stats(raw_sleep_stats: dict) -> dict:
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

    stats = dict([(stat,raw_sleep_stats[stat]) for stat in raw_sleep_stats.keys() if stat not in unwanted_stats])
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

    return sleep_stats

@job
def save_to_minio():
    return None
