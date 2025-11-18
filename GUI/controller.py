# GUI/controller.py
import tkinter as tk
from tkinter import messagebox
from typing import Dict, Any
from Core.inference_engine import InferenceEngine
from Core.knowledge_base import PRIORIDADE_ANIMAIS

class Controller:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.motor = InferenceEngine()

    def run_analysis(self, facts: Dict[str, str]):
        """
        Executa inferência e retorna:
         - recomendacao_ordenada (list)
         - regras_disparadas (list)
         - texto_explicacao (str)
        """
        recs, regras = self.motor.inferir(facts)

        # montar explicação textual
        if not recs:
            texto = "❌ Nenhuma recomendação encontrada para esse perfil.\n"
        else:
            texto = f"⭐ Recomendação principal: {recs[0]}\n\n"
            if len(recs) > 1:
                texto += "🔄 Alternativas:\n"
                for i, a in enumerate(recs[1:], start=1):
                    texto += f"  {i}. {a}\n"
                texto += "\n"

        texto += "📋 Regras disparadas:\n"
        if regras:
            for r in regras:
                texto += f" - {r}\n"
        else:
            texto += " Nenhuma regra disparada.\n"

        texto += "\n📌 Fatos fornecidos:\n"
        for k, v in facts.items():
            texto += f" • {k}: {v}\n"

        return recs, regras, texto
