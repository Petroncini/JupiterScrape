from Scraper import Scraper 
from USP import USP
from Unidade import Unidade
from Curso import Curso 
from Disciplina import Disciplina

class Main:

    def main():
        usp = USP()
        s = Scraper()
        s.acessarSite()
        s.navegarJupiter(usp)

    if __name__ == "__main__":
        main()
                                                                                                                                              