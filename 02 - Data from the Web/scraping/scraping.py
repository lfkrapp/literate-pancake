import os
import glob
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait

# element_names = ['ww_i_reportModelXsl', 'zz_x_UNITE_ACAD0', 'ww_x_UNITE_ACAD', 'zz_x_PERIODE_ACAD', 'ww_x_PERIODE_ACAD', 'zz_x_PERIODE_PEDAGO', 'ww_x_PERIODE_PEDAGO', 'zz_x_HIVERETE', 'ww_x_HIVERETE']

# ------- SETUP VARIABLES -------
download_path = "/home/khaos/Downloads" # !!! DOWNLOAD FOLDER MUST BE EMPTY !!!
url = 'http://isa.epfl.ch/imoniteur_ISAP/%21gedpublicreports.htm?ww_i_reportmodel=133685247'

# ------- INITIALIZATION -------
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.panel.shown", False)
profile.set_preference("browser.helperApps.neverAsk.openFile","text/csv,application/vnd.ms-excel")
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/vnd.ms-excel")
profile.set_preference("browser.download.folderList", 2);
profile.set_preference("browser.download.dir", download_path)
driver = webdriver.Firefox(profile)

driver.get(url)
driver.implicitly_wait(60)

driver.switch_to_frame(driver.find_element_by_name('toc'))

# print_elements_by_name(driver)

# ------- SCRAPING -------
print('Start scraping website...')

radiobtn = driver.find_element_by_xpath("//input[@name='ww_i_reportModelXsl'][@value='133685271']")
radiobtn.click()

okbtn = driver.find_element_by_name('dummy')
okbtn.click()

# n = 10
n = 7613+2
for i in range(2,n):
	test = driver.find_element_by_xpath("(//a[@class='ww_x_GPS'])["+str(i)+"]")
	test.click()
        while len(glob.glob(download_path+'/*.XLS')) <= i-2:
            sleep(0.05)
        while glob.glob(download_path+'/*.part'):
            sleep(0.05)
        print(test.text)
        fversion = str(len(glob.glob(download_path+'/'+"".join(test.text.split())+"*")))
        os.rename(download_path+'/!GEDPUBLICREPORTS.XLS', download_path+"/"+"".join(test.text.split())+"_"+fversion+'.XLS')
        while len(glob.glob(download_path+'/'+"".join(test.text.split())+"_"+fversion+'.XLS'))==0:
            sleep(0.05)

# ------ LOOP METHOD ------- (NOT IMPLEMENTED)
# loop over an element
# select = driver.find_element_by_name('ww_x_PERIODE_ACAD')
# options = select.find_elements_by_tag_name('option')

# optionsList = []

# for option in options:
	# optionsList.append(option.get_attribute("value"))

# for optionValue in optionsList:
	# print("starting loop on option " + str(optionValue))




print('Scraping complete, closing browser...')
driver.quit()
