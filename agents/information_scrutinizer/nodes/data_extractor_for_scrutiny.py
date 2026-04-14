import os
from get_llm_model import GetLLM
from langchain_core.prompts import ChatPromptTemplate
from agents.information_scrutinizer.utils.data_extractor_for_scrutiny_specs import DataExtractorForScrutinySpecs

def DataExtractorForScrutiny(state):
    extracted_data=state["extracted_data"]

    llm = GetLLM(
        service_provider=os.environ["DEFAULT_SERVICE_PROVIDER"],
        temperature=os.environ["DEFAULT_TEMPERATURE"]
    )
    llm=llm.with_structured_output(DataExtractorForScrutinySpecs)

    template="""
    You are provided with the data required to plan a trip from the conversation between the user and the trip planner.
    Extracted Data:
    {extracted_data}
    
    Now among the extracted data, you have to decide which data needs to be scrutinized.
    Return only those data items that need to be scrutinized.
    
    The data that needs to be scrutinized could be:
     - The trip budget
     - The number of days allocated for trip
     - The trip dates
     - And other information that you feel should be scrutinized
    
    If you feel that there is no need to scrutinize any data then just return empty dict.
    """

    prompt=ChatPromptTemplate.from_template(
        template=template,
        input_variable=['extracted_data']
    )

    chain=prompt|llm
    result=chain.invoke({
        "extracted_data":extracted_data
    })

    response={
        "data_to_scrutinize":result.data_to_scrutinize
    }

    return response