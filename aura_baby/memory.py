import json
import os

memory = {}

def load_memory():
    global memory
    if os.path.exists("data/memory.json"):
        with open("data/memory.json", "r", encoding="utf-8") as f:
            memory = json.load(f)

def save_memory():
    with open("data/memory.json", "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)
