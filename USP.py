from Disciplina import Disciplina
from Unidade import Unidade
from unidecode import unidecode

# Classe que contém todas as informações coletadas do JupiterWeb e
# que realiza as consultas
class USP:
    def __init__(self):
        self.unidades = [] # lista de unidades da usp
        self._disciplinasPorCod = {} # Dicionário das disciplinas indexadas por código
        # Dicionário que relaciona um nome de disciplina a uma lista de códigos correspondentes
        self._codigosPorNome = {}

    # Adiciona disciplina na usp, a USP guarda disciplinas diretamente para operações de busca
    def adicionarDisciplina(self, disciplina: Disciplina):
        codigo = disciplina.cod
        nome = disciplina.nome

        # Adiciona a disciplina no dicionário
        # Cria a disciplina ou atualiza com os novos dados do scraper
        self._disciplinasPorCod[codigo] = disciplina

        # Verifica se o nome já existe no dicionário
        if nome not in self._codigosPorNome:
            self._codigosPorNome[nome] = []

        # Verifica se o codigo já está no dicionário
        if codigo not in self._codigosPorNome[nome]:
            self._codigosPorNome[nome].append(codigo)
        

    # Adiciona a  unidade na lista
    def adicionarUnidade(self, unidade):
        self.unidades.append(unidade)


    # Consulta 1: Lista o nome dos cursos da unidade especificada
    def listarCursosPorUnidade(self, nomeUnidade):
        # Coleta as unidades compatíveis com a entrada do usuário
        unidades = [u for u in self.unidades if unidecode(nomeUnidade.lower()) in unidecode(u.nome.lower())]
        if unidades:
            # Imprime os nomes das unidades encontradas
            nomes = ", ".join(u.nome for u in unidades)
            print(f"\nCursos oferecidos por {nomes}:\n")
            listaCursos = []
            for u in unidades:
                listaCursos += u.listarCursos()
            return listaCursos  # Retorna a lista de cursos
        else:
            print("\nUnidade não encontrada")


    # Consultas 2 e 3: Mostra os dados de um curso ou de todos
    def mostrarCursos(self, nomeCurso=None):
        cursoEncontrado = False
        listaCursos = []
        # Retorna todos os cursos
        if nomeCurso is None:
            cursoEncontrado = True
            for unidade in self.unidades:
                for curso in unidade.cursos:
                    listaCursos.append(curso)

        # Retorna os cursos cujos nomes contêm a substring nomeCurso       
        else:
            for unidade in self.unidades:
                # Ignora maiúsculas e acentos
                cursos = [c for c in unidade.cursos if unidecode(nomeCurso.lower()) in unidecode(c.nome.lower())]
                if cursos:
                    cursoEncontrado = True
                    for curso in cursos:
                        listaCursos.append(curso)

        if cursoEncontrado:
            print(f"Foram encontrados {len(listaCursos)} cursos:\n" if len(listaCursos) > 1 else "")
            return listaCursos
        else:
            print("Curso não encontrado")
                

    # Consulta 4: Retorna os resultados da busca por uma disciplina via nome ou código
    def mostrarDisciplina(self, disciplina):
        # Se for código
        if any(char.isdigit() for char in disciplina):
            codigo = disciplina
            d = self.buscarDisciplina(codigo)
            if d: # Retorna uma lista com o par (Disciplina, lista de nomes de cursos)
                return [(d, d.cursosAssociados())]
            else:
                print("Disciplina não encontrada")
        # Busca por nome
        else:
            disciplinas = self._buscarDisciplinaNome(disciplina)
            if disciplinas:
                listaDisc = []
                # Retorna uma lista com as disciplinas compatíveis com o nome e seus cursos
                for d in disciplinas:
                    listaDisc.append((d, d.cursosAssociados()))
                return listaDisc
            else:
                print("Disciplina não encontrada")
        

    # Busca disciplina por código
    def buscarDisciplina(self, codigo) -> Disciplina:
        return self._disciplinasPorCod.get(codigo)
    

    # Busca disciplina por nome
    def _buscarDisciplinaNome(self, nomeDisc) -> Disciplina:
        # Acessa a lista de códigos do dicionário
        codigos = self._codigosPorNome.get(nomeDisc)
        if codigos: # Retorna a lista de códigos
            return [self._disciplinasPorCod[cod] for cod in codigos]
        
        else: # Se não achou, busca sequencial por substring
            # Lista de nomes com a substring nomeDisc, ignora maiúscula e acento
            nomesCompativeis = [nome for nome in self._codigosPorNome if unidecode(nomeDisc.lower()) in unidecode(nome.lower())]
            if nomesCompativeis:
                # Pra cada nome, pega a lista de códigos do dicionário
                listasCodigos = [self._codigosPorNome[n] for n in nomesCompativeis]
                codigos = []
                for lista in listasCodigos:
                    codigos += [l for l in lista]
                # Retorna a lista de disciplinas relativa a cada código
                return [self._disciplinasPorCod[cod] for cod in codigos]
        return None

    # Consulta 5: lista as disciplinas presentes em mais de um curso, junto com a
    # lista de cursos que oferecem a disciplina
    def listarDisciplinasCompartilhadas(self):
        listaDiscCursos = []
        # Percorre as disciplinas verificando se ela está presente em mais de um curso
        for disciplina in self._disciplinasPorCod.values():
            if disciplina.cursosComuns and len(disciplina.cursosComuns) > 1:
                listaDiscCursos.append((f"{disciplina.cod} - {disciplina.nome}", disciplina.cursosAssociados()))
                
        return listaDiscCursos
