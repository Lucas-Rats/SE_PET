# GUI/main_window.py
"""
Sistema Especialista para Recomendação de Pets
Interface Gráfica Principal - Versão Melhorada
"""

import tkinter as tk
from tkinter import ttk
from GUI.controller import Controller


class App:
    """
    Classe principal da aplicação que gerencia as páginas e navegação.
    Implementa um sistema de navegação entre diferentes telas (frames).
    """
    
    def __init__(self, root):
        """
        Inicializa a aplicação principal.
        
        Args:
            root: Janela principal do Tkinter
        """
        self.root = root
        self.root.title("🐾 SE_Pet — Sistema Especialista de Recomendação de Pets")
        
        # Inicia em tela cheia (fullscreen)
        self.root.state('zoomed')  # Windows
        # Para outros sistemas: self.root.attributes('-zoomed', True)  # Linux
        # Para Mac: self.root.attributes('-fullscreen', True)
        
        # Dimensões mínimas caso o usuário saia do fullscreen
        self.root.minsize(900, 700)
        
        # Configura cores do tema moderno
        self.colors = {
            'primary': '#4A90E2',      # Azul principal
            'secondary': '#50C878',    # Verde secundário
            'background': '#F5F7FA',   # Fundo claro
            'card': '#FFFFFF',         # Branco para cards
            'text_dark': '#2C3E50',    # Texto escuro
            'text_light': '#7F8C8D',   # Texto claro
            'accent': '#E74C3C',       # Vermelho para destaques
            'success': '#27AE60'       # Verde para sucesso
        }
        
        # Aplica cor de fundo à janela
        self.root.configure(bg=self.colors['background'])
        
        # Inicializa o controlador de lógica
        self.controller = Controller(root)

        # Container principal que irá conter todas as páginas empilhadas
        self.container = tk.Frame(root, bg=self.colors['background'])
        self.container.pack(fill="both", expand=True)
        
        # Configura para centralização
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Dicionário para armazenar todas as páginas
        self.frames = {}
        
        # Cria todas as páginas e as empilha no mesmo espaço
        for F in (HomePage, QuestionsPage, ResultPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self, colors=self.colors)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Configura estilos personalizados
        self._configure_styles()
        
        # Mostra a página inicial
        self.show_frame("HomePage")
        
        # Variável para armazenar dados de resultado
        self.result_data = None

    def _configure_styles(self):
        """
        Configura estilos personalizados para os widgets ttk.
        Define aparência consistente em toda a aplicação.
        """
        style = ttk.Style()
        
        # Frame principal
        style.configure('Main.TFrame', background=self.colors['background'])
        
        # Botão primário (destaque)
        style.configure('Primary.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       padding=12,
                       relief='flat')
        
        # Botão secundário
        style.configure('Secondary.TButton',
                       font=('Segoe UI', 10),
                       padding=10,
                       relief='flat')
        
        # Label de título
        style.configure('Title.TLabel',
                       font=('Segoe UI', 24, 'bold'),
                       foreground=self.colors['text_dark'],
                       background=self.colors['background'])
        
        # Label de subtítulo
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 12),
                       foreground=self.colors['text_light'],
                       background=self.colors['background'])

    def show_frame(self, page_name):
        """
        Exibe uma página específica trazendo-a para frente.
        
        Args:
            page_name: Nome da classe da página a ser exibida
        """
        frame = self.frames[page_name]
        frame.tkraise()

    def run_inference_and_show(self, facts):
        """
        Executa a inferência do sistema especialista e exibe os resultados.
        
        Args:
            facts: Dicionário com os fatos coletados do usuário
        """
        # Executa análise através do controlador
        recs, regras, explicacao = self.controller.run_analysis(facts)
        
        # Passa os resultados para a página de resultados
        result_page: ResultPage = self.frames["ResultPage"]
        result_page.set_result(recs, regras, explicacao, facts)
        
        # Exibe a página de resultados
        self.show_frame("ResultPage")


