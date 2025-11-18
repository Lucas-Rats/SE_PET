# Core/inference_engine.py
import sys
from typing import Dict, Tuple, List
from .knowledge_base import REGRAS, PRIORIDADE_ANIMAIS

class InferenceEngine:
    """
    Motor de Inferência: encadeamento para frente.
    Avalia todas as regras (REGRAS) contra os fatos (dict).
    """

    def __init__(self, regras=REGRAS):
        self.regras = regras

    def inferir(self, fatos: Dict[str, str]) -> Tuple[List[str], List[str]]:
        recomendacoes = set()
        regras_disparadas = []

        for (nome_regra, condicao, consequencia) in self.regras:
            try:
                if condicao(fatos):
                    regras_disparadas.append(nome_regra)
                    recomendacoes.update(consequencia)
            except Exception as e:
                print(f"[AVISO] Erro ao avaliar a Regra {nome_regra}: {e}", file=sys.stderr)

        recomendacoes_ordenadas = sorted(
            recomendacoes,
            key=lambda x: PRIORIDADE_ANIMAIS.index(x) if x in PRIORIDADE_ANIMAIS else 999
        )

        return recomendacoes_ordenadas, regras_disparadas
