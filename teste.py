import tkinter as tk
from tkinter import ttk, font
import tkinter as tk
from Curso import Curso
from Disciplina import Disciplina


class Tabela:
    def __init__(self, janela, dados, titulo):
        self.dadosBrutos = dados  # Dados estruturados por bloco (curso, disciplina, etc.)
        self.dadosFormatados = self.formatarDados(dados)

        janela.title(titulo)
        janela.geometry("900x600")

        self.varBusca = tk.StringVar()

        frameBusca = tk.Frame(janela)
        frameBusca.pack(fill=tk.X)

        tk.Label(frameBusca, text="Buscar: ").pack(side=tk.LEFT, padx=5)
        entrada = tk.Entry(frameBusca, textvariable=self.varBusca)
        entrada.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        entrada.bind("<KeyRelease>", self.filtrar)

        self.tree = ttk.Treeview(janela, selectmode="extended", columns=("Campo", "Valor"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        scroll = ttk.Scrollbar(janela, orient="vertical", command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scroll.set)

        self.fonte = font.nametofont("TkDefaultFont")

        self.preencher(self.dadosFormatados)

        self.configurarCabecalho()


    def configurarCabecalho(self):
        self.tree.heading("Campo", text="Campo")
        self.tree.heading("Valor", text="Valor")
        self.tree.column("Campo", width=300, anchor="w")
        self.tree.column("Valor", width=550, anchor="w")


    def formatarDados(self, dados):
        """
        Cada elemento de dados é um bloco (ex.: um curso ou uma disciplina), que é uma lista de tuplas (campo, valor).
        """
        dadosFormatados = []
        for bloco in dados:
            dadosFormatados.append(bloco)
        return dadosFormatados


    def preencher(self, dados):
        self.tree.delete(*self.tree.get_children())
        for bloco in dados:
            for linha in bloco:
                self.tree.insert("", tk.END, values=linha)
            self.tree.insert("", tk.END, values=("", ""))  # Linha vazia separadora


    def filtrar(self, event=None):
        criterio = self.varBusca.get().lower()
        if not criterio:
            self.preencher(self.dadosFormatados)
            return

        dadosFiltrados = []

        for bloco in self.dadosBrutos:
            blocoTexto = " ".join(f"{campo} {valor}" for campo, valor in bloco).lower()
            if criterio in blocoTexto:
                dadosFiltrados.append(bloco)

        self.preencher(dadosFiltrados)


if __name__ == "__main__":
    janela = tk.Tk()

    # Example data
    d1 = Disciplina("MAC0110", "Intro Comp", "4", "2", "60", "0", "0", "0")
    d2 = Disciplina("MAT2450", "Calculus", "6", "0", "90", "0", "0", "0")

    curso = Curso("BCC", "ICMC", "10", "8", "20")
    curso.adicionarDisciplina(d1, "Obrigatória")
    curso.adicionarDisciplina(d2, "Livre")

    dados = [
        [
            ("Unidade", curso.unidade),
            ("Curso", curso.nome),
            ("Duração", f"Ideal: {curso.ideal}\tMínima: {curso.min}\t Máxima: {curso.max}"),
            ("", ""),
            ("Disciplinas Obrigatórias", ""),
            (f"{d1.cod} - {d1.nome}", f"Aula: {d1.aula} Trabalho: {d1.trabalho} CH: {d1.CH}")
        ],
        [
            ("Disciplina", f"{d2.cod} - {d2.nome}"),
            ("Créditos Aula", d2.aula),
            ("Créditos Trabalho", d2.trabalho),
            ("Carga Horária", d2.CH)
        ]
    ]

    tabela = Tabela(janela, dados, "Tabela de Cursos e Disciplinas")

    janela.mainloop()
