from Curso import Curso

# Classe que representa uma unidade
class Unidade:
    def __init__(self, nome: str):
        self.nome = nome  # Nome da unidade
        self.cursos = [] # Lista de cursos oferecidos

    # Retorna a lista dos nomes dos cursos da unidade
    def listarCursos(self):
        if self.cursos:
            cursos = [self.nome]
            for curso in self.cursos:
                cursos.append(curso.nome)
            cursos.append("")
            return cursos

    # Adiciona um curso na unidade
    def adicionarCurso(self, curso: Curso):
        self.cursos.append(curso)
