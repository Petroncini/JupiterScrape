from Disciplina import Disciplina


class Curso:
    def __init__(self, nome: str, unidade: str, ideal: int, minimo: int, maximo: int):
        self.nome = str(nome) # Nome: str
        self.unidade = str(unidade) # unidade: str
        self.ideal = int(ideal)
        self.min = int(minimo)
        self.max = int(maximo)
        self.obrigatorias = [] # lista de disciplinas obrigatorias
        self.livres = [] # lista de disciplinas livres
        self.eletivas = [] # lista de disciplinas livres

    def adicionarDisciplina(self, disciplina: Disciplina, tipo):
        if tipo == "Obrigatória":
            self.obrigatorias.append(disciplina)
        elif tipo == "Livre":
            self.livres.append(disciplina)
        else:
            self.eletivas.append(disciplina)
    

    def __str__(self):
        s = ""
        s += f"Unidade: {self.unidade}\n"
        s += f"Curso: {self.nome}\n"
        s += "Duração\n"
        s += f"\tIdeal: {self.ideal}\tMínima: {self.min}\tMáxima: {self.max}\n"

        s += "\nDisciplinas Obrigatórias\n"
        for disciplina in self.obrigatorias:
            s += str(disciplina)

        if self.eletivas:
            s += "\nDisciplinas Optativas Eletivas\n"
            for disciplina in self.eletivas:
                s += str(disciplina)

        if self.livres: 
            s += "\nDisciplinas Optativas Livres\n"
            for disciplina in self.livres:
                s += str(disciplina)

        return s
