from typing import List
from pydantic import BaseModel, Field


class QuestionGeneratorForInformationGatheringSpecs(BaseModel):
    generated_questions: List[str]= Field(description="A set of questions to gather information.")