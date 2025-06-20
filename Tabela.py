import tkinter as tk
from tkinter import ttk, font
import tkinter as tk


class Tabela:
    def __init__(self, janela, dados, colunas, titulo):
        self.dados = dados
        self.colunas = colunas
        janela.title(titulo)
        janela.geometry("1400x600")

        self.varBusca = tk.StringVar()

        frameBusca = tk.Frame(janela)
        frameBusca.pack(fill=tk.X)

        tk.Label(frameBusca, text="Buscar: ").pack(side=tk.LEFT, padx=5)
        entrada = tk.Entry(frameBusca, textvariable=self.varBusca)
        entrada.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        entrada.bind("<KeyRelease>", self.filtrar)

        self.tree = ttk.Treeview(janela, selectmode="extended", columns=self.colunas, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        scroll = ttk.Scrollbar(janela, orient="vertical", command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scroll.set)

        self.fonte = font.nametofont("TkDefaultFont")

        self.preencher(self.dados)

        self.configurarCabecalho()

        janela.bind("<Escape>", lambda e: janela.destroy())



    def configurarCabecalho(self):
        for i, coluna in enumerate(self.colunas):
            self.tree.heading(coluna, text=coluna)
            if i == 1:
                self.tree.column(coluna, width=850, stretch=False)
            else:
                self.tree.column(coluna, stretch=True)

        self.tree.update_idletasks()



    def preencher(self, dados):
        self.tree.delete(*self.tree.get_children())
        for bloco in dados:
            for linha in bloco:
                self.tree.insert("", tk.END, values=linha)
            if len(self.colunas) == 1:
                self.tree.insert("", tk.END, values=("",))
            else:
                self.tree.insert("", tk.END, values=("", "") )


    def extrair_texto_do_bloco(self, bloco):
        texto_completo = []
        
        for linha in bloco:
            if isinstance(linha, (list, tuple)):
                for item in linha:
                    if item is not None:
                        texto_completo.append(str(item))
            else:
                if linha is not None:
                    texto_completo.append(str(linha))
        
        return " ".join(texto_completo).lower()

    def filtrar(self, event=None):
        criterio = self.varBusca.get().lower().strip()
        if not criterio:
            self.preencher(self.dados)
            return

        dadosFiltrados = []

        for bloco in self.dados:
            bloco_texto = self.extrair_texto_do_bloco(bloco)
            
            if criterio in bloco_texto:
                dadosFiltrados.append(bloco)

        self.preencher(dadosFiltrados)
