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
from selenium_tools.canvas_info_tool import CanvasInfoTool
from selenium_tools.draw_on_canvas_tool import DrawOnCanvasTool
from selenium_tools.robust_click_tool import RobustClickTool
from selenium_tools.save_canvas_image_tool import SaveCanvasImageTool
from selenium_tools.quickdraw_word_reader import QuickDrawWordReaderTool
from selenium_tools.session_context import SeleniumSessionContext
from selenium_tools.navigate_tool import NavigateTool


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
            SaveSeleniumScriptTool(),
            ReadSeleniumScriptTool(),
            ClickerTool(),
            QuickDrawCanvasGetterTool(),
            SaveResultTool(),
            ReadResultTool(),
            CanvasInfoTool(),
            DrawOnCanvasTool(),
            RobustClickTool(),
            SaveCanvasImageTool(),
            QuickDrawWordReaderTool(),
            NavigateTool(),
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
        IMPORTANT: Do NOT create or close the Selenium WebDriver instance yourself.
        Never write code like `driver = webdriver.Chrome()`, `driver.quit()`, or `driver.get(url)`.
        Only use the provided tools (such as navigate_tool, robust_click_tool, draw_on_canvas_tool, etc.) for all Selenium operations.

        At the beginning of your workflow, use navigate_tool to open the target URL ONCE (e.g., https://quickdraw.withgoogle.com/).
        For all subsequent steps, do NOT open the URL again—assume the browser is already on the correct page.
        All other tools must NOT open or reload the URL; they should only interact with the current page/session.
        All tools except navigate_tool do NOT accept a url parameter. For example, use save_canvas_image_tool(filename=..., wait_time=...) with no url argument.
        After each tool call, check if the result contains 'Error'. If so, print the error, call final_answer with a failure message, and exit the script immediately. This ensures the workflow stops and notifies the user if the Selenium session is closed or any step fails.

        You are an autonomous AI agent for automating the Quick, Draw! game using Selenium and a set of modular tools.
        You must think step by step, reflect on past results and scripts, and optimize your strategy each round.

        Before starting:
        - Use read_result_tool to review all previous Selenium test results in the results folder.
        - Reflect on the difficulties and improvement suggestions from past runs.
        - Use these insights to evolve your strategy for this round.

        Next:
        - Use read_selenium_script_tool to review previous Selenium scripts.
        - Do not simply copy or repeat old scripts.
        - Prioritize learning from scripts that have a high score and are marked as successful in their summary.
        - Analyze their strategies and results, and use these insights to optimize your own drawing strategy and element interactions for this run.

        When interacting with the page:
        - Use robust_click_tool for all button clicks. It will automatically handle overlays and use multiple strategies to ensure the click succeeds.
        - Before drawing, use canvas_info_tool to get the canvas size and coordinates.
        - Use draw_on_canvas_tool to draw lines, circles, or sine waves on the canvas according to the drawing goal.
        - After drawing, use save_canvas_image_tool to save the canvas as a PNG file (do NOT pass a url argument).
        - Always handle exceptions and provide fallback strategies if an action fails.

        DOM analysis:
        - After entering any page, wait for 2 seconds, then read the entire DOM structure for better analysis.

        Game flow:
        0. Initial Setup & Game Start:
        0.1. Use navigate_tool to open: https://quickdraw.withgoogle.com/
        0.2. Wait for the page to load (3-5 seconds).
        0.3. Use robust_click_tool to click the 'Let's Draw!' button to start the game.
        0.4. If there's an overlay or introduction, robust_click_tool will handle it.

        1. After clicking 'Let's Draw', wait for 2 seconds. You will see another page with a yellow background.
        1.1. Use quickdraw_word_reader to get the drawing goal (e.g. car).
        1.2. Remember the drawing goal and print it out.
        1.3. Use robust_click_tool or mouse events to enter the drawing stage.

        2. After entering the drawing stage, wait for 1 second.
        2.1. Use canvas_info_tool to locate the white board canvas.
        2.2. Use draw_on_canvas_tool to draw on the white board canvas according to the drawing goal.
        2.3. Use save_canvas_image_tool to save a picture of your drawing whiteboard to the 'draws/' folder (do NOT pass a url argument).

        Finalization:
        - Use save_selenium_script_tool to save the script you just used. Add a summary to explain what went wrong, what was good, and what can be improved in the future.
        - Print the result you got for this round of selenium usage, any difficulties, and what you can do to improve.
        - Use save_result_tool to save the result.

        In your summary, clearly explain:
        - What you learned from both the previous results and scripts.
        - What you improved compared to previous attempts.
        - Any new strategies or fallback logic you implemented.
        """
    )


    output = agent.run(query)

    # memory.save_context({"input": query}, {"output": output})
