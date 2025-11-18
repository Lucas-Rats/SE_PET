# Core/knowledge_loader.py
import json
import os
from typing import Dict, Any

def load_rules_json(path: str = None) -> Dict[str, Any]:
    if path is None:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(base_dir, "DataBase", "rules.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo de regras não encontrado: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
