from langchain_core.prompts import ChatPromptTemplate
from agents.query_checker.utils.travel_destination_extractor_specs import TravelDestinationExtractorSpecs


def TravelDestinationExtractor(state):
    model=state["model"].with_structured_output(TravelDestinationExtractorSpecs)
    query=state["query"]

    template="""
    You are provided with the user query.
    Your job is to return the travelling destination from the query if present or else return 'None'.
    Just return the destination and nothing else.
    Query:
    {query}
    """

    prompt=ChatPromptTemplate.from_template(
        template=template,
        input_variable=["query"]
    )

    chain=prompt|model

    response=chain.invoke(
        {
            "query":query
        }
    )

    destination=response.destination

    result={
        "destination":destination
    }

    return result