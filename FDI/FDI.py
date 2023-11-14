from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
import numpy as np
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-setuid-sandbox")

# data_input = pd.read_csv('/Users/dinhvan/Documents/Projects/Crawl/datainput/MST_FDI.csv',dtype = {'mst':np.str})
# data_input['0'] = data_input['0'].str.strip()
# list_input = data_input['0'].to_list()
list_input = [
'1101692479-001',
'0102879245-001',
'3600262524-002',
'0801038936']
dataFrame = pd.DataFrame()
list_lost = []

def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return True

for mst in list_input:
    try:
        driver = webdriver.Chrome(options=options, executable_path=r'/Users/dinhvan/Downloads/chromedriver')
        driver.get("https://masothue.com/")
     
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@id='search']"))).clear()
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@id='search']"))).send_keys('{}'.format(mst))
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH,"(//button[@class='btn btn-secondary btn-search-submit'])"))).click()

        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, "//main[@id='main']/section[@class='animate-in-view fadeIn animated'][1]/div[@class='container']/header/h1[@class='h1']"), '{}'.format(mst)))
        list_result = []
        table1 = driver.find_elements(By.XPATH,"//table[@class='table-taxinfo']//tr/td")
        for key in table1:
            list_result.append(key.text) 

        if len(list_result) % 2 == 0:
            del list_result[-2:]

        dict_result = {}
        for element in range(0,len(list_result)):
            if(element%2 == 0):
                dict_result['{}'.format(list_result[element])] = list_result[element+1]
        print(dict_result)
        dataFrame_temp = pd.DataFrame([dict_result])
        dataFrame  = pd.concat([dataFrame,dataFrame_temp],ignore_index= True)
        dataFrame.to_csv('Result_FDI_1.csv')
        driver.close()
    except Exception as excep:
        print(str(excep))
        print('Error : ' + str(mst))
        list_lost.append(mst)
        driver.close()
        continue
df = pd.DataFrame(list_lost)
df.to_csv('Lost_FDI.csv')
