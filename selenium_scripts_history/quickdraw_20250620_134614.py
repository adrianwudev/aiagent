
# --- Script Summary ---
# Purpose: Automate Quick, Draw! game start, overlay dismissal, reading drawing goal,
# entering drawing stage, and drawing a rectangle on the canvas simulating mouse events asynchronously.
# Result: Successfully interacts with UI elements and draws a basic shape with pauses for smoother strokes.
# Achieved: Robust game start and overlay handling, basic drawing automation.
# Score: 8.5/10
# Suggestions: Improve by adding drawing gestures tailored to the actual drawing goal,
# adding variable stroke timings, curves and multi-round automation.
# ----------------------

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
    print(f"Disabled {count} 'card-container fill' overlays.")
    return count

def click_button_safe(driver, button_text):
    escaped_text = button_text.lower()
    for attempt in range(15):
        buttons = driver.find_elements(By.XPATH, f"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), \"{escaped_text}\")]")
        for btn in buttons:
            if btn.is_displayed() and btn.is_enabled():
                try:
                    remove_newround_card_overlay(driver)
                    disable_card_container_overlays(driver)
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                    time.sleep(0.5)
                    btn.click()
                    print(f"Clicked '{button_text}' button.")
                    return True
                except Exception as e:
                    try:
                        driver.execute_script("arguments[0].click();", btn)
                        print(f"Clicked '{button_text}' button by JS fallback.")
                        return True
                    except Exception:
                        continue
        print(f"Attempt {{attempt+1}} failed to click '{button_text}' button, retrying in 2 seconds...")
        time.sleep(2)
    print(f"Failed to click '{button_text}' button after retries.")
    return False

def simulate_drawing(driver):
    import json
    canvas_info = quickdraw_canvas_getter(url="https://quickdraw.withgoogle.com/", wait_time=10)
    print("Canvas info:", canvas_info)
    try:
        canvas_data = json.loads(canvas_info)
        rect = canvas_data.get('boundingClientRect', {})
        left = rect.get('left', 100)
        top = rect.get('top', 100)
        width = rect.get('width', 280)
        height = rect.get('height', 280)
    except Exception as e:
        print(f"Failed to parse canvas info: {e}")
        left, top, width, height = 100, 100, 280, 280

    js_draw_script = """
    var canvas = document.getElementById('drawingCanvas');
    if (!canvas) {
        return 'Canvas not found';
    }
    var rect = canvas.getBoundingClientRect();

    function createMouseEvent(type, x, y){
        return new MouseEvent(type, {
            clientX: x,
            clientY: y,
            bubbles: true,
            cancelable: true,
            view: window
        });
    }
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function draw(){
        var startX = rect.left + rect.width * 0.2;
        var startY = rect.top + rect.height * 0.2;
        var width = rect.width * 0.6;
        var height = rect.height * 0.6;

        canvas.dispatchEvent(createMouseEvent('mousedown', startX, startY));
        await sleep(100);

        var steps = 10;

        for(var i=1; i<=steps; i++){
            canvas.dispatchEvent(createMouseEvent('mousemove', startX + width * i / steps, startY));
            await sleep(50);
        }
        for(var i=1; i<=steps; i++){
            canvas.dispatchEvent(createMouseEvent('mousemove', startX + width, startY + height * i / steps));
            await sleep(50);
        }
        for(var i=1; i<=steps; i++){
            canvas.dispatchEvent(createMouseEvent('mousemove', startX + width - width * i / steps, startY + height));
            await sleep(50);
        }
        for(var i=1; i<=steps; i++){
            canvas.dispatchEvent(createMouseEvent('mousemove', startX, startY + height - height * i / steps));
            await sleep(50);
        }

        canvas.dispatchEvent(createMouseEvent('mouseup', startX, startY));
        return 'Rectangle drawn';
    }
    return draw();
    """
    try:
        result = driver.execute_async_script(js_draw_script)
        print(result)
        return result
    except Exception as e:
        print(f"Drawing script execution failed: {e}")
        return None

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://quickdraw.withgoogle.com/")
        print("Navigated to quickdraw.withgoogle.com")
        time.sleep(5)

        if not click_button_safe(driver, "let's draw"):
            print("Failed to start the game.")
            return

        time.sleep(4)
        click_button_safe(driver, "got it")

        from quickdraw_word_reader import quickdraw_word_reader
        drawing_goal = quickdraw_word_reader()
        print(f"Drawing goal: {drawing_goal}")

        driver.execute_script("document.body.click();")
        print("Clicked body to enter drawing stage")
        time.sleep(2)

        simulate_drawing(driver)
        time.sleep(5)
    finally:
        driver.quit()

main()
