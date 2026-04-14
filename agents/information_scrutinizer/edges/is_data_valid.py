def IsDataValid(state):
    data_test=state["data_scrutiny_test"]

    for test in data_test:
        if test["data_field_scrutiny_test"] == "Failed":
            return "invalid data"


    return "valid data"