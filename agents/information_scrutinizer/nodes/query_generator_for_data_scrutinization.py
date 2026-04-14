import os
from get_llm_model import GetLLM
from langchain_core.prompts import ChatPromptTemplate
from agents.information_scrutinizer.utils.query_generator_for_data_scrutinization_specs import QueryGeneratorForDataScrutinizationSpecs


def QueryGeneratorForDataScrutinization(state):
    trip_destination=state["trip_destination"]
    data_to_scrutinize=state["data_to_scrutinize"]

    llm=GetLLM(
        service_provider=os.environ["DEFAULT_SERVICE_PROVIDER"],
        temperature=os.environ["DEFAULT_TEMPERATURE"]
    )
    llm=llm.with_structured_output(QueryGeneratorForDataScrutinizationSpecs)

    template="""
    You are provided with a trip destination and data regarding trip.
    Trip Destination: {trip_destination}
    Data: {trip_data}
    
    Your job is to generate queries regarding the data. 
    So that the generated queries can be searched on internet and then the data item is scrutinized using the information fetched from internet.
    
    Example:
    Trip Destination: Italy
    Data item: {'trip budget':1000 dollars, 'number of days':7, 'trip dates':'1 May-7 May','number of members':4}
    
    Generated Queries=[
      'What should be the minimum budget for a trip to Italy?',
      'Can we explore Italy in just 7 days?',
      'How is Italy in May?',
      'Which one will be better experience: solo trip to Italy or family trip to Italy?',
      'Any idea about how much it will cost for a week trip to Italy for 4 members?'
    ]
    
    Note: Generate at least three queries.
    """

    prompt=ChatPromptTemplate.from_template(
        template=template,
        input_variable=['trip_destination','trip_data']
    )

    chain=prompt|llm
    result=chain.invoke(
        {
            "trip_destination":trip_destination,
            "trip_data":data_to_scrutinize
        }
    )

    response={
        "generated_queries_for_data_scrutinization":result.generated_queries_for_data_scrutinization
    }

    return response