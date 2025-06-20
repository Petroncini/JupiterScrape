from Scraper import Scraper 
from USP import USP
from Formatador import Formatador
from Tabela import Tabela
import sys
import tkinter as tk
from tkinter import ttk
import os.path
import dill as pickle

class Main:

    def menuFuncionalidades(self):
        s = "\nMENU DE COMANDOS:\n\n"
        s += "\t1 : Listar os cursos de uma unidade\n"
        s += "\t2 : Mostrar os dados de um curso\n"
        s += "\t3 : Mostrar os dados de todos os cursos\n"
        s += "\t4 : Mostrar os dados de uma disciplina\n"
        s += "\t5 : Listar as disciplinas presentes em mais de um curso\n"
        s += "\tm : Exibir o menu de comandos\n"
        s += "\tq : Encerrar o programa\n"

        return s

       
    def main(self):
        nroUnidades = int(sys.argv[1]) if len(sys.argv) > 1 else None
        print("\n***------------- Aguarde o carregamento das unidades -------------***\n")

        carregarUsp = None
        if os.path.os.path.isfile("usp.pkl"):
            carregarUsp = input("Deseja carregar os dados salvos? (y/n) ").strip().lower()

        if carregarUsp is not None and carregarUsp in {"y", "yes"}:
            with open("usp.pkl", "rb") as f:
                usp = pickle.load(f)
        else:
            usp = USP()
            s = Scraper(usp, nroUnidades)
            s.acessarSite()
            s.navegarJupiter()
           
            with open("usp.pkl", "wb") as f:
                pickle.dump(usp, f, byref=False, recurse=True)


        print("\n***-------------------- Carregamento completo ---------------------***")
        menu = self.menuFuncionalidades()
        print(menu)
        self.form = Formatador()

        while True:
            comando = input("\nDigite um comando ou 'm' para ver as opções: ")
        
            match comando:
                # Lista de cursos por unidades
                case '1':
                    unidade = input("Insira o nome da unidade: ")
                    listaCursos = usp.listarCursosPorUnidade(unidade)
                    self.mostrarTabela(listaCursos, colunas=["Lista de cursos oferecidos"], titulo="Resultado de 'Listar cursos por unidade'")

                # Dados de um determinado curso
                case '2':
                    curso = input("Insira o nome do curso: ")
                    print()
                    dadosCurso = usp.mostrarCursos(curso)
                    self.mostrarTabela(dadosCurso, colunas=["Dados dos cursos encontrados"], titulo="Resultado de 'Mostrar os dados de um curso'")
                    
                # Dados de todos os cursos 
                case '3':
                    dadosCursos = usp.mostrarCursos()
                    self.mostrarTabela(dadosCursos, colunas=["Dados de todos os cursos"], titulo="Resultado de 'Mostrar os dados de todos os cursos'")

                # Dados de uma disciplina
                case '4':
                    disciplina = input("Insira o nome ou código da disciplina: ")
                    print()
                    dadosDisciplina = usp.mostrarDisciplina(disciplina)
                    self.mostrarTabela(dadosDisciplina, colunas=["Dados das disciplinas encontradas"], titulo="Resultado de 'Mostrar os dados de uma disciplina'")
                
                # Disciplinas que são usadas em mais de um curso
                case '5':
                    listaDisc = usp.listarDisciplinasCompartilhadas()
                    self.mostrarTabela(listaDisc, colunas=["Nome e código da disciplina", "Cursos que a contêm"], titulo="Resultado de 'Listar as disciplinas incluídas em mais de um curso'")

                # Mostrar o menu de comandos
                case 'm':
                    print(menu)

                # Encerra o programa
                case 'q':
                    print("Encerrando o programa...")
                    return
                
                # Mensagem para comando inválido
                case _:
                    print("\nComando inválido, tente novamente ou digite 'm' para ver as opções.\n")


    def mostrarTabela(self, dados, colunas, titulo):
        if dados:
            dadosFormatados = self.form.estruturar(dados)
            janela = tk.Tk()
            tabela = Tabela(janela, dadosFormatados, colunas, titulo)
            janela.mainloop()


if __name__ == "__main__":
    Main().main()
                                                                                                                                              
