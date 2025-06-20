from Disciplina import Disciplina
from Curso import Curso
import USP
import tkinter as tk
from tkinter import ttk, font

class Tabela:
    def __init__(self, janela, dados, colunas, titulo):
        self.dados = dados
        janela.title(titulo)
        janela.geometry("900x600")

        self.varBusca = tk.StringVar()

        frameBusca = tk.Frame(janela)
        frameBusca.pack(fill=tk.X)

        tk.Label(frameBusca, text="Buscar: ").pack(side=tk.LEFT, padx=5)
        entrada = tk.Entry(frameBusca, textvariable=self.varBusca)
        entrada.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        entrada.bind("<KeyRelease>", self.filtrar)

        self.tree = ttk.Treeview(janela, selectmode="extended", columns=colunas, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        scroll = ttk.Scrollbar(janela, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)

        style = ttk.Style()
        self.fonte = font.nametofont(style.lookup("Treeview", "font"))

        self.preencher(dados)


    def preencher(self, dados):
        self.tree.delete(*self.tree.get_children())
        for linha in dados:
            self.tree.insert("", tk.END, values=linha)

    def filtrar(self, event=None):
        criterio = self.varBusca.get().lower()
        filtrado = [
            linha for linha in self.dados
            if any(criterio in str(campo).lower() for campo in linha)
        ]
        self.preencher(filtrado)

class Formatador:
    def estruturar(self, dado):
        if isinstance(dado, Disciplina):
            return self.fDisciplina(dado)
        if isinstance(dado, Curso):
            return self.fCurso(dado)
        
    def larguras(self, dado):
        if isinstance(dado, Disciplina):
            return self.lDisciplina(dado)
        if isinstance(dado, Curso):
            return self.lCurso(dado)   
      
    def fDisciplina(self, disc):
        disciplina = [
            ("Disciplina:", f"{disc.cod} - {disc.nome}"),
            ("Créditos Aula:", disc.aula),
            ("Créditos Trabalho:", disc.trabalho),
            ("Carga Horária Total:", f"{disc.CH} h"),
            ("Carga Horária de Estágio:", f"{disc.CE} h")
        ]
        if disc.CP:
            disciplina += [("Carga Horária de Práticas como Componentes Curriculares: ", f"{disc.CP} h")]
        if disc.ATPA:
            disciplina += [("Atividades Teórico-Práticas de Aprofundamento: ", disc.ATPA)]
        
        return disciplina
    
    def fCurso(self, curso):
        c = [
            ("Unidade:", curso.unidade),
            ("Curso:", curso.nome),
            ("Duração", f"Ideal: {curso.ideal}    Mínima: {curso.min}    Máxima: {curso.max}"),
            ("",""),
            ("Disciplinas Obrigatórias", "")
        ]
        for d in curso.obrigatorias:
            c += self.fDisciplina(d)
        c += [("","")]
        if curso.eletivas:
            c += [("Disciplinas Optativas Eletivas", "")]
            for d in curso.eletivas:
                c += self.fDisciplina(d)
            c += [("","")]
        if curso.livres:
            c += [("Disciplinas Optativas Livres", "")]
            for d in curso.livres:
                c += self.fDisciplina(d)
        
        return c
    
    def lCurso():
        return
    def lDisciplina():
        return

        

    # def fCurso(self, curso):

    # def colunas(self, dados):
    #     # se é disciplina
    #     col = []


class TabelaDisciplinas(Tabela) :
    def __init__(self, janela, dados, titulo):
        self.colunas = ["",""]
        super().__init__(janela, dados, self.colunas, titulo)

        maxLargura = 0
        for label, dado in dados:
            largura = self.fonte.measure(label)
            maxLargura = max(largura, maxLargura)

        for i, coluna in enumerate(self.colunas):
            self.tree.heading(coluna, text=coluna)
            if i == 1:
                self.tree.column(coluna, width=2060, stretch=False)
            else:
                self.tree.column(coluna, stretch=True)

        self.tree.update_idletasks()

    def update_filter(self, event=None):
        criterio = self.varBusca.get().lower()
        
        filtrado = [
            linha for linha in self.dados
            if any(criterio in str(campo).lower() for campo in linha)
        ]
        self.preencher(filtrado)

# Example usage:
if __name__ == "__main__":
    disciplinas = [
        ("MAC0110", "Introdução à Computação", "60h"),
        ("MAT2450", "Cálculo I", "90h"),
        ("FIS1234", "Física Mecânica", "75h"),
        ("HST5678", "História Moderna", "45h"), ("MAC0110", "Introdução à Computação", "60h"),
        ("MAT2450", "Cálculo I", "90h"),
        ("FIS1234", "Física Mecânica", "75h"),
        ("HST5678", "História Moderna", "45h"), ("MAC0110", "Introdução à Computação", "60h"),
        ("MAT2450", "Cálculo I", "90h"),
        ("FIS1234", "Física Mecânica", "75h"),
        ("HST5678", "História Moderna", "45h"), ("MAC0110", "Introdução à Computação", "60h"),
        ("MAT2450", "Cálculo I", "90h"),
        ("FIS1234", "Física Mecânica", "75h"),
        ("HST5678", "História Moderna", "45h"), ("MAC0110", "Introdução à Computação", "60h"),
        ("MAT2450", "Cálculo I", "90h"),
        ("FIS1234", "Física Mecânica", "75h"),
        ("HST5678", "História Moderna", "45h"), ("MAC0110", "Introdução à Computação", "60h"),
        ("MAT2450", "Cálculo I", "90h"),
        ("FIS1234", "Física Mecânica", "75h"),
        ("HST5678", "História Moderna", "45h"), ("MAC0110", "Introdução à Computação", "60h"),
        ("MAT2450", "Cálculo I", "90h"),
        ("FIS1234", "Física Mecânica", "75h"),
        ("HST5678", "História Moderna", "45h"), ("MAC0110", "Introdução à Computação", "60h"),
        ("MAT2450", "Cálculo I", "90h"),
        ("FIS1234", "Física Mecânica", "75h"),
        ("HST5678", "História Moderna", "45h"), ("MAC0110", "Introdução à Computação", "60h"),
        ("MAT2450", "Cálculo I", "90h"),
        ("FIS1234", "Física Mecânica", "75h"),
        ("HST5678", "História Moderna", "45h"), ("MAC0110", "Introdução à Computação", "60h"),
        ("MAT2450", "Cálculo I", "90h"),
        ("FIS1234", "Física Mecânica", "75h"),
        ("HST5678", "História Moderna", "45h")
    ]

    f = Formatador()
    d = Disciplina("SCC201", "Algoritmos e Estruturas de Dados I", "4", "2", "40", "0", "0", "0")
    disciplina = f.estruturar(d)
    bcc = Curso("BCC", "ICMC", "10", "8", "20")
    bcc.adicionarDisciplina(d, "Obrigatória")
    curso = f.estruturar(bcc)
    #cursoLarguras = f.larguras(bcc)
    janela = tk.Tk()
    #tabela = Tabela(janela, curso, colunas=["",""], titulo="Disciplinas")
    tabela = TabelaDisciplinas(janela, curso, "Disciplinas")
    janela.mainloop()
