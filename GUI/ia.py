import sys

# -----------------------------------------------------------------
# ARQUIVO: knowledge_base.py
# DESCRIÇÃO: Define a Base de Conhecimento (as 16 regras).
# -----------------------------------------------------------------
# Cada regra é uma tupla contendo:
# 1. Nome da Regra (string)
# 2. Condição (uma função lambda que recebe 'fatos' e retorna True/False)
# 3. Consequência (uma lista de strings de recomendação)
# -----------------------------------------------------------------

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


# -----------------------------------------------------------------
# ARQUIVO: inference_engine.py
# DESCRIÇÃO: O Motor de Inferência (Forward-Chaining).
# -----------------------------------------------------------------

class InferenceEngine:
    """
    Motor de Inferência baseado em encadeamento para frente.
    Avalia todas as regras da base de conhecimento contra um 
    conjunto de fatos.
    """
    
    def __init__(self, regras):
        """
        Carrega a base de conhecimento na inicialização.
        
        Args:
            regras (list): A lista de regras (REGRAS).
        """
        self.regras = regras

    def inferir(self, fatos):
        """
        Executa o motor de inferência.

        Args:
            fatos (dict): O perfil do cliente (fatos de entrada).

        Returns:
            tuple: (list de recomendações, list de regras disparadas)
        """
        
        # Usamos um set() para coletar resultados e evitar duplicatas
        recomendacoes = set()
        regras_disparadas = []
        
        # 1. Ciclo de Inferência (Forward-Chaining)
        # O motor itera por TODAS as regras
        for (nome_regra, condicao, consequencia) in self.regras:
            
            # 2. Avaliação da Regra
            try:
                # A função lambda da regra é executada passando os fatos
                if condicao(fatos):
                    # 3. Disparo da Regra
                    regras_disparadas.append(nome_regra)
                    
                    # 4. Acumulação de Resultados
                    # O operador .update() do set adiciona os novos itens
                    recomendacoes.update(consequencia)
                    
            except Exception as e:
                # Captura erros (ex: um fato ausente que não foi 
                # tratado com .get())
                print(f"[AVISO] Erro ao avaliar a Regra {nome_regra}: {e}", file=sys.stderr)
                
        # 5. Conclusão Final
        # Retorna as recomendações e as regras que as geraram
        return list(recomendacoes), regras_disparadas


# -----------------------------------------------------------------
# ARQUIVO: main.py
# (Esta seção foi ATUALIZADA para entrada interativa)
# -----------------------------------------------------------------

def formatar_fatos(fatos):
    """Função auxiliar para imprimir os fatos de forma legível."""
    display = "  " + "\n  ".join(f"{k.ljust(15)}: {v}" for k, v in fatos.items())
    return display

def fazer_pergunta(pergunta_texto, opcoes_validas):
    """
    Exibe uma pergunta e valida a resposta do usuário contra uma lista de opções.
    """
    print(f"\n{pergunta_texto}")
    # Formata as opções para exibição, ex: (Casa / Apartamento)
    opcoes_display = " / ".join(opcoes_validas)
    print(f"(Opções: {opcoes_display})")
    
    while True:
        # Padroniza a entrada: remove espaços e capitaliza a primeira letra
        # Isso garante que 'casa' vire 'Casa' e 'nao' vire 'Nao'
        resposta = input("Sua resposta: ").strip().capitalize()

        if resposta in opcoes_validas:
            return resposta
        else:
            print(f"--- Erro: Resposta '{resposta}' inválida. Por favor, use uma das opções: {opcoes_validas}")

def executar_sistema_interativo():
    """
    Executa o fluxo principal do sistema especialista de forma interativa.
    """
    
    # 1. Define as perguntas e suas opções válidas (que correspondem às regras)
    mapa_perguntas = [
        ("moradia", "Qual o tipo de imóvel que você mora?", ["Casa", "Apartamento"]),
        ("tam_moradia", "Qual o Tamanho do imóvel?", ["Grande", "Pequeno"]),
        ("area_moradia", "O imóvel possui área externa, como quintal?", ["Sim", "Nao"]),
        ("TempoPasseio", "Você tem tempo para passeio?", ["Sim", "Nao"]),
        ("interacao", "Você tem necessidade de toque, atenção, carinho... (interação)?", ["Sim", "Nao"]),
        ("investimento", "O investimento que você pode ter para dar uma qualidade de vida é:", ["Alto", "Medio", "Baixo"]),
    ]
    
    # 2. Inicializa o Motor de Inferência
    # (Assume que 'REGRAS' e 'InferenceEngine' estão definidos acima no script)
    motor = InferenceEngine(REGRAS)
    
    # 3. Coleta os Fatos do Usuário
    print("--- Sistema Especialista de Recomendação de Pet ---")
    print("Por favor, responda às 6 perguntas a seguir para definirmos seu perfil.")
    
    fatos_cliente = {}
    for chave, texto_pergunta, opcoes in mapa_perguntas:
        resposta_usuario = fazer_pergunta(texto_pergunta, opcoes)
        fatos_cliente[chave] = resposta_usuario
        
    # 4. Processa os Fatos e Executa a Inferência
    print("\n---------------------------------------------------------")
    print("Processando seu perfil...")
    print("---------------------------------------------------------")
    
    resultados, regras_disparadas = motor.inferir(fatos_cliente)
    
    # 5. Exibe o Relatório Final
    print("Fatos do Cliente (Entrada):")
    print(formatar_fatos(fatos_cliente))
    
    print("\nRegras Disparadas:")
    if not regras_disparadas:
        print("  Nenhuma regra disparada.")
    else:
        print("  " + "\n  ".join(regras_disparadas))
        
    print("\nRecomendações Finais:")
    if not resultados:
        print("  Nenhuma recomendação encontrada para este perfil.")
    else:
        for r in resultados:
            print(f"  - {r}")
    print("\n")


# Ponto de entrada do script
if __name__ == "__main__":
    # Agora executa o modo interativo em vez das simulações
    executar_sistema_interativo()