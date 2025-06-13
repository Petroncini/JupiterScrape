from Curso import Curso


class Unidade:
    def __init__(self, nome):
        self.nome = nome
        self.cursos = []

    def adicionarCurso(self, curso: Curso):
        self.cursos.append(curso)
