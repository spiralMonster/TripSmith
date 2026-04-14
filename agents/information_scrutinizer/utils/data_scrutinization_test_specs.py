from typing_extensions import List, TypedDict, Literal
from pydantic import BaseModel,Field


class DataItemScrutinySpecs(TypedDict):
    data_field_name:str
    data_field_value:str|int
    data_field_scrutiny_test: Literal["Passed","Failed"]
    scrutiny_test_explanation:str

class DataScrutinyTestSpecs(BaseModel):
    data_scrutiny_test: List[DataItemScrutinySpecs]