from typing_extensions import List,TypedDict

class InputState(TypedDict):
    trip_destination:str
    extracted_data:dict



class OutputStateSchema(TypedDict):
    data_scrutiny_test:List[dict]|str
    data_scrutinization_remarks: List[dict]|str



class OutputState(TypedDict):
    agent_response:OutputStateSchema

class OverallState(InputState,OutputState):
    pass

