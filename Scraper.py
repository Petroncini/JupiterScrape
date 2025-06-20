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
        # configurações do webdriver
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
        self.usp = usp # objeto usp que receberá informação
        self.unidadeAtual = None # unidade sendo processda
        self.cursoAtual = None # curso send processado
        self.limite = (nroUnidades + 1) if nroUnidades is not None else None # limite de busca


        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, timeout=30)
    
    def acessarSite(self):
        self.driver.get("https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275")
    
    def navegarJupiter(self): # navega pagina do jupiter para acessar informações
        self.acessarSite()
        # Espera até encontrar o elemento comboUnidade
        self.wait.until(EC.presence_of_element_located((By.ID, "comboUnidade")))
        # espera opçÕes carregarem
        self.wait.until(lambda d: len(Select(d.find_element(By.ID, "comboUnidade")).options) > 1)
        # elemento dropdown de unidades
        unidadeSelect_element = self.driver.find_element("id", value="comboUnidade") 
        #botao de busca
        buscarButton = self.driver.find_element("id", value="enviar")
        
        # select de unidade
        unidadeSelect = Select(unidadeSelect_element)
        # timer para avaliar performance
        t0 = time.time()

        if self.limite is None : self.limite = len(unidadeSelect.options)

        # itera por cada unidade
        for unidade in unidadeSelect.options[1:self.limite]:
            # Cria unidade e adiciona na USP 
            self.unidadeAtual = Unidade(unidade.text)
            print(self.unidadeAtual.nome)
            self.usp.adicionarUnidade(self.unidadeAtual)
            
            #seleciona unidade no menu
            unidadeSelect.select_by_visible_text(unidade.text) 

            # espera carregar dropdown e opções de curso da unidade
            self.wait.until(EC.presence_of_element_located((By.ID, "comboCurso")))
            self.wait.until(lambda _: len(Select(self.driver.find_element("id", value="comboCurso")).options) > 1)

            # elemeto de seleção de curso
            cursoSelect_element = self.driver.find_element("id", value="comboCurso")
            cursoSelect = Select(cursoSelect_element)

            # itera por cada curso na unidade
            for curso in cursoSelect.options[1:]:
                #seleciona curso no menu
                cursoSelect.select_by_visible_text(curso.text)

                # a os elementos da classe blockUI aparecem quando a página está carregando algo
                # esperando o número de elementos blockUI ser 0, esperamos todos os dados serem carregados
                self.wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "blockUI")) == 0)
                self.wait.until(EC.element_to_be_clickable(("id", "enviar"))) # confere ser é clicável
                # clica botão para ir para a aba "informações de curso" do curso selecionado
                buscarButton.click()   

                # chama função para de fato carregar as informações do curso 
                self.navegarCurso()

        self.unidadeAtual = None
        self.cursoAtual = None

        t1 = time.time()
        total = t1 - t0
        print(f'Time: {total}')

    def navegarCurso(self): # navega página do curso para encontrar informações
        try:
            # espera carregar e aba de Grade Curriscular ser clicável
            self.wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "blockUI")) == 0)
            self.wait.until(EC.element_to_be_clickable(("id", "step4-tab")))
            # aba da grade
            abaGrade = self.driver.find_element("id", "step4-tab")
            # clica na aba da grade
            abaGrade.click()

            # depois de chegar na aba da grade, chama função para processar HTML
            self.wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "blockUI")) == 0)
            self.getCurso()

            # depois de carregar informações do curso, volta para o menu de unidades e cursos
            self.wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "blockUI")) == 0)
            abaMenus = self.driver.find_element("id", value="step1-tab")
            abaMenus.click()

            
        except ElementClickInterceptedException:
            # esse erro ocorre quando o curso selecionado e buscando não tem informações 
            # aparece então uma janela de erro informando esse fato e
            # o click na aba de "Informações de Curso" é interceptado

            print("             Erro - dados não encontrados")

            try:
                # acha e clica o botão de fechar na janela de erro
                fechar = self.driver.find_element(By.XPATH, '//button[contains(@class, "ui-button") and .//span[text()="Fechar"]]')
                fechar.click()

                self.wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "blockUI")) == 0)
                abaMenus = self.driver.find_element("id", value="step1-tab")
                abaMenus.click()

            except NoSuchElementException:
                # algo deu muito errado
                print("Fatal")
    
    def getCurso(self):
        # baixa o html da página e criar uma instância do BeautifulSoup pra processar ele
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        divInformacoes = soup.find('div', id='step4') # div de informações do curso
        assert divInformacoes is not None

        # Informações do curso 
        unidadeNome = divInformacoes.find('span', class_='unidade').contents[0]
        cursoNome = divInformacoes.find('span', class_='curso').contents[0]
        ideal = divInformacoes.find('span', class_='duridlhab').contents[0]
        minima = divInformacoes.find('span', class_='durminhab').contents[0]
        maxima = divInformacoes.find('span', class_='durmaxhab').contents[0]

        # Cria o curso
        self.cursoAtual = Curso(cursoNome, unidadeNome, ideal, minima, maxima)
        print(f"\t{self.cursoAtual.nome}")


        divGrade = soup.find('div', id="gradeCurricular") # div com as tabelas das grade
    
        # itera pelas tabelas de disciplinas obrigatórias, eletivas e livres
        for tableGrade in divGrade.find_all('table'):
            tipoDisciplinas = "Obrigatória" # tipo default
            # itera por cada linha da tabela

            for tr in tableGrade.find_all('tr'):
                # o estilo de cada row é o que diferencia os rows diferentes, deselegante
                style = tr.get('style')

                # Se a row é do tipo de disciplina, verifica qual tipo de disciplina é
                if style is not None and style.strip() == "background-color: rgb(16, 148, 171); color: white;":
                    if "Livres" in tr.td.contents[0]:
                        tipoDisciplinas = "Livre"
                    elif "Eletivas" in tr.td.contents[0]:
                        tipoDisciplinas = "Eletiva"
                    continue

                # se a row conter as informações das disciplinas
                if style is not None and style.strip() == 'height: 20px;':
                    # peda os dado da row
                    tds = tr.find_all('td')

                    # acha o link da disciplina
                    linkDisciplina = tds[0].find('a')
                    # Pega o código no nome desse link
                    disciplinaCodigo = linkDisciplina.contents[0] if tds[0].contents else None

                    # Verifica se a disciplina já está na lista de disciplinas em usp, se sim pega ela
                    disciplina = self.usp.buscarDisciplina(disciplinaCodigo)
                    
                    # se é nova, pega os daodos dela que estão em ordem nos tds
                    if disciplina is None:
                        disciplinaNome = tds[1].contents[0] if tds[1].contents else None
                        credAula = tds[2].contents[0] if tds[2].contents else None
                        credTrab = tds[3].contents[0] if tds[3].contents else None
                        CH = tds[4].contents[0] if tds[4].contents else None
                        CE = tds[5].contents[0] if tds[5].contents else None
                        CP = tds[6].contents[0] if tds[6].contents else None
                        ATPA = tds[7].contents[0] if tds[7].contents else None

                        # cria disciplina
                        disciplina = Disciplina(
                            disciplinaCodigo, 
                            disciplinaNome,
                            credAula,
                            credTrab,
                            CH, CE, CP, ATPA)
                    
                    # Quais cursos tem essa disciplina, adiciona
                    if tipoDisciplinas == "Obrigatória":
                        disciplina.incluirCurso(self.cursoAtual.unidade, self.cursoAtual.nome)

                    # Adiciona a disciplina na lista de disciplinas da usp
                    self.usp.adicionarDisciplina(disciplina)
                    # O curso atual recebe a disciplina
                    self.cursoAtual.adicionarDisciplina(disciplina, tipoDisciplinas)

        #adiciona curso na unidade
        self.unidadeAtual.adicionarCurso(self.cursoAtual)   
