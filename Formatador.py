from Curso import Curso
from Disciplina import Disciplina

class Formatador:
    def estruturar(self, dados):
        if isinstance(dados[0], Disciplina):
            return self.f_disciplinas(dados)
        if isinstance(dados[0], Curso):
            return self.f_cursos(dados)
        if isinstance(dados[0][0], Disciplina):
            return self.f_discComCursos(dados)
        if isinstance(dados[0], tuple):
            return self.f_listaDiscCursos(dados)
        else:
            return self.f_lista(dados)

      
    def f_disciplinas(self, disciplinas):
        dados = []
        for disc in disciplinas:
            disciplina = [
                (f"Disciplina:    {disc.cod} - {disc.nome}",),
                (f"Créditos Aula:    {disc.aula}",),
                (f"Créditos Trabalho:    {disc.trabalho}",),
                (f"Carga Horária Total:    {disc.CH} h",),
                (f"Carga Horária de Estágio:    {disc.CE} h",)
            ]
            if disc.CP:
                disciplina += [(f"Carga Horária de Práticas como Componentes Curriculares:\t{disc.CP} h",)]
            if disc.ATPA:
                disciplina += [(f"Atividades Teórico-Práticas de Aprofundamento:\t{disc.ATPA}",)]
            dados.append(disciplina)
        
        return dados
    
    def f_discComCursos(self, disciplinas):
        dados = []
        for (disc, cursos) in disciplinas:
            d = self.f_disciplinas([disc])[0]
            if cursos:
                d.append(("Cursos associados:",))
                formCursos = self.f_lista([f"\t{c}" for c in cursos])
                for c in formCursos:
                    d += c
            dados.append(d)
        return dados
    
    def f_cursos(self, cursos):
        dados = []
        for curso in cursos:
            bloco = [
                (f"Unidade:\t{curso.unidade}",),
                (f"Curso:\t{curso.nome}",),
                (f"Duração\tIdeal: {curso.ideal}    Mínima: {curso.min}    Máxima: {curso.max}",),
                ("",),
                ("Disciplinas Obrigatórias",),
                ("",)
            ]
            disc = self.f_lista([f"{d.cod} - {d.nome}" for d in curso.obrigatorias])
            for d in disc:
                bloco.extend(d)

            bloco += [("",)]

            if curso.eletivas:
                bloco += [("Disciplinas Optativas Eletivas",)]
                bloco += [("",)]
                disc = self.f_lista([f"{d.cod} - {d.nome}" for d in curso.eletivas])
                for d in disc:
                    bloco += d
                bloco += [("",)]

            if curso.livres:
                bloco += [("Disciplinas Optativas Livres",)]
                bloco += [("",)]
                disc = self.f_lista([f"{d.cod} - {d.nome}" for d in curso.livres])
                for d in disc:
                    bloco += d
                bloco += [("",)]

            dados.append(bloco)

        return dados
    
    def f_listaDiscCursos(self, lista):
        dados = []
        for (nome, cursos) in lista:
            bloco = [(nome, "")]
            bloco += [("", c) for c in cursos]
            bloco += [("", "")]
            dados.append(bloco)
        return dados
    
    def f_lista(self, lista):
        dados = [[(nome,)] for nome in lista]
        return dados
    