# SE_Pet — Sistema Especialista (completo) compatível com Python 3.13

## Resumo
Projeto modular para recomendação de pets:
- Motor de inferência (forward chaining) totalmente implementado em Python (sem experta).
- Base de conhecimento em JSON (DataBase/rules.json) contendo 16 regras completas.
- Interface GUI com Tkinter (formularios, visualização de regras, export de relatório).
- Architecture modular (Core / GUI / DataBase).

## Como executar
1. Crie venv (recomendado):
   python -m venv venv
   venv\Scripts\activate   # Windows

2. Instale requisitos opcionais:
   pip install -r requirements.txt

3. Execute:
   python main.py

## Estrutura
- `Core/engine.py` — motor completo
- `Core/knowledge_loader.py` — carregador JSON
- `Core/models.py` — modelos (se precisar estender)
- `GUI/*` — interface e controller
- `DataBase/rules.json` — regras

## Observações
- Regras podem ser editadas sem alterar o código.
- Sistema explica quais regras dispararam e por quê.
