from dotenv import load_dotenv
import os
from smolagents.models import AzureOpenAIServerModel
from smolagents import CodeAgent, WebSearchTool, Tool
from tools import conversation_save_tool, selenium_script_tool, read_script_tool
from selenium_tools.element_tools import find_elements_tool, debug_elements_tool

load_dotenv("sample.env")

class PatchedAzureOpenAIServerModel(AzureOpenAIServerModel):
    def _prepare_completion_kwargs(self, *args, **kwargs):
        completion_kwargs = super()._prepare_completion_kwargs(*args, **kwargs)
        
        # Remove the 'stop' parameter if it exists
        if 'stop' in completion_kwargs:
            del completion_kwargs['stop']
        
        return completion_kwargs

if __name__ == "__main__":
    model = PatchedAzureOpenAIServerModel(
        model_id=os.environ.get("AZURE_OPENAI_MODEL_ID"),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        custom_role_conversions={"system": "assistant", "tool-call": "assistant", "tool-response": "user"}
    )

    agent = CodeAgent(
        tools=[
            WebSearchTool(),
            Tool.from_langchain(conversation_save_tool), # Make tool to write the testing result into txt file
            Tool.from_langchain(selenium_script_tool), # Save Selenium scripts
            Tool.from_langchain(read_script_tool), # Read previous Selenium scripts
            Tool.from_langchain(find_elements_tool), # Find Gemini page elements
            Tool.from_langchain(debug_elements_tool), # Debug page elements
        ],
        model=model,
        additional_authorized_imports=[
            "selenium",
            "selenium.webdriver.common.by",
            "selenium.webdriver.common.keys",
            "webdriver_manager.chrome",
            "selenium.webdriver.chrome.service",

            "selenium.webdriver.support.ui",
            "selenium.webdriver.support.expected_conditions",
            "selenium.common.exceptions",
            "selenium.webdriver.chrome.options",
            "time",
            "json"
        ]
    )
    query = (
        """
        Use Selenium WebDriver, launch a chrome webpage to open the page and simulate a QA test: 

        # IMPORTANT: Before starting, read previous Selenium scripts for reference
        # Use the read_selenium_scripts tool to get previous scripts and learn from them
        
        # Make your web browser in full screen mode.
        Please enter this link: https://gemini.google.com/app. Follow the steps below.
        
        0. Before starting the automation:
           0.1. Use the read_selenium_scripts tool to read previous Selenium scripts
           0.2. Analyze the previous scripts to understand successful patterns and avoid common mistakes
           0.3. Plan your approach based on what worked before
        
        1. After loading the page, wait for 3-5 seconds for the page to fully load.
        1.1. Use browser developer tools (F12) to inspect the DOM structure and find the input elements.
        1.2. The input box is typically located at the bottom of the page, look for elements with:
            - CSS selectors like: 'textarea[placeholder*="Message"]', 'div[contenteditable="true"]', 'input[type="text"]'
            - XPath like: '//textarea[contains(@placeholder, "Message")]', '//div[@contenteditable="true"]'
            - Class names containing: 'input', 'textarea', 'message', 'chat'
        1.3. If the input is not immediately visible, scroll to the bottom of the page.
        
        2. Try multiple strategies to locate the input box:
           2.1. First try: driver.find_element(By.CSS_SELECTOR, 'textarea[placeholder*="Message"]')
           2.2. If not found, try: driver.find_element(By.CSS_SELECTOR, 'div[contenteditable="true"]')
           2.3. If not found, try: driver.find_element(By.XPATH, '//textarea[contains(@placeholder, "Message")]')
           2.4. If not found, try: driver.find_element(By.XPATH, '//div[@contenteditable="true"]')
           2.5. If not found, try: driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
           2.6. If still not found, try these additional selectors:
                - 'textarea[aria-label*="Message"]'
                - 'div[role="textbox"]'
                - 'input[placeholder*="Ask"]'
                - 'textarea[placeholder*="Ask"]'
           2.7. If still not found, print all textarea and input elements on the page for debugging:
                textareas = driver.find_elements(By.TAG_NAME, 'textarea')
                inputs = driver.find_elements(By.TAG_NAME, 'input')
                print(f"Found {len(textareas)} textareas and {len(inputs)} inputs")
                for i, elem in enumerate(textareas + inputs):
                    print(f"Element {i}: {elem.get_attribute('outerHTML')[:200]}")
         
        3. Once you find the input element:
           3.1. Clear it first: element.clear()
           3.2. Type your question slowly with explicit waits between characters
           3.3. Verify the text was entered by getting the element's value
           3.4. Look for the submit button (usually appears after typing) with selectors like:
                - 'button[type="submit"]', 'button[aria-label*="Send"]', 'button[data-testid*="send"]'
                - 'button[aria-label*="Submit"]', 'button[title*="Send"]'
                - 'svg[aria-label*="Send"]', 'button:has(svg[aria-label*="Send"])'
         
        4. Click the submit button and wait for response:
           4.1. Wait for 5-10 seconds for Gemini's response to appear
           4.2. Look for response elements with selectors like:
                - 'div[data-testid*="response"]', 'div[class*="response"]', 'div[class*="message"]'
                - 'div[class*="conversation"]', 'div[class*="chat"]'
           4.3. Save your question and Gemini's response using the conversation_save_tool
           4.4. Wait for the input box to be ready for the next question
         
        5. Repeat step 4 until you have 20 conversations with Gemini.
        
        6. IMPORTANT: After completing all conversations:
           6.1. Use the save_selenium_script tool to save your complete Selenium script
           6.2. Include all the code you wrote, including imports, setup, and the main automation logic
           6.3. Make sure to save the script with proper comments and structure
        
        Important debugging tips:
        - If elements are not found, use driver.page_source to print the HTML and analyze the structure
        - Use WebDriverWait with explicit waits instead of time.sleep() when possible
        - If the page uses dynamic loading, wait for elements to be present and clickable
        - Check if there are any overlays, modals, or popups that need to be dismissed first
        - If you see a "Sign in" button, you may need to handle authentication first
        - Try using JavaScript executor to scroll and focus on elements if normal methods fail
        
        Final. Please give me a summary of what happened and save your Selenium script.
        """
    )


    output = agent.run(query)

    memory.save_context({"input": query}, {"output": output})