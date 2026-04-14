import os
from get_llm_model import GetLLM
from langchain_core.prompts import ChatPromptTemplate
from agents.information_gatherer.utils.information_extractor_specs import InformationExtractorSpecs


def InformationExtractor(state):
    user_conversation=state["user_conversation"]
    llm=GetLLM(
        service_provider=os.environ["DEFAULT_SERVICE_PROVIDER"],
        temperature=os.environ["DEFAULT_TEMPERATURE"]
    )
    llm=llm.with_structured_output(InformationExtractorSpecs)

    template="""
    The user wants to have a trip.
    You are provided with the conversation between the user and the trip planner.
    Conversation:
    {conversation}
    
    From the conversation you have to extract information that you think is necessary to plan a trip.
    The information could be about:
     - the destination
     - number of days
     - trip budget
     - number of members
     - the dates
     And other things which you feel are important.
     
     Return Format:
     {
       'destination':
       'trip_dates':
       'trip_budget':
       'num_days':
       'number_of_memebers':
     }
     Just return those information that can be extracted.
    """

    prompt=ChatPromptTemplate.from_template(
        template=template,
        input_variable=["conversation"]
    )

    chain=prompt|llm

    result=chain.invoke(
        {
            "conversation":user_conversation
        }
    )

    response={
        "extracted_information":result.extracted_information
    }

    return response



