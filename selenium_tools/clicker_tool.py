from typing import Optional
from smolagents.tools import Tool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ClickerTool(Tool):
    """
    A SmolAgents Tool that clicks a specified button on a web page using Selenium WebDriver.
    By default, it clicks the 'Let's Draw!' button on Quick, Draw! (button id='button-play').
    """
    name = "clicker_tool"
    description = (
        "Click a button on a web page using Selenium WebDriver. "
        "By default, clicks the 'Let's Draw!' button on Quick, Draw! (id='button-play'). "
        "You can specify a custom CSS selector if needed."
    )
    inputs = {
        "url": {
            "type": "string",
            "description": "The URL of the page to open."
        },
        "selector": {
            "type": "string",
            "description": "CSS selector for the button to click. Default: '#button-play'",
            "required": False,
            "nullable": True
        },
        "wait_time": {
            "type": "integer",
            "description": "Seconds to wait for the button to appear. Default: 10",
            "required": False,
            "nullable": True
        }
    }
    output_type = "string"

    def __init__(self):
        super().__init__()

    def forward(self, url: str, selector: Optional[str] = None, wait_time: Optional[int] = 10) -> str:
        selector = selector or "#button-play"
        wait_time = wait_time or 10
        driver = webdriver.Chrome()
        try:
            driver.get(url)
            WebDriverWait(driver, wait_time).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            ).click()
            time.sleep(1)
            return f"Clicked button with selector '{selector}' on {url} successfully."
        except Exception as e:
            return f"Error clicking button with selector '{selector}' on {url}: {e}"
        finally:
            driver.quit() 