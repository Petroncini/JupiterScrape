from Disciplina import Disciplina
from Unidade import Unidade
from unidecode import unidecode

# classe que contém todas as informações raspadas do Jupiter
class USP:
    def __init__(self):
        self.unidades = [] # unidades da usp
        self._disciplinasPorCod = {} # dicionário das disciplinas indexadas por código
        self._codigosPorNome = {} # dicionário de códigos indexados por nome, para busca

    # adiciona disciplina na usp, a USP guarda disciplinas diretamente para operações de busca de disciplinas
    def adicionarDisciplina(self, disciplina: Disciplina):
        codigo = disciplina.cod
        nome = disciplina.nome

        # adiciona disciplina
        # Se não existe, é criada
        # Se existe, adiciona a disicplina que foi atualizada no scraper
        self._disciplinasPorCod[codigo] = disciplina

        # verifica se nome já existe
        if nome not in self._codigosPorNome:
            self._codigosPorNome[nome] = []

        # Verifica se o codigo já está no dicionário
        if codigo not in self._codigosPorNome[nome]:
            self._codigosPorNome[nome].append(codigo)
        

    # adiciona unidade
    def adicionarUnidade(self, unidade):
        self.unidades.append(unidade)


    # Imprime o nome dos cursos da unidade especificada
    def listarCursosPorUnidade(self, nomeUnidade):
        unidades = [u for u in self.unidades if unidecode(nomeUnidade.lower()) in unidecode(u.nome.lower())]
        if unidades:
            nomes = ", ".join(u.nome for u in unidades)
            print(f"\nCursos oferecidos por {nomes}:\n")
            listaCursos = []
            for u in unidades:
                listaCursos += u.listarCursos()
            return listaCursos
        else:
            print("\nUnidade não encontrada")


    # Imprime os dados de um curso ou de todos
    def mostrarCursos(self, nomeCurso=None):
        cursoEncontrado = False
        listaCursos = []
        # Imprime os dados de todos os cursos
        if nomeCurso is None:
            cursoEncontrado = True
            for unidade in self.unidades:
                for curso in unidade.cursos:
                    listaCursos.append(curso)
                    # print()
                    # print(curso)

        # Imprime os dados dos cursos que contêm a substring nomeCurso       
        else:
            for unidade in self.unidades:
                # ignora case e acentos
                cursos = [c for c in unidade.cursos if unidecode(nomeCurso.lower()) in unidecode(c.nome.lower())]
                if cursos:
                    cursoEncontrado = True
                    for curso in cursos:
                        # print(curso)
                        listaCursos.append(curso)

        if cursoEncontrado:
            print(f"Foram encontrados {len(listaCursos)} cursos:\n" if len(listaCursos) > 1 else "")
            return listaCursos
        else:
            print("Curso não encontrado")
                

    # Imprime os resultados da busca por uma disciplina via nome ou código
    def mostrarDisciplina(self, disciplina):
        # Se for código
        if any(char.isdigit() for char in disciplina):
            codigo = disciplina
            d = self.buscarDisciplina(codigo)
            if d:
                # print(disciplina)
                # print(disciplina.cursosAssociados())
                # print("**********")
                return [(d, d.cursosAssociados())]
            else:
                print("Disciplina não encontrada")
        # Busca por nome
        else:
            disciplinas = self._buscarDisciplinaNome(disciplina)
            if disciplinas:
                listaDisc = []
                for d in disciplinas:
                    # print(d)
                    # print(d.cursosAssociados())
                    # print("**********")
                    listaDisc.append((d, d.cursosAssociados()))
                return listaDisc
            else:
                print("Disciplina não encontrada")
        

    # busca disciplina por código
    def buscarDisciplina(self, codigo) -> Disciplina:
        return self._disciplinasPorCod.get(codigo)
    

    # busca disciplina por nome
    def _buscarDisciplinaNome(self, nomeDisc) -> Disciplina:
        codigos = self._codigosPorNome.get(nomeDisc)
        if codigos:
            return [self._disciplinasPorCod[cod] for cod in codigos]
        else:
            # Lista de nomes com a substring nomeDisc, ignora caracter e acento
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
        listaDiscCursos = []
        for disciplina in self._disciplinasPorCod.values():
            if disciplina.cursosComuns and len(disciplina.cursosComuns) > 1:
                listaDiscCursos.append((f"{disciplina.cod} - {disciplina.nome}", disciplina.cursosAssociados()))
                # print(f"{disciplina.cod} - {disciplina.nome}")
                # print(disciplina.cursosAssociados())
                #print("**********")
        return listaDiscCursos

    def listarCursosComDisciplina(self, disciplinaNome: str):
        listaCursos = []
        for disciplina in self._buscarDisciplinaNome(disciplinaNome):
            print(disciplina.cursosAssociados())

