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
    def __init__(self):
        options = Options()
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, timeout=30)
    
    def acessarSite(self):
        self.driver.get("https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275")
    
    def navegarJupiter(self, usp):
        self.acessarSite()
        # Espera até encontrar o elemento comboUnidade
        self.wait.until(EC.presence_of_element_located((By.ID, "comboUnidade")))
        self.wait.until(lambda d: len(Select(d.find_element(By.ID, "comboUnidade")).options) > 1)
        unidadeSelect_element = self.driver.find_element("id", value="comboUnidade") 

        buscarButton = self.driver.find_element("id", value="enviar")

        unidadeSelect = Select(unidadeSelect_element)
        t0 = time.time()

        for unidade in unidadeSelect.options[1:]:
            # Cria unidade e adiciona na USP 
            uni = Unidade(unidade)
            usp.adicionaUnidade(uni)
            print(unidade.text)
            unidadeSelect.select_by_visible_text(unidade.text) 
            self.wait.until(EC.presence_of_element_located((By.ID, "comboCurso")))
            self.wait.until(lambda _: len(Select(self.driver.find_element("id", value="comboCurso")).options) > 1)
            cursoSelect_element = self.driver.find_element("id", value="comboCurso")
            cursoSelect = Select(cursoSelect_element)

            for curso in cursoSelect.options[1:]:
                print("\t", curso.text)
                cursoSelect.select_by_visible_text(curso.text)
                buscarButton.click()    
                self.carregarGradeCurricular()

        t1 = time.time()
        total = t1 - t0
        print(f'Time: {total}')

        input("Aperte Enter para terminar...")

    def carregarGradeCurricular(self):
        try:
            self.wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "blockUI")) == 0)
            self.wait.until(EC.element_to_be_clickable(("id", "step4-tab")))
            abaGrade = self.driver.find_element("id", "step4-tab")
            abaGrade.click()

            self.wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "blockUI")) == 0)
            abaMenus = self.driver.find_element("id", value="step1-tab")
            abaMenus.click()

            self.getCurso()
            
        except ElementClickInterceptedException:
            print("             Erro - dados não encontrados")

            try:
                fechar = self.driver.find_element(By.XPATH, '//button[contains(@class, "ui-button") and .//span[text()="Fechar"]]')
                fechar.click()
            except NoSuchElementException:
                print("Fatal")
    
    def getCurso(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        divInformacoes = soup.find('div', id='step4')
        #print(divInformacoes.prettify())
        # Informações do curso 
        unidade = divInformacoes.find('span', class_='unidade')
        curso = divInformacoes.find('span', class_='curso')
        ideal = divInformacoes.find('span', class_='duridlhab')
        minima = divInformacoes.find('span', class_='durminhab')
        maxima = divInformacoes.find('span', class_='durmaxhab')
        # Cria o curso
        curso = Curso(curso, unidade, ideal, minima, maxima)

        divGrade = soup.find('div', id="gradeCurricular")

        tableGrade = divGrade.find('table')
        for tr in tableGrade.find_all('tr'):
            style = tr.get('style')
            if style is not None and style.strip() == 'height: 20px;':
                
                print(tr.prettify())