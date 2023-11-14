from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options, executable_path=r'/Users/dinhvan/Downloads/chromedriver')
driver.get("https://masothue.com/")
print ("Headless Chrome Initialized !")

list_url = []
# data_input = pd.read_excel('/Users/dinhvan/Documents/Crawl/selenium/getLink/Ngan_Trang_1210 copy.xlsx',dtype={'MST': np.str})
# list_input = data_input['MST'].to_list()
list_input = ['0103811666',
'0102577004',
'4900844797',
'0102727651',
'0102121412', 
'0104079036', 
'0313720398',
'0100100181', 
'0101511949', 
'2800799804', 
'3401133034',
'6101256048', 
'6101210389', 
'2800799804-001', 
'0109298049', 
'5500290578', 
'2801952893', 
'2802200078', 
'0102180545', 
'0312467752', 
'6000346337', 
'0301851276', 
'0301930337', 
'0100774342',
'0302249586',
'0301450108', 
'0300808687',
'0302803331', 
'0312545104', 
'0300797153', 
'0311241512', 
'0309103635', 
'0101210878', 
'1100102656', 
'0305707643', 
'0301232798',
'0309069208',
'0300608568', 
'3700667933', 
'0303845969', 
'0304990133',
'0101225306',
'0107009894', 
'5700101210', 
'0100113494',
'0900841823', 
'0107520795', 
'0300733752', 
'0305774706', 
'3700229030',
'0309875328', 
'2600924092',
'0101452588', 
'0109078678', 
'2802846993',
'5300778978', 
'0109516875', 
'5300299830', 
'5300656602', 
'0100100417', 
'0104297034', 
'0100942205', 
'0500463609',
'0317452407',
'0102324187', 
'0100105380', 
'0108453005', 
'0104794967', 
'0100112733',
'3500881545', 
'0101398161', 
'0104288054', 
'5300239937', 
'0103648258',
'0105890977', 
'0400563536',
'0103141556',
'0100977705']
for element in list_input:
    try:
        driver.find_element(By.XPATH,"(//input[@id='search'])").send_keys('{}'.format(element))
        time.sleep(1)
        driver.find_element(By.XPATH,"(//button[@class='btn btn-secondary btn-search-submit'])").click()
        time.sleep(1)
        
        list_url.append(driver.current_url)
        print(driver.current_url)

    except:
        print(element)
        driver.refresh()
        continue
dataFrame = pd.DataFrame(list_url)
dataFrame.to_csv('Link_chi_nhanh_3.csv')
driver.quit()