import os
from get_llm_model import GetLLM
from langchain_core.prompts import ChatPromptTemplate
from agents.information_gatherer.utils.information_sufficiency_decider_specs import InformationSufficiencyDeciderSpecs


def InformationSufficienyDecider(state):
    extracted_information=state["extracted_information"]

    llm=GetLLM(
        service_provider=os.environ["DEFAULT_SERVICE_PROVIDER"],
        temperature=os.environ["DEFAULT_TEMPERATURE"]
    )
    llm=llm.with_structured_output(InformationSufficiencyDeciderSpecs)

    template="""
    You are provided with the information extracted from the conversation of the user and trip planner.
    Extracted Information:
    {extracted_information}
    
    Do you think whether the extracted information is enough to plan a trip or not?
    If you feel that the extracted information is not enough then mention what else information is needed to plan a trip.
    """

    prompt=ChatPromptTemplate.from_template(
        template=template,
        input_variable=["extracted_information"]
    )

    chain=prompt|llm

    result=chain.invoke(
        {
            "extracted_information":extracted_information
        }
    )

    response={
        "is_extracted_information_sufficient":result.is_information_sufficient,
        "insights_regarding_information":result.explanation
    }

    return response