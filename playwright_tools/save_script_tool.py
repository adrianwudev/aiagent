from smolagents.tools import tool
from datetime import datetime
import os

@tool
def save_script_tool(script_content: str) -> str:
    """
    Save a script content to the 'playwright_scripts_history' folder.
    The filename defaults to playwright_ plus a timestamp.
    Please include a summary block at the top of each script you save.

    The summary block must follow this format:
    ===
    Goal: <What was the objective of this script run?>
    Achieved: <Yes/No>
    Reason for Failure: <Why did it fail, if it did?>
    Suggestions for Improvement: <What can be improved or changed next time?>
    ===
    (Place this summary at the very top of the script file.)

    Args:
        script_content (str): The content of the script to save. The content must start with the summary block as described above.
    Returns:
        str: Result message indicating success or failure.
    """
    os.makedirs("playwright_scripts_history", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"playwright_{timestamp}.py"
    file_path = os.path.join("playwright_scripts_history", filename)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return f"Script saved to {file_path}"
    except Exception as e:
        return f"Error saving script: {e}" 