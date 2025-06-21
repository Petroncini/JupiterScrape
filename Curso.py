from Disciplina import Disciplina

# Classe que representa um curso
class Curso:
    def __init__(self, nome: str, unidade: str, ideal: int, minimo: int, maximo: int):
        self.nome = str(nome) # Nome do curso: str
        self.unidade = str(unidade) # Nome da unidade: str
        self.ideal = int(ideal) # Duração ideal
        self.min = int(minimo) # Duração mínima
        self.max = int(maximo) # Duração máxima
        self.obrigatorias = [] # Lista de disciplinas obrigatórias
        self.livres = [] # Lista de disciplinas optativas livres
        self.eletivas = [] # Lista de disciplinas optativas eletivas

    # Inclui uma disciplina em uma das listas do curso de acordo com o tipo fornecido
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
