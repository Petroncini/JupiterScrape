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

    def imprimirCurso(self):
        print(f"Unidade: {self.unidade}")
        print(f"Curso: {self.nome}")
        print("Duração")
        print(f"Ideal: {self.ideal}\tMínima: {self.min}\tMáxima: {self.max}")

        print("\nDisciplinas Obrigatórias\n")
        for disciplina in self.obrigatorias:
            disciplina.imprimir()

        if self.eletivas:
            print("\nDisciplinas Optativas Eletivas\n")
            for disciplina in self.eletivas:
                disciplina.imprimir()

        if self.livres: 
            print("\nDisciplinas Optativas Livres\n")
            for disciplina in self.obrigatorias:
                disciplina.imprimir()
