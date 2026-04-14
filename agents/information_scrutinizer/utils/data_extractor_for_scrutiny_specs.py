from pydantic import BaseModel, Field

class DataExtractorForScrutinySpecs(BaseModel):
    data_to_scrutinize: dict = Field(description="The data you feel should be scrutinized.")


