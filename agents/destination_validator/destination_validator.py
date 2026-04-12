import os

from langchain_core.messages import SystemMessage,HumanMessage
from langchain_core.prompts import ChatPromptTemplate

from tools.quora_scrapper import scrape_from_quora
from tools.reddit_scrapper import scrape_from_reddit
from tools.news_scrappper import scrape_news_articles

from get_llm_model import GetLLM
from agents.destination_validator.utils.destination_validator_specs import DestinationValidatorSpecs


def DestinationValidator(destination:str)->dict:
    llm=GetLLM(
        service_provider=os.environ["DEFAULT_SERVICE_PROVIDER"],
        temperature=os.environ["DEFAULT_TEMPERATURE"]
    )

    tools=[scrape_from_quora,scrape_from_reddit,scrape_news_articles]

    available_tools={
        "scrape_from_quora":scrape_from_quora,
        "scrape_from_reddit":scrape_from_reddit,
        "scrape_news_articles":scrape_news_articles
    }
    llm_with_tools=llm.bind_tools(tools)


    messages=[
        SystemMessage(
            """
            The user is planning to visit given.
            Decide whether it is a right time to visit the given destination or not.
            In order to make decision you can use:
             - Public opinions about the best time to visit the given destination.
             - Recent news about the given destination.
            """
        ),
        HumanMessage(
            f"I am planning to visit {destination}."
        )
    ]

    ai_msg=llm_with_tools.invoke(messages)
    messages.append(ai_msg)

    for tool_call in ai_msg.tool_calls:
        tool_name=tool_call["name"].lower()
        print(f"[INFO] Calling tool: {tool_name}")

        selected_tool=available_tools[tool_name]

        tool_msg=selected_tool.invoke(tool_call)
        messages.append(tool_msg)

    llm_with_structured_output=state["model"].with_structured_output(DestinationValidatorSpecs)

    template="""
    You are provided with a series of messages between the user and AI.
    By analysing it, decide whether it is the right time to visit the destination or not with proper explanation.
    
    Messages:
    {messages}
    """

    prompt=ChatPromptTemplate.from_template(
        template=template,
        input_variable=["messages"]
    )

    chain=prompt|llm_with_structured_output
    response=chain.invoke(
        {
            "messages":messages
        }
    )

    right_time_to_visit=response.right_time_to_visit
    explanation=response.explanation

    if right_time_to_visit=="Yes":
        agent_remark=f"It is a right time to visit {destination}."


    else:
        agent_remark=f"""
        It is not right time to visit {destination}.
        Provide user with appropriate explanation regarding why it is not right time to visit {destination}.
        Ask user to either change the destination or to suggest some destination spots.
        """

    result={
        "agent_name":"Destination Validator",
        "agent_response":{
            "is_it_right_time_to_visit_destination":right_time_to_visit,
            "explanation":explanation,
            "agent_remark":agent_remark
        }
    }

    return result






