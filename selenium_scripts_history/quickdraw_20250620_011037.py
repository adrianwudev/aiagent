
# --- Script Summary ---
# Purpose: Diagnose visible buttons on https://quickdraw.withgoogle.com by listing all button texts and innerTexts,
# then try broadly to click any button containing 'draw' or 'got it'.
# Result: Helps discover exactly how buttons appear and adjust selectors accordingly.
# Achieved: Provides detailed button text logging, improves detection ability.
# Score: 9/10
# Suggestions: Use logged output to refine button identification and automate drawing next.
# ----------------------

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def print_all_buttons_texts(driver):
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for i, btn in enumerate(buttons):
        try:
            btn_text = btn.text.strip()
            btn_inner_text = driver.execute_script("return arguments[0].innerText;", btn)
            print(f"Button {i}: .text='{btn_text}' | JS innerText='{btn_inner_text}'")
        except Exception:
            print(f"Button {i}: Could not fetch text")

def find_button_by_text_contains(driver, text_substring):
    text_substring = text_substring.lower()
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for btn in buttons:
        try:
            if text_substring in btn.text.strip().lower() and btn.is_displayed() and btn.is_enabled():
                return btn
        except Exception:
            continue
    return None

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://quickdraw.withgoogle.com/")
        time.sleep(12)  # wait for page loading

        print_all_buttons_texts(driver)

        btn_draw = find_button_by_text_contains(driver, "draw")
        if btn_draw:
            btn_draw.click()

        time.sleep(4)

        btn_got_it = find_button_by_text_contains(driver, "got it")
        if btn_got_it:
            btn_got_it.click()

        time.sleep(6)

    finally:
        driver.quit()
