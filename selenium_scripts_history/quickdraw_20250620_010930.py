
# --- Script Summary ---
# Purpose: Navigate to quickdraw.withgoogle.com, click "Let's Draw!" and dismiss overlays with "Got It!" without using disallowed imports
# Result: Navigated and clicked buttons using simple find_elements + time.sleep waits
# Achieved: Yes, avoided forbidden imports and still succeeded
# Score: 9/10
# Suggestions: Improve detection of alternative overlays / buttons and prepare drawing automation
# ----------------------

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get("https://quickdraw.withgoogle.com/")
    time.sleep(5)
    time.sleep(2)
    # dom = driver.page_source

    lets_draw_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), \"Let's Draw\")]")
    if lets_draw_buttons:
        lets_draw_buttons[0].click()

    time.sleep(2)

    got_it_buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'Got It')]")
    if got_it_buttons:
        got_it_buttons[0].click()

    time.sleep(2)

finally:
    driver.quit()
