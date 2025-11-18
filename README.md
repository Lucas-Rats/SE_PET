# 🐾 SE_Pet — Sistema Especialista para Recomendação de Pets

## 📋 Resumo do Projeto

**SE_Pet** é um sistema especialista completo desenvolvido em Python 3.13 que recomenda o pet ideal para cada pessoa baseado em seu perfil e estilo de vida. O sistema utiliza técnicas de Inteligência Artificial simbólica através de um motor de inferência baseado em **forward chaining** (encadeamento para frente).

### ✨ Características Principais

- ✅ **Motor de Inferência Completo**: Implementação nativa em Python, sem dependências de bibliotecas de IA
- ✅ **Base de Conhecimento Extensível**: 16 regras especializadas armazenadas em JSON
- ✅ **Interface Gráfica Moderna**: GUI intuitiva desenvolvida com Tkinter
- ✅ **Arquitetura Modular**: Separação clara entre Core, GUI e Database
- ✅ **Totalmente Comentado**: Código documentado para fácil compreensão e manutenção
- ✅ **Explicabilidade**: Sistema explica quais regras foram ativadas e por quê

---

## 🎯 Como Funciona

O sistema coleta informações do usuário através de 6 perguntas fundamentais:

1. **🏠 Tipo de moradia** (Casa ou Apartamento)
2. **📏 Tamanho da moradia** (Grande ou Pequeno)
3. **🌳 Área externa** (Possui quintal?)
4. **⏰ Disponibilidade para passeio**
5. **💝 Necessidade de interação**
6. **💰 Nível de investimento** (Alto, Médio ou Baixo)

Com base nessas informações, o motor de inferência avalia 16 regras especializadas e recomenda:
- **Pet principal** mais adequado ao perfil
- **Alternativas viáveis** compatíveis
- **Explicação detalhada** de por que cada recomendação foi feita

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.13 ou superior
- Tkinter (geralmente incluído na instalação padrão do Python)

### Passo a Passo

#### 1. Clone ou baixe o projeto

```bash
git clone <url-do-repositorio>
cd SE_Pet
```

#### 2. (Recomendado) Crie um ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instale dependências (opcional)

```bash
pip install -r requirements.txt
```
> **Nota**: O projeto não possui dependências externas obrigatórias. O Tkinter é nativo do Python.

#### 4. Execute a aplicação

```bash
python main.py
```

---

## 📁 Estrutura do Projeto

```
SE_Pet/
│
├── main.py                      # Ponto de entrada da aplicação
│
├── Core/                        # Núcleo do sistema especialista
│   ├── __init__.py
│   ├── inference_engine.py     # Motor de inferência (forward chaining)
│   ├── knowledge_base.py       # Base de conhecimento com regras
│   ├── knowledge_loader.py     # Carregador de regras JSON
│   └── models.py               # Modelos de dados (extensível)
│
├── GUI/                         # Interface gráfica do usuário
│   ├── __init__.py
│   ├── main_window.py          # Janela principal e páginas
│   └── controller.py           # Controlador (ponte entre GUI e Core)
│
├── DataBase/                    # Base de dados
│   └── rules.json              # Regras em formato JSON
│
├── requirements.txt             # Dependências do projeto
└── README.md                    # Este arquivo
```

---

## 🧠 Arquitetura do Sistema

### Motor de Inferência (`inference_engine.py`)

O motor implementa o algoritmo de **encadeamento para frente**:

```python
Para cada regra na base de conhecimento:
    SE condições da regra são satisfeitas pelos fatos:
        ENTÃO adiciona consequências às recomendações
        E marca a regra como disparada

Ordena recomendações por prioridade predefinida
Retorna (recomendações, regras_disparadas)
```

**Características do Motor:**
- ✅ Avaliação automática de todas as regras
- ✅ Tratamento de erros robusto
- ✅ Rastreamento de regras disparadas
- ✅ Ordenação por prioridade
- ✅ Estatísticas de uso
- ✅ Métodos de debug e teste

### Base de Conhecimento (`knowledge_base.py` e `rules.json`)

As regras são definidas em três componentes:

1. **Nome**: Identificador único (ex: `R1_CAO_GRANDE_IDEAL`)
2. **Condições**: Função lambda que avalia os fatos
3. **Consequências**: Lista de pets recomendados

**Exemplo de regra:**
```python
(
    "R1_CAO_GRANDE_IDEAL",
    lambda f: (
        f.get("moradia") == "Casa" and
        f.get("tam_moradia") == "Grande" and
        f.get("area_moradia") == "Sim" and
        f.get("TempoPasseio") == "Sim" and
        f.get("interacao") == "Sim" and
        f.get("investimento") == "Alto"
    ),
    ["Cachorro de Grande Porte", "Cachorro de Médio Porte"]
)
```

### Interface Gráfica (`main_window.py`)

A GUI é composta por 3 páginas principais:

#### 1. **HomePage** - Página Inicial
- Apresentação do sistema
- Motivação para usar
- Botão para iniciar teste

#### 2. **QuestionsPage** - Formulário
- 6 perguntas com opções múltipla escolha
- Layout em cards com scroll
- Validação de respostas
- Design moderno e intuitivo

