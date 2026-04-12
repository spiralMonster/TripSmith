from typing import Literal
from pydantic import BaseModel,Field

class QueryValidatorSpecs(BaseModel):
    is_query_valid: Literal['Yes','No']=Field(description="Whether the query is related to planning a trip or not?")