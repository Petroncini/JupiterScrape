class Disciplina:
    def __init__(self, cod, nome, aula, trabalho, CH, CE, CP, ATPA, tipo):
        self.cod = cod
        self.nome = nome
        self.aula = aula
        self.trabalho = trabalho
        self.CH = CH
        self.CE = CE
        self.CP = CP
        self.ATPA = ATPA
        self.tipo = tipo
        self.cursosComuns = []


    def incluirCurso(self, curso):
        self.cursosComuns.append((curso.unidade, curso.nome))


    def __str__(self):
        print(f"\t\t{self.cod} - {self.nome}")
        print(f"\tCréditos Aula: {self.aula}")
        print(f"\tCréditos Trabalho: {self.trabalho}")
        print(f"\tCarga Horária Total: {self.CH} h")
        if self.CE:
            print(f"\tCarga Horária de Estágio: {self.CH} h")
        if self.CP:
            print(f"\tCarga Horária de Práticas como Componentes Curriculares: {self.CP} h")
        if self.ATPA:
            print(f"\tAtividades Teórico-Práticas de Aprofundamento: {self.ATPA}")
        print()
    

    def cursosAssociados(self):
        self.cursosComuns.sort()
        string = "Cursos associados:\n\n"
        for (unidade, curso) in self.cursosComuns:
            string += (f"{curso} - {unidade}\n")

        return string
