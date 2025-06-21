# Classe que representa uma disciplina
class Disciplina:
    def __init__(self, cod: str, nome: str, aula: int, trabalho: int, CH: int, CE: int, CP: int, ATPA: int):
        self.cod = str(cod) # Código
        self.nome = str(nome) # Nome
        self.aula = int(aula) # Créditos aula
        self.trabalho = int(trabalho) # Créditos trabalho
        self.CH = int(CH) if CH is not None else 0 # Carga horária
        self.CE = int(CE)  if CE is not None else 0 # Carga horária de estágio
        self.CP = int(CP) if CP is not None else 0 # Carga horária de Práticas como Componentes Curriculares
        self.ATPA = int(ATPA) if ATPA is not None else 0 # Atividades Teórico-Práticas de Aprofundamento
        # Set que guarda os cursos que contém essa disciplina, sem considerar o período (matutino, integral, etc)
        self.cursosComuns = set()

    # Inclui um curso no conjunto de cursos comuns
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

        return s
    
    # Retorna a lista dos nomes dos cursos associados à disciplina
    def cursosAssociados(self):
        listaNomes = []
        for (unidade, curso) in self.cursosComuns:
            listaNomes.append(f"{curso} - {unidade}")
        
        return listaNomes

    # Remove o período do nome do curso, que é separado por hífen
    def nomeSemPeriodo(self, nomeCurso):
        return nomeCurso.split(" - ")[0].strip()
