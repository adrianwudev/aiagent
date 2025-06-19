from typing import Optional
from datetime import datetime
from smolagents.tools import Tool
import os

class SaveSeleniumScriptTool(Tool):
    """
    A SmolAgents Tool that saves Selenium script content to the 'selenium_scripts_history' folder.
    # --- Script Summary ---
    # Purpose: [What is the goal of this script?]
    # Result: [What was the outcome?]
    # Achieved: [Did it meet the expectations? Yes/No. Briefly explain.]
    # Score: [Rate this script from 1 (poor) to 10 (excellent)]
    # Suggestions: [How could this script be improved in the future?]
    # ----------------------
    """
    
    name = "save_selenium_script_tool"
    description = (
        "Save a Selenium script to the 'selenium_scripts_history' folder. "
        "You can specify a filename, or it will use a timestamp by default."
    )
    inputs = {
        "script_content": {
            "type": "string",
            "description": "The content of the Selenium script to save."
        },
        "filename": {
            "type": "string",
            "description": "Optional filename (e.g. 'my_script.py'). If not provided, a timestamped filename will be used.",
            "required": False,
            "nullable": True
        }
    }
    output_type = "string"

    def __init__(self):
        super().__init__()

    def doSave(self, script_content: str, filename: Optional[str] = None) -> str:
        os.makedirs("selenium_scripts_history", exist_ok=True)
        if not filename or not filename.strip():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"selenium_script_{timestamp}.py"
        else:
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}{ext or '.py'}"
        file_path = os.path.join("selenium_scripts_history", filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(script_content)
            return f"Selenium script saved to {file_path}"
        except Exception as e:
            return f"Error saving Selenium script: {e}" 