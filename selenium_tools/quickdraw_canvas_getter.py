from typing import Optional
from smolagents.tools import Tool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class QuickDrawCanvasGetterTool(Tool):
    """
    A SmolAgents Tool that retrieves the <canvas id="drawingCanvas"> element from Quick, Draw! game.
    Returns its size, coordinates, and style attributes for drawing automation.
    """
    name = "quickdraw_canvas_getter"
    description = (
        "Get the <canvas id='drawingCanvas'> element from Quick, Draw! and return its size, coordinates, and style attributes."
    )
    inputs = {
        "url": {
            "type": "string",
            "description": "The URL of the Quick, Draw! game page."
        },
        "wait_time": {
            "type": "integer",
            "description": "Seconds to wait for the canvas element to appear. Default: 10",
            "required": False,
            "nullable": True
        }
    }
    output_type = "string"

    def __init__(self):
        super().__init__()

    def forward(self, url: str, wait_time: Optional[int] = 10) -> str:
        wait_time = wait_time or 10
        driver = webdriver.Chrome()
        try:
            driver.get(url)
            canvas = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.ID, "drawingCanvas"))
            )
            width = canvas.get_attribute("width")
            height = canvas.get_attribute("height")
            style = canvas.get_attribute("style")
            rect = driver.execute_script("return arguments[0].getBoundingClientRect();", canvas)
            info = (
                f"Canvas found!\n"
                f"Width: {width}\n"
                f"Height: {height}\n"
                f"Style: {style}\n"
                f"Bounding rect: {rect}\n"
            )
            return info
        except Exception as e:
            return f"Error getting canvas: {e}"
        finally:
            driver.quit() 