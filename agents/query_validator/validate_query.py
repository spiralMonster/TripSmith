import os
from typing import List

from langchain_core.prompts import ChatPromptTemplate
from get_llm_model import GetLLM
from agents.query_validator.utils.query_validator_specs import QueryValidatorSpecs


def QueryValidator(user_queries:List[str])->dict:
    query=user_queries

    model=GetLLM(
        service_provider=os.environ["DEFAULT_SERVICE_PROVIDER"],
        temperature=os.environ["DEFAULT_TEMPERATURE"]
    )
    model=model.with_structured_output(QueryValidatorSpecs)

    template="""
    You are provided with user queries.
    Your job is to decide whether the query is related to planning a trip or not.
    Query:
    {query}
    """

    prompt=ChatPromptTemplate.from_template(
        template=template,
        input_variable=['query']
    )

    chain=prompt|model

    result=chain.invoke({
        'query':query
    })

    is_query_valid=result.is_query_valid

    if is_query_valid=="Yes":
        agent_remark="The query is related to planning a trip, so it is a valid query."

    else:
        agent_remark="""
        The query is not related to planning a trip.
        Kindly tell the user that you cannot process their request.
        Remind user about the tasks you can perform
        """

    response={
        "agent_name":"Query Validator",
        "agent_response":{
            "is_query_valid":is_query_valid,
            "agent_remark":agent_remark

        }
    }

    return response