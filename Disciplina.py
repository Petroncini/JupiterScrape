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

    def imprimir(self):
        print(f"Disciplina: {self.cod} - {self.nome}\n")
        print(f"Créditos Aula: {self.aula}")
        print(f"Créditos Trabalho: {self.trabalho}")
        print(f"Carga Horária Total: {self.CH} h")
        print(f"Carga Horária de Estágio: {self.CH}{' h' if self.CH else ''}")
        print(f"Carga Horária de Práticas como Componentes Curriculares: {self.CP or ""}{' h' if self.CP else ''}")
        print(f"Atividades Teórico-Práticas de Aprofundamento: {self.ATPA or ''}")
