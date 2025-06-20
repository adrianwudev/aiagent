from typing import Optional
from smolagents.tools import Tool
from datetime import datetime
import os

class SaveResultTool(Tool):
    """
    A SmolAgents Tool that saves the result, difficulties, and improvement suggestions for a Selenium test round.
    The result is saved to the 'result_history' folder with a timestamped filename.
    """
    name = "save_result_tool"
    description = (
        "Save the result, difficulties, and improvement suggestions for this round of Selenium testing "
        "to the 'result_history' folder."
    )
    inputs = {
        "result": {
            "type": "string",
            "description": "The result you got for this round of Selenium testing."
        },
        "difficulty": {
            "type": "string",
            "description": "Any difficulties encountered during this round."
        },
        "improvement": {
            "type": "string",
            "description": "Suggestions for improvement in the future."
        }
    }
    output_type = "string"

    def __init__(self):
        super().__init__()

    def forward(self, result: str, difficulty: str, improvement: str) -> str:
        os.makedirs("result_history", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"result_{timestamp}.txt"
        file_path = os.path.join("result_history", filename)
        content = (
            f"--- Selenium Test Result ---\n"
            f"Timestamp: {timestamp}\n\n"
            f"Result: {result}\n\n"
            f"Difficulty: {difficulty}\n\n"
            f"Improvement: {improvement}\n"
        )
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Result saved to {file_path}"
        except Exception as e:
            return f"Error saving result: {e}" 