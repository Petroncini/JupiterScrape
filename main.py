from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

import time
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")  # Run headless (no GUI)
options.add_argument("--disable-gpu")  # Disable GPU acceleration (Windows)
options.add_argument("--no-sandbox")  # Useful for Linux
options.add_argument("--disable-dev-shm-usage")  # Prevents crashes in headless mode

driver = webdriver.Chrome(options=options)
driver.get("https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275")

wait = WebDriverWait(driver, timeout=2)

wait.until(lambda _: len(Select(driver.find_element("id", value="comboUnidade")).options) > 1)

unidadeSelect_element = driver.find_element("id", value="comboUnidade") 

buscarButton = driver.find_element("id", value="enviar")

unidadeSelect = Select(unidadeSelect_element)
t0 = time.time()

for unidade in unidadeSelect.options[1:]:
    print(unidade.text)
    unidadeSelect.select_by_visible_text(unidade.text)
    wait.until(lambda _: len(Select(driver.find_element("id", value="comboCurso")).options) > 1)
    cursoSelect_element = driver.find_element("id", value="comboCurso")
    cursoSelect = Select(cursoSelect_element)

    for curso in cursoSelect.options[1:]:
        print("\t", curso.text)
        cursoSelect.select_by_visible_text(curso.text)
        buscarButton.click()

        try:
            wait.until(EC.element_to_be_clickable(("id", "step4-tab")))
            abaGrade = driver.find_element("id", "step4-tab")
            abaGrade.click()

            wait.until(EC.element_to_be_clickable(("id", "step1-tab")))
            abaMenus = driver.find_element("id", value="step1-tab")
            abaMenus.click()
        except ElementClickInterceptedException:
            print("Erro - dados não encontrados")

            try:
                fechar = driver.find_element(By.XPATH, '//button[contains(@class, "ui-button") and .//span[text()="Fechar"]]')
                fechar.click()


                wait.until(EC.element_to_be_clickable(("id", "step4-tab")))
                abaGrade = driver.find_element("id", "step4-tab")
                abaGrade.click()

                wait.until(EC.element_to_be_clickable(("id", "step1-tab")))
                abaMenus = driver.find_element("id", value="step1-tab")
                abaMenus.click()
            except NoSuchElementException:
                print("Fatal")

t1 = time.time()
total = t1 - t0
print(f'Time: {total}')

input("Aperte Enter para terminar...")
