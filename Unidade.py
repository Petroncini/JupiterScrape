from Curso import Curso

class Unidade:
    def __init__(self, nome: str):
        self.nome = nome
        self.cursos = []

    def listarCursos(self):
        if self.cursos:
            cursos = [self.nome]
            for curso in self.cursos:
                # print(curso.nome)
                cursos.append(curso.nome)
            cursos.append("")
            return cursos

            
    def adicionarCurso(self, curso: Curso):
        self.cursos.append(curso)
