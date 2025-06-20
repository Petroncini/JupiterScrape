class Disciplina:
    def __init__(self, cod: str, nome: str, aula: int, trabalho: int, CH: int, CE: int, CP: int, ATPA: int):
        self.cod = str(cod) 
        self.nome = str(nome)
        self.aula = int(aula) 
        self.trabalho = int(trabalho)
        self.CH = int(CH) if CH is not None else 0
        self.CE = int(CE)  if CE is not None else 0
        self.CP = int(CP) if CP is not None else 0
        self.ATPA = int(ATPA) if ATPA is not None else 0
        # set pra não repetir o mesmo curso em perídos diferentes (integarl, matutino, etc)
        self.cursosComuns = set()


    def incluirCurso(self, cursoNome: str, unidadeNome: str):
        curso = self.nomeSemPeriodo(str(cursoNome))
        self.cursosComuns.add((str(unidadeNome), curso))


    def __str__(self):
        s = ""
        s += f"{self.cod} - {self.nome}\n"
        s += f"\tCréditos Aula: {self.aula}\n"
        s += f"\tCréditos Trabalho: {self.trabalho}\n"
        s += f"\tCarga Horária Total: {self.CH} h\n"
        if self.CE:
            s += f"\tCarga Horária de Estágio: {self.CE} h\n"
        if self.CP:
            s += f"\tCarga Horária de Práticas como Componentes Curriculares: {self.CP} h\n"
        if self.ATPA:
            s += f"\tAtividades Teórico-Práticas de Aprofundamento: {self.ATPA}\n"
        #s += "\n"

        return s
    
    # retorna string dos curso associados a disciplina
    def cursosAssociados(self):
        # if not self.cursosComuns:
        #     return "Disciplina não é obrigatória em nenhum curso\n"
        # #self.cursosComuns.sort()
        # s = "Cursos associados:\n"
        # for (unidade, curso) in self.cursosComuns:
        #     s += f"\t{curso} - {unidade}\n\n"
        listaNomes = []
        for (unidade, curso) in self.cursosComuns:
            listaNomes.append(f"{curso} - {unidade}")
        
        return listaNomes

    def nomeSemPeriodo(self, nomeCurso):
        return nomeCurso.split(" - ")[0].strip()
