from smolagents.tools import Tool
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from selenium_tools.session_context import SeleniumSessionContext

class CanvasInfoTool(Tool):
    """
    Get the bounding rect, width, height, and style of the canvas element (id='drawingCanvas').
    The driver instance is managed internally and shared across all tools using SeleniumSessionContext.
    This tool does NOT open or reload the URL; it only interacts with the current page/session.
    """
    name = "canvas_info_tool"
    description = "Get the bounding rect, width, height, and style of the canvas element (id='drawingCanvas')."
    inputs = {
        "wait_time": {"type": "integer", "description": "Wait seconds", "required": False, "nullable": True}
    }
    output_type = "string"

    def __init__(self):
        super().__init__()

    def forward(self, wait_time: int = 10) -> str:
        driver = SeleniumSessionContext().get_driver()
        try:
            canvas = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.ID, "drawingCanvas"))
            )
            width = canvas.get_attribute("width")
            height = canvas.get_attribute("height")
            style = canvas.get_attribute("style")
            rect = driver.execute_script("return arguments[0].getBoundingClientRect();", canvas)
            info = {
                "width": width,
                "height": height,
                "style": style,
                "boundingClientRect": rect
            }
            return json.dumps(info)
        except Exception as e:
            return f"Error: {e}"
        finally:
            driver.quit() 