#### 3. **ResultPage** - Resultados
- Pet principal recomendado
- Ilustração visual do pet
- Alternativas viáveis
- Explicação detalhada:
  - Justificativa da recomendação
  - Regras que foram ativadas
  - Resumo do perfil do usuário
- Opções para refazer ou voltar ao início

### Controlador (`controller.py`)

Faz a ponte entre GUI e motor de inferência:
- Recebe dados do formulário
- Executa inferência
- Formata resultados para exibição
- Gera explicações contextualizadas

---

## 🎨 Melhorias Implementadas na GUI

### Design Moderno
- ✨ Paleta de cores profissional
- 🎯 Cards com sombras e bordas suaves
- 📱 Layout responsivo e centralizado
- 🖱️ Efeitos hover nos botões
- 🎭 Emojis contextuais para melhor UX

### Experiência do Usuário
- 🔄 Navegação fluida entre páginas
- 📊 Visualização clara dos resultados
- 💡 Explicações detalhadas e contextualizadas
- 🎨 Ilustrações visuais dos pets
- ✅ Feedback visual em todas as ações

### Funcionalidades
- 📋 Formulário com hints explicativos
- 🔍 Validação de dados
- 📈 Exibição de múltiplas alternativas
- 🧾 Resumo completo do perfil
- 🔄 Fácil refazer teste

---

## 🐕 Pets Recomendados

O sistema pode recomendar 9 categorias de pets:

1. 🐶 **Cachorro de Grande Porte** (ex: Labrador, Pastor Alemão)
2. 🐕 **Cachorro de Médio Porte** (ex: Beagle, Cocker Spaniel)
3. 🐩 **Cachorro de Pequeno Porte** (ex: Chihuahua, Poodle Toy)
4. 🐱 **Gato** (ex: Persa, Siamês, SRD)
5. 🐦 **Pássaro** (ex: Calopsita, Periquito)
6. 🦎 **Réptil** (ex: Iguana, Gecko)
7. 🐹 **Roedor** (ex: Hamster, Porquinho-da-índia)
8. 🐟 **Peixe** (ex: Betta, Guppy)
9. 🕷️ **Aracnídeo** (ex: Tarântula)

---

## 💻 Código Comentado

Todo o código foi extensivamente comentado para facilitar:
- 📖 **Compreensão**: Explicações claras de cada função e classe
- 🔧 **Manutenção**: Fácil localização e modificação de funcionalidades
- 📚 **Aprendizado**: Ideal para estudantes de IA e Python
- 🚀 **Extensão**: Documentação para adicionar novas features

### Exemplo de Documentação

```python
def inferir(self, fatos: Dict[str, str]) -> Tuple[List[str], List[str]]:
    """
    Executa o processo de inferência sobre os fatos fornecidos.
    
    Este é o método principal do motor de inferência. Ele:
    1. Percorre todas as regras da base de conhecimento
    2. Avalia a condição de cada regra contra os fatos
    3. Coleta as consequências das regras que disparam
    4. Remove duplicatas e ordena as recomendações
    
    Args:
        fatos: Dicionário com os fatos conhecidos
        
    Returns:
        Tupla (recomendações_ordenadas, regras_disparadas)
    """
    # Implementação...
```

---

## 🔧 Personalização

### Adicionar Novas Regras

Edite `DataBase/rules.json`:

```json
{
  "name": "R17_MINHA_NOVA_REGRA",
  "conditions": {
    "moradia": "Casa",
    "interacao": "Sim"
  },
  "consequences": ["Novo Pet"],
  "explanation": "Explicação da regra"
}
```

### Modificar Prioridades

Edite `Core/knowledge_base.py`:

```python
PRIORIDADE_ANIMAIS = [
    "Seu Pet Favorito",
    "Cachorro de Grande Porte",
    # ... resto da lista
]
```

### Customizar Cores

Modifique o dicionário `colors` em `main_window.py`:

```python
self.colors = {
    'primary': '#SEU_COR_PRIMARIA',
    'secondary': '#SUA_COR_SECUNDARIA',
    # ...
}
```

---

## 📊 Recursos Avançados

### Estatísticas do Motor

```python
engine = InferenceEngine()
# ... realizar inferências ...
stats = engine.get_statistics()
print(stats)
# {'total_inferences': 5, 'total_rules': 16, ...}
```

### Teste de Regras Específicas

```python
fatos = {'moradia': 'Casa', 'tam_moradia': 'Grande', ...}
disparou = engine.test_rule("R1_CAO_GRANDE_IDEAL", fatos)
```

### Explicação de Recomendação

```python
explicacao = engine.explain_recommendation("Gato", fatos)
print(explicacao)
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

---

## 👥 Autores

Desenvolvido como projeto acadêmico de Sistema Especialista.

---

## 📞 Suporte

Para dúvidas ou sugestões, abra uma issue no repositório do projeto.

---

## 🎓 Aprendizado

Este projeto demonstra:
- ✅ Implementação de Sistema Especialista
- ✅ Técnicas de Inteligência Artificial Simbólica
- ✅ Forward Chaining (Encadeamento para Frente)
- ✅ Arquitetura MVC em Python
- ✅ Design de Interface com Tkinter
- ✅ Boas práticas de documentação de código

---

**Feito com ❤️ e 🐾**