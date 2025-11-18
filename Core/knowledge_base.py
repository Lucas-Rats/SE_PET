# Core/knowledge_base.py
import sys

REGRAS = [
    # --- Grupo A: Interação = Sim ---
    (
        "R1_CAO_GRANDE_IDEAL",
        lambda f: f.get("moradia") == "Casa" and f.get("tam_moradia") == "Grande" and f.get("area_moradia") == "Sim" and f.get("TempoPasseio") == "Sim" and f.get("interacao") == "Sim" and f.get("investimento") == "Alto",
        ["Cachorro de Grande Porte", "Cachorro de Médio Porte"]
    ),
    (
        "R2_CAO_MEDIO_CASA_OU_GRANDE",
        lambda f: (f.get("moradia") == "Casa" or f.get("tam_moradia") == "Grande") and f.get("area_moradia") == "Sim" and f.get("TempoPasseio") == "Sim" and f.get("interacao") == "Sim" and f.get("investimento") != "Baixo",
        ["Cachorro de Médio Porte"]
    ),
    (
        "R3_CAO_PEQUENO_APTO",
        lambda f: f.get("moradia") == "Apartamento" and f.get("TempoPasseio") == "Sim" and f.get("interacao") == "Sim",
        ["Cachorro de Pequeno Porte"]
    ),
    (
        "R4_CAO_PEQUENO_CASA_PEQUENA",
        lambda f: f.get("moradia") == "Casa" and f.get("tam_moradia") == "Pequeno" and f.get("TempoPasseio") == "Sim" and f.get("interacao") == "Sim",
        ["Cachorro de Pequeno Porte", "Gato"]
    ),
    (
        "R5_GATO_SEM_PASSEIO",
        lambda f: f.get("TempoPasseio") == "Nao" and f.get("interacao") == "Sim" and f.get("investimento") != "Baixo",
        ["Gato"]
    ),
    (
        "R6_GATO_OU_ROEDOR_APTO_PEQUENO",
        lambda f: f.get("moradia") == "Apartamento" and f.get("tam_moradia") == "Pequeno" and f.get("interacao") == "Sim",
        ["Gato", "Roedor"]
    ),
    
    # --- Grupo B: Interação = Nao ---
    (
        "R7_PEIXE_BAIXO_CUSTO",
        lambda f: f.get("interacao") == "Nao" and f.get("investimento") == "Baixo",
        ["Peixe"]
    ),
    (
        "R8_ROEDOR_OU_PEIXE_BAIXO_CUSTO_PEQUENO",
        lambda f: f.get("interacao") == "Nao" and f.get("investimento") == "Baixo" and f.get("tam_moradia") == "Pequeno",
        ["Roedor", "Peixe"]
    ),
    (
        "R9_PASSARO_MEDIO_CUSTO_SEM_PASSEIO",
        lambda f: f.get("interacao") == "Nao" and f.get("TempoPasseio") == "Nao" and f.get("investimento") == "Medio",
        ["Pássaro"]
    ),
    (
        "R10_REPTIL_CUSTO_ALTO_MEDIO",
        lambda f: f.get("interacao") == "Nao" and f.get("TempoPasseio") == "Nao" and (f.get("investimento") == "Alto" or f.get("investimento") == "Medio"),
        ["Réptil"]
    ),
    (
        "R11_ARACNIDEO_CUSTO_BAIXO_MEDIO",
        lambda f: f.get("interacao") == "Nao" and f.get("TempoPasseio") == "Nao" and (f.get("investimento") == "Baixo" or f.get("investimento") == "Medio"),
        ["Aracnídeo"]
    ),
    (
        "R12_PEIXE_OU_REPTIL_ALTO_CUSTO",
        lambda f: f.get("interacao") == "Nao" and f.get("investimento") == "Alto",
        ["Peixe", "Réptil"]
    ),

    # --- Grupo C: Regras de Remendo ---
    (
        "R13_GATO_OU_ROEDOR_BAIXO_CUSTO_INTERACAO",
        lambda f: f.get("TempoPasseio") == "Nao" and f.get("interacao") == "Sim" and f.get("investimento") == "Baixo",
        ["Gato", "Roedor"]
    ),
    (
        "R14_OBSERVACIONAIS_MEDIO_CUSTO_COM_PASSEIO",
        lambda f: f.get("interacao") == "Nao" and f.get("TempoPasseio") == "Sim" and f.get("investimento") == "Medio",
        ["Pássaro", "Réptil", "Aracnídeo"]
    ),
    (
        "R15_CASA_GRANDE_SEM_QUINTAL",
        lambda f: f.get("moradia") == "Casa" and f.get("tam_moradia") == "Grande" and f.get("area_moradia") == "Nao" and f.get("TempoPasseio") == "Sim" and f.get("interacao") == "Sim",
        ["Cachorro de Médio Porte", "Gato"]
    ),
    (
        "R16_INTERACAO_BAIXO_CUSTO_COM_QUINTAL",
        lambda f: f.get("area_moradia") == "Sim" and f.get("TempoPasseio") == "Sim" and f.get("interacao") == "Sim" and f.get("investimento") == "Baixo",
        ["Gato", "Cachorro de Pequeno Porte", "Cachorro de Médio Porte"]
    ),
]

PRIORIDADE_ANIMAIS = [
    "Cachorro de Grande Porte",
    "Cachorro de Médio Porte", 
    "Cachorro de Pequeno Porte",
    "Gato",
    "Pássaro",
    "Réptil",
    "Roedor",
    "Peixe",
    "Aracnídeo"
]
