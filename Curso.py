from Disciplina import Disciplina


class Curso:
    def __init__(self, nome, unidade, ideal, minimo, maximo):
        self.nome = nome
        self.unidade = unidade
        self.ideal = ideal
        self.min = minimo
        self.max = maximo
        self.obrigatorias = []
        self.livres = []
        self.eletivas = []

    def adicionarDisciplina(self, disciplina: Disciplina):
        if disciplina.tipo == "obrigatoria":
            self.obrigatorias.append(disciplina)
        elif disciplina.tipo == "Livre":
            self.livres.append(disciplina)
        else:
            self.eletivas.append(disciplina)
    



