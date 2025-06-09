from dotenv import load_dotenv
import os
from langchain_openai import AzureChatOpenAI

load_dotenv("sample.env")

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME"),
    api_version="2025-01-01-preview",
)

resp = llm.invoke("What are you?")

print(resp)