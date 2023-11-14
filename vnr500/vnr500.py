from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd


options = Options()
options.headless = True
driver = webdriver.Chrome(options=options, executable_path=r'/Users/dinhvan/Downloads/chromedriver')
driver.get("https://vnr500.com.vn/")
print ("Headless Chrome Initialized !")

dataFrame = pd.DataFrame()
dict_result ={}
list = ['0102744865','0200253985','0102683813','0839111301','0100105870','0100105870','0301129367','0301450108']
for element in list:
    try:
        driver.find_element(By.XPATH,"(//input[@id='mst'])").send_keys('{}'.format(element))
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "(//input[@id='searchsubmit'])[2]"))))

        list_table1 = []
        list_table2 = []

        list_table1.append('Ngành nghề')
        list_table2.append(driver.find_element(By.XPATH,"//table[@id='dataTables-search']/tbody/tr[@class='row_tr odd']/th/span/div[@class='row']/span[@class='col-xs-12 col-sm-6 nganh-nghe']/span/a").text)

        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//table[@id='dataTables-search1']//tr[@class='row_tr odd']/th/span/span[@class='name_1']/a"))))

        table1 = driver.find_elements(By.XPATH,"//table[@class='conpany_info']//tr/td[@class='label_tc']")
        for key in table1:
            list_table1.append(key.text)

        table2 = driver.find_elements(By.XPATH,"//table[@class='conpany_info']//tr/td[2]")
        for value in table2:
            list_table2.append(value.text)

        dict_temp = dict(zip(list_table1,list_table2))
        print(dict_temp)
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[@id='page']/div[@id='header']/div[@class='main-menu']/div[@class='container']/nav[@class='navbar navbar-default']/div[@id='bs-example-navbar-collapse-2']/ul[@class='nav navbar-nav']/li[1]/a"))))
        dataFrame = dataFrame.append(dict_temp, ignore_index = True)
    except NoSuchElementException:
        print('Không tìm thấy Element !')
        driver.quit()
dataFrame.to_csv('Result.csv')
driver.quit()
