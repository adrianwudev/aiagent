from dotenv import load_dotenv
import os
from smolagents.models import AzureOpenAIServerModel
from smolagents import CodeAgent, WebSearchTool

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
            # Tool.from_langchain() #TODO Make tool to write the testing result into txt file
        ],
        model=model,
        additional_authorized_imports=[
            "selenium",
            "selenium.webdriver.common.by",
            "selenium.webdriver.common.keys",
            "webdriver_manager.chrome",
            "selenium.webdriver.chrome.service",

            # "selenium.webdriver.support.ui",
            # "selenium.common.exceptions",
        ]
    )
    query = (
        "Use Selenium WebDriver to open the page and simulate a QA test: "

        # "Make your web browser in full screen mode."
        "Please enter this link: https://territorial.io/."
        "1. Click Multiplayer button at the center of web page. Wait for 5 sec."
        "2. Click Ready button. Wait for team matched, it may take more than 1 min."
        "3. Click left mouse click, you will see a sword icon, and click it with left mouse click again."
        "4. After step 3, you can see your territory is growing."
        "5. Keep playing till the game end."
        "6. Read the LEADERBOARD put it into report."
        
        # "After open the link, you will see a input box in the bottom with phrase 'Ask Gemini', it's the input box you need."
        # "If you can not find the input box, it's next to a '+' sign. Try to find it."
        # "1. Type a creative question and click summit button in the right side of the input box."
        # "1.1. In this step, you might be transfer to human verify page, please study the article provided in step 0, and try to overcome it."
        # "2. Analyze the response and summit another interesting question based on its reply."
        # "3. Observe and do the same, until 10 conversations."
        "7. Please give me a summary of what happened."
        # "NOTE: If you failed to find any input box or summit button, "
        # "please re-try 10 times with new selenium script until you find it."
    )
    agent.run(query)