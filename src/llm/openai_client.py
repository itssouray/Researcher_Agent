from langchain_openai import ChatOpenAI

from src.config.settings import (
    OPENAI_API_KEY,
    MODEL_NAME
)


llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model=MODEL_NAME,
    temperature=0
)