from dagster import StringSource, resource, ConfigurableResource
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError
)

class GarminResource(ConfigurableResource):
    email: str
    password: str

    def get_api(self) -> Garmin:
        try:
            api = Garmin(self.email, self.password)
            api.login()

        except(
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
            requests.exceptions.HTTPError
        ) as err:
            logger.error('Error ocurred during Garmin Connect comm %s', err)
            return None

        return api
