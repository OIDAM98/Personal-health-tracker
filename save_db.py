import datetime
import logging
import os
from dotenv import load_dotenv
import json
from minio import Minio
from sqlalchemy.engine import URL
from tasks.producer import (
    get_minio_data
    , convert_raw_to_db
    , compact_for_db
    , save_to_db
)
from functools import reduce

if __name__=='__main__':
    FORMAT = "[%(asctime)s - %(levelname)s - %(funcName)s] %(message)s"
    DATEFORMAT = "%Y-%m-%d %I:%M:%S %p"
    logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFORMAT)
    logger = logging.getLogger(__name__)

    load_dotenv()

    host = os.getenv('MINIO_HOST')
    minio_acc_key = os.getenv('MINIO_ACCESS_KEY')
    minio_secret_key = os.getenv('MINIO_SECRET_KEY')
    bucket = os.getenv('BUCKET_NAME')

    dwh_username = os.getenv('DWH_USERNAME')
    dwh_password = os.getenv('DWH_PASSWORD')
    dwh_host = os.getenv('DWH_HOST')
    dwh_database = os.getenv('DWH_DATABASE')

    api_type = 'garmin'
    date_query = datetime.date.today() - datetime.timedelta(days=1)
    date_query_dt = datetime.datetime.combine(date_query, datetime.datetime.min.time())
    logger.info(f"Getting data for: {date_query.isoformat()}")

    con =  Minio(
        host,
        access_key=minio_acc_key,
        secret_key=minio_secret_key,
        secure=False
    )

    user = get_minio_data(con, bucket, api_type, date_query, 'user')
    overview = get_minio_data(con, bucket, api_type, date_query, 'overview')
    sleep = get_minio_data(con, bucket, api_type, date_query, 'sleep')
    activities = get_minio_data(con, bucket, api_type, date_query, 'activities')

    overview['userFullname'] = user['username']
    overview_db = convert_raw_to_db(overview, date_query_dt, 'overview')
    sleep_db = convert_raw_to_db(sleep, date_query_dt, 'sleep')
    activities_db = convert_raw_to_db(activities, date_query_dt, 'activities')

    to_add = compact_for_db(activities_db, sleep_db, overview_db)

    dwh_url = URL.create(
        drivername='postgresql'
        , username=dwh_username
        , host=dwh_host
        , database=dwh_database
        , password=dwh_password
    )
    save_to_db(dwh_url, to_add)
