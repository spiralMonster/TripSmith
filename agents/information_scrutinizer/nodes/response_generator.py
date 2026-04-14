def ResponseGenerator(state):
    agent_response={}

    data = state["data_to_scrutinize"]
    data_test = state["data_scrutiny_test"]

    if data:
        remark_gen = False
        for test in data_test:
            if test["data_field_scrutiny_test"] == "Failed":
                remark_gen = True
                break

        if remark_gen:
            agent_response={
                "data_scrutiny_test":state["data_scrutiny_test"],
                "data_scrutinization_remarks":state["data_scrutinization_remarks"]
            }

        else:
            agent_response = {
                "data_scrutiny_test": state["data_scrutiny_test"],
                "data_scrutinization_remarks":"All the data fields have valid values."
            }



    else:
        agent_response={
            "data_scrutiny_test":"There was no need for data scrutinization.",
            "data_scrutinization_remarks":"No remarks."
        }


    response={
        "agent_response":agent_response
    }

    return response