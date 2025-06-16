from Scraper import Scraper 
from USP import USP
from Unidade import Unidade
from Curso import Curso 
from Disciplina import Disciplina
import sys

class Main:

    #@staticmethod
    def menuFuncionalidades():
        s = "\nMENU DE COMANDOS:\n\n"
        s += "\t1 : Listar os cursos de uma unidade\n"
        s += "\t2 : Mostrar os dados de um curso\n"
        s += "\t3 : Mostrar os dados de todos os cursos\n"
        s += "\t4 : Mostrar os dados de uma disciplina\n"
        s += "\t5 : Listar as disciplinas presentes em mais de um curso\n"
        s += "\tm : Exibir o menu de comandos\n"
        s += "\tq : Encerrar o programa\n"

        return s
    
    #@staticmethod
    def main():
        nroUnidades = int(sys.argv[1]) if len(sys.argv) > 1 else None
        print("\n***------------- Aguarde o carregamento das unidades -------------***\n")

        usp = USP()
        s = Scraper(usp, nroUnidades)
        s.acessarSite()
        s.navegarJupiter()

        print("\n***-------------------- Carregamento completo ---------------------***")
        menu = Main.menuFuncionalidades()
        print(menu)

        while True:
            comando = input("\nDigite um comando ou 'm' para ver as opções: ")
        
            match comando:
                # Lista de cursos por unidades
                case '1':
                    unidade = input("Insira o nome da unidade: ")
                    usp.listarCursosPorUnidade(unidade)
                # Dados de um determinado curso
                case '2':
                    curso = input("Insira o nome do curso: ")
                    print()
                    usp.mostrarCursos(curso)
                # Dados de todos os cursos 
                case '3':
                    usp.mostrarCursos()
                # Dados de uma disciplina
                case '4':
                    disciplina = input("Insira o nome ou código da disciplina: ")
                    print()
                    # Se for código
                    if any(char.isdigit() for char in disciplina):
                        usp.mostrarDisciplina(None, disciplina)
                    # Se for nome
                    else:
                        usp.mostrarDisciplina(disciplina)
                # Disciplinas que são usadas em mais de um curso
                case '5':
                    usp.listarDisciplinasCompartilhadas()
                # Imprime o menu de funcionalidades
                case 'm':
                    print(menu)
                # Encerra o programa
                case 'q':
                    print("Encerrando o programa...")
                    return
                #
                case _:
                    print("\nComando inválido, tente novamente ou digite 'm' para ver as opções.\n")


if __name__ == "__main__":
    Main.main()
                                                                                                                                              