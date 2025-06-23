from smolagents.tools import tool
from datetime import datetime
import os

@tool
def save_script_tool(script_content: str, stage: int = None) -> str:
    """
    name=save_script_tool
    Save a script content to the 'playwright_scripts_history' folder.
    The filename defaults to playwright_ plus a timestamp, and includes the stage if provided.
    You must include a summary block at the top of each playwright script you save.
    You must save playwright script that you just used.
    Args:
        script_content (str): The content of the script to save.
        stage (int, optional): The stage number to include in the filename.
    Returns:
        str: Result message indicating success or failure.
    """
    os.makedirs("playwright_scripts_history", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if stage is not None:
        filename = f"playwright_stage{stage}_{timestamp}.py"
    else:
        filename = f"playwright_{timestamp}.py"
    file_path = os.path.join("playwright_scripts_history", filename)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return f"Script saved to {file_path}"
    except Exception as e:
        return f"Error saving script: {e}"

@tool
def save_summary_tool(stage: int, target: str, failure_reason: str, suggestion: str) -> str:
    """
    Save a summary in a fixed format to the 'playwright_scripts_history' folder.
    The summary includes: Stage, Target, Failure Reason, Suggestions.
    Args:
        stage (int): The stage number.
        target (str): What you wanted to do.
        failure_reason (str): Why it failed.
        suggestion (str): How to improve next time.
    Returns:
        str: Result message indicating success or failure.
    """
    os.makedirs("playwright_scripts_history", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"summary_stage{stage}_{timestamp}.txt"
    file_path = os.path.join("playwright_scripts_history", filename)
    summary = (
        f"Stage: {stage}\n"
        f"Target: {target}\n"
        f"Failure Reason: {failure_reason}\n"
        f"Suggestions: {suggestion}\n"
    )
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(summary)
        return f"Summary saved to {file_path}"
    except Exception as e:
        return f"Error saving summary: {e}" 