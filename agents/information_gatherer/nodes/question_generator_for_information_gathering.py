import os
from get_llm_model import GetLLM
from langchain_core.prompts import ChatPromptTemplate
from agents.information_gatherer.utils.question_generator_for_information_gathering_specs import QuestionGeneratorForInformationGatheringSpecs


def QuestionGeneratorForInformationGathering(state):
    insights_regarding_information=state["insights_regarding_information"]

    llm=GetLLM(
        service_provider=os.environ["DEFAULT_SERVICE_PROVIDER"],
        temperature=os.environ["DEFAULT_TEMPERATURE"]
    )
    llm=llm.with_structured_output(QuestionGeneratorForInformationGatheringSpecs)

    template="""
    A trip planner doesn't have sufficient information to plan a trip for user.
    These are some key insights about the information not available:
    {insights}
    
    Your job is to:
     Generate a set of questions which can be asked to user in order get the required information regarding planning a trip.
    
    The generated questions should be unambiguous,coherent,not repeatable and should sound polite.
    """

    prompt=ChatPromptTemplate.from_template(
        template=template,
        input_variable=['insights']
    )

    chain=prompt|llm
    result=chain.invoke({
        "insights":insights_regarding_information
    })

    response={
        "generated_questions_for_information_gathering":result.generated_questions
    }

    return response