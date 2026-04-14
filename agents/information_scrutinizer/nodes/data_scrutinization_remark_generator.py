import os
from get_llm_model import GetLLM
from langchain_core.prompts import ChatPromptTemplate
from agents.information_scrutinizer.utils.data_scrutinization_remark_generator_specs import DataScrutinizationRemarkGeneratorSpecs

def generate_remark(llm,scrutinization_test):
    template="""
    You are provided the data scrutinization test for a data item.
    Data Scrutinization Test:
    {test}
    
    Based on it you have to generate remarks that will have the trip planner to:
     - Convey the information of scrutinization test to the user.
     - Guide the trip planner to frame questions that will ask the user to modify the vale of data field.
    
    Let's say the user has decided that the budget of the trip should be 500 dollars.
    And after scrutinizing the data we found that the average budget for that trip would be 800 dollars.
    Then you have to provide remark is such a way that will guide the trip planner to ask the right questions.
    For example in this case, asking the user to modify the trip budget from 500 dollars to 800 dollars.
    You can also include that how can the budget of 800 dollars would be a great choice instead of 800 dollars one. 
    """

    prompt=ChatPromptTemplate.from_template(
        template=template,
        input_variable=['test']
    )

    chain=prompt|llm
    result=chain.invoke(
        {
            "test":scrutinization_test
        }
    )

    response={
        "data_field_name":result.data_field_name,
        "remark_regarding_data_field":result.remark_regarding_data_field
    }

    return response


def DataScrutinizationRemarkGenerator(state):
    data_scrutinization_test=state["data_scrutiny_test"]

    llm = GetLLM(
        service_provider=os.environ["DEFAULT_SERVICE_PROVIDER"],
        temperature=os.environ["DEFAULT_TEMPERATURE"]
    )
    llm=llm.with_structured_output(DataScrutinizationRemarkGeneratorSpecs)

    data_scrutinization_remarks=[]
    for test in data_scrutinization_test:
        if test["data_field_scrutiny_test"]=="Failed":
            remark=generate_remark(llm,test)
            data_scrutinization_remarks.append(remark)


    response={
        "data_scrutinization_remarks":data_scrutinization_remarks
    }

    return response