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
    
    def adicionar_disciplina (self, tipo, disciplina):
        if (tipo == "obrigatoria"):
            self.obrigatoria.append(disciplina)
        if (tipo == "livre"):
            self.livres.append(disciplina)
        if (tipo == "eletiva"):
            self.eletivas.append(disciplina)
              


