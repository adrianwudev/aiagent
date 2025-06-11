from dotenv import load_dotenv
import os
from smolagents.models import AzureOpenAIServerModel
from smolagents import CodeAgent, WebSearchTool, Tool
from memory.PersistentFileMemory import PersistentFileMemory

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
        model_id=os.environ.get("AZURE_OPENAI_MODEL_ID"),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        custom_role_conversions={"system": "assistant", "tool-call": "assistant", "tool-response": "user"}
    )

    # Add memory
    memory = PersistentFileMemory(file_path="memory.json")

    history_prompt = ""
    for message in memory.chat_memory.messages:
        if message.type == "human":
            history_prompt += f"User: {message.content}\n"
        elif message.type == "ai":
            history_prompt += f"AI: {message.content}\n"

    agent = CodeAgent(
        tools=[
            WebSearchTool(),
            # Tool.from_langchain() #TODO Make tool to write the testing result into txt file
        ],
        model=model,
        additional_authorized_imports=[
            "selenium",
            "selenium.webdriver.common.by",
            "selenium.webdriver.common.keys",
            "webdriver_manager.chrome",
            "selenium.webdriver.chrome.service",

            "selenium.webdriver.support.ui",
            "selenium.common.exceptions",
            "selenium.webdriver.chrome.options"
        ]
    )
    query = (
        "Use Selenium WebDriver, launch a chrome webpage to open the page and simulate a QA test: "

        # "Make your web browser in full screen mode."
        "Please enter this link: https://gemini.google.com/. Make the browser full screen. Follow the steps below."
        "0. please read the DOM structure after you get in the Gemini page."
        "0.1. The location of the input box is at the bottom of the page."
        "1. Wait for 5 seconds, Type a creative question in the input box."
        # "this class is the dive for input box class='text-input-field_textarea-wrapper ng-tns-c2117731150-3', please find the input box according to this information."
        "1.1 The submit button will show up after you type the question, make sure the text you typed is really in the input box."
        "1.2. Click the submit button to send the question."
        "2.1. Wait for 5 seconds, observe the response from Gemini."
        "2.2. Type another creative question based on the response, and click the submit button again."
        "3. You must repeat step 2 until you have 20 conversations with Gemini."
        
        "Final. Please give me a summary of what happened."
        # "NOTE: If you failed to find any input box or summit button, "
        # "please re-try 10 times with new selenium script until you find it."
    )

    full_prompt = history_prompt + "\n" + query

    output = agent.run(full_prompt)

    memory.save_context({"input": query}, {"output": output})