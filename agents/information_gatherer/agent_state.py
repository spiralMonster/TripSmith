from typing_extensions import TypedDict,List
from langchain_core.messages import AIMessage,HumanMessage

class InputState(TypedDict):
    user_conversation: List[AIMessage|HumanMessage]


class OutputState(TypedDict):
    agent_response: dict


class OverallState(InputState,OutputState):
    pass