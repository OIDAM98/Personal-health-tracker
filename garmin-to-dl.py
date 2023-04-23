import datetime
import logging
import os
from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error
from tasks.consume import (
    init_api
    , get_full_name
    , get_overview_stats
    , get_daily_activities
    , transform_overview_stats
    , transform_daily_activities
    , get_sleep_stats
    , transform_sleep_stats
    , prepare_json
    , save_json
)

if __name__=='__main__':
    FORMAT = "[%(asctime)s - %(levelname)s - %(funcName)s] %(message)s"
    DATEFORMAT = "%Y-%m-%d %I:%M:%S %p"
    logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFORMAT)
    logger = logging.getLogger(__name__)

    load_dotenv()

    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')

    host = os.getenv('MINIO_HOST')
    minio_acc_key = os.getenv('MINIO_ACCESS_KEY')
    minio_secret_key = os.getenv('MINIO_SECRET_KEY')
    bucket = os.getenv('BUCKET_NAME')

    date_query = datetime.date.today() - datetime.timedelta(days=2)
    logger.info(f"Getting data for: {date_query.isoformat()}")
    try:
        con =  Minio(
            host,
            access_key=minio_acc_key,
            secret_key=minio_secret_key,
            secure=False
        )
        api = init_api(email, password)
        name = get_full_name(api)
        overview = transform_overview_stats(get_overview_stats(api, date_query))
        activities = transform_daily_activities(get_daily_activities(api, date_query))
        sleep = transform_sleep_stats(get_sleep_stats(api, date_query))
        save_json(name, date_query, 'user', con, bucket)
        save_json(overview, date_query, 'overview', con, bucket)
        save_json(activities, date_query, 'activities', con, bucket)
        save_json(sleep, date_query, 'sleep', con, bucket)
    except S3Error:
        api = init_api(email, password)
        overview = transform_overview_stats(get_overview_stats(api, date_query))
        activities = transform_daily_activities(get_daily_activities(api, date_query))
        sleep = transform_sleep_stats(get_sleep_stats(api, date_query))
        save_json(overview, date_query, 'overview')
        save_json(activities, date_query, 'activities')
        save_json(sleep, date_query, 'sleep')
