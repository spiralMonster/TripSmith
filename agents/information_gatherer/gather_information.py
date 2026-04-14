from typing import List
from langchain_core.messages import AIMessage,HumanMessage
from agents.information_gatherer.build_agent import BuildAgent

def GatherInformation(user_conversation: List[AIMessage|HumanMessage])->dict:
    agent=BuildAgent()

    response=agent.invoke({
        "user_conversation":user_conversation
    })

    agent_response={
        "agent_name":"Information Gatherer",
        "agent_response":response["agent_response"]
    }

    return agent_response