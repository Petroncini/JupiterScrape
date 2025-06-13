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
        if disciplina.tipo == "obrigatoria":
            self.obrigatorias.append(disciplina)
        elif disciplina.tipo == "Livre":
            self.livres.append(disciplina)
        else:
            self.eletivas.append(disciplina)
    

    def __str__(self):
        print(f"Unidade: {self.unidade}")
        print(f"Curso: {self.nome}")
        print("Duração")
        print(f"\tIdeal: {self.ideal}\tMínima: {self.min}\tMáxima: {self.max}")

        print("\nDisciplinas Obrigatórias\n")
        for disciplina in self.obrigatorias:
            disciplina.imprimir()
            print()

        if self.eletivas:
            print("\nDisciplinas Optativas Eletivas\n")
            for disciplina in self.eletivas:
                disciplina.imprimir()
                print()

        if self.livres: 
            print("\nDisciplinas Optativas Livres\n")
            for disciplina in self.obrigatorias:
                disciplina.imprimir()
                print()
