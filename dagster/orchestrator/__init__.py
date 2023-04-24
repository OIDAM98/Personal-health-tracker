from dagster import Definitions, load_assets_from_modules, define_asset_job, ScheduleDefinition

from .garmin_consumer import assets as garmin_assets
from .resources.garmin_client import GarminResource
from .resources.minio_client import MinioResource
from .elt import assets
from sqlalchemy.engine import URL
import os

etl_assets = load_assets_from_modules([garmin_assets])

garmin_email = os.getenv('EMAIL')
garmin_pass = os.getenv('PASSWORD')

# defs = Definitions(
#     assets=all_assets,
#     resources={
#         'garmin_api':
#        GarminResource(
#            email=garmin_email,
#            password=garmin_pass
#        ).get_api()
#     }
# )

elt_assets = load_assets_from_modules([assets])

minio_host = os.getenv('MINIO_HOST')
minio_acc_key = os.getenv('MINIO_ACCESS_KEY')
minio_secret_key = os.getenv('MINIO_SECRET_KEY')
bucket = os.getenv('BUCKET_NAME')

dwh_username = os.getenv('DWH_USERNAME')
dwh_password = os.getenv('DWH_PASSWORD')
dwh_host = os.getenv('DWH_HOST')
dwh_database = os.getenv('DWH_DATABASE')

url = URL.create(
    drivername='postgresql'
    , username=dwh_username
    , host=dwh_host
    , database=dwh_database
    , password=dwh_password
    , port=5430
)

elt_job = define_asset_job(
    "save_to_dwh",
    elt_assets
)

elt_schedule = ScheduleDefinition(
    job=elt_job,
    cron_schedule="20 3 * * *"
)

defs = Definitions(
    assets=elt_assets,
    resources={
        'minio': MinioResource(
            host=minio_host,
            access_key=minio_acc_key,
            secret_key=minio_secret_key
        ).get_client(),
        'dwh_url': url ,
        'bucket': bucket,
        'api_type': 'garmin'
    },
    schedules=[elt_schedule]
)
