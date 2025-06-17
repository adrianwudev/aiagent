from langchain.tools import Tool

def find_gemini_elements(driver_source: str = "", element_type: str = "input"):
    """
    專門用於尋找 Gemini 頁面元素的工具
    element_type: "input", "submit", "response", "all"
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException, NoSuchElementException
        import time
        
        strategies = {
            "input": [
                "textarea[placeholder*='Message']",
                "textarea[placeholder*='Ask']", 
                "div[contenteditable='true']",
                "input[type='text']",
                "textarea[aria-label*='Message']",
                "div[role='textbox']",
                "input[placeholder*='Ask']",
                "textarea[placeholder*='Type']",
                "//textarea[contains(@placeholder, 'Message')]",
                "//div[@contenteditable='true']",
                "//textarea[contains(@placeholder, 'Ask')]",
                "//input[@type='text']",
                "//div[@role='textbox']"
            ],
            "submit": [
                "button[type='submit']",
                "button[aria-label*='Send']",
                "button[data-testid*='send']",
                "button[aria-label*='Submit']",
                "button[title*='Send']",
                "svg[aria-label*='Send']",
                "button:has(svg[aria-label*='Send'])",
                "//button[contains(@aria-label, 'Send')]",
                "//button[@type='submit']",
                "//svg[contains(@aria-label, 'Send')]",
                "//button[.//svg[contains(@aria-label, 'Send')]]"
            ],
            "response": [
                "div[data-testid*='response']",
                "div[class*='response']",
                "div[class*='message']",
                "div[class*='conversation']",
                "div[class*='chat']",
                "div[class*='output']",
                "//div[contains(@class, 'response')]",
                "//div[contains(@class, 'message')]",
                "//div[contains(@class, 'conversation')]"
            ]
        }
        
        if element_type == "all":
            all_strategies = {}
            for key, value in strategies.items():
                all_strategies[key] = value
            return f"All element finding strategies:\n{all_strategies}"
        elif element_type in strategies:
            return f"Strategies for finding {element_type} elements:\n{strategies[element_type]}"
        else:
            return f"Available element types: {list(strategies.keys())}"
            
    except ImportError:
        return "Selenium not available. Please install selenium package."
    except Exception as e:
        return f"Error in find_gemini_elements: {str(e)}"

def debug_page_elements(page_url: str = "https://gemini.google.com/app"):
    """
    調試頁面元素，返回頁面上所有可能的輸入和按鈕元素
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        import time
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
            driver.get(page_url)
            time.sleep(5)
            input_elements = []
            button_elements = []
            textareas = driver.find_elements(By.TAG_NAME, "textarea")
            for i, elem in enumerate(textareas):
                try:
                    input_elements.append({
                        "type": "textarea",
                        "index": i,
                        "placeholder": elem.get_attribute("placeholder"),
                        "aria-label": elem.get_attribute("aria-label"),
                        "class": elem.get_attribute("class"),
                        "id": elem.get_attribute("id"),
                        "contenteditable": elem.get_attribute("contenteditable")
                    })
                except:
                    pass
            inputs = driver.find_elements(By.TAG_NAME, "input")
            for i, elem in enumerate(inputs):
                try:
                    input_elements.append({
                        "type": "input",
                        "index": i,
                        "type_attr": elem.get_attribute("type"),
                        "placeholder": elem.get_attribute("placeholder"),
                        "aria-label": elem.get_attribute("aria-label"),
                        "class": elem.get_attribute("class"),
                        "id": elem.get_attribute("id")
                    })
                except:
                    pass
            contenteditable_divs = driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")
            for i, elem in enumerate(contenteditable_divs):
                try:
                    input_elements.append({
                        "type": "contenteditable_div",
                        "index": i,
                        "aria-label": elem.get_attribute("aria-label"),
                        "class": elem.get_attribute("class"),
                        "id": elem.get_attribute("id"),
                        "role": elem.get_attribute("role")
                    })
                except:
                    pass
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for i, elem in enumerate(buttons):
                try:
                    button_elements.append({
                        "type": "button",
                        "index": i,
                        "aria-label": elem.get_attribute("aria-label"),
                        "title": elem.get_attribute("title"),
                        "class": elem.get_attribute("class"),
                        "id": elem.get_attribute("id"),
                        "type_attr": elem.get_attribute("type")
                    })
                except:
                    pass
            svg_buttons = driver.find_elements(By.TAG_NAME, "svg")
            for i, elem in enumerate(svg_buttons):
                try:
                    aria_label = elem.get_attribute("aria-label")
                    if aria_label and ("send" in aria_label.lower() or "submit" in aria_label.lower()):
                        button_elements.append({
                            "type": "svg",
                            "index": i,
                            "aria-label": aria_label,
                            "class": elem.get_attribute("class"),
                            "id": elem.get_attribute("id")
                        })
                except:
                    pass
            result = f"""
Page Analysis for {page_url}:
================================

INPUT ELEMENTS ({len(input_elements)} found):
{input_elements}

BUTTON ELEMENTS ({len(button_elements)} found):
{button_elements}

RECOMMENDED SELECTORS:
"""
            for elem in input_elements:
                if elem.get("placeholder") and "message" in elem.get("placeholder", "").lower():
                    result += f"- Input: textarea[placeholder*='{elem['placeholder']}']\n"
                elif elem.get("aria-label") and "message" in elem.get("aria-label", "").lower():
                    result += f"- Input: textarea[aria-label*='{elem['aria-label']}']\n"
            for elem in button_elements:
                if elem.get("aria-label") and "send" in elem.get("aria-label", "").lower():
                    result += f"- Button: button[aria-label*='{elem['aria-label']}']\n"
            return result
        finally:
            driver.quit()
    except Exception as e:
        return f"Error in debug_page_elements: {str(e)}"

find_elements_tool = Tool(
    name="find_gemini_elements",
    func=find_gemini_elements,
    description="Provides strategies for finding input, submit, and response elements on Gemini page.",
)

debug_elements_tool = Tool(
    name="debug_page_elements",
    func=debug_page_elements,
    description="Analyzes the Gemini page and returns all input and button elements with recommended selectors.",
) 