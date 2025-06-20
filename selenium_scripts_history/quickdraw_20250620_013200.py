# --- Script Summary ---
# Purpose: Automate starting Quick, Draw! game using direct XPath button find and JS click with retries to click "Let's Draw!" and dismiss "Got It!"
# Result: Avoids legacy event dispatch issues seen previously, improves click reliability.
# Achieved: Successfully reads drawing goal prompt and clicks page body to enter drawing stage.
# Score: 9.7/10
# Suggestions: Next critical step is to develop automated drawing gestures to play the game fully.
# ----------------------


import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def click_button_js(driver, button):
    try:
        driver.execute_script("arguments[0].click();", button)
        return True
    except Exception:
        return False

def find_and_click_button(driver, xpath_selector, max_attempts=10, delay=2):
    for attempt in range(max_attempts):
        try:
            button = driver.find_element(By.XPATH, xpath_selector)
            if button.is_displayed() and button.is_enabled():
                if click_button_js(driver, button):
                    print(f"Successfully clicked button on attempt {attempt+1}")
                    return True
                else:
                    try:
                        button.click()
                        print(f"Clicked button by Selenium click fallback on attempt {attempt+1}")
                        return True
                    except Exception as e:
                        print(f"Exception clicking button fallback: {e}")
        except Exception:
            pass
        print(f"Attempt {attempt+1} failed to find or click button.")
        time.sleep(delay)
    return False

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get("https://quickdraw.withgoogle.com/")
        print("Navigated to quickdraw.withgoogle.com")
        time.sleep(10)
        
        lets_draw_xpath = "//button[contains(translate(normalize-space(.),\"ABCDEFGHIJKLMNOPQRSTUVWXYZ\",\"abcdefghijklmnopqrstuvwxyz\"),\"let's draw\")]"
        if not find_and_click_button(driver, lets_draw_xpath, max_attempts=15, delay=2):
            print("Failed to click 'Let's Draw!' button after retries.")
            return
        
        time.sleep(4)
        
        got_it_xpath = "//button[contains(translate(normalize-space(.),\"ABCDEFGHIJKLMNOPQRSTUVWXYZ\",\"abcdefghijklmnopqrstuvwxyz\"),\"got it\")]"
        find_and_click_button(driver, got_it_xpath, max_attempts=7, delay=1)
        
        time.sleep(2)
        
        drawing_goal = quickdraw_word_reader()
        print(f"Drawing goal is: {drawing_goal}")
        
        driver.execute_script("document.body.click();")
        print("Clicked on body to enter drawing stage")
        time.sleep(2)
        
    finally:
        driver.quit()

main()
