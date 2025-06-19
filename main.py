from dotenv import load_dotenv
import os
from smolagents.models import AzureOpenAIServerModel
from smolagents import CodeAgent, WebSearchTool, Tool
from selenium_tools.save_selenium_script_tool import SaveSeleniumScriptTool

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

    agent = CodeAgent(
        tools=[
            WebSearchTool(),
            # Tool.from_langchain(SaveSeleniumScriptTool()), # Make tool to write the testing result into txt file
            SaveSeleniumScriptTool(),
        ],
        model=model,
        additional_authorized_imports=[
            "selenium",
            "selenium.webdriver.common.by",
            "selenium.webdriver.common.keys",
            "webdriver_manager.chrome",
            "selenium.webdriver.chrome.service",

            "selenium.webdriver.support.ui",
            "selenium.webdriver.support.expected_conditions",
            "selenium.common.exceptions",
            "selenium.webdriver.chrome.options",
            "selenium.webdriver.common.action_chains",
            "time",
            "json"
        ]
    )
    query = (
        # IMPORTANT: Before starting, read previous Selenium scripts for reference
        # Use the read_selenium_scripts tool to get previous scripts and learn from them to optimize your drawing strategy and element interactions.
        """
        Use Selenium WebDriver, enable UI to play the Quick, Draw! game at https://quickdraw.withgoogle.com/ and assess your ability.
        
        
        Follow these steps to play the game and record your performance:
        
        0. **Initial Setup & Game Start:**
           0.1. Navigate to: https://quickdraw.withgoogle.com/
           0.2. Wait for the page to load (3-5 seconds).
           0.3. Locate and click the "Let's Draw!" button to start the game. You need to find a button with text like "Let's Draw!".
           0.4. IMPORTANT: If there's an overlay or introduction, make sure to dismiss it or click "Got It!" to proceed.
       
        
        Final. Use tool save_selenium_script_tool to save the script you just used. And add summary on it to explian what's wrong, what's good and what can you do to improve in the future.
        Print me the result you got for this round of selenium using, is there any difficulty? What can you do to improve?
       """
    )


    output = agent.run(query)

    # memory.save_context({"input": query}, {"output": output})