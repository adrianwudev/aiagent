from smolagents.tools import tool
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from selenium_tools.session_context import SeleniumSessionContext

@tool
def canvas_info_tool(wait_time: int = 10) -> str:
    """
    Get the bounding rect, width, height, and style of the canvas element (id='drawingCanvas').
    Only interacts with the current page/session, does not open or reload the URL.

    Args:
        wait_time (int): Seconds to wait for the canvas element to appear. Default: 10.
    Returns:
        str: JSON string with canvas info or error message.
    """
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