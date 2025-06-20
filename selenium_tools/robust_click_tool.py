from smolagents.tools import Tool
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium_tools.session_context import SeleniumSessionContext

class RobustClickTool(Tool):
    """
    Click a button by text or selector, auto-handle overlays, and use JS fallback if needed.
    The driver instance is managed internally and shared across all tools using SeleniumSessionContext.
    This tool does NOT open or reload the URL; it only interacts with the current page/session.
    """
    name = "robust_click_tool"
    description = "Robustly click a button by text or selector, auto-handle overlays, and use JS fallback if needed."
    inputs = {
        "button_text": {"type": "string", "description": "Button text to match", "required": False, "nullable": True},
        "selector": {"type": "string", "description": "CSS selector", "required": False, "nullable": True},
        "wait_time": {"type": "integer", "description": "Wait seconds", "required": False, "nullable": True}
    }
    output_type = "string"

    def __init__(self):
        super().__init__()

    def forward(self, button_text: str = None, selector: str = None, wait_time: int = 10) -> str:
        driver = SeleniumSessionContext().get_driver()
        try:
            button = None
            if selector:
                button = WebDriverWait(driver, wait_time).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
            elif button_text:
                buttons = driver.find_elements(By.TAG_NAME, "button")
                for b in buttons:
                    if button_text.lower() in b.text.lower():
                        button = b
                        break
                if not button:
                    return f"Button with text '{button_text}' not found."
            else:
                return "No selector or button_text provided."
            driver.execute_script("""
                var overlays = document.querySelectorAll('div.card-container.fill, #newround-card');
                overlays.forEach(el => {el.style.pointerEvents = 'none'; el.style.opacity = '0';});
            """)
            try:
                actions = ActionChains(driver)
                actions.move_to_element(button).pause(0.2).click_and_hold(button).pause(0.1).release(button).perform()
            except Exception:
                driver.execute_script("arguments[0].click();", button)
            return "Button clicked successfully."
        except Exception as e:
            return f"Error: {e}" 