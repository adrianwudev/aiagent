from typing import Optional
from smolagents.tools import Tool
import os

class ReadSeleniumScriptTool(Tool):
    """
    A SmolAgents Tool that reads all Selenium scripts from the 'selenium_scripts_history' folder.
    Returns the summary and script content for each file for agent reflection and self-improvement.
    """
    name = "read_selenium_script_tool"
    description = (
        "Read all Selenium scripts from the 'selenium_scripts_history' folder, "
        "including the summary and script content for each, to help the agent reflect and improve."
    )
    inputs = {}
    output_type = "string"

    def __init__(self):
        super().__init__()

    def forward(self) -> str:
        folder = "selenium_scripts_history"
        if not os.path.exists(folder):
            return f"No script history folder found: {folder}"
        files = [f for f in os.listdir(folder) if f.endswith('.py')]
        if not files:
            return f"No Selenium scripts found in {folder}."
        files.sort(key=lambda f: os.path.getmtime(os.path.join(folder, f)), reverse=True)
        results = []
        for fname in files:
            file_path = os.path.join(folder, fname)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                # Extract summary (assume it's the first comment block)
                summary = ""
                lines = content.splitlines()
                for line in lines:
                    if line.strip().startswith("# --- Script Summary ---"):
                        summary_lines = [line]
                        for l in lines[lines.index(line)+1:]:
                            summary_lines.append(l)
                            if l.strip() == "# ----------------------":
                                break
                        summary = "\n".join(summary_lines)
                        break
                results.append(f"Script: {fname}\n\n{summary}\n\nFull script:\n{content}\n{'='*60}\n")
            except Exception as e:
                results.append(f"Error reading {fname}: {e}\n{'='*60}\n")
        return "\n".join(results) 