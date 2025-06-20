from dotenv import load_dotenv
import os
from smolagents.models import AzureOpenAIServerModel
from smolagents import CodeAgent, WebSearchTool, Tool
from selenium_tools.save_selenium_script_tool import SaveSeleniumScriptTool
from selenium_tools.read_selenium_script_tool import ReadSeleniumScriptTool
from selenium_tools.clicker_tool import ClickerTool
from selenium_tools.quickdraw_canvas_getter import QuickDrawCanvasGetterTool
from result_tools.save_result_tool import SaveResultTool
from result_tools.read_result_tool import ReadResultTool

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
            ReadSeleniumScriptTool(),
            ClickerTool(),
            QuickDrawCanvasGetterTool(),
            SaveResultTool(),
            ReadResultTool(),
        ],
        model=model,
        additional_authorized_imports=[
            "selenium",
            "selenium.webdriver.common.by",
            "selenium.webdriver.common.keys",
            "webdriver_manager.chrome",
            "selenium.webdriver.chrome.service",

            # "selenium.webdriver.support.ui",
            # "selenium.webdriver.support.expected_conditions",
            # "selenium.common.exceptions",
            # "selenium.webdriver.chrome.options",
            "selenium.webdriver.common.action_chains",

            "base64",
            "time",
            "json"
        ]
    )
    query = (
        """
        Read summary before you use any tools.

        IMPORTANT: Before starting, use the read_result_tool to review all previous Selenium test results in the results folder.
        Reflect on the difficulties and improvement suggestions from past runs, and use these insights to evolve your strategy for this round.

        Next, use the read_selenium_script_tool to review previous Selenium scripts. 
        Do not simply copy or repeat old scripts. 
        Prioritize learning from scripts that have a high score and are marked as successful in their summary.
        Analyze their strategies and results, and use these insights to optimize your own drawing strategy and element interactions for this run.

        In your summary, clearly explain what you learned from both the previous results and scripts, and what you improved compared to previous attempts.

        DOM: After enter any page, wait for 2 seconds, read all the DOM structure for better analysis.
        Use Selenium WebDriver to play the Quick Draw! game at https://quickdraw.withgoogle.com/ and assess your ability,
        !!!You must open the UI browser.!!!
        
        
        Follow these steps to play the game and record your performance:
        
        0. **Initial Setup & Game Start:**
           0.1. Navigate to: https://quickdraw.withgoogle.com/
           0.2. Wait for the page to load (3-5 seconds).
           0.3. Locate and use tool clicker_tool to click the "Let's Draw!" button to start the game. You need to find a button with text like "Let's Draw!".
           0.4. IMPORTANT: If there's an overlay or introduction, make sure to dismiss it or click "Got It!" to proceed.
       
       1. After click "Let's Draw", wait for 2 seconds, you will see another page with yellow background.
        1.1. Use tool quickdraw_word_reader to get the Drawing goal (e.g. car)
        1.2. Remember the Drawing goal and print it out
        1.3. Click mouse down and mouse up anywhere on the web page, move the cursor, get into the drawing stage

       2. After move the cursor from 1.3, wait for 1 secound, we should get to drawing stage
        2.1. Please follow the `Drawing goal` you just remembered, and use tool quickdraw_canvas_getter to locate the white board canvas.
        2.2. use mouse down and mouse up to draw on the white board canvas.
        2.3. use selenium_driver.save_screenshot to take a picure of your drawing whiteboard, download it to folder `draws/`
        
        Final. Use tool save_selenium_script_tool to save the script you just used. And add summary on it to explian what's wrong, what's good and what can you do to improve in the future.
        If you find the selenium script is repeated from the history, please refer its file_name, don't just leave it empty.
        Print me the result you got for this round of selenium using, is there any difficulty? What can you do to improve?
        Use tool save_result_tool to save the result.
       """
    )


    output = agent.run(query)

    # memory.save_context({"input": query}, {"output": output})