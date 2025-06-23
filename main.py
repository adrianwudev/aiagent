from dotenv import load_dotenv
import os
from smolagents.models import AzureOpenAIServerModel
from smolagents import CodeAgent, WebSearchTool, Tool
from playwright_tools.save_script_tool import save_script_tool
from playwright_tools.read_script_tool import read_script_tool
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
            save_script_tool,
            read_script_tool,
            SaveResultTool(),
            ReadResultTool(),
        ],
        model=model,
        additional_authorized_imports=[
            "base64",
            "time",
            "json",

            "playwright",
            "playwright",
            "playwright.sync_api",
            "playwright.async_api",
            "asyncio",
            "playwright_tools.session_context.PlaywrightSessionContext.init_session",
            "playwright_tools.session_context",
            
        ]
    )
    query = (
        """
        IMPORTANT: You are a stepwise, stateful agent for automating the Quick, Draw! game using Playwright and Python.
            Befroe start, please read documentation of Playwright https://playwright.dev/python/docs/api/class-playwright ,
            learn how to leverage playwright in your testing script.
        Session Management:
        - Always use the provided PlaywrightSessionContext to manage the browser session and state.
        - When you need to open the browser window for the first time, always call:
          ```python
          from playwright_tools.session_context import PlaywrightSessionContext
          PlaywrightSessionContext().init_session()
          ```
          This will initialize the Playwright session and automatically navigate to the initial URL (e.g., https://quickdraw.withgoogle.com/).
          Do NOT call `get_page()` before `init_session()` on the first run.
        - Get the shared page with:
          ```python
          page = PlaywrightSessionContext().get_page()
          ```
        - To get and update the current state, use:
          ```python
          state = PlaywrightSessionContext().get_state()
          # update state as needed
          PlaywrightSessionContext().save_state()
          ```
        - Do NOT create a new Playwright/browser instance in each function. Only call `PlaywrightSessionContext().close()` at the very end.

        Stepwise Execution:
        - The workflow is divided into multiple steps. After each step, update and save the current state (e.g., which step is completed, what is the current prompt, is the canvas ready, etc.).
        - At each step, check the current state and only perform the next required action.
        - If an error occurs, retry the current step or handle the error gracefully. Do NOT refresh (F5) the page or restart the entire script unless absolutely necessary.
        - If the script is interrupted or fails, you must be able to resume from the last successful step using the saved state.

        Workflow Example:
        1. Open https://quickdraw.withgoogle.com/ (step 0)
        2. Click the 'Let's Draw!' button (step 1)
        3. Get the drawing prompt, using tool WebSearchTool to search how to draw the prompt (step 2)
        4. Click the 'Got It!' button to enter the drawing stage (step 3)
        5. Wait for the canvas to be ready (step 4)
        6. Use WebSearchTool to search for "how to draw a {prompt}" and analyze the results (step 5)
        7. Draw on the canvas based on the tutorial, you only have 20 secounds to draw, if exceed you will go back to step 3 (step 6)
        8. Save the canvas image (step 7)
        9. Save your script and results (step 8)
        10. At the end, call `PlaywrightSessionContext().close()` (step 9)
        11. Print the result of how you doing good, bad, your target, whether success.

        State Management:
        - Maintain a state variable (e.g., a Python dict) to track progress and avoid repeating completed steps.
        - After each step, update the state and, if possible, persist it (e.g., save to a file or variable).
        - When resuming, read the state and continue from the last incomplete step.

        You must flexibly combine Playwright browser automation and web search, dynamically adapting your workflow based on the latest online knowledge and the current state.
        """
    )


    output = agent.run(query)

    # memory.save_context({"input": query}, {"output": output})
