from smolagents.tools import Tool
import base64
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium_tools.session_context import SeleniumSessionContext

class SaveCanvasImageTool(Tool):
    """
    Save the canvas (id='drawingCanvas') as a PNG file to the 'draws/' folder.
    The driver instance is managed internally and shared across all tools using SeleniumSessionContext.
    This tool does NOT open or reload the URL; it only interacts with the current page/session.
    """
    name = "save_canvas_image_tool"
    description = "Save the canvas (id='drawingCanvas') as a PNG file to the 'draws/' folder."
    inputs = {
        "filename": {"type": "string", "description": "Filename for the PNG image."},
        "wait_time": {"type": "integer", "description": "Wait seconds", "required": False, "nullable": True}
    }
    output_type = "string"

    def __init__(self):
        super().__init__()

    def forward(self, filename: str, wait_time: int = 10) -> str:
        driver = SeleniumSessionContext().get_driver()
        try:
            canvas = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.ID, "drawingCanvas"))
            )
            base64_img = driver.execute_script('return arguments[0].toDataURL("image/png").substring(22);', canvas)
            img_bytes = base64.b64decode(base64_img)
            os.makedirs("draws", exist_ok=True)
            file_path = os.path.join("draws", filename)
            with open(file_path, "wb") as f:
                f.write(img_bytes)
            return f"Canvas image saved to {file_path}"
        except Exception as e:
            return f"Error: {e}" 