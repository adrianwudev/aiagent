from smolagents.tools import tool
from datetime import datetime
import os

@tool
def save_selenium_script_tool(script_content: str) -> str:
    """
    Save Selenium script content to the 'selenium_scripts_history' folder.
    The filename defaults to quickdraw_ plus a timestamp.
    Please include a summary block at the top of each script you save.
    Args:
        script_content (str): The content of the Selenium script to save.
    Returns:
        str: Result message indicating success or failure.
    """
    os.makedirs("selenium_scripts_history", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"quickdraw_{timestamp}.py"
    file_path = os.path.join("selenium_scripts_history", filename)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return f"Selenium script saved to {file_path}"
    except Exception as e:
        return f"Error saving Selenium script: {e}" 