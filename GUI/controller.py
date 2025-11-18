# GUI/controller.py
"""
Controlador da Interface Gráfica
Faz a ponte entre a GUI e o motor de inferência do sistema especialista.
"""

import tkinter as tk
from tkinter import messagebox
from typing import Dict, List, Tuple
from Core.inference_engine import InferenceEngine
from Core.knowledge_base import PRIORIDADE_ANIMAIS


class Controller:
    """
    Controlador principal da aplicação.
    Gerencia a comunicação entre a interface gráfica e o motor de inferência,
    processando as entradas do usuário e formatando os resultados para exibição.
    """
    
    def __init__(self, root: tk.Tk):
        """
        Inicializa o controlador.
        
        Args:
            root: Janela raiz do Tkinter
        """
        self.root = root
        # Inicializa o motor de inferência com as regras da base de conhecimento
        self.motor = InferenceEngine()

    def run_analysis(self, facts: Dict[str, str]) -> Tuple[List[str], List[str], str]:
        """
        Executa a análise completa do perfil do usuário.
        
        Este método:
        1. Recebe os fatos coletados do usuário
        2. Executa a inferência através do motor
        3. Formata os resultados em texto explicativo
        4. Retorna recomendações, regras e explicação
        
        Args:
            facts: Dicionário com os fatos fornecidos pelo usuário
                   Ex: {'moradia': 'Casa', 'tam_moradia': 'Grande', ...}
        
        Returns:
            Tupla contendo:
            - recomendacoes_ordenadas (list): Lista de pets recomendados ordenados por prioridade
            - regras_disparadas (list): Lista de nomes das regras que foram ativadas
            - texto_explicacao (str): Texto formatado com explicação completa
        """
        # Executa inferência usando o motor
        recs, regras = self.motor.inferir(facts)

        # Constrói explicação textual formatada
        texto = self._build_explanation(recs, regras, facts)

        return recs, regras, texto

    def _build_explanation(self, recomendacoes: List[str], 
                          regras: List[str], 
                          facts: Dict[str, str]) -> str:
        """
        Constrói texto explicativo detalhado dos resultados.
        
        Args:
            recomendacoes: Lista de pets recomendados
            regras: Lista de regras que foram disparadas
            facts: Dicionário com os fatos fornecidos
        
        Returns:
            String com explicação formatada em seções
        """
        texto = ""
        
        # Seção 1: Recomendação Principal
        if not recomendacoes:
            texto += "❌ RESULTADO\n"
            texto += "━" * 50 + "\n"
            texto += "Nenhuma recomendação encontrada para esse perfil.\n"
            texto += "Isso pode ocorrer se as condições fornecidas não\n"
            texto += "corresponderem a nenhuma regra da base de conhecimento.\n\n"
        else:
            texto += "⭐ RECOMENDAÇÃO PRINCIPAL\n"
            texto += "━" * 50 + "\n"
            texto += f"{recomendacoes[0]}\n\n"
            
            # Adiciona justificativa baseada no tipo de pet
            texto += self._get_pet_justification(recomendacoes[0], facts)
            texto += "\n"
            
            # Seção 2: Alternativas (se houver mais de uma recomendação)
            if len(recomendacoes) > 1:
                texto += "\n🔄 ALTERNATIVAS VIÁVEIS\n"
                texto += "━" * 50 + "\n"
                for i, animal in enumerate(recomendacoes[1:], start=1):
                    texto += f"{i}. {animal}\n"
                texto += "\n"

        # Seção 3: Regras do Sistema Especialista que foram ativadas
        texto += "📋 REGRAS DISPARADAS\n"
        texto += "━" * 50 + "\n"
        if regras:
            for r in regras:
                # Remove prefixo "RX_" para melhor legibilidade
                nome_formatado = r.replace("_", " ").title()
                texto += f"✓ {nome_formatado}\n"
        else:
            texto += "Nenhuma regra foi disparada.\n"
        texto += "\n"

        # Seção 4: Resumo do Perfil do Usuário
        texto += "👤 SEU PERFIL\n"
        texto += "━" * 50 + "\n"
        # Mapeia os códigos para descrições amigáveis
        labels_amigaveis = {
            'moradia': 'Tipo de moradia',
            'tam_moradia': 'Tamanho da moradia',
            'area_moradia': 'Possui área externa',
            'TempoPasseio': 'Disponibilidade para passeio',
            'interacao': 'Deseja interação',
            'investimento': 'Nível de investimento'
        }
        
        # Mapeia valores para texto mais legível
        valor_amigavel = {
            'Sim': '✓ Sim',
            'Nao': '✗ Não',
            'Casa': '🏠 Casa',
            'Apartamento': '🏢 Apartamento',
            'Grande': '⬆️ Grande',
            'Pequeno': '⬇️ Pequeno',
            'Alto': '💰💰💰 Alto',
            'Medio': '💰💰 Médio',
            'Baixo': '💰 Baixo'
        }
        
        for k, v in facts.items():
            label = labels_amigaveis.get(k, k)
            valor = valor_amigavel.get(v, v)
            texto += f"• {label}: {valor}\n"

        return texto

    def _get_pet_justification(self, pet: str, facts: Dict[str, str]) -> str:
        """
        Gera justificativa personalizada para a recomendação do pet.
        
        Args:
            pet: Nome do pet recomendado
            facts: Dicionário com os fatos do usuário
        
        Returns:
            String com justificativa contextualizada
        """
        justificativa = "💡 Por que esta recomendação?\n"
        
        pet_lower = pet.lower()
        
        # Justificativas contextualizadas por tipo de pet
        if "cachorro de grande porte" in pet_lower:
            justificativa += (
                "Cães de grande porte precisam de muito espaço e exercício.\n"
                "Seu perfil indica que você tem as condições ideais:\n"
            )
            if facts.get('moradia') == 'Casa':
                justificativa += "✓ Casa com espaço adequado\n"
            if facts.get('area_moradia') == 'Sim':
                justificativa += "✓ Área externa para o pet se exercitar\n"
            if facts.get('TempoPasseio') == 'Sim':
                justificativa += "✓ Disponibilidade para passeios diários\n"
            if facts.get('investimento') == 'Alto':
                justificativa += "✓ Recursos para alimentação e cuidados veterinários\n"
                
        elif "cachorro de médio porte" in pet_lower:
            justificativa += (
                "Cães de médio porte são versáteis e se adaptam bem.\n"
                "Seu perfil oferece boas condições:\n"
            )
            if facts.get('TempoPasseio') == 'Sim':
                justificativa += "✓ Tempo para passeios regulares\n"
            if facts.get('interacao') == 'Sim':
                justificativa += "✓ Disposição para interação e companheirismo\n"
                
        elif "cachorro de pequeno porte" in pet_lower:
            justificativa += (
                "Cães pequenos são ótimos para espaços menores.\n"
                "Vantagens para seu perfil:\n"
            )
            if facts.get('moradia') == 'Apartamento':
                justificativa += "✓ Adaptam-se bem a apartamentos\n"
            justificativa += "✓ Menores custos de manutenção\n"
            justificativa += "✓ Mais fáceis de transportar\n"
            
        elif "gato" in pet_lower:
            justificativa += (
                "Gatos são independentes e de baixa manutenção.\n"
                "Ideais para seu perfil porque:\n"
            )
            if facts.get('TempoPasseio') == 'Nao':
                justificativa += "✓ Não precisam de passeios externos\n"
            justificativa += "✓ São limpos e cuidam da própria higiene\n"
            justificativa += "✓ Oferecem companhia sem demandar atenção constante\n"
            
        elif "peixe" in pet_lower:
            justificativa += (
                "Peixes são ideais para observação e relaxamento.\n"
                "Perfeitos para você porque:\n"
            )
            justificativa += "✓ Requerem mínima interação física\n"
            justificativa += "✓ Baixo custo de manutenção\n"
            justificativa += "✓ Ocupam pouco espaço\n"
            
        elif "pássaro" in pet_lower or "passaro" in pet_lower:
            justificativa += (
                "Pássaros trazem vida e sons agradáveis ao ambiente.\n"
                "Adequados ao seu perfil:\n"
            )
            justificativa += "✓ Interação moderada através de cantos e sons\n"
            justificativa += "✓ Ocupam pouco espaço\n"
            justificativa += "✓ Manutenção relativamente simples\n"
            
        elif "réptil" in pet_lower or "reptil" in pet_lower:
            justificativa += (
                "Répteis são pets únicos e fascinantes.\n"
                "Combinam com seu perfil por:\n"
            )
            justificativa += "✓ Baixa necessidade de interação\n"
            justificativa += "✓ Interessantes para observação\n"
            justificativa += "✓ Silenciosos e discretos\n"
            
        elif "roedor" in pet_lower:
            justificativa += (
                "Roedores são companheiros carinhosos e brincalhões.\n"
                "Ótimos para você porque:\n"
            )
            justificativa += "✓ Tamanho compacto\n"
            justificativa += "✓ Baixo custo\n"
            justificativa += "✓ Interativos e divertidos\n"
            
        elif "aracnídeo" in pet_lower or "aracnideo" in pet_lower:
            justificativa += (
                "Aracnídeos são pets exóticos e de fácil manutenção.\n"
                "Adequados para:\n"
            )
            justificativa += "✓ Quem busca pets não convencionais\n"
            justificativa += "✓ Custo mínimo de manutenção\n"
            justificativa += "✓ Pouco espaço necessário\n"
        
        return justificativa

    def validate_facts(self, facts: Dict[str, str]) -> Tuple[bool, str]:
        """
        Valida os fatos fornecidos pelo usuário.
        
        Args:
            facts: Dicionário com os fatos a validar
        
        Returns:
            Tupla (válido, mensagem_erro)
            - válido: True se todos os fatos são válidos
            - mensagem_erro: Mensagem explicando o erro (vazia se válido)
        """
        # Lista de campos obrigatórios
        campos_obrigatorios = [
            'moradia', 
            'tam_moradia', 
            'area_moradia', 
            'TempoPasseio', 
            'interacao', 
            'investimento'
        ]
        
        # Verifica campos vazios
        campos_vazios = [campo for campo in campos_obrigatorios 
                        if not facts.get(campo)]
        
        if campos_vazios:
            return False, f"Campos obrigatórios não preenchidos: {', '.join(campos_vazios)}"
        
        # Valida valores permitidos para cada campo
        valores_validos = {
            'moradia': ['Casa', 'Apartamento'],
            'tam_moradia': ['Grande', 'Pequeno'],
            'area_moradia': ['Sim', 'Nao'],
            'TempoPasseio': ['Sim', 'Nao'],
            'interacao': ['Sim', 'Nao'],
            'investimento': ['Alto', 'Medio', 'Baixo']
        }
        
        for campo, valor in facts.items():
            if campo in valores_validos and valor not in valores_validos[campo]:
                return False, f"Valor inválido para {campo}: {valor}"
        
        return True, ""