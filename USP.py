class USP:
    def __init__(self):
        self.unidades = []
        self._disciplinas = set()

    def adicionaDisciplina(self, disciplina):
        if disciplina not in self._disciplinas:
            self._disciplinas.add(disciplina)
        
    def adicionaUnidade(self, unidade):
        self.unidades.append(unidade)

    # Imprime o nome dos cursos da unidade especificada
    def listarCursosPorUnidade(self, nomeUnidade):
        unidade = next((u for u in self.unidades if u.nome == nomeUnidade), None)
        if unidade is not None:
            unidade.listarCursos()

    # Imprime os dados de um curso ou de todos
    def mostrarCursos(self, nomeCurso=None):
        if nomeCurso is None:
            for unidade in self.unidades:
                for curso in unidade.cursos:
                    print(curso)
        else:
            for unidade in self.unidades:
                curso = next((c for c in unidade.cursos if c.nome == nomeCurso), None)
                if curso:
                    print(curso)
                    return
                
    # def mostrarDisciplina(self, nome=None, codigo=None):

