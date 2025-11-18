# GUI/main_window.py
import tkinter as tk
from tkinter import ttk
from GUI.controller import Controller

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SE_Pet — Recomendador de Pets")
        self.root.geometry("900x700")
        self.controller = Controller(root)

        # container frames (stack)
        self.container = ttk.Frame(root)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (HomePage, QuestionsPage, ResultPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")
        self.result_data = None

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def run_inference_and_show(self, facts):
        recs, regras, explicacao = self.controller.run_analysis(facts)
        # passar para ResultPage
        result_page: ResultPage = self.frames["ResultPage"]
        result_page.set_result(recs, regras, explicacao)
        self.show_frame("ResultPage")


class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.app_controller = controller

        title = ttk.Label(self, text="Descubra quem é seu Pet Ideal", font=("Arial", 22, "bold"))
        title.pack(pady=20)

        subtitle = ttk.Label(self, text="Responda às perguntas e o sistema recomendará o pet ideal.", wraplength=700)
        subtitle.pack(pady=10)

        start_btn = ttk.Button(self, text="Iniciar o Teste", command=lambda: controller.show_frame("QuestionsPage"))
        start_btn.pack(pady=30)


class QuestionsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.app_controller = controller

        # criar canvas para permitir scroll
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Perguntas (as 6 do seu teste)
        self.vars = {}

        perguntas = [
            ("moradia", "Qual o tipo de imóvel que você mora?", ["Casa", "Apartamento"]),
            ("tam_moradia", "Qual o Tamanho do imóvel?", ["Grande", "Pequeno"]),
            ("area_moradia", "O imóvel possui área externa, como quintal?", ["Sim", "Nao"]),
            ("TempoPasseio", "Você tem tempo para passeio?", ["Sim", "Nao"]),
            ("interacao", "Você tem necessidade de toque, atenção, carinho... (interação)?", ["Sim", "Nao"]),
            ("investimento", "O investimento que você pode ter para dar uma qualidade de vida é:", ["Alto", "Medio", "Baixo"])
        ]

        row = 0
        for key, text, options in perguntas:
            lbl = ttk.Label(scrollable_frame, text=text, wraplength=700)
            lbl.grid(row=row, column=0, pady=(12,4), padx=20, sticky="w")
            row += 1

            var = tk.StringVar(value=options[0])
            self.vars[key] = var

            # buttons as radiobuttons horizontally
            btn_frame = ttk.Frame(scrollable_frame)
            btn_frame.grid(row=row, column=0, padx=20, sticky="w")
            for opt in options:
                rb = ttk.Radiobutton(btn_frame, text=opt, value=opt, variable=var)
                rb.pack(side="left", padx=8, pady=6)
            row += 1

        # botão concluir
        concluir_btn = ttk.Button(scrollable_frame, text="Concluir", command=self.on_conclude)
        concluir_btn.grid(row=row, column=0, pady=24)

    def on_conclude(self):
        facts = {k: v.get() for k, v in self.vars.items()}
        # validar (garante valores)
        missing = [k for k, v in facts.items() if v is None or v == ""]
        if missing:
            tk.messagebox.showerror("Erro", f"Responda todas as perguntas: {missing}")
            return
        self.app_controller.run_inference_and_show(facts)


class ResultPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.app_controller = controller

        self.title_lbl = ttk.Label(self, text="Resultado", font=("Arial", 20, "bold"))
        self.title_lbl.pack(pady=12)

        self.main_lbl = ttk.Label(self, text="", font=("Arial", 16, "bold"))
        self.main_lbl.pack(pady=8)

        # imagem placeholder (canvas)
        self.canvas = tk.Canvas(self, width=240, height=180, bg="#e6f7f2", highlightthickness=0)
        self.canvas.pack(pady=10)

        # explanation text
        self.text = tk.Text(self, height=12, wrap="word")
        self.text.pack(fill="both", expand=True, pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=8)
        back_btn = ttk.Button(btn_frame, text="Refazer Teste", command=lambda: controller.show_frame("QuestionsPage"))
        back_btn.pack(side="left", padx=8)
        home_btn = ttk.Button(btn_frame, text="Voltar ao Início", command=lambda: controller.show_frame("HomePage"))
        home_btn.pack(side="left", padx=8)

    def set_result(self, recomendacoes, regras_disparadas, explicacao):
        if recomendacoes:
            main = recomendacoes[0]
            self.main_lbl.config(text=main)
            # desenhar imagem simbólica dependendo do pet (placeholder)
            self.canvas.delete("all")
            pet = main.lower()
            if "cachorro" in pet:
                self.canvas.create_oval(20, 20, 220, 160, fill="#f2d3b6", outline="#b5845f")
                self.canvas.create_text(120, 90, text="🐶", font=("Arial", 48))
            elif "gato" in pet:
                self.canvas.create_oval(20, 20, 220, 160, fill="#ffd6c2", outline="#d08a6a")
                self.canvas.create_text(120, 90, text="🐱", font=("Arial", 48))
            elif "peixe" in pet or "peixe" in main.lower():
                self.canvas.create_rectangle(20, 30, 220, 150, fill="#cfeef5", outline="#6fb7c9")
                self.canvas.create_text(120, 90, text="🐟", font=("Arial", 48))
            elif "réptil" in pet or "reptil" in pet:
                self.canvas.create_rectangle(20, 30, 220, 150, fill="#dff0d8", outline="#8fb28f")
                self.canvas.create_text(120, 90, text="🦎", font=("Arial", 48))
            elif "pássaro" in pet or "passaro" in pet:
                self.canvas.create_oval(20, 20, 220, 160, fill="#fff1c9", outline="#d6b65a")
                self.canvas.create_text(120, 90, text="🐦", font=("Arial", 48))
            else:
                self.canvas.create_text(120, 90, text="🙂", font=("Arial", 48))

        else:
            self.main_lbl.config(text="Nenhuma recomendação")
            self.canvas.delete("all")

        # inserir explicação no text widget
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, explicacao)
        self.text.configure(state="disabled")

def start_app():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    start_app()
