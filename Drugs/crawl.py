from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    ElementClickInterceptedException, 
    TimeoutException, 
    NoSuchElementException, 
    TimeoutException, 
    InvalidSessionIdException
    )
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import pandas as pd
import os

options = Options()
options.add_argument("--no-sandbox")
# options.add_argument("--headless")    
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")

def crawl():
    global dataFrame_result
    driver = webdriver.Chrome(
        service = Service(ChromeDriverManager().install()), 
        chrome_options= options
    )
    driver.get(
        "https://www.drugs.com/pharmaceutical-companies.html"
    )
    
    # WebDriverWait(driver, 20).until(
    #         EC.presence_of_element_located(
    #             (By.XPATH, "//div[@class='ddc-grid']/div[@class='ddc-grid-col-6 col-list-az'][1]/ul[1]/li/a")
    #             )
    #         )
    # urls = []
    # path = '/Users/dinhvan/Projects/Code/crawl/selenium/Drugs/url.csv'
    # for number in range(1,3,1):
    #     name = driver.find_element(By.XPATH, "//div[@class='ddc-grid']/div[@class='ddc-grid-col-6 col-list-az'][2]/ul[15]/li[{}]/a".format(number)).text
    #     url = driver.find_element(By.XPATH, "//div[@class='ddc-grid']/div[@class='ddc-grid-col-6 col-list-az'][2]/ul[15]/li[{}]/a".format(number)).get_attribute('href')
    #     dict_url = {'name':name,
    #         'url' : url}
    #     data = pd.DataFrame([dict_url])
    #     # data.to_csv('/Users/dinhvan/Projects/Code/crawl/selenium/Drugs/url.csv', index = False)
    #     data.to_csv(path, mode='a', header=not os.path.exists(path), index = False)
    #     print(dict_url)
    # # WebDriverWait(driver, 20).until(
    # #         EC.presence_of_element_located(
    # #             (By.XPATH, "//div[@class='ddc-grid']/div[@class='ddc-grid-col-6 col-list-az'][1]/ul[1]/li/a")
    # #             )
    # #         ).click()
    # driver.close()

if __name__ == '__main__': 
    columns = ['ten_co_so','dia_chi_tru_so','dia_chi_kinh_doanh','dien_thoai','loai_hinh','so_GCN']
    crawl()