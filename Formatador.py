from Curso import Curso
from Disciplina import Disciplina

# Classe que formata os dados (cursos, disciplinas, pares, nomes)
# em estruturas adequadas para serem exibidas na interface
class Formatador:
    # Método principal que direciona para os métodos
    # específicos de acordo com o tipo do dado
    def estruturar(self, dados):
        # Se dados é lista de Disciplinas
        if isinstance(dados[0], Disciplina):
            return self.f_disciplinas(dados)
        # Se é lista de Cursos
        if isinstance(dados[0], Curso):
            return self.f_cursos(dados)
        # Se é lista de tuplas (Disciplina, x)
        if isinstance(dados[0][0], Disciplina):
            return self.f_discComCursos(dados)
        # Se é lista de tuplas
        if isinstance(dados[0], tuple):
            return self.f_listaDiscCursos(dados)
        # Se é lista de outro tipo de dado
        else:
            return self.f_lista(dados)

    # Trata uma lista de objetos Disciplina
    def f_disciplinas(self, disciplinas : list[Disciplina]):
        dados = []
        for disc in disciplinas:
            # Dados básicos
            disciplina = [
                (f"Disciplina:    {disc.cod} - {disc.nome}",),
                (f"Créditos Aula:    {disc.aula}",),
                (f"Créditos Trabalho:    {disc.trabalho}",),
                (f"Carga Horária Total:    {disc.CH} h",),
                (f"Carga Horária de Estágio:    {disc.CE} h",)
            ]
            # Exibe os dados específicos se existirem
            if disc.CP:
                disciplina += [(f"Carga Horária de Práticas como Componentes Curriculares:\t{disc.CP} h",)]
            if disc.ATPA:
                disciplina += [(f"Atividades Teórico-Práticas de Aprofundamento:\t{disc.ATPA}",)]
            dados.append(disciplina)
        
        return dados
    
    # Trata uma lista de pares (Disciplina, [nomes de cursos])
    def f_discComCursos(self, disciplinas):
        dados = []
        # Para cada par
        for (disc, cursos) in disciplinas:
            # Trata a disciplina
            d = self.f_disciplinas([disc])[0]
            if cursos:
                d.append(("Cursos associados:",))
                # Trata a correspondente lista de nomes de cursos 
                formCursos = self.f_lista([f"\t{c}" for c in cursos])
                for c in formCursos:
                    d += c
            dados.append(d)
        return dados
    
    # Trata uma lista de cursos
    def f_cursos(self, cursos : list[Curso]):
        dados = []
        for curso in cursos:
            # Informações do curso
            bloco = [
                (f"Unidade:\t{curso.unidade}",),
                (f"Curso:\t{curso.nome}",),
                (f"Duração\tIdeal: {curso.ideal}    Mínima: {curso.min}    Máxima: {curso.max}",),
                ("",),
                ("Disciplinas Obrigatórias",),
                ("",)
            ]
            # Inclui código e nome das obrigatórias
            disc = self.f_lista([f"{d.cod} - {d.nome}" for d in curso.obrigatorias])
            for d in disc:
                bloco.extend(d)

            bloco += [("",)]
            # Inclui eletivas se existirem
            if curso.eletivas:
                bloco += [("Disciplinas Optativas Eletivas",)]
                bloco += [("",)]
                disc = self.f_lista([f"{d.cod} - {d.nome}" for d in curso.eletivas])
                for d in disc:
                    bloco += d
                bloco += [("",)]
            # Inclui livres se existirem
            if curso.livres:
                bloco += [("Disciplinas Optativas Livres",)]
                bloco += [("",)]
                disc = self.f_lista([f"{d.cod} - {d.nome}" for d in curso.livres])
                for d in disc:
                    bloco += d
                bloco += [("",)]

            dados.append(bloco)

        return dados
    
    # Trata listas de pares (nome de disciplina, [nomes dos cursos que oferecem ela])
    def f_listaDiscCursos(self, lista):
        dados = []
        for (nome, cursos) in lista:
            # Separa uma coluna para o nome da disciplina
            bloco = [(nome, "")]
            # E a outra para listar os cursos
            bloco += [("", c) for c in cursos]
            bloco += [("", "")]
            dados.append(bloco)
        return dados
    
    # Trata uma lista de strings
    def f_lista(self, lista):
        dados = [[(nome,)] for nome in lista]
        return dados
    