# ===============================
# Python Coding Best Practices for AI Agent
# - Always use isinstance(x, TYPE) for type checking in Python. The second argument of isinstance must be a type object (e.g., dict), not a string.
# - Prefer isinstance(x, dict) over type(x) is dict, as isinstance supports inheritance.
# - All Python code blocks (such as if, for, while, def, class) must be properly indented with 4 spaces. Never leave a code block empty.
# - Every if/elif/else/for/while/try/except block must contain at least one executable statement. Do not leave blocks empty.
# - Strictly follow Python syntax rules to avoid IndentationError, TypeError, and other common mistakes.
# - Before using a variable as a dictionary, always check its type with isinstance(variable, dict) and initialize it if necessary.
# - Never use a string as the type argument in isinstance or type checks.
# ===============================

from dotenv import load_dotenv
import os
from smolagents.models import AzureOpenAIServerModel
from smolagents import CodeAgent, WebSearchTool, Tool
from playwright_tools.save_script_tool import save_script_tool, save_summary_tool
from playwright_tools.read_script_tool import read_script_tool
from playwright_tools.read_prompt_tool import read_prompt_tool
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
            read_prompt_tool,
            save_summary_tool,
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
            "playwright_tools.session_context",
            "playwright_tools.detect_stage_tool",
            "typing",
            "inspect",
            "traceback"
            
        ]
    )
    query = (
        """
        You are a stepwise, stateful agent for automating the Quick, Draw! game using Playwright and Python.
        
        [Type Checking Best Practices]
        - Read official Python documentation about type checking: https://docs.python.org/3/library/typing.html
        - Search for Python type checking best practices using WebSearchTool before implementing any type checks
        - Always use these approaches when checking types:
          ```python
          # For single type check:
          if not isinstance(x, dict):
              x = {}
              
          # For multiple type checks:
          if not isinstance(x, (int, float)):
              x = 0
              
          # For complex type checks:
          try:
              if not isinstance(x, dict):
                  x = {}
          except TypeError:
              x = {}
          ```
        - NEVER use:
          - String type names in isinstance (e.g., isinstance(x, "dict"))
          - Direct type comparison with is (e.g., type(x) is dict)
          - Variable type names (e.g., isinstance(x, type_var))
        - Before implementing any type check:
          1. Search best practices with WebSearchTool
          2. Test in a small code snippet
          3. Include proper error handling
        - If type check fails:
          1. Log the error with full traceback
          2. Initialize to a safe default value
          3. Save both error and recovery action in state
        
        [General Python Coding Instructions]
        - Always use isinstance(x, TYPE) for type checking in Python. The second argument of isinstance must be a type object (e.g., dict), not a string.
        - Prefer isinstance(x, dict) over type(x) is dict, as isinstance supports inheritance.
        - All Python code blocks (such as if, for, while, def, class) must be properly indented with 4 spaces. Never leave a code block empty.
        - Every if/elif/else/for/while/try/except block must contain at least one executable statement. Do not leave blocks empty.
        - Strictly follow Python syntax rules to avoid IndentationError, TypeError, and other common mistakes.
        - Before using a variable as a dictionary, always check its type with isinstance(variable, dict) and initialize it if necessary.
        - Never use a string as the type argument in isinstance or type checks.
        - When using isinstance in Python, always use the type object (e.g., isinstance(x, dict)), not a string.
        - When using save_script_tool, you must follow the summary instruction, save playwright script and summary.
        - If your scripts have error after executed, please search on internet and think better quality of code.

        [Error Handling and Type Checking]
        - When encountering errors, ALWAYS:
          1. Search the web for solutions using WebSearchTool()
          2. Test your solution in a smaller code snippet first
          3. Only save working code into playwright scripts
        - For type checking, ONLY use these patterns:
          ```python
          # Pattern 1: Direct type check (PREFERRED)
          if not isinstance(state, dict):
              state = {}
          
          # Pattern 2: Safe type check with exception handling
          try:
              if not isinstance(state, dict):
                  state = {}
          except TypeError:
              state = {}
          
          # Pattern 3: Simple type comparison (use only if isinstance fails)
          if type(state) is not dict:
              state = {}
          ```
        - Never use string type names or variables as the second argument of isinstance()
        - Before running any code block, test it for basic syntax and type errors
        - After fixing any error, ALWAYS save the working version using save_script_tool

        [Script Content Requirements]
        - Your saved scripts MUST contain all necessary imports at the top
        - ALWAYS initialize state and page objects first
        - Include proper error handling for EVERY operation
        - Use consistent code style and patterns through the entire script
        - When saving scripts that encountered errors:
          1. First fix the error using web search and testing
          2. Save the FIXED version of the script, not the error version
          3. Include comments explaining what was fixed and why

        [Web Search Instructions]
        - Before writing any complex logic, search for best practices
        - When encountering errors, IMMEDIATELY search for solutions
        - Use code examples from trusted sources (official docs, Stack Overflow)
        - Adapt found solutions to match our exact needs and style

        [Self-Reflection and Learning]
        - Before each execution, you MUST read both previous scripts (using read_script_tool) and previous summaries (by reading all summary files in the playwright_scripts_history folder, or using a read_summary_tool if available).
        - After reading the history scripts, please find a better way to approach from internet using tool WebSearchTool().
        - Carefully reflect on past failures and suggestions from these summaries, and use this information to improve your next execution. Avoid repeating previous mistakes and try to implement suggested improvements.

        [Playwright Usage]
        - Please read the official Playwright documentation: https://playwright.dev/python/docs/api/class-playwright
        - All browser operations must use the shared page instance from PlaywrightSessionContext:
          ```python
          from playwright_tools.session_context import PlaywrightSessionContext
          page = PlaywrightSessionContext().get_page()
          ```
        - State management:
          ```python
          state = PlaywrightSessionContext().get_state()
          # update state
          PlaywrightSessionContext().save_state()
          ```
        - Do NOT create a new Playwright/browser instance in each function. Only call `PlaywrightSessionContext().close()` at the very end of the workflow.

        [Stage Detection]
        - Before every step, you MUST call `detect_quickdraw_stage()` (from playwright_tools.detect_stage_tool) to determine the current page state.
        - detect_quickdraw_stage will automatically reload the homepage and re-detect if the stage is unknown, and will always return the correct stage number:
          1 = Home page (Let's Draw! button visible)
          2 = Got It! button visible (prompt/keyword is visible)
          3 = Got It! button is being clicked
          4 = Drawing canvas visible
          0 = Still unknown
        - You only need to handle the returned stage; do NOT manually reload the page.

        [Stepwise Execution]
        - As soon as the prompt/keyword is visible in stage 2, ALWAYS use read_prompt_tool to extract the prompt word from the #challengetext-word div. Use this word for all subsequent web search and drawing plan preparation.
        - Stage 3 should ONLY click the 'Got It!' button and do nothing else.
        - Stage 4 should IMMEDIATELY execute the drawing commands with no delay, using the pre-prepared plan from stage 2. Do not perform any web search or planning in stage 4.
        - After each step, update and save the state (e.g., completed steps, current prompt, whether the canvas is ready, etc.).
        - At each step, check the state and only perform actions that have not been completed.
        - If an error occurs, retry the current step or handle it gracefully. Do NOT refresh (F5) or restart the entire script unless detect_quickdraw_stage still returns 0.
        - If the script is interrupted or fails, you must be able to resume from the last successful step using the saved state and the detected stage.
        - IMPORTANT: At each step, before marking the step as completed in the state, you MUST verify that the action was actually successful (e.g., the prompt was found and is not empty, the drawing was performed, the canvas was saved, etc.).
        - Only proceed to the summary and close the session if BOTH `drawing_done` and `canvas_image_saved` are True.
        - If any critical step fails (e.g., prompt not found, drawing not performed, canvas not saved), log the problem in the state, print an error summary, and do NOT mark the step as completed.
        - Always check the current stage and state before each action, and do not skip or mark steps as done unless they are truly completed.
        - After completing each stage (step), you MUST:
            - Immediately call save_script_tool to save the current playwright script, always including the stage number in the filename, you must save playwright script that you just ran.
            - Record any error log for this stage (if no error, record "No error").
            - Call save_summary_tool to save a summary for this stage, including: Stage, Target, Failure Reason (error log), Suggestions.
            - This must be done for every stage, not just at the end.

        [Workflow Example]
        0. Before starting, read all previous scripts (read_script_tool) and all previous summaries (read all summary files in playwright_scripts_history or use read_summary_tool). Reflect on past failures and suggestions, and use this information to improve your next execution.
        1. Call detect_quickdraw_stage() to determine the current stage.
        2. If stage 1, click the 'Let's Draw!' button.
        3. If stage 2, as soon as the prompt/keyword is visible, ALWAYS use read_prompt_tool to extract the prompt word from the #challengetext-word div. Use this word for all subsequent web search and drawing plan preparation.
        4. If stage 3, ONLY click the 'Got It!' button and do nothing else.
        5. If stage 4, IMMEDIATELY execute the drawing commands with no delay, using the pre-prepared plan from stage 2. Do not perform any web search or planning in stage 4. Only draw the simplest outline to maximize the chance of finishing within 20 seconds.
        6. After each action, update and save the state.
        7. If interrupted, resume from the detected stage.
        8. Save the canvas image.
        9. Save your playwright script and results using save_script_tool, always including the stage number in the filename, you must save the playwright script that you just ran.
        10. After each run and after every stage, call save_summary_tool to save a summary for this stage in the following fixed format: Stage, Target, Failure Reason (error log), Suggestions. This must be done for every stage, not just at the end.
        11. At the end, call `PlaywrightSessionContext().close()`.
        12. Print a summary: describe the result, success or failure, encountered problems, your target, and whether you succeeded.

        [State Management]
        - You must maintain a state variable (e.g., a Python dict) to track progress and avoid repeating steps.
        - After each step, update and save the state.
        - When resuming, read the state and continue from the last incomplete step.
        - If detect_quickdraw_stage still returns 0, go back to step 0 and restart the process.

        You must flexibly combine Playwright browser automation and web search using WebSearchTool, dynamically adapting your workflow based on the latest knowledge and the current state.

        [Script Saving Instructions]
        - Every time you call save_script_tool, you MUST save the actual Python Playwright code that was just executed for this stage.
        - The saved script must be a complete, runnable Python script, including all necessary imports, Playwright setup, and the exact actions performed.
        - Do NOT save only comments, error logs, or state summaries. The script must be executable and able to reproduce the automation for this stage.
        - If an error occurs, also save the code that led to the error, not just the error message.
        """
    )


    output = agent.run(query)

    # memory.save_context({"input": query}, {"output": output})
