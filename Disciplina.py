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

    def __str__(self):
        str = ""
        str += f"\t{self.cod} - {self.nome}\n"
        str += f"\tCréditos Aula: {self.aula}\n"
        str += f"\tCréditos Trabalho: {self.trabalho}\n"
        str += f"\tCarga Horária Total: {self.CH} h\n"
        if self.CE:
            str += f"\tCarga Horária de Estágio: {self.CH} h\n"
        if self.CP:
            str += f"\tCarga Horária de Práticas como Componentes Curriculares: {self.CP} h\n"
        if self.ATPA:
            str += f"\tAtividades Teórico-Práticas de Aprofundamento: {self.ATPA}\n"
        str += "\n"

        return str;