class HomePage(ttk.Frame):
    """
    Página inicial da aplicação.
    Apresenta o sistema e convida o usuário a iniciar o teste.
    """
    
    def __init__(self, parent, controller, colors):
        """
        Inicializa a página inicial.
        
        Args:
            parent: Widget pai
            controller: Controlador principal da aplicação
            colors: Dicionário com as cores do tema
        """
        super().__init__(parent)
        self.app_controller = controller
        self.colors = colors
        
        # Configura o fundo
        self.configure(style='Main.TFrame')
        
        # Configura grid para expansão total
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Frame principal que ocupará todo o espaço
        main_wrapper = tk.Frame(self, bg=self.colors['background'])
        main_wrapper.grid(row=0, column=0, sticky='nsew')
        
        # Configura grid do wrapper para centralizar
        main_wrapper.grid_rowconfigure(0, weight=1)
        main_wrapper.grid_columnconfigure(0, weight=1)
        
        # Container central para conteúdo
        # Centralizado perfeitamente no meio da tela
        content_frame = tk.Frame(main_wrapper, bg=self.colors['background'])
        content_frame.grid(row=0, column=0)

        # Ícone decorativo (emoji de pet)
        icon_label = tk.Label(
            content_frame,
            text="🐾",
            font=('Segoe UI', 72),
            bg=self.colors['background'],
            fg=self.colors['primary']
        )
        icon_label.pack(pady=(0, 20))

        # Título principal
        title = tk.Label(
            content_frame,
            text="Descubra Seu Pet Ideal",
            font=('Segoe UI', 28, 'bold'),
            fg=self.colors['text_dark'],
            bg=self.colors['background']
        )
        title.pack(pady=(0, 15))

        # Subtítulo explicativo
        subtitle = tk.Label(
            content_frame,
            text="Responda a 6 perguntas simples e descubra qual animal\n"
                 "de estimação combina perfeitamente com seu estilo de vida!",
            font=('Segoe UI', 13),
            fg=self.colors['text_light'],
            bg=self.colors['background'],
            justify='center'
        )
        subtitle.pack(pady=(0, 30))

        # Card decorativo com informações
        info_card = tk.Frame(
            content_frame,
            bg=self.colors['card'],
            relief='flat',
            bd=0,
            highlightthickness=0
        )
        info_card.pack(pady=(0, 30), padx=40)
        
        # Não adiciona sombra/borda

        # Lista de benefícios/características
        benefits = [
            "✓ Análise personalizada baseada em suas necessidades",
            "✓ Consideramos espaço, tempo e investimento disponível",
            "✓ Recomendações baseadas em sistema especialista"
        ]
        
        for benefit in benefits:
            benefit_label = tk.Label(
                info_card,
                text=benefit,
                font=('Segoe UI', 11),
                fg=self.colors['text_dark'],
                bg=self.colors['card'],
                anchor='w',
                padx=25,
                pady=8
            )
            benefit_label.pack(fill='x')

        # Botão para iniciar o teste
        button_frame = tk.Frame(content_frame, bg=self.colors['background'])
        button_frame.pack(pady=(30, 0))
        
        start_btn = tk.Button(
            button_frame,
            text="Iniciar Teste Agora",
            font=('Segoe UI', 13, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['secondary'],
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=40,
            pady=15,
            command=lambda: controller.show_frame("QuestionsPage")
        )
        start_btn.pack()
        
        # Efeito hover no botão
        start_btn.bind('<Enter>', lambda e: start_btn.config(bg=self.colors['secondary']))
        start_btn.bind('<Leave>', lambda e: start_btn.config(bg=self.colors['primary']))


class QuestionsPage(ttk.Frame):
    """
    Página de perguntas do sistema.
    Coleta informações do usuário através de um formulário interativo.
    """
    
    def __init__(self, parent, controller, colors):
        """
        Inicializa a página de perguntas.
        
        Args:
            parent: Widget pai
            controller: Controlador principal da aplicação
            colors: Dicionário com as cores do tema
        """
        super().__init__(parent)
        self.app_controller = controller
        self.colors = colors
        
        # Configura fundo
        self.configure(style='Main.TFrame')

        # Header fixo com título
        header = tk.Frame(self, bg=self.colors['primary'], height=100)
        header.pack(fill='x', side='top')
        
        header_title = tk.Label(
            header,
            text="📋 Questionário de Perfil",
            font=('Segoe UI', 20, 'bold'),
            fg='white',
            bg=self.colors['primary']
        )
        header_title.pack(pady=30)

        # Container principal para área de scroll
        main_container = tk.Frame(self, bg=self.colors['background'])
        main_container.pack(fill='both', expand=True, side='top')

        # Canvas para permitir scroll
        canvas = tk.Canvas(
            main_container,
            bg=self.colors['background'],
            highlightthickness=0
        )
        
        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(
            main_container,
            orient="vertical",
            command=canvas.yview
        )
        
        # Frame que conterá todo o conteúdo scrollável
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])

        # Atualiza região de scroll quando o conteúdo muda
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Cria janela no canvas para o frame scrollável
        canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Posiciona canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Habilita scroll com mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Centraliza o conteúdo horizontalmente
        def _center_window(event):
            canvas_width = event.width
            canvas.itemconfig(canvas.create_window((0, 0), window=scrollable_frame, anchor="n"), 
                            width=min(canvas_width, 900))
        canvas.bind('<Configure>', _center_window)

        # Dicionário para armazenar as variáveis das respostas
        self.vars = {}
        
        # Container para as perguntas com largura máxima e centralizado
        questions_container = tk.Frame(scrollable_frame, bg=self.colors['background'])
        questions_container.pack(fill='both', expand=True, padx=100, pady=20)

        # Define todas as perguntas do sistema
        perguntas = [
            ("moradia", "🏠 Qual o tipo de imóvel onde você mora?", 
             ["Casa", "Apartamento"],
             "Importante para determinar o espaço disponível"),
            
            ("tam_moradia", "📏 Qual o tamanho do seu imóvel?", 
             ["Grande", "Pequeno"],
             "Ajuda a identificar pets que se adaptam ao espaço"),
            
            ("area_moradia", "🌳 Seu imóvel possui área externa (quintal)?", 
             ["Sim", "Nao"],
             "Alguns pets precisam de espaço ao ar livre"),
            
            ("TempoPasseio", "⏰ Você tem tempo para passear com seu pet?", 
             ["Sim", "Nao"],
             "Essencial para cães que precisam de exercícios"),
            
            ("interacao", "💝 Você busca interação e carinho com seu pet?", 
             ["Sim", "Nao"],
             "Define o nível de sociabilidade do animal"),
            
            ("investimento", "💰 Qual seu orçamento para cuidados com o pet?", 
             ["Alto", "Medio", "Baixo"],
             "Considera custos de alimentação, saúde e manutenção")
        ]

        # Cria um card para cada pergunta
        for idx, (key, text, options, hint) in enumerate(perguntas, 1):
            # Card da pergunta com sombra suave
            card = tk.Frame(
                questions_container,
                bg=self.colors['card'],
                relief='solid',
                bd=1,
                highlightthickness=0
            )
            card.pack(fill='x', pady=12)
            card.configure(borderwidth=0)  # Remove bordas completamente
            
            # Container interno com padding
            card_content = tk.Frame(card, bg=self.colors['card'])
            card_content.pack(fill='both', padx=25, pady=20)
            
            # Número e texto da pergunta
            question_text = f"Pergunta {idx}: {text}"
            lbl = tk.Label(
                card_content,
                text=question_text,
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text_dark'],
                bg=self.colors['card'],
                anchor='w',
                justify='left'
            )
            lbl.pack(anchor='w', pady=(0, 5))
            
            # Dica/explicação da pergunta
            hint_lbl = tk.Label(
                card_content,
                text=hint,
                font=('Segoe UI', 9, 'italic'),
                fg=self.colors['text_light'],
                bg=self.colors['card'],
                anchor='w'
            )
            hint_lbl.pack(anchor='w', pady=(0, 15))

            # Variável para armazenar a resposta
            var = tk.StringVar(value=options[0])
            self.vars[key] = var

            # Frame para os botões de opção (horizontal)
            btn_frame = tk.Frame(card_content, bg=self.colors['card'])
            btn_frame.pack(anchor='w', pady=(5, 0))
            
            # Cria radiobuttons estilizados para cada opção
            for opt in options:
                rb = tk.Radiobutton(
                    btn_frame,
                    text=opt,
                    value=opt,
                    variable=var,
                    font=('Segoe UI', 11),
                    bg=self.colors['card'],
                    fg=self.colors['text_dark'],
                    activebackground=self.colors['card'],
                    activeforeground=self.colors['primary'],
                    selectcolor=self.colors['card'],
                    cursor='hand2',
                    relief='flat',
                    padx=15,
                    pady=8
                )
                rb.pack(side="left", padx=(0, 15))

        # Espaçador
        spacer = tk.Frame(questions_container, bg=self.colors['background'], height=30)
        spacer.pack()

        # Frame para botões de ação
        action_frame = tk.Frame(questions_container, bg=self.colors['background'])
        action_frame.pack(pady=20)
        
        # Botão para voltar
        back_btn = tk.Button(
            action_frame,
            text="← Voltar",
            font=('Segoe UI', 11),
            bg='white',
            fg=self.colors['text_dark'],
            activebackground='#F0F0F0',
            relief='flat',
            cursor='hand2',
            padx=25,
            pady=12,
            command=lambda: controller.show_frame("HomePage")
        )
        back_btn.pack(side='left', padx=10)
        
        # Efeito hover no botão voltar
        back_btn.bind('<Enter>', lambda e: back_btn.config(bg='#F0F0F0'))
        back_btn.bind('<Leave>', lambda e: back_btn.config(bg='white'))

        # Botão para concluir e ver resultados
        concluir_btn = tk.Button(
            action_frame,
            text="Ver Resultados →",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['success'],
            fg='white',
            activebackground=self.colors['primary'],
            relief='flat',
            cursor='hand2',
            padx=35,
            pady=12,
            command=self.on_conclude
        )
        concluir_btn.pack(side='left', padx=10)
        
        # Efeito hover no botão concluir
        concluir_btn.bind('<Enter>', lambda e: concluir_btn.config(bg=self.colors['primary']))
        concluir_btn.bind('<Leave>', lambda e: concluir_btn.config(bg=self.colors['success']))

    def on_conclude(self):
        """
        Valida as respostas e executa a inferência.
        Chamado quando o usuário clica em "Ver Resultados".
        """
        # Coleta todas as respostas em um dicionário de fatos
        facts = {k: v.get() for k, v in self.vars.items()}
        
        # Valida se todas as perguntas foram respondidas
        missing = [k for k, v in facts.items() if v is None or v == ""]
        
        if missing:
            # Exibe mensagem de erro se houver campos vazios
            tk.messagebox.showerror(
                "Atenção",
                "Por favor, responda todas as perguntas antes de continuar."
            )
            return
        
        # Executa inferência e mostra resultados
        self.app_controller.run_inference_and_show(facts)


