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
        s = ""
        s += f"\t{self.cod} - {self.nome}\n"
        s += f"\tCréditos Aula: {self.aula}\n"
        s += f"\tCréditos Trabalho: {self.trabalho}\n"
        s += f"\tCarga Horária Total: {self.CH} h\n"
        if self.CE:
            s += f"\tCarga Horária de Estágio: {self.CH} h\n"
        if self.CP:
            s += f"\tCarga Horária de Práticas como Componentes Curriculares: {self.CP} h\n"
        if self.ATPA:
            s += f"\tAtividades Teórico-Práticas de Aprofundamento: {self.ATPA}\n"
        s += "\n"

        return s
    
    def cursosAssociados(self):
        self.cursosComuns.sort()
        s = "Cursos associados:\n\n"
        for (unidade, curso) in self.cursosComuns:
            s += f"{curso} - {unidade}\n"
        
        return s
