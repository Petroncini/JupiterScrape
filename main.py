from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import time

driver = webdriver.Chrome()

driver.get("https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275")

wait = WebDriverWait(driver, timeout=2)

wait.until(lambda _: len(Select(driver.find_element("id", value="comboUnidade")).options) > 1)

unidadeSelect_element = driver.find_element("id", value="comboUnidade") 

buscarButton = driver.find_element("id", value="enviar")

unidadeSelect = Select(unidadeSelect_element)
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
        wait.until(lambda _: driver.find_element("id", "step1-tab").is_displayed())
        abaMenus = driver.find_element("id", value="step1-tab")
        abaMenus.click()



input("Aperte Enter para terminar...")
