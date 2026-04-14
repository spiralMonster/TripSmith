from typing_extensions import Literal
from pydantic import BaseModel,Field

class InformationSufficiencyDeciderSpecs(BaseModel):
    is_information_sufficient: Literal["Yes","No"]= Field(description="""
    Is the information extracted sufficient or not for planning a trip?
    """)

    explanation: str= Field(description="Why do you think the information is sufficient or not?")

