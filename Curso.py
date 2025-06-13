from Disciplina import Disciplina


class Curso:
    def __init__(self, nome, unidade, ideal, minimo, maximo):
        self.nome = nome
        self.unidade = unidade
        self.ideal = ideal
        self.min = minimo
        self.max = maximo
        self.obrigatorias = []
        self.livres = []
        self.eletivas = []

    def adicionarDisciplina(self, disciplina: Disciplina):
        if disciplina.tipo == "Obrigatória":
            self.obrigatorias.append(disciplina)
        elif disciplina.tipo == "Livre":
            self.livres.append(disciplina)
        else:
            self.eletivas.append(disciplina)
    

    def __str__(self):
        string = ""
        string += (f"Unidade: {self.unidade}\n")
        string += (f"Curso: {self.nome}\n")
        string += ("Duração\n")
        string += (f"\tIdeal: {self.ideal}\tMínima: {self.min}\tMáxima: {self.max}\n")

        string += ("\nDisciplinas Obrigatórias\n")
        for disciplina in self.obrigatorias:
            string += (f"\t{disciplina.cod} - {disciplina.nome}\n")

        if self.eletivas:
            string += ("\nDisciplinas Optativas Eletivas\n")
            for disciplina in self.eletivas:
                string += (f"\t{disciplina.cod} - {disciplina.nome}\n")

        if self.livres: 
            string += ("\nDisciplinas Optativas Livres\n")
            for disciplina in self.obrigatorias:
                string += (f"\t{disciplina.cod} - {disciplina.nome}\n")
        return string
