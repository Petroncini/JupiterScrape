from Curso import Curso

class Unidade:
    def __init__(self, nome: str):
        self.nome = nome
        self.cursos = []

    def listarCursos(self):
        for curso in self.cursos:
            print(curso.nome)
            
    def adicionarCurso(self, curso: Curso):
        self.cursos.append(curso)
