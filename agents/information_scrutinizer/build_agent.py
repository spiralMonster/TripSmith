import os
from langgraph.graph import StateGraph,START,END
from agents.information_scrutinizer.agent_state import OverallState,InputState,OutputState

from agents.information_scrutinizer.nodes.data_extractor_for_scrutiny import DataExtractorForScrutiny
from agents.information_scrutinizer.nodes.query_generator_for_data_scrutinization import QueryGeneratorForDataScrutinization
from agents.information_scrutinizer.nodes.gathering_information_from_web_for_data_scrutiny import GatherInformationFromWebForDataScrutiny
from agents.information_scrutinizer.nodes.data_scrutinization_test import DataScrutinizationTest
from agents.information_scrutinizer.nodes.data_scrutinization_remark_generator import DataScrutinizationRemarkGenerator
from agents.information_scrutinizer.nodes.response_generator import ResponseGenerator

from agents.information_scrutinizer.edges.is_data_available_for_scrutinization import IsDataAvailableForScrutinization
from agents.information_scrutinizer.edges.is_data_valid import IsDataValid


def BuildAgent():
    builder=StateGraph(OverallState,input_schema=InputState,output_schema=OutputState)

    builder.add_node("data_extractor_for_scrutinization",DataExtractorForScrutiny)
    builder.add_node("query_gen_for_data_scrutinization",QueryGeneratorForDataScrutinization)
    builder.add_node("gather_info_for_data_scrutiny",GatherInformationFromWebForDataScrutiny)
    builder.add_node("data_scrutinization_tester",DataScrutinizationTest)
    builder.add_node("data_scrutinization_remark_gen",DataScrutinizationRemarkGenerator)
    builder.add_node("response_generator",ResponseGenerator)

    builder.add_edge(START,"data_extractor_for_scrutinization")
    builder.add_conditional_edges(
        "data_extractor_for_scrutinization",
        IsDataAvailableForScrutinization,
        {
            "data for scrutinization":"query_gen_for_data_scrutinization",
            "no data for scrutinization":"response_generator"
        }
    )

    builder.add_edge("query_gen_for_data_scrutinization","gather_info_for_data_scrutiny")
    builder.add_edge("gather_info_for_data_scrutiny","data_scrutinization_tester")
    builder.add_conditional_edges(
        "data_scrutinization_tester",
        IsDataValid,
        {
            "invalid data":"data_scrutinization_remark_gen",
            "valid data":"response_generator"
        }
    )

    builder.add_edge("data_scrutinization_remark_gen","response_generator")
    builder.add_edge("response_generator",END)

    agent=builder.compile()

    try:
        if os.path.exists("information_scrutinizer_agent.png"):
            pass

        else:
            img = agent.get_graph().draw_mermaid_png()
            with open("information_scrutinizer_agent.png", "wb") as file:
                file.write(img)

    except Exception as e:
        print(e)


    return agent


if __name__=="__main__":
    BuildAgent()
