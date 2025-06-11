import json
from langchain.memory import ConversationBufferMemory
from langchain.schema import messages_from_dict, messages_to_dict
from typing import Optional

class PersistentFileMemory(ConversationBufferMemory):
    file_path: Optional[str] = "memory.json"

    def __init__(self, file_path="memory.json", **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, "file_path", file_path)
        self._load_memory()

    def _load_memory(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_dict = json.load(f)
                self.chat_memory.messages = messages_from_dict(messages_dict)
        except FileNotFoundError:
            self.chat_memory.messages = []

    def save_context(self, inputs, outputs):
        super().save_context(inputs, outputs)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(messages_to_dict(self.chat_memory.messages), f, indent=2)
