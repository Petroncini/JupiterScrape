from Curso import Curso


class Unidade:
    def __init__(self, nome):
        self.nome = nome
        self.cursos = []

    def imprimirCursos(self):
        for curso in self.cursos:
            print(curso.nome)
            
    def adicionarCurso(self, curso: Curso):
        self.cursos.append(curso)
