def IsInformationSufficient(state):
    if state["is_extracted_information_sufficient"]=="Yes":
        return "sufficient information"

    else:
        return "not sufficient information"