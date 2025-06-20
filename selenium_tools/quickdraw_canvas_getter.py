from smolagents.tools import tool
from selenium_tools.session_context import SeleniumSessionContext
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@tool
def quickdraw_canvas_getter(wait_time: int = 10) -> str:
    """
    Retrieve the <canvas id="drawingCanvas"> element from the Quick, Draw! game and return its size, coordinates, and style attributes.
    Only interacts with the current page/session, does not open or reload the URL.

    Args:
        wait_time (int): Seconds to wait for the canvas element to appear. Default: 10.
    Returns:
        str: Canvas information or error message.
    """
    driver = SeleniumSessionContext().get_driver()
    wait_time = wait_time or 10
    try:
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