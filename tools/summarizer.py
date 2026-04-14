import torch
from langchain_core.tools import tool
from transformers import AutoTokenizer, AutoModelForCausalLM

@tool
def summarize_document(document:str,max_length:int)->str:
    """
    Summarize the given document.
    Args:
        document (str): The document to be summarized.
        max_length (int): The maximum length of the summary.
    """

    tokenizer=AutoTokenizer.from_pretrained("T5-base")
    model=AutoModelForCausalLM.from_pretrained("T5-base",return_dict=True)

    tokenized_text=tokenizer.encode(
        "Summarize: "+document,
        return_tensors="pt",
        max_length=max_length,
        truncation=False
    )

    output=model.generate(
        tokenized_text,
        max_length=max_length
    )

    summary=tokenizer.decode(output[0],skip_special_tokens=True)
    summary=summary.capitalize()

    return summary


if __name__=="__main__":
    document="""
    Players of Chennai Super Kings and Kolkata Knight Riders were seen wearing black armbands during their IPL 2026 clash, but it was not for legendary singer Asha Bhosale, as many fans initially believed.
    A day earlier, during the Sunrisers Hyderabad vs Rajasthan Royals match, players had worn black armbands to pay tribute to Asha Bhosale, who passed away at the age of 92. This led to some confusion among fans when similar visuals were seen in the CSK vs KKR game.
   However, the reason behind CSK and KKR players wearing black armbands was to mourn the passing of former India cricketer CD Gopinath. The gesture was a mark of respect for one of the early contributors to Indian cricket.
   The Board of Control for Cricket in India also expressed deep sorrow over Gopinath’s demise in Chennai. He was a part of India’s historic first-ever Test-winning team and played a key role during the early years when Indian cricket was still in developing stage.
    """

    max_length=30
    summary=summarize_document.invoke(
        {
            "document":document,
            "max_length":max_length
        }
    )

    print(summary)
