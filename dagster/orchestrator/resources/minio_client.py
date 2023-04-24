from dagster import StringSource, resource, ConfigurableResource
from minio import Minio

class MinioResource(ConfigurableResource):
    host: str
    access_key: str
    secret_key: str

    def get_client(self) -> Minio:
        return Minio(
            self.host,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=False
        )
