def ResponseGenerator(state):

    agent_response={
        "extracted_information":state["extracted_information"],
        "is_information_sufficient":state["is_extracted_information_sufficient"],
        "insights_regarding_information":state["insights_regarding_information"]

    }

    is_information_sufficient=state["is_extracted_information_sufficient"]


    if is_information_sufficient=="Yes":
        agent_response["generated_questions_for_information_gathering"]=[]

    else:
        agent_response["generated_questions_for_information_gathering"]\
            =state["generated_questions_for_information_gathering"]


    return {
        "agent_response":agent_response
    }


