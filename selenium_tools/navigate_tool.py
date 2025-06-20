from smolagents.tools import Tool
from selenium_tools.session_context import SeleniumSessionContext

class NavigateTool(Tool):
    """
    Navigate the shared Selenium WebDriver to the specified URL.
    The driver instance is managed internally and shared across all tools using SeleniumSessionContext.
    """
    name = "navigate_tool"
    description = "Navigate the shared Selenium WebDriver to the specified URL."
    inputs = {
        "url": {"type": "string", "description": "The URL to navigate to."}
    }
    output_type = "string"

    def __init__(self):
        super().__init__()

    def forward(self, url: str) -> str:
        driver = SeleniumSessionContext().get_driver()
        try:
            driver.get(url)
            return f"Navigated to {url} successfully."
        except Exception as e:
            return f"Error navigating to {url}: {e}" 