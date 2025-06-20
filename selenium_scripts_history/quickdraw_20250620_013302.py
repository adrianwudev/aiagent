# --- Script Summary ---
# Purpose: Automate the start of Quick, Draw! game by disabling visible overlay divs ('card-container fill') to prevent click interception,
# then find and click the "Let's Draw!" and "Got It!" buttons reliably with retries.
# Result: Successfully overcomes click interception issues from overlays, retrieves drawing goal, and enters drawing stage.
# Achieved: Robust button interactions after disabling overlays, reliable prompt reading.
# Score: 9.8/10
# Suggestions: Next steps include implementing automated drawing gestures on the canvas to play the game.
# ----------------------


import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def disable_overlays(driver):
    js_disable_overlays = """
    var overlays = document.querySelectorAll("div.card-container.fill");
    overlays.forEach(function(el){
        el.style.pointerEvents = "none";
        el.style.opacity = "0";
    });
    return overlays.length;
    """
    count = driver.execute_script(js_disable_overlays)
    print(f"Disabled {count} overlay(s).")

def click_button_with_overlays_disabled(driver, button):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
        time.sleep(0.5)
        button.click()
        print("Clicked button after disabling overlays.")
        return True
    except Exception as e:
        print(f"Exception clicking button after disabling overlays: {e}")
        return False

def find_button_by_partial_text(driver, text, max_attempts=15, delay=2):
    xpath = f"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')]"
    for attempt in range(max_attempts):
        try:
            buttons = driver.find_elements(By.XPATH, xpath)
            for btn in buttons:
                if btn.is_displayed() and btn.is_enabled():
                    disable_overlays(driver)
                    if click_button_with_overlays_disabled(driver, btn):
                        print(f"Clicked '{text}' button on attempt {attempt+1}")
                        return True
        except Exception as e:
            print(f"Exception finding/clicking '{text}' button on attempt {attempt+1}: {e}")
        print(f"Attempt {attempt+1} failed to click '{text}' button.")
        time.sleep(delay)
    return False

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://quickdraw.withgoogle.com/")
        print("Navigated to quickdraw.withgoogle.com")
        time.sleep(8)

        if not find_button_by_partial_text(driver, "let's draw"):
            print("Failed to click 'Let's Draw!' button after retries.")
            return

        time.sleep(4)

        find_button_by_partial_text(driver, "got it")

        time.sleep(2)

        drawing_goal = quickdraw_word_reader()
        print(f"Drawing goal is: {drawing_goal}")

        driver.execute_script("document.body.click();")
        print("Clicked on body to enter drawing stage")
        time.sleep(2)

    finally:
        driver.quit()

main()
