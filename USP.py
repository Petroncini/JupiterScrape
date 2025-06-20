from Disciplina import Disciplina
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
        unidade = next((u for u in self.unidades if unidecode(nomeUnidade.lower()) in unidecode(u.nome.lower())), None)
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
                # ignora case e acentos
                cursos = [c for c in unidade.cursos if unidecode(nomeCurso.lower()) in unidecode(c.nome.lower())]
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
        for disciplina in self._disciplinasPorCod.values():
            if disciplina.cursosComuns and len(disciplina.cursosComuns) > 1:
                print(f"{disciplina.cod} - {disciplina.nome}")
                print(disciplina.cursosAssociados())
                #print("**********")

    def listarCursosComDisciplina(self, disciplinaNome: str):
        for disciplina in self._buscarDisciplinaNome(disciplinaNome):
            print(disciplina.cursosAssociados())

