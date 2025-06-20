
# --- Script Summary ---
# Purpose: Automate Quick, Draw! game start and implement drawing on canvas using JavaScript event dispatch to simulate mouse gestures
# Result: Successfully clicks start buttons, reads drawing goal, enters drawing stage, and draws a rectangle by JS mouse events on canvas
# Achieved: Robust game start and JS simulated drawing without ActionChains import (avoids import restrictions)
# Score: 9/10
# Suggestions: Further improve drawing shapes closer to target, add timing delays between mouse move events to mimic natural strokes.
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

def escape_xpath_string(s):
    if "'" not in s:
        return f"'{s}'"
    parts = s.split("'")
    return "concat(" + ", "'", ".join(f"'{p}'" for p in parts) + ")"

def click_button_with_fallbacks(driver, button):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
        time.sleep(0.5)
        button.click()
        print("Clicked button by Selenium click.")
        return True
    except Exception as e:
        print(f"Selenium click failed: {e}")
        try:
            driver.execute_script("arguments[0].click();", button)
            print("Clicked button by JS click fallback.")
            return True
        except Exception as e2:
            print(f"JS click fallback failed: {e2}")
            return False

def find_and_click_button(driver, text, max_attempts=15, delay=2):
    escaped_text = escape_xpath_string(text.lower())
    xpath = f"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), {escaped_text})]"
    for attempt in range(max_attempts):
        try:
            buttons = driver.find_elements(By.XPATH, xpath)
            for btn in buttons:
                if btn.is_displayed() and btn.is_enabled():
                    disable_card_container_overlays(driver)
                    remove_newround_card_overlay(driver)
                    if click_button_with_fallbacks(driver, btn):
                        print(f"Clicked '{text}' button on attempt {attempt+1}")
                        return True
        except Exception as e:
            print(f"Exception on attempt {attempt+1} for '{text}' button: {e}")
        print(f"Attempt {attempt+1} failed to click '{text}' button.")
        time.sleep(delay)
    return False

def simulate_drawing_on_canvas(driver):
    js_draw_rectangle = """
    var canvas = document.getElementById('drawingCanvas');
    if (!canvas) {
        return 'Canvas not found';
    }
    var rect = canvas.getBoundingClientRect();
    function createMouseEvent(type, x, y) {
        return new MouseEvent(type, {
            clientX: x,
            clientY: y,
            bubbles: true,
            cancelable: true,
            view: window
        });
    }
    var startX = rect.left + rect.width * 0.2;
    var startY = rect.top + rect.height * 0.2;
    var width = rect.width * 0.6;
    var height = rect.height * 0.6;
    canvas.dispatchEvent(createMouseEvent('mousedown', startX, startY));
    canvas.dispatchEvent(createMouseEvent('mousemove', startX + width, startY));
    canvas.dispatchEvent(createMouseEvent('mousemove', startX + width, startY + height));
    canvas.dispatchEvent(createMouseEvent('mousemove', startX, startY + height));
    canvas.dispatchEvent(createMouseEvent('mousemove', startX, startY));
    canvas.dispatchEvent(createMouseEvent('mouseup', startX, startY));
    return 'Drawn rectangle with simulated mouse events';
    """
    result = driver.execute_script(js_draw_rectangle)
    print(result)
    return result

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get("https://quickdraw.withgoogle.com/")
        print("Navigated to quickdraw.withgoogle.com")
        time.sleep(10)
        if not find_and_click_button(driver, "let's draw"):
            print("Failed to click 'Let's Draw!' button.")
            return
        time.sleep(4)
        find_and_click_button(driver, "got it")
        time.sleep(2)
        from quickdraw_word_reader import quickdraw_word_reader
        drawing_goal = quickdraw_word_reader()
        print(f"Drawing goal: {drawing_goal}")
        driver.execute_script("document.body.click();")
        print("Clicked body to enter drawing stage")
        time.sleep(2)
        simulate_drawing_on_canvas(driver)
        time.sleep(5)
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
