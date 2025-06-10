from dotenv import load_dotenv
import os
# from pydantic import BaseModel # If no need Pydantic
# from langchain_openai import AzureChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate # If no need LangChain
# from langchain_core.output_parsers import PydanticOutputParser # If no need Pydantic
# from langchain.agents import create_tool_calling_agent, AgentExecutor # If dont use LangChain Agent
# from tools import search_tool, wiki_tool # If dont use LangChain
# from memory.PersistentFileMemory import PersistentFileMemory # If dont use LangChain

from smolagents.models import AzureOpenAIServerModel
from smolagents import CodeAgent, WebSearchTool # InferenceClientModel # No Need Anymore InferenceClientModel

load_dotenv("sample.env")

class PatchedAzureOpenAIServerModel(AzureOpenAIServerModel):
    def _prepare_completion_kwargs(self, *args, **kwargs):
        completion_kwargs = super()._prepare_completion_kwargs(*args, **kwargs)
        
        # Remove the 'stop' parameter if it exists
        if 'stop' in completion_kwargs:
            del completion_kwargs['stop']
        
        return completion_kwargs

if __name__ == "__main__":
    model = PatchedAzureOpenAIServerModel(
        model_id="4.1-mini",
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        custom_role_conversions={"system": "assistant", "tool-call": "assistant", "tool-response": "user"}
    )
    agent = CodeAgent(tools=[WebSearchTool()], model=model, add_base_tools=True)
    query = "https://www.google.com/search?q=snake+game"
    agent.run(query)


# class ResearchResponse(BaseModel):
#     topic: str
#     summary: str
#     sources: list[str]
#     tools_used: list[str]


# llm = AzureChatOpenAI(
#     azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME"),
#     api_version="2025-01-01-preview",
# )
# parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             """
#             You are a research assistant that will help generate a research paper.
#             Answer the user query and use neccessary tools. 
#             Wrap the output in this format and provide no other text\n{format_instructions}
#             """,
#         ),
#         ("placeholder", "{chat_history}"),
#         ("human", "{query}"),
#         ("placeholder", "{agent_scratchpad}"),
#     ]
# ).partial(format_instructions=parser.get_format_instructions())

# tools = [search_tool, wiki_tool]
# agent = create_tool_calling_agent(
#     llm=llm,
#     prompt=prompt,
#     tools=tools,
# )

# memory = PersistentFileMemory(
#     memory_key="chat_history",
#     return_messages=True,
#     file_path="chat_memory.json"
# )

# agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)
# query = input("Enter your query: ")
# raw_response = agent_executor.invoke({"query": query})

# try:
#     structured_response = parser.parse(raw_response.get("output"))
#     print("Prompt Successfully Parsed.")
#     print(structured_response)
# except Exception as e:
#     print("Error parsing response", e, "Raw Response - ", raw_response)