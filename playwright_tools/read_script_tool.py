from smolagents.tools import tool
import os

@tool
def read_script_tool() -> str:
    """
    Read all scripts from the 'playwright_scripts_history' folder and return the summary and content of each file.
    Useful for agent reflection and self-improvement.
    Returns:
        str: All script summaries and contents, or error message.
    """
    folder = "playwright_scripts_history"
    if not os.path.exists(folder):
        return f"No script history folder found: {folder}"
    files = [f for f in os.listdir(folder) if f.endswith('.py')]
    if not files:
        return f"No scripts found in {folder}."
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