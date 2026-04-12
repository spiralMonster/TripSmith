from langchain_core.prompts import ChatPromptTemplate
from agents.query_checker.utils.query_validator_specs import QueryValidatorSpecs


def QueryValidator(state):
    query=state["query"]

    model=state["model"]
    model=model.with_structured_output(QueryValidatorSpecs)

    template="""
    You are provided with a query.
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

    return {
        'is_query_valid':is_query_valid
    }