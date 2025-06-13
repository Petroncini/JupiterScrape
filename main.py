from Scraper import Scraper 
from USP import USP
from Unidade import Unidade
from Curso import Curso 
from Disciplina import Disciplina

class Main:

    def main():
        usp = USP()
        s = Scraper(usp)
        s.acessarSite()
        s.navegarJupiter()

    if __name__ == "__main__":
        main()
                                                                                                                                              