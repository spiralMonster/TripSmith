from pydantic import BaseModel,Field

class TravelDestinationExtractorSpecs(BaseModel):
    destination:str =Field(description="Extract the travel destination from the query if present or else return None.")