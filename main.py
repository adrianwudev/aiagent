from dotenv import load_dotenv
import os
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.chat_models import AzureChatOpenAI

load_dotenv("sample.env")

llm = AzureChatOpenAI(
    deployment_name=os.getenv("Microsoft.CognitiveServicesOpenAI-20250610015116"),
    openai_api_version="2024-05-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
)

resp = llm.invoke("What are you?")

print(resp)