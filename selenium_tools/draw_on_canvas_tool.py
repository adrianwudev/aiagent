from smolagents.tools import Tool
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium_tools.session_context import SeleniumSessionContext

class DrawOnCanvasTool(Tool):
    """
    Draw on the canvas (id='drawingCanvas') using mouse events. Supports line, circle, or sine wave.
    The driver instance is managed internally and shared across all tools using SeleniumSessionContext.
    This tool does NOT open or reload the URL; it only interacts with the current page/session.
    """
    name = "draw_on_canvas_tool"
    description = "Draw on the canvas (id='drawingCanvas') using mouse events. Supports line, circle, or sine wave."
    inputs = {
        "shape": {"type": "string", "description": "Shape to draw: 'line', 'circle', or 'sine'"},
        "wait_time": {"type": "integer", "description": "Wait seconds", "required": False, "nullable": True}
    }
    output_type = "string"

    def __init__(self):
        super().__init__()

    def forward(self, shape: str, wait_time: int = 10) -> str:
        driver = SeleniumSessionContext().get_driver()
        try:
            canvas = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.ID, "drawingCanvas"))
            )
            rect = driver.execute_script("return arguments[0].getBoundingClientRect();", canvas)
            actions = []
            if shape == 'line':
                actions = [
                    {'type': 'mousedown', 'x': rect['left']+10, 'y': rect['top']+10},
                    {'type': 'mousemove', 'x': rect['left']+rect['width']-10, 'y': rect['top']+rect['height']-10},
                    {'type': 'mouseup', 'x': rect['left']+rect['width']-10, 'y': rect['top']+rect['height']-10}
                ]
            elif shape == 'circle':
                import math
                cx = rect['left'] + rect['width']/2
                cy = rect['top'] + rect['height']/2
                r = min(rect['width'], rect['height'])/3
                steps = 36
                actions.append({'type': 'mousedown', 'x': cx+r, 'y': cy})
                for i in range(1, steps+1):
                    angle = 2*math.pi*i/steps
                    x = cx + r*math.cos(angle)
                    y = cy + r*math.sin(angle)
                    actions.append({'type': 'mousemove', 'x': x, 'y': y})
                actions.append({'type': 'mouseup', 'x': cx+r, 'y': cy})
            elif shape == 'sine':
                import math
                cx = rect['left'] + rect['width']*0.2
                cy = rect['top'] + rect['height']/2
                w = rect['width']*0.6
                h = rect['height']*0.2
                steps = 40
                actions.append({'type': 'mousedown', 'x': cx, 'y': cy})
                for i in range(1, steps+1):
                    progress = i/steps
                    x = cx + w*progress
                    y = cy + h*math.sin(4*math.pi*progress)
                    actions.append({'type': 'mousemove', 'x': x, 'y': y})
                actions.append({'type': 'mouseup', 'x': cx+w, 'y': cy})
            else:
                return f"Unknown shape: {shape}"
            js = """
            var canvas = document.getElementById('drawingCanvas');
            if (!canvas) return 'Canvas not found';
            var rect = canvas.getBoundingClientRect();
            function fire(type, x, y) {
                var evt = new MouseEvent(type, {clientX:x, clientY:y, bubbles:true});
                canvas.dispatchEvent(evt);
            }
            var actions = arguments[0];
            for (var i=0; i<actions.length; ++i) {
                fire(actions[i].type, actions[i].x, actions[i].y);
            }
            return 'Drawn '+actions.length+' events.';
            """
            driver.execute_script(js, actions)
            time.sleep(1)
            return f"Drawn {shape} on canvas."
        except Exception as e:
            return f"Error: {e}"
        finally:
            driver.quit() 