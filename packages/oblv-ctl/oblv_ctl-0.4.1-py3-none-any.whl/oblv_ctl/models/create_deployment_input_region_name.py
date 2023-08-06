from enum import Enum


class CreateDeploymentInputRegionName(str, Enum):
    EU_CENTRAL_1 = "eu-central-1"
    EU_WEST_2 = "eu-west-2"
    US_EAST_1 = "us-east-1"
    US_WEST_2 = "us-west-2"

    def __str__(self) -> str:
        return str(self.value)
