import os
from langgraph.graph import StateGraph,START,END
from agent_state import InputState,OutputState,OverallState

from agents.information_gatherer.nodes.information_extractor import InformationExtractor
from agents.information_gatherer.nodes.information_sufficiency_decider import InformationSufficienyDecider
from agents.information_gatherer.nodes.question_generator_for_information_gathering import QuestionGeneratorForInformationGathering
from agents.information_gatherer.nodes.response_generator import ResponseGenerator

from agents.information_gatherer.edges.is_information_sufficient import IsInformationSufficient

def BuildAgent():
    builder=StateGraph(OverallState,input_schema=InputState,output_schema=OutputState)

    #Add nodes:
    builder.add_node("information_extractor",InformationExtractor)
    builder.add_node("information_sufficiency_decider",InformationSufficienyDecider)
    builder.add_node("question_gen_for_info_gathering",QuestionGeneratorForInformationGathering)
    builder.add_node("response_generator",ResponseGenerator)

    #Add edges:
    builder.add_edge(START,"information_extractor")
    builder.add_edge("information_extractor","information_sufficiency_decider")

    builder.add_conditional_edges(
        "information_sufficiency_decider",
        IsInformationSufficient,
        {
            "sufficient information": "response_generator",
            "not sufficient information":"question_gen_for_info_gathering"
                 }
    )

    builder.add_edge("question_gen_for_info_gathering","response_generator")
    builder.add_edge("response_generator",END)

    agent=builder.compile()

    try:
        if os.path.exists("information_gatherer_agent.png"):
            pass

        else:
            img = agent.get_graph().draw_mermaid_png()
            with open("information_gatherer_agent.png", "wb") as file:
                file.write(img)

    except Exception as e:
        print(e)


    return agent


if __name__=="__main__":
    BuildAgent()

