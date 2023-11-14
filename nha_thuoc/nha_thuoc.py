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

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--headless")    
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")

dataFrame_result = pd.DataFrame()
def crawl(columns):
    global dataFrame_result
    driver = webdriver.Chrome(
        service = Service(ChromeDriverManager().install()), 
        chrome_options= options
    )
    driver.get(
        "https://drugbank.vn/danh-sach/co-so-phan-phoi?page=1&size=20&sort=id,desc"
    )

    number_results = 20
    for page in range(2,55,1):
        WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH,"//ngb-pagination/ul[@class='pagination']/li[@class='page-item'][5]/a[@class='page-link']")
                    )
                ).click()
        time.sleep(1)
        for click in range(page-2):
            WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH,"//ngb-pagination/ul[@class='pagination']/li[@class='page-item'][6]/a[@class='page-link']")
                    )
                ).click()
            time.sleep(1)
        
        for number_result in range(1,number_results+1,1):
            print('Page ' + str(page) +' : '+ 'Number ' + str(number_result))
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH,"//table[@class='table table-striped table-bordered']//tr[{}]/td[@class='text-right']/div[@class='btn-group']/button[@class='btn btn-info btn-sm']/span[@class='d-none d-md-inline']".format(number_result))
                    )
                ).click()
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH,"//li[@class='d-flex justify-content-between'][1]/h6/strong")
                    )
                )
            ten_co_so = driver.find_element(By.XPATH,"//ul[@class='list-unstyled']/li[@class='d-flex justify-content-between'][1]/div").text
            dia_chi_tru_so = driver.find_element(By.XPATH,"//ul[@class='list-unstyled']/li[@class='d-flex justify-content-between'][2]/div").text
            dia_chi_kinh_doanh = driver.find_element(By.XPATH,"//ul[@class='list-unstyled']/li[@class='d-flex justify-content-between'][3]/div").text
            dien_thoai = driver.find_element(By.XPATH,"//ul[@class='list-unstyled']/li[@class='d-flex justify-content-between'][4]/div").text
            loai_hinh = driver.find_element(By.XPATH,"//ul[@class='list-unstyled']/li[@class='d-flex justify-content-between'][5]/div").text
            so_GCN = driver.find_element(By.XPATH,"//ul[@class='list-unstyled']/li[@class='d-flex justify-content-between'][6]/div").text

            dict_result = {'ten_co_so': ten_co_so,
                        'dia_chi_tru_so': dia_chi_tru_so,
                        'dia_chi_kinh_doanh': dia_chi_kinh_doanh,
                        'dien_thoai' : dien_thoai,
                        'loai_hinh': loai_hinh,
                        'so_GCN': so_GCN
                        }
            data = pd.DataFrame([dict_result])  
            data = data.reindex(columns = columns)
            dataFrame_result = pd.concat([data,dataFrame_result], ignore_index= True)
            driver.back()
            time.sleep(2)
            dataFrame_result.to_csv('/Users/dinhvan/Projects/Code/crawl/selenium/nha_thuoc/test1.csv', index = False)
if __name__ == '__main__': 
    columns = ['ten_co_so','dia_chi_tru_so','dia_chi_kinh_doanh','dien_thoai','loai_hinh','so_GCN']
    crawl(columns)
    