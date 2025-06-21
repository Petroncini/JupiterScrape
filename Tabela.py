import tkinter as tk
from tkinter import ttk

# Classe que configura e controla a janela de interface visual
class Tabela:
    def __init__(self, janela, dados, colunas, titulo):
        # Dados da tabela e configurações
        self.dados = dados # Dados separados em blocos
        self.colunas = colunas
        janela.title(titulo)
        janela.geometry("1400x600")

        # Variável para filtrar
        self.varBusca = tk.StringVar()
        # Cria a barra de busca no topo da janela
        campoBusca = tk.Frame(janela)
        campoBusca.pack(fill=tk.X)
        tk.Label(campoBusca, text="Buscar: ").pack(side=tk.LEFT, padx=5)

        # Campo de entrada do usuário
        entrada = tk.Entry(campoBusca, textvariable=self.varBusca) # Guarda a entrada em varBusca
        entrada.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Filtra a busca a cada tecla digitada
        entrada.bind("<KeyRelease>", self.filtrar)

        # Cria o campo para a tabela
        frameTabela = tk.Frame(janela)
        frameTabela.pack(fill=tk.BOTH, expand=True)

        # Cria a tabela (Treeview) com as colunas especificadas
        self.tree = ttk.Treeview(frameTabela, selectmode="extended", columns=self.colunas, show="headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Barra para scroll vertical
        scroll = ttk.Scrollbar(frameTabela, orient="vertical", command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        # Adiciona a barra na tabela
        self.tree.configure(yscrollcommand=scroll.set)

        self.preencher(self.dados) # Mostra os dados fonecidos na tabela

        self.configurarCabecalho() # Ajusta o cabeçalho conforme as colunas
        # Permite fechar a janela com ESC
        janela.bind("<Escape>", lambda e: janela.destroy())


    # Ajusta o tamanho das colunas de acordo com a quantidade
    def configurarCabecalho(self):
        for i, coluna in enumerate(self.colunas):
            self.tree.heading(coluna, text=coluna)
            if i == 1:
                self.tree.column(coluna, width=850, stretch=False)
            else:
                self.tree.column(coluna, stretch=True)

        self.tree.update_idletasks()


    # Exibe os dados na tabela
    def preencher(self, dados):
        self.tree.delete(*self.tree.get_children()) # Limpa a tabela
        # Insere os dados por blocos
        for bloco in dados:
            for linha in bloco:
                self.tree.insert("", tk.END, values=linha)
            # Linha separadora entre os blocos
            if len(self.colunas) == 1:
                self.tree.insert("", tk.END, values=("",))
            else:
                self.tree.insert("", tk.END, values=("", "") )


    # Extrai o texto de um bloco para filtrar na busca
    def extrairTexto(self, bloco):
        texto = []
        # Trata blocos de listas, tuplas e elementos únicos
        for linha in bloco:
            if isinstance(linha, (list, tuple)):
                for item in linha:
                    if item is not None:
                        texto.append(str(item))
            else:
                if linha is not None:
                    texto.append(str(linha))
        
        return " ".join(texto).lower()

    # Filtra o conteúdo da tabela com base na variável de busca
    def filtrar(self, event=None):
        criterio = self.varBusca.get().lower().strip()
        # Se o campo de busca está vazio, mostra tudo
        if not criterio:
            self.preencher(self.dados)
            return

        dadosFiltrados = []
        # Para cada bloco, extrai o texto e verifica se  o bloco contém
        # os critérios digitados
        for bloco in self.dados:
            bloco_texto = self.extrairTexto(bloco)
            # Se tem, inclui o bloco nos dados filtrados
            if criterio in bloco_texto:
                dadosFiltrados.append(bloco)
        # Mostra na tabela os blocos que contêm os critérios
        self.preencher(dadosFiltrados)
