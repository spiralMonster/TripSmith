from typing import Literal
from pydantic import BaseModel,Field

class IsQueryValidSpecs(BaseModel):
    is_query_valid: Literal['true','false']=Field(description="Whether the query is related to planning a trip or not?")