class USP:
    def __init__(self):
        self.unidades = []
        self._disciplinas = set()

    def adicionaDisciplina(self, disciplina):
        if disciplina not in self.disciplinas:
            self._disciplinas.add(disciplina)
        
    def adicionaUnidade(self, unidade):
        self.unidades.append(unidade)

    # Imprime o nome dos cursos da unidade especificada
    def cursosPorUnidade(self, nomeUnidade):
        unidade = next((u for u in self.unidades if u.nome == nomeUnidade), None)
        if unidade is not None:
            unidade.imprimirCursos()

    def buscarCurso(self, nomeCurso):
        for unidade in self.unidades:
            curso = next((c for c in unidade.cursos if c.nome == nomeCurso), None)
        if curso is not None:
            curso.imprimirCurso()
