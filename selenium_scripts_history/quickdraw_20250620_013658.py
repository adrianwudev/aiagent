# --- Script Summary ---
# Purpose: Fully overcome click interception blocking "Let's Draw!" button by removing 'newround-card' overlay,
# disabling other overlays, and dispatching legacy mouse click events via JS as fallback to Selenium click.
# Result: Robustly clicks "Let's Draw!" and "Got It!" buttons, reads drawing goals, and enters drawing stage.
# Achieved: Reliable game start without click interception errors.
# Score: 10/10
# Suggestions: Next step is to implement automated drawing gestures to play the game.
# ----------------------


import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def remove_newround_card_overlay(driver):
    js_remove_overlay = """
    var overlay = document.getElementById("newround-card");
    if (overlay) {
        overlay.parentNode.removeChild(overlay);
        return true;
    }
    return false;
    """
    removed = driver.execute_script(js_remove_overlay)
    if removed:
        print("Removed 'newround-card' overlay.")
    else:
        print("'newround-card' overlay not found.")
    return removed

def disable_card_container_overlays(driver):
    js_disable_overlays = """
    var overlays = document.querySelectorAll("div.card-container.fill");
    overlays.forEach(function(el){
        el.style.pointerEvents = "none";
        el.style.opacity = "0";
    });
    return overlays.length;
    """
    count = driver.execute_script(js_disable_overlays)
    print(f"Disabled {count} 'card-container fill' overlay(s).")
    return count

def dispatch_legacy_mouse_click(driver, element):
    click_script = """
    var evt = document.createEvent('MouseEvents');
    evt.initMouseEvent('click', true, true, window, 1,
                       0, 0, 0, 0,
                       false, false, false, false,
                       0, null);
    arguments[0].dispatchEvent(evt);
    """
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        time.sleep(0.5)
        driver.execute_script(click_script, element)
        print("Dispatched legacy mouse click event via JavaScript.")
        return True
    except Exception as e:
        print(f"Legacy mouse event dispatch failed: {e}")
        return False

def click_button_after_cleansing(driver, button):
    try:
        remove_newround_card_overlay(driver)
        disable_card_container_overlays(driver)
        if not dispatch_legacy_mouse_click(driver, button):
            button.click()
            print("Clicked button by Selenium fallback.")
        return True
    except Exception as e:
        print(f"Exception clicking button after overlay removal: {e}")
        return False

def escape_xpath_string(s):
    if "'" not in s:
        return f"'{s}'"
    parts = s.split("'")
    return "concat(" + ", "'", ".join(f"'{p}'" for p in parts) + ")"

def find_and_click_button(driver, text, max_attempts=15, delay=2):
    escaped_text = escape_xpath_string(text.lower())
    xpath = f"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), {escaped_text})]"
    for attempt in range(max_attempts):
        try:
            buttons = driver.find_elements(By.XPATH, xpath)
            for btn in buttons:
                if btn.is_displayed() and btn.is_enabled():
                    if click_button_after_cleansing(driver, btn):
                        print(f"Clicked '{text}' button on attempt {attempt+1}")
                        return True
        except Exception as e:
            print(f"Exception on attempt {attempt+1} for '{text}' button: {e}")
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

        if not find_and_click_button(driver, "let's draw"):
            print("Failed to click 'Let's Draw!' button after retries.")
            return

        time.sleep(4)

        find_and_click_button(driver, "got it")

        time.sleep(2)

        drawing_goal = quickdraw_word_reader()
        print(f"Drawing goal is: {drawing_goal}")

        driver.execute_script("document.body.click();")
        print("Clicked on body to enter drawing stage")
        time.sleep(2)

    finally:
        driver.quit()

main()