class ResultPage(ttk.Frame):
    """
    Página de resultados do sistema.
    Exibe a recomendação principal, alternativas e explicações detalhadas.
    """
    
    def __init__(self, parent, controller, colors):
        """
        Inicializa a página de resultados.
        
        Args:
            parent: Widget pai
            controller: Controlador principal da aplicação
            colors: Dicionário com as cores do tema
        """
        super().__init__(parent)
        self.app_controller = controller
        self.colors = colors
        
        # Configura fundo
        self.configure(style='Main.TFrame')

        # Header fixo
        header = tk.Frame(self, bg=self.colors['success'], height=80)
        header.pack(fill='x', side='top')
        
        self.header_title = tk.Label(
            header,
            text="✨ Seu Pet Ideal",
            font=('Segoe UI', 20, 'bold'),
            fg='white',
            bg=self.colors['success']
        )
        self.header_title.pack(pady=25)

        # Container principal
        main_container = tk.Frame(self, bg=self.colors['background'])
        main_container.pack(fill='both', expand=True)

        # Canvas para scroll
        canvas = tk.Canvas(
            main_container,
            bg=self.colors['background'],
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Habilita scroll com mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Centraliza o conteúdo horizontalmente
        def _center_window(event):
            canvas_width = event.width
            canvas.itemconfig(canvas.create_window((0, 0), window=scrollable_frame, anchor="n"), 
                            width=min(canvas_width, 1000))
        canvas.bind('<Configure>', _center_window)

        # Container principal de conteúdo centralizado
        content = tk.Frame(scrollable_frame, bg=self.colors['background'])
        content.pack(fill='both', expand=True, padx=100, pady=20)

        # Card principal com a recomendação
        main_card = tk.Frame(content, bg=self.colors['card'], relief='flat', bd=0, highlightthickness=0)
        main_card.pack(fill='x', pady=(0, 20))

        # Label para o pet recomendado
        self.main_lbl = tk.Label(
            main_card,
            text="",
            font=('Segoe UI', 22, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['card']
        )
        self.main_lbl.pack(pady=(25, 10))

        # Canvas para imagem ilustrativa do pet
        self.canvas = tk.Canvas(
            main_card,
            width=280,
            height=200,
            bg=self.colors['background'],
            highlightthickness=0,
            relief='flat'
        )
        self.canvas.pack(pady=(10, 25))

        # Separator visual
        sep1 = tk.Frame(content, bg='#E0E0E0', height=2)
        sep1.pack(fill='x', pady=20)

        # Seção de alternativas
        self.alternatives_frame = tk.Frame(content, bg=self.colors['background'])
        self.alternatives_frame.pack(fill='x', pady=(0, 20))

        # Separator
        sep2 = tk.Frame(content, bg='#E0E0E0', height=2)
        sep2.pack(fill='x', pady=20)

        # Seção de explicação detalhada
        explanation_label = tk.Label(
            content,
            text="📊 Análise Detalhada",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['text_dark'],
            bg=self.colors['background'],
            anchor='w'
        )
        explanation_label.pack(anchor='w', pady=(0, 15))

        # Card de explicação
        explanation_card = tk.Frame(content, bg=self.colors['card'], relief='flat', bd=0, highlightthickness=0)
        explanation_card.pack(fill='both', expand=True, pady=(0, 20))

        # Text widget para explicação detalhada
        self.text = tk.Text(
            explanation_card,
            height=14,
            wrap="word",
            font=('Segoe UI', 10),
            bg=self.colors['card'],
            fg=self.colors['text_dark'],
            relief='flat',
            padx=20,
            pady=15,
            spacing1=5,
            spacing2=3,
            spacing3=5
        )
        self.text.pack(fill='both', expand=True, padx=5, pady=5)

        # Separator
        sep3 = tk.Frame(content, bg='#E0E0E0', height=2)
        sep3.pack(fill='x', pady=20)

        # Frame para botões de ação
        btn_frame = tk.Frame(content, bg=self.colors['background'])
        btn_frame.pack(pady=20)
        
        # Botão para refazer o teste
        retry_btn = tk.Button(
            btn_frame,
            text="🔄 Refazer Teste",
            font=('Segoe UI', 11),
            bg='white',
            fg=self.colors['text_dark'],
            activebackground='#F0F0F0',
            relief='flat',
            cursor='hand2',
            padx=25,
            pady=12,
            command=lambda: controller.show_frame("QuestionsPage")
        )
        retry_btn.pack(side="left", padx=10)
        
        retry_btn.bind('<Enter>', lambda e: retry_btn.config(bg='#F0F0F0'))
        retry_btn.bind('<Leave>', lambda e: retry_btn.config(bg='white'))
        
        # Botão para voltar ao início
        home_btn = tk.Button(
            btn_frame,
            text="🏠 Voltar ao Início",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['secondary'],
            relief='flat',
            cursor='hand2',
            padx=25,
            pady=12,
            command=lambda: controller.show_frame("HomePage")
        )
        home_btn.pack(side="left", padx=10)
        
        home_btn.bind('<Enter>', lambda e: home_btn.config(bg=self.colors['secondary']))
        home_btn.bind('<Leave>', lambda e: home_btn.config(bg=self.colors['primary']))

    def set_result(self, recomendacoes, regras_disparadas, explicacao, facts=None):
        """
        Define e exibe os resultados da inferência.
        
        Args:
            recomendacoes: Lista de pets recomendados (ordenada por prioridade)
            regras_disparadas: Lista de regras que foram ativadas
            explicacao: Texto explicativo completo
            facts: Dicionário com os fatos fornecidos pelo usuário
        """
        # Limpa alternativas anteriores
        for widget in self.alternatives_frame.winfo_children():
            widget.destroy()

        if recomendacoes:
            # Pet principal recomendado
            main = recomendacoes[0]
            self.main_lbl.config(text=f"🎯 {main}")
            
            # Desenha ilustração do pet
            self._draw_pet_illustration(main)
            
            # Exibe alternativas se houver mais de uma recomendação
            if len(recomendacoes) > 1:
                alt_title = tk.Label(
                    self.alternatives_frame,
                    text="🔄 Outras Opções Compatíveis",
                    font=('Segoe UI', 14, 'bold'),
                    fg=self.colors['text_dark'],
                    bg=self.colors['background'],
                    anchor='w'
                )
                alt_title.pack(anchor='w', pady=(0, 15))
                
                # Grid de alternativas
                alt_container = tk.Frame(self.alternatives_frame, bg=self.colors['background'])
                alt_container.pack(fill='x')
                
                for idx, pet in enumerate(recomendacoes[1:], start=1):
                    # Card para cada alternativa
                    alt_card = tk.Frame(
                        alt_container,
                        bg=self.colors['card'],
                        relief='flat',
                        bd=0,
                        highlightthickness=0
                    )
                    alt_card.pack(fill='x', pady=8)
                    
                    # Conteúdo do card
                    card_content = tk.Frame(alt_card, bg=self.colors['card'])
                    card_content.pack(fill='x', padx=20, pady=15)
                    
                    # Ícone e nome do pet
                    pet_icon = self._get_pet_emoji(pet)
                    pet_label = tk.Label(
                        card_content,
                        text=f"{pet_icon}  {pet}",
                        font=('Segoe UI', 12, 'bold'),
                        fg=self.colors['text_dark'],
                        bg=self.colors['card'],
                        anchor='w'
                    )
                    pet_label.pack(anchor='w')
                    
                    # Descrição
                    desc_label = tk.Label(
                        card_content,
                        text=f"Alternativa {idx} - Também compatível com seu perfil",
                        font=('Segoe UI', 9),
                        fg=self.colors['text_light'],
                        bg=self.colors['card'],
                        anchor='w'
                    )
                    desc_label.pack(anchor='w', pady=(5, 0))

        else:
            # Caso não haja recomendações
            self.main_lbl.config(text="❌ Nenhuma recomendação encontrada")
            self.canvas.delete("all")
            self.canvas.create_text(
                140, 100,
                text="😕",
                font=("Arial", 64),
                fill=self.colors['text_light']
            )

        # Insere explicação no text widget
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, explicacao)
        self.text.configure(state="disabled")

    def _draw_pet_illustration(self, pet):
        """
        Desenha uma ilustração visual do pet recomendado.
        
        Args:
            pet: Nome do pet a ser ilustrado
        """
        self.canvas.delete("all")
        pet_lower = pet.lower()
        
        # Define cores e forma baseado no tipo de pet
        if "cachorro" in pet_lower:
            # Círculo marrom para cachorro
            self.canvas.create_oval(
                40, 40, 240, 180,
                fill='#F4E4C1',
                outline='#D4A574',
                width=3
            )
            emoji = "🐶"
            bg_color = '#FFF8E7'
            
        elif "gato" in pet_lower:
            # Círculo laranja para gato
            self.canvas.create_oval(
                40, 40, 240, 180,
                fill='#FFE5D0',
                outline='#E89B6D',
                width=3
            )
            emoji = "🐱"
            bg_color = '#FFF5ED'
            
        elif "peixe" in pet_lower:
            # Retângulo azul para peixe (aquário)
            self.canvas.create_rectangle(
                40, 50, 240, 170,
                fill='#D6F0FF',
                outline='#6BB6D6',
                width=3
            )
            emoji = "🐟"
            bg_color = '#E8F8FF'
            
        elif "réptil" in pet_lower or "reptil" in pet_lower:
            # Retângulo verde para réptil
            self.canvas.create_rectangle(
                40, 50, 240, 170,
                fill='#E0F5E0',
                outline='#8FBC8F',
                width=3
            )
            emoji = "🦎"
            bg_color = '#F0FFF0'
            
        elif "pássaro" in pet_lower or "passaro" in pet_lower:
            # Círculo amarelo para pássaro
            self.canvas.create_oval(
                40, 40, 240, 180,
                fill='#FFF9D6',
                outline='#E6D05C',
                width=3
            )
            emoji = "🐦"
            bg_color = '#FFFEF0'
            
        elif "roedor" in pet_lower:
            # Círculo bege para roedor
            self.canvas.create_oval(
                40, 40, 240, 180,
                fill='#F5E6D3',
                outline='#C9A876',
                width=3
            )
            emoji = "🐹"
            bg_color = '#FFF8F0'
            
        elif "aracnídeo" in pet_lower or "aracnideo" in pet_lower:
            # Polígono escuro para aracnídeo
            self.canvas.create_rectangle(
                40, 50, 240, 170,
                fill='#E8E0D8',
                outline='#8B7355',
                width=3
            )
            emoji = "🕷️"
            bg_color = '#F5F0EB'
            
        else:
            # Default genérico
            self.canvas.create_oval(
                40, 40, 240, 180,
                fill='#F0F0F0',
                outline='#999999',
                width=3
            )
            emoji = "🐾"
            bg_color = '#F8F8F8'
        
        # Aplica cor de fundo
        self.canvas.configure(bg=bg_color)
        
        # Desenha emoji grande no centro
        self.canvas.create_text(
            140, 110,
            text=emoji,
            font=("Segoe UI Emoji", 72)
        )

    def _get_pet_emoji(self, pet):
        """
        Retorna o emoji correspondente ao tipo de pet.
        
        Args:
            pet: Nome do pet
            
        Returns:
            String com o emoji correspondente
        """
        pet_lower = pet.lower()
        
        if "cachorro" in pet_lower:
            return "🐶"
        elif "gato" in pet_lower:
            return "🐱"
        elif "peixe" in pet_lower:
            return "🐟"
        elif "réptil" in pet_lower or "reptil" in pet_lower:
            return "🦎"
        elif "pássaro" in pet_lower or "passaro" in pet_lower:
            return "🐦"
        elif "roedor" in pet_lower:
            return "🐹"
        elif "aracnídeo" in pet_lower or "aracnideo" in pet_lower:
            return "🕷️"
        else:
            return "🐾"


def start_app():
    """
    Função principal para iniciar a aplicação.
    Cria a janela raiz do Tkinter e inicializa a aplicação.
    """
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    start_app()