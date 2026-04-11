from typing_extensions import TypedDict
from langchain_core.language_models.chat_models import BaseChatModel

class InputState(TypedDict):
    query:str
    model:BaseChatModel


class OutputState(TypedDict):
    is_query_valid:str
    shall_destination_should_be_visited:str
    agent_response:str

