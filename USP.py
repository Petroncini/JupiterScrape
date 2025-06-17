from Disciplina import Disciplina
from unidecode import unidecode

class USP:
    def __init__(self):
        self.unidades = []
        self._disciplinasPorCod = {}
        self._codigosPorNome = {}

    def adicionarDisciplina(self, disciplina: Disciplina):
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
        unidade = next((u for u in self.unidades if nomeUnidade in u.nome), None)
        if unidade is not None:
            print(f"\nCursos oferecidos por {unidade.nome}:\n")
            unidade.listarCursos()
        else:
            print("Unidade não encontrada")


    # Imprime os dados de um curso ou de todos
    def mostrarCursos(self, nomeCurso=None):
        cursoEncontrado = False
        # Imprime os dados de todos os cursos
        if nomeCurso is None:
            cursoEncontrado = True
            for unidade in self.unidades:
                for curso in unidade.cursos:
                    print()
                    print(curso)
        # Imprime os dados dos cursos que contêm a substring nomeCurso       
        else:
            for unidade in self.unidades:
                cursos = [c for c in unidade.cursos if nomeCurso in c.nome]
                if cursos:
                    cursoEncontrado = True
                    print(f"Foram encontrados {len(cursos)} cursos:\n" if len(cursos) > 1 else "")
                    for curso in cursos:
                        print(curso)
        if not cursoEncontrado:
            print("Curso não encontrado")
                

    # Imprime os resultados da busca por uma disciplina via nome ou código
    def mostrarDisciplina(self, nome=None, codigo=None):
        print()
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
        

    def buscarDisciplina(self, codigo) -> Disciplina:
        return self._disciplinasPorCod.get(codigo)
    

    def _buscarDisciplinaNome(self, nomeDisc) -> Disciplina:
        codigos = self._codigosPorNome.get(nomeDisc)
        if codigos:
            return [self._disciplinasPorCod[cod] for cod in codigos]
        else:
            # Lista de nomes com a substring nomeDisc
            nomesCompativeis = [nome for nome in self._codigosPorNome if unidecode(nomeDisc.lower()) in unidecode(nome.lower())]
            if nomesCompativeis:
                # Pra cada nome, pega a lista de códigos
                listasCodigos = [self._codigosPorNome[n] for n in nomesCompativeis]
                codigos = []
                for lista in listasCodigos:
                    codigos += [l for l in lista]
                # Retorna a lista de disciplinas relativa a cada código
                return [self._disciplinasPorCod[cod] for cod in codigos]
        return None

    def listarDisciplinasCompartilhadas(self):
        for disciplina in self._disciplinasPorCod.values():
            if disciplina.cursosComuns and len(disciplina.cursosComuns) > 1:
                print(f"{disciplina.cod} - {disciplina.nome}")
                print(disciplina.cursosAssociados())
                #print("**********")

    def listarCursosComDisciplina(self, disciplinaNome: str):
        for disciplina in self._buscarDisciplinaNome(disciplinaNome):
            print(disciplina.cursosAssociados())

