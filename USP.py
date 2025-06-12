class USP:
    def __init__(self):
        self.unidades = []
        self._disciplinas = set()

    def adicionaDisciplina(self, disciplina):
        if disciplina not in self.disciplinas:
            self._disciplinas.add(disciplina)
        
    def adicionaUnidade(self, unidade):
        self.unidades.append(unidade)
