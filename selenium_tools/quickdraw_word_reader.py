from typing import Optional
from smolagents.tools import Tool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class QuickDrawWordReaderTool(Tool):
    """
    A SmolAgents Tool that reads the current drawing word from Quick, Draw! game.
    It extracts and concatenates all <span> elements inside <div id="challengetext-word">.
    """
    name = "quickdraw_word_reader"
    description = (
        "Read the current drawing word from Quick, Draw! by extracting all <span> elements inside <div id='challengetext-word'>."
    )
    inputs = {
        "url": {
            "type": "string",
            "description": "The URL of the Quick, Draw! game page."
        },
        "wait_time": {
            "type": "integer",
            "description": "Seconds to wait for the word element to appear. Default: 10",
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
            word_div = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.ID, "challengetext-word"))
            )
            spans = word_div.find_elements(By.TAG_NAME, "span")
            word = ''.join([span.text for span in spans])
            return f"Current drawing word: {word}"
        except Exception as e:
            return f"Error reading drawing word: {e}"
        finally:
            driver.quit() 