class USP:
    def __init__(self):
        self.unidades = []
        self._disciplinasPorCod = {}
        self._codigosPorNome = {}

    def adicionarDisciplina(self, disciplina):
        codigo = disciplina.cod
        nome = disciplina.nome

        self._disciplinasPorCod[codigo] = disciplina

        if nome not in self._codigosPorNome:
            self._codigosPorNome[nome] = []

        # Verifica se o codigo já está no dicionário
        if codigo not in self._codigosPorNome[nome]:
            self._codigosPorNome[nome].append(codigo)
        

    def adicionarUnidade(self, unidade):
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
                
    # Imprime os resultados da busca por uma disciplina via nome ou código
    def mostrarDisciplina(self, nome=None, codigo=None):
        # Busca por código
        if codigo:
            disciplina = self.buscarDisciplina(codigo)
            if disciplina:
                print(disciplina)
                print(disciplina.cursosAssociados())
                print("**********")
            else:
                print("Disciplina não encontrada")
        # Busca por nome
        elif nome:
            disciplinas = self._buscarDisciplinaNome(nome)
            if disciplinas:
                for d in disciplinas:
                    print(d)
                    print(d.cursosAssociados())
                    print("**********")
            else:
                print("Disciplina não encontrada")
        

    def buscarDisciplina(self, codigo):
        return self._disciplinasPorCod.get(codigo)
    

    def _buscarDisciplinaNome(self, nomeDisc):
        codigos = self._codigosPorNome.get(nomeDisc)
        if codigos:
            return [self._disciplinasPorCod[cod] for cod in codigos]
        return None

    def disciplinasCursos(self):
        for codigo, disciplina in self._disciplinasPorCod.items():
            if disciplina.cursosComuns and len(disciplina.cursosComuns) > 1:
                print(disciplina)
                print(disciplina.cursosAssociados())
                print("**********")
            

