import os
from get_llm_model import GetLLM
from langchain_core.prompts import ChatPromptTemplate
from agents.information_scrutinizer.utils.data_scrutinization_test_specs import DataScrutinyTestSpecs


def DataScrutinizationTest(state):
    data=state["data_to_scrutinize"]
    scrapped_information_for_data_scrutinization=state["scrapped_information_for_data_scrutinization"]

    llm = GetLLM(
        service_provider=os.environ["DEFAULT_SERVICE_PROVIDER"],
        temperature=os.environ["DEFAULT_TEMPERATURE"]
    )
    llm=llm.with_structured_output(DataScrutinyTestSpecs)

    template="""
    You are provided with data required for planning a trip.
    You are also provided with information scrapped from the web to scrutinize the provided data.
    
    Data extracted for a trip planning:
    {data}
    Information scrapped for scrutinizing data:
    {scrapped_information_for_data_scrutinization}
    
    Based on the information provided, for each data field you have to generate:
     - data_field_name (Use the same as provided)
     - data_field_value (Use the same as provided)
     - data_field_scrutiny_test (Passed/Failed based upon whether the data value is in accordance with the scrapped information)
     - scrutiny_test_explanation (Why you Passed/Failed the data scrutiny test.If the data field Failed the test then suggest the optimal value for the field based on the scrapped information)
     
     For example for each data field generate as follows:
     {
      'data_field_name':'trip_budget'
      'data_field_value': '1000 dollars'
      'data_field_scrutiny_test': 'Passed'
      'scrutiny_test_explanation': 'The information provided suggests that the average budget for the trip is around 700 dollars, so the provided data value is more than enough.'
     }
    """

    prompt=ChatPromptTemplate.from_template(
        template=template,
        input_variable=['data','scrapped_information_for_data_scrutinization']
    )

    chain=prompt|llm
    result=chain.invoke(
        {
            "data":data,
            "scrapped_information_for_data_scrutinization":scrapped_information_for_data_scrutinization
        }
    )

    response={
        "data_scrutiny_test":result.data_scrutiny_test
    }

    return response