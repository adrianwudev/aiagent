from typing import Optional
from smolagents.tools import Tool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium_tools.session_context import SeleniumSessionContext

class QuickDrawWordReaderTool(Tool):
    """
    Read the current drawing word from Quick, Draw! by extracting all <span> elements inside <div id="challengetext-word">.
    The driver instance is managed internally and shared across all tools using SeleniumSessionContext.
    This tool does NOT open or reload the URL; it only interacts with the current page/session.
    """
    name = "quickdraw_word_reader"
    description = (
        "Read the current drawing word from Quick, Draw! by extracting all <span> elements inside <div id='challengetext-word'>."
    )
    inputs = {
        "wait_time": {"type": "integer", "description": "Seconds to wait for the word element to appear. Default: 10", "required": False, "nullable": True}
    }
    output_type = "string"

    def __init__(self):
        super().__init__()

    def forward(self, wait_time: int = 10) -> str:
        driver = SeleniumSessionContext().get_driver()
        wait_time = wait_time or 10
        try:
            word_div = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.ID, "challengetext-word"))
            )
            spans = word_div.find_elements(By.TAG_NAME, "span")
            word = ''.join([span.text for span in spans])
            return f"Current drawing word: {word}"
        except Exception as e:
            return f"Error reading drawing word: {e}" 