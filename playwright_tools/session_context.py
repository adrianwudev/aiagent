from playwright.sync_api import sync_playwright
import json
import os

class PlaywrightSessionContext:
    _instance = None
    _state_file = "playwright_session_state.json"
    _initial_url="https://quickdraw.withgoogle.com/"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._playwright = None
            cls._instance._browser = None
            cls._instance._context = None
            cls._instance._page = None
            cls._instance._state = None
        return cls._instance

    def init_session(self):
        if self._page is None:
            self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.launch(headless=False)
            self._context = self._browser.new_context()
            self._page = self._context.new_page()
            # Automatically go to the initial URL when the page is first created
            if self._initial_url:
                self._page.goto(self._initial_url, wait_until="networkidle")
    

    def get_page(self):
        if self._page is None:
            self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.launch(headless=False)
            self._context = self._browser.new_context()
            self._page = self._context.new_page()
        return self._page

    def close(self):
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()
        self._browser = None
        self._context = None
        self._page = None
        self._playwright = None

    def get_state(self):
        if self._state is None:
            if os.path.exists(self._state_file):
                try:
                    with open(self._state_file, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        if content:  # Check if file is not empty
                            self._state = json.load(f)
                        else:
                            self._state = self._init_default_state()
                except json.JSONDecodeError:  # Handle invalid JSON
                    self._state = self._init_default_state()
            else:
                self._state = self._init_default_state()
        return self._state

    def _init_default_state(self):
        """Initialize default state with necessary starting values"""
        return {
            "current_step": 0,          # Track current workflow step
            "is_session_active": False,  # Track if browser session is active
            "last_prompt": None,        # Store last drawing prompt
            "canvas_ready": False,      # Track if canvas is ready for drawing
            "results": [],              # Store drawing results history
            "timestamp": None           # Track last state update time
        }

    def save_state(self):
        if self._state is not None:
            with open(self._state_file, "w", encoding="utf-8") as f:
                json.dump(self._state, f) 