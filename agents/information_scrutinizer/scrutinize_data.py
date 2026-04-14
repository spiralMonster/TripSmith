from agents.information_scrutinizer.build_agent import BuildAgent

def ScrutinizeData(trip_destination:str, extracted_data:dict)->dict:
    agent=BuildAgent()

    response=agent.invoke({
        "trip_destination":trip_destination,
        "extracted_data":extracted_data
    })

    agent_response={
        "agent_name":"Information Scrutinizer",
        "agent_response":response["agent_response"]
    }

    return agent_response