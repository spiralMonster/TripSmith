def IsDataAvailableForScrutinization(state):
    data=state["data_to_scrutinize"]

    if data:
        return "data for scrutinization"

    else:
        return "no data for scrutinization"