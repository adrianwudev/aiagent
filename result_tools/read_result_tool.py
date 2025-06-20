from smolagents.tools import Tool
import os

class ReadResultTool(Tool):
    """
    A SmolAgents Tool that reads all result files from the 'results' folder.
    Returns the content of each file for agent reflection and self-improvement.
    """
    name = "read_result_tool"
    description = (
        "Read all result files from the 'results' folder, "
        "returning the content of each for agent reflection and improvement."
    )
    inputs = {}
    output_type = "string"

    def __init__(self):
        super().__init__()

    def forward(self) -> str:
        folder = "results"
        if not os.path.exists(folder):
            return f"No results folder found: {folder}"
        files = [f for f in os.listdir(folder) if f.endswith('.txt')]
        if not files:
            return f"No result files found in {folder}."
        files.sort(key=lambda f: os.path.getmtime(os.path.join(folder, f)), reverse=True)
        results = []
        for fname in files:
            file_path = os.path.join(folder, fname)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                results.append(f"Result file: {fname}\n{content}\n{'='*60}\n")
            except Exception as e:
                results.append(f"Error reading {fname}: {e}\n{'='*60}\n")
        return "\n".join(results) 