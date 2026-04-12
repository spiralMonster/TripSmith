from typing_extensions import Literal
from pydantic import BaseModel,Field

class DestinationValidatorSpecs(BaseModel):
    right_time_to_visit: Literal["Yes","No"]= Field(description="Whether it is right time to visit destination or not.")
    explanation: str= Field(description="The explanation of why it is right time or not a right time to visit.")