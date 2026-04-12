import os
from dotenv import load_dotenv

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
from langchain_groq import ChatGroq
from langchain_cohere import ChatCohere
from langchain_perplexity import ChatPerplexity
from langchain_anthropic import ChatAnthropic
from langchain_deepseek import ChatDeepSeek


load_dotenv()


def GetLLM(service_provider:str,temperature:float)-> BaseChatModel:

    if service_provider=="openai":
        llm=ChatOpenAI(
            model="gpt-4.1",
            temperature=temperature,
            max_retries=2,
            api_key=os.environ["OPENAI_API_KEY"]
        )

    elif service_provider=="anthropic":
        llm=ChatAnthropic(
            model="claude-sonnet-4-5-20250929",
            temperature=temperature,
            max_retries=2,
            api_key=os.environ["ANTHROPIC_API_KEY"]
        )

    elif service_provider=="google":
        llm=ChatGoogleGenerativeAI(
            model="gemini-3.1-pro-preview",
            temperature=temperature,
            max_retries=2,
            api_key=os.environ["GOOGLE_GEMINI_API_KEY"]
        )

    elif service_provider=="deepseek":
        llm=ChatDeepSeek(
            model="deepseek-chat",
            temperature=temperature,
            max_retries=2,
            api_key=os.environ["DEEPSEEK_API_KEY"]
        )

    elif service_provider=="mistral":
        llm=ChatMistralAI(
            model="mistral-large-latest",
            temperature=temperature,
            max_retries=2,
            api_key=os.environ["MISTRAL_API_KEY"]

        )

    elif service_provider=="cohere":
        llm=ChatCohere(
            model="command-r",
            cohere_api_key=os.environ["COHERE_API_KEY"],
            max_retries=2,
            temperature=temperature
        )

    elif service_provider=="perplexity":
        llm=ChatPerplexity(
            model="sonar",
            temperature=temperature,
            max_retries=2,
            api_key=os.environ["PERPLEXITY_API_KEY"]
        )


    else:
        llm= ChatGroq(
            model="qwen/qwen3-32b",
            api_key=os.environ["GROQ_API_KEY"],
            max_retries=2,
            temperature=temperature
        )


    return llm
