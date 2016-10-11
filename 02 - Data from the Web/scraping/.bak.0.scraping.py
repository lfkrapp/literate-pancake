from selenium import webdriver
from selenium.webdriver.support.ui import Select

url = 'http://isa.epfl.ch/imoniteur_ISAP/%21gedpublicreports.htm?ww_i_reportmodel=133685247'

driver = webdriver.Firefox()
driver.get(url)

driver.find_element_by_xpath("//select[@name='zz_x_HIVERETE']/option[text()='Semestre d\'automne']").click()

driver.findElement(By.xpath("//input[@name='zz_x_HIVERETE'])).setAttribute("value", "Semestre d\'automne")

