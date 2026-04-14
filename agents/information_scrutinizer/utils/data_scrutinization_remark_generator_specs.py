from pydantic import BaseModel,Field

class DataScrutinizationRemarkGeneratorSpecs(BaseModel):
    data_field:str= Field(description="The name of data field.")
    remark_regarding_data_field:str= Field(description="""
    The remarks to guide the trip planner to convey the results about data scrutinization.
    """)