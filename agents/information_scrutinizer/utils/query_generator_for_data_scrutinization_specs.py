from typing import List
from pydantic import BaseModel, Field

class QueryGeneratorForDataScrutinizationSpecs(BaseModel):
    generated_queries_for_data_scrutinization: List[str] =Field(description="The generated queries for data scrutinization.")