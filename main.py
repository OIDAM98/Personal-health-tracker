import datetime
import logging
import os
from dotenv import load_dotenv
from minio import Minio
from tasks.consume import (
    init_api
    , get_overview_stats
    , get_daily_activities
    , transform_overview_stats
    , transform_daily_activities
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

    # date_query = datetime.date.today()
    date_query = datetime.date.today() - datetime.timedelta(days=1)
    logger.info(f"Getting data for: {date_query.isoformat()}")
    try:
        con =  Minio(
            host,
            access_key=minio_acc_key,
            secret_key=minio_secret_key,
            secure=False
        )
        api = init_api(email, password)
        overview = transform_overview_stats(get_overview_stats(api, date_query))
        activities = transform_daily_activities(get_daily_activities(api, date_query))
        data = prepare_json(overview, activities)
        save_json(data, date_query, con, bucket)
    except:
        api = init_api(email, password)
        overview = transform_overview_stats(get_overview_stats(api, date_query))
        activities = transform_daily_activities(get_daily_activities(api, date_query))
        data = prepare_json(overview, activities)
        save_json(data, date_query)
