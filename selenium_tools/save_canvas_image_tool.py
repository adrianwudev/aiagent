from smolagents.tools import tool
import base64
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium_tools.session_context import SeleniumSessionContext

@tool
def save_canvas_image_tool(filename: str, wait_time: int = 10) -> str:
    """
    Save the canvas (id='drawingCanvas') as a PNG file to the 'draws/' folder.
    Only interacts with the current page/session, does not open or reload the URL.

    Args:
        filename (str): Filename for the PNG image.
        wait_time (int): Seconds to wait for the canvas element to appear. Default: 10.
    Returns:
        str: Result message indicating success or error.
    """
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