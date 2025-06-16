from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from bs4 import BeautifulSoup


import time
from selenium.webdriver.chrome.options import Options

from USP import USP
from Unidade import Unidade
from Curso import Curso 
from Disciplina import Disciplina

class Scraper:
    def __init__(self, usp: USP, nroUnidades=None):
        options = Options()
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )
        options.add_argument(f"user-agent={user_agent}")
        # options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        self.usp = usp
        self.unidadeAtual = None
        self.cursoAtual = None
        self.limite = (nroUnidades + 1) if nroUnidades is not None else None
        self.prevGrade = None


        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, timeout=30)
    
    def acessarSite(self):
        self.driver.get("https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275")
    
    def navegarJupiter(self):
        self.acessarSite()
        # Espera até encontrar o elemento comboUnidade
        self.wait.until(EC.presence_of_element_located((By.ID, "comboUnidade")))
        self.wait.until(lambda d: len(Select(d.find_element(By.ID, "comboUnidade")).options) > 1)
        unidadeSelect_element = self.driver.find_element("id", value="comboUnidade") 

        buscarButton = self.driver.find_element("id", value="enviar")

        unidadeSelect = Select(unidadeSelect_element)
        t0 = time.time()

        if self.limite is None : self.limite = len(unidadeSelect.options)

        for unidade in unidadeSelect.options[1:self.limite]:
            # Cria unidade e adiciona na USP 
            self.unidadeAtual = Unidade(unidade.text)
            print(self.unidadeAtual.nome)

            self.usp.adicionarUnidade(self.unidadeAtual)

            unidadeSelect.select_by_visible_text(unidade.text) 
            self.wait.until(EC.presence_of_element_located((By.ID, "comboCurso")))
            self.wait.until(lambda _: len(Select(self.driver.find_element("id", value="comboCurso")).options) > 1)
            cursoSelect_element = self.driver.find_element("id", value="comboCurso")
            cursoSelect = Select(cursoSelect_element)

            for curso in cursoSelect.options[1:]:
                cursoSelect.select_by_visible_text(curso.text)
                self.wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "blockUI")) == 0)
                self.wait.until(EC.element_to_be_clickable(("id", "enviar")))
                buscarButton.click()    
                self.carregarGradeCurricular()

        self.unidadeAtual = None
        self.cursoAtual = None

        t1 = time.time()
        total = t1 - t0
        print(f'Time: {total}')

    def carregarGradeCurricular(self):
        try:
            time.sleep(0.1)
            self.wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "blockUI")) == 0)
            self.wait.until(EC.element_to_be_clickable(("id", "step4-tab")))
            abaGrade = self.driver.find_element("id", "step4-tab")
            abaGrade.click()

            
            self.wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "blockUI")) == 0)
            self.getCurso()

            self.wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "blockUI")) == 0)
            abaMenus = self.driver.find_element("id", value="step1-tab")
            abaMenus.click()

            
        except ElementClickInterceptedException:
            print("             Erro - dados não encontrados")

            try:
                fechar = self.driver.find_element(By.XPATH, '//button[contains(@class, "ui-button") and .//span[text()="Fechar"]]')
                fechar.click()

                self.wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "blockUI")) == 0)
                abaMenus = self.driver.find_element("id", value="step1-tab")
                abaMenus.click()

            except NoSuchElementException:
                print("Fatal")
    
    def getCurso(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        divInformacoes = soup.find('div', id='step4') 
        assert divInformacoes is not None
        #print(divInformacoes.prettify())
        # Informações do curso 
        unidadeNome = divInformacoes.find('span', class_='unidade').contents[0]
        cursoNome = divInformacoes.find('span', class_='curso').contents[0]
        ideal = divInformacoes.find('span', class_='duridlhab').contents[0]
        minima = divInformacoes.find('span', class_='durminhab').contents[0]
        maxima = divInformacoes.find('span', class_='durmaxhab').contents[0]
        # Cria o curso
        self.cursoAtual = Curso(cursoNome, unidadeNome, ideal, minima, maxima)
        print(f"\t{self.cursoAtual.nome}")


        divGrade = soup.find('div', id="gradeCurricular")


        if "Engenharia Florestal - integral" in self.cursoAtual.nome:
            print(divInformacoes.prettify())
            time.sleep(300)
        #     print(divGrade.prettify())

        for tableGrade in divGrade.find_all('table'):
            tipoDisciplinas = "Obrigatória"
            for tr in tableGrade.find_all('tr'):
                # processarDisciplina(tr)?
                style = tr.get('style')

                # Verifica qual tipo de disciplina é
                if style is not None and style.strip() == "background-color: rgb(16, 148, 171); color: white;":
                    if "Livres" in tr.td.contents[0]:
                        tipoDisciplinas = "Livre"
                    elif "Eletivas" in tr.td.contents[0]:
                        tipoDisciplinas = "Eletiva"
                    continue

                if style is not None and style.strip() == 'height: 20px;':
                    tds = tr.find_all('td')

                    linkDisciplina = tds[0].find('a')
                    disciplinaCodigo = linkDisciplina.contents[0] if tds[0].contents else None

                    # Verifica se a disciplina já está na lista de disciplinas em usp 
                    disciplina = self.usp.buscarDisciplina(disciplinaCodigo)

                    if disciplina is None:
                        disciplinaNome = tds[1].contents[0] if tds[1].contents else None
                        credAula = tds[2].contents[0] if tds[2].contents else None
                        credTrab = tds[3].contents[0] if tds[3].contents else None
                        CH = tds[4].contents[0] if tds[4].contents else None
                        CE = tds[5].contents[0] if tds[5].contents else None
                        CP = tds[6].contents[0] if tds[6].contents else None
                        ATPA = tds[7].contents[0] if tds[7].contents else None

                        disciplina = Disciplina(
                            disciplinaCodigo, 
                            disciplinaNome,
                            credAula,
                            credTrab,
                            CH, CE, CP, ATPA)
                    
                    # Quais cursos tem essa disciplina
                    if tipoDisciplinas == "Obrigatória":
                        disciplina.incluirCurso(self.cursoAtual)
                    # Adiciona a disciplina na lista de disciplinas da usp
                    self.usp.adicionarDisciplina(disciplina)
                    # O curso atual recebe a disciplina
                    self.cursoAtual.adicionarDisciplina(disciplina, tipoDisciplinas)

        self.unidadeAtual.adicionarCurso(self.cursoAtual)   

        if len(self.cursoAtual.obrigatorias) == 0:
            print("\t\tCurso sem obrigatórias")
        if len(self.cursoAtual.eletivas) == 0:
            print("\t\tCurso sem eletivas")
        if len(self.cursoAtual.livres) == 0:
            print("\t\tCurso sem livres")

        # if self.cursoAtual.nome == "Engenharia Florestal - integral":
        #     print(self.cursoAtual)

                # print(self.cursoAtual)
