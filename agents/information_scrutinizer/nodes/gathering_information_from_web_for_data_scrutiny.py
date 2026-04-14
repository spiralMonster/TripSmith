import re
from tools.quora_scrapper import scrape_from_quora
from tools.reddit_scrapper import scrape_from_reddit
from tools.summarizer import summarize_document

def GatherInformationFromWebForDataScrutiny(state):
    queries=state["generated_queries_for_data_scrutinization"]

    generated_query_and_scrapped_information=[]

    for query in queries:
        information_from_reddit=scrape_from_reddit(
            query=query,
            num_articles_to_scrape=5
        )["tool_response"]

        information_from_quora=scrape_from_quora(
            query=query,
            num_articles_to_scrape=5
        )["tool_response"]

        information_scrapped=information_from_reddit+'\n'+information_from_quora
        information_scrapped=re.sub(r'\s\s+','',information_scrapped)

        summarized_information=summarize_document.invoke(
            {
                "document":information_scrapped,
                "max_length":40
            }
        )

        resp={
            "query":query,
            "information_scrapped":summarized_information
        }

        generated_query_and_scrapped_information.append(resp)


    response={
        "scrapped_information_for_data_scrutinization":generated_query_and_scrapped_information
    }

    return response




