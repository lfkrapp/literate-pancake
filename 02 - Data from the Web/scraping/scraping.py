import os
import glob
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait


# ------- SETUP VARIABLES -------
# manually setup variables for the program
download_path = "/home/khaos/Downloads" # !!! DOWNLOAD FOLDER MUST BE EMPTY !!!
url = 'http://isa.epfl.ch/imoniteur_ISAP/%21gedpublicreports.htm?ww_i_reportmodel=133685247'

# ------- INITIALIZATION -------
# setup profile of the browser
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.panel.shown", False)
profile.set_preference("browser.helperApps.neverAsk.openFile","text/csv,application/vnd.ms-excel")
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/vnd.ms-excel")
profile.set_preference("browser.download.folderList", 2);
profile.set_preference("browser.download.dir", download_path)
driver = webdriver.Firefox(profile)

# load URL and wait that it is loaded
driver.get(url)
driver.implicitly_wait(60)

# go to the frame containing the select menu
driver.switch_to_frame(driver.find_element_by_name('toc'))

# ------- SCRAPING -------
print('Start scraping website...')

# find and click radio button for xls format
radiobtn = driver.find_element_by_xpath("//input[@name='ww_i_reportModelXsl'][@value='133685271']")
radiobtn.click()

# find and click on OK button
okbtn = driver.find_element_by_name('dummy')
okbtn.click()

def halt_until_downloaded(filepath):
    # wait filename exists
    while not(os.path.isfile(filepath)):
        sleep(0.05)

    # wait file is readable
    while os.path.getsize(filepath)<1000:
        print('Waiting on file '+str(filepath))
        sleep(0.05)

    while True:
        s1 = os.path.getsize(filepath)
        sleep(0.05)
        s2 = os.path.getsize(filepath)
        if s1==s2:
            return

list_of_matches = driver.find_elements_by_xpath("//*[contains(text(), 'Informatique, 20')]")
for test in list_of_matches:
    # find element and click on it
    print(test.text)
    test.click()

    # wait for download and wait download complete
    halt_until_downloaded(download_path+'/!GEDPUBLICREPORTS.XLS')

    # rename file with version to manage duplicates
    fversion = str(len(glob.glob(download_path+'/'+"".join(test.text.split())+"*")))
    filename = "/"+"".join(test.text.replace('/','-').split())+"_"+fversion+'.XLS'
    os.rename(download_path+'/!GEDPUBLICREPORTS.XLS', download_path+filename)

    # wait rename is done
    halt_until_downloaded(download_path+'/'+filename)

print('Scraping complete, closing browser...')
driver.quit()
