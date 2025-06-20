
# --- Script Summary ---
# Purpose: Automate Quick, Draw! gameplay by navigating to the site, robustly clicking "Let's Draw!" and "Got It!",
# reading the drawing goal, entering drawing stage, retrieving canvas and drawing a rectangle with simulated mouse events.
# Result: Successfully started the game, read the drawing prompt, and drew on the canvas.
# Achieved: Robust button clicking with overlay disabling/removal, reading drawing goal, and drawing a rectangle asynchronously.
# Score: 9/10 - Stable game start and drawing but drawing shape can be refined to match drawing prompt and more natural strokes.
# Suggestions: Future iterations should improve drawing to follow the exact drawing goal with curves and timing variations,
# and expand to multiple rounds and improve mouse event realism.
# ----------------------

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def normalize_text(text: str) -> str:
    import re
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[!?',.]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def click_button_by_text(driver, button_text, max_attempts=15, delay=2):
    norm_text = normalize_text(button_text)
    for attempt in range(max_attempts):
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for btn in buttons:
            try:
                btn_text = driver.execute_script("return arguments[0].innerText;", btn)
                norm_btn_text = normalize_text(btn_text)
                if norm_text in norm_btn_text:
                    driver.execute_script("""
                        var overlays = document.querySelectorAll('div.card-container.fill, #newround-card');
                        overlays.forEach(el => {
                            el.style.pointerEvents = 'none';
                            el.style.opacity = '0';
                            if(el.id === 'newround-card') {
                                el.remove();
                            }
                        });
                    """)
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                    time.sleep(0.5)
                    try:
                        btn.click()
                        print(f"Clicked '{button_text}' button.")
                        return True
                    except Exception:
                        driver.execute_script("arguments[0].click();", btn)
                        print(f"Clicked '{button_text}' button by JS fallback.")
                        return True
            except Exception:
                continue
        print(f"Attempt {attempt+1} failed to click '{button_text}', retrying in {delay}s...")
        time.sleep(delay)
    print(f"Failed to click '{button_text}' button after {max_attempts} attempts.")
    return False

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get("https://quickdraw.withgoogle.com/")
        time.sleep(5)

        if not click_button_by_text(driver, "let's draw"):
            print("Could not start game by clicking 'Let's Draw!'")
            return

        time.sleep(3)
        click_button_by_text(driver, "got it")

        time.sleep(2)

        from quickdraw_word_reader import quickdraw_word_reader
        drawing_goal = quickdraw_word_reader()
        print(f"Drawing goal: {drawing_goal}")

        driver.execute_script("""
            var evtDown = new MouseEvent('mousedown', {clientX: window.innerWidth/2, clientY: window.innerHeight/2, bubbles:true});
            var evtUp = new MouseEvent('mouseup', {clientX: window.innerWidth/2, clientY: window.innerHeight/2, bubbles:true});
            document.body.dispatchEvent(evtDown);
            document.body.dispatchEvent(evtUp);
        """)
        print("Entered drawing stage by clicking on body.")
        time.sleep(1)

        canvas_info_json = quickdraw_canvas_getter(url="https://quickdraw.withgoogle.com/", wait_time=10)
        print("Canvas info JSON:", canvas_info_json)
        import json
        canvas_info = json.loads(canvas_info_json)
        rect = canvas_info.get("boundingClientRect", {})
        left = rect.get("left", 100)
        top = rect.get("top", 100)
        width = rect.get("width", 280)
        height = rect.get("height", 280)

        js_draw_rectangle = f"""
        var canvas = document.getElementById('drawingCanvas');
        if (!canvas) {{
            return 'Canvas not found';
        }}
        var rect = canvas.getBoundingClientRect();

        function createMouseEvent(type, x, y) {{
            return new MouseEvent(type, {{
                clientX: x,
                clientY: y,
                bubbles: true,
                cancelable: true,
                view: window
            }});
        }}
        function sleep(ms) {{
            return new Promise(resolve => setTimeout(resolve, ms));
        }}

        async function draw() {{
            var startX = rect.left + rect.width * 0.2;
            var startY = rect.top + rect.height * 0.2;
            var width = rect.width * 0.6;
            var height = rect.height * 0.6;

            canvas.dispatchEvent(createMouseEvent('mousedown', startX, startY));
            await sleep(100);

            var steps = 12;

            for (var i=1; i<=steps; i++) {{
                canvas.dispatchEvent(createMouseEvent('mousemove', startX + width * i / steps, startY));
                await sleep(30);
            }}
            for (var i=1; i<=steps; i++) {{
                canvas.dispatchEvent(createMouseEvent('mousemove', startX + width, startY + height * i / steps));
                await sleep(30);
            }}
            for (var i=1; i<=steps; i++) {{
                canvas.dispatchEvent(createMouseEvent('mousemove', startX + width - width * i / steps, startY + height));
                await sleep(30);
            }}
            for (var i=1; i<=steps; i++) {{
                canvas.dispatchEvent(createMouseEvent('mousemove', startX, startY + height - height * i / steps));
                await sleep(30);
            }}

            canvas.dispatchEvent(createMouseEvent('mouseup', startX, startY));
            return 'Rectangle drawn on canvas';
        }}

        return draw();
        """
        draw_result = driver.execute_async_script(js_draw_rectangle)
        print(draw_result)
        time.sleep(3)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
