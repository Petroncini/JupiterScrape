from Scraper import Scraper 
from USP import USP
from Unidade import Unidade
from Curso import Curso 
from Disciplina import Disciplina
import sys

class Main:

    def main():
        nroUnidades = int(sys.argv[1]) if len(sys.argv) > 1 else None
        usp = USP()
        s = Scraper(usp, nroUnidades)
        s.acessarSite()
        s.navegarJupiter()
        while True:
            try:
                comando = int(input())
            except ValueError:
                print("\nEntrada inválida! Digite um número.\n")
                continue
        
            match comando:
                case 1: # Lista de cursos por unidades
                    unidade = input()
                    usp.listarCursosPorUnidade(unidade)
                case 2: # Dados de um determinado curso
                    curso = input()
                    usp.mostrarCursos(curso)
                case 3: # Dados de todos os cursos 
                    usp.mostrarCursos()
                case 4: # Dados de uma disciplina
                    disciplina = input()
                    # Se for código
                    if any(char.isdigit() for char in disciplina):
                        usp.mostrarDisciplina(None, disciplina)
                    # Se for nome
                    else:
                        usp.mostrarDisciplina(disciplina, None)
                case 5: # Disciplinas que são usadas em mais de um curso
                    usp.disciplinasCursos()
                case -1:
                    break
                case _:
                    print("\nCódigo Inválido!\n")



    if __name__ == "__main__":
        main()
                                                                                                                                              