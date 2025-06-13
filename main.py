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

    if __name__ == "__main__":
        main()
                                                                                                                                              