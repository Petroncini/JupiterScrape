from Curso import Curso

class Unidade:
    def __init__(self, nome: str):
        # nome da unidade
        self.nome = nome
        # lista de curso
        self.cursos = []

    # lista cursos da unidade
    def listarCursos(self):
        if self.cursos:
            cursos = [self.nome]
            for curso in self.cursos:
                # print(curso.nome)
                cursos.append(curso.nome)
            cursos.append("")
            return cursos

            
    # adiciona curso
    def adicionarCurso(self, curso: Curso):
        self.cursos.append(curso)
