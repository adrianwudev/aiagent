from smolagents.tools import tool
from selenium_tools.session_context import SeleniumSessionContext
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

@tool
def clicker_tool(selector: str = '', wait_time: int = 10) -> str:
    """
    Click a specified button on a web page using Selenium WebDriver. Simulates human-like mouse move, mouse down, and mouse up events.
    The driver instance is managed internally and shared across all tools using SeleniumSessionContext.
    This tool does NOT open or reload the URL; it only interacts with the current page/session.

    Args:
        selector (str): CSS selector for the button to click. Default: '#button-play'.
        wait_time (int): Seconds to wait for the button to appear. Default: 10.

    Returns:
        str: Result message indicating success or failure.
    """
    driver = SeleniumSessionContext().get_driver()
    if not selector:
        selector = "#button-play"
    wait_time = wait_time or 10
    try:
        button = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )
        actions = ActionChains(driver)
        actions.move_to_element(button).pause(0.2).click_and_hold(button).pause(0.1).release(button).perform()
        time.sleep(1)
        return f"Clicked button with selector '{selector}' using mouse down/up simulation."
    except Exception as e:
        return f"Error clicking button with selector '{selector}': {e}" 