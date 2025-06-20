from smolagents.tools import tool
from selenium_tools.session_context import SeleniumSessionContext
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@tool
def quickdraw_word_reader(wait_time: int = 10) -> str:
    """
    Read the current drawing word from Quick, Draw! by extracting all <span> elements inside <div id="challengetext-word">.
    Only interacts with the current page/session, does not open or reload the URL.

    Args:
        wait_time (int): Seconds to wait for the word element to appear. Default: 10.
    Returns:
        str: The drawing word or error message.
    """
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