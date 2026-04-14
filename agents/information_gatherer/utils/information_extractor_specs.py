from pydantic import BaseModel,Field

class InformationExtractorSpecs(BaseModel):
    extracted_information:dict= Field(description="The extracted information from the conversation.")

