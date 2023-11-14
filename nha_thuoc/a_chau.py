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
from selenium.webdriver.support.ui import Select
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

def crawl(options):
    driver = webdriver.Chrome(
        service = Service(ChromeDriverManager().install()), 
        chrome_options= options
    )
    driver.get(
        "https://seller-vn.tiktok.com/account/register?ad_platform_id=googleadwords_int_lead&ug_google_tracking_id=G-BZBQ2QHQSP&utm_from=google_inhouse_all&campaign_id=16870615394&adset_id=138470373107&ad_id=600247673904&keyword_id=kwd-818868003335&channel=g&placement=&target=&gad=1&gclid=Cj0KCQjwldKmBhCCARIsAP-0rfzcz-CDpfm2lj9TqdrRMrxzmXoH163GgVH8I6ruNuUIucxz6dvjznwaAq0hEALw_wcB"
    )
    
    # xpath_1 = "//div[@class='form-box text-center']/form/div[@class='row']/div[@class='col-md-4'][1]/div[@class='form-group']/select[@id='product']"
    # xpath_2 = "//div[@class='form-box text-center']/form/div[@class='row']/div[@class='col-md-4'][2]/div[@class='form-group']/select[@id='province']"
    # xpath_3 = "//div[@class='form-box text-center']/form/div[@class='row']/div[@class='col-md-4'][3]/div[@class='form-group']/select[@id='district']"
    
    # l_1= driver.find_element(By.XPATH, xpath_1)
    # select_1= Select(l_1)
    # list_product = []

    # for opt in select_1.options:
    #     list_product.append(opt.text)
    # list_product.remove('Tên sản phẩm')
    
    # for value in list_product:
    #     select_1.select_by_visible_text(value)
        
    #     l_2 = driver.find_element(By.XPATH, xpath_2)
    #     select_2 = Select(l_2)
    #     time.sleep(2)
    #     list_city = []
    #     for opt in select_2.options:
    #         list_city.append(opt.text)
    #     list_city.remove('Tỉnh, thành phố')
    #     if None in list_city:
    #         list_city.remove(None)
    #     for city in list_city:
    #         select_2.select_by_visible_text(city)
    #         try:
    #             l_3 = driver.find_element(By.XPATH, xpath_3)
    #             select_3 = Select(l_3)
    #             time.sleep(2)
    #             list_district =[]
    #             for opt in select_3.options:
    #                 list_district.append(opt.text)
    #             list_district.remove('Quận, huyện')
    #             if None in list_district:
    #                 list_district.remove(None)
    #             for district in list_district:
    #                 select_3 = Select(l_3)
    #                 select_3.select_by_visible_text(district)
    #                 time.sleep(2)

    #                 nha_thuoc_driver = driver.find_elements(By.XPATH,"//table[@id='table-data']//tr/td[1]")
    #                 nha_thuoc = [driver.text for driver in nha_thuoc_driver]
                    
    #                 dia_chi_driver = driver.find_elements(By.XPATH,"//table[@id='table-data']//tr/td[@class='d-none d-sm-table-cell']")
    #                 dia_chi = [driver.text for driver in dia_chi_driver]
                    
    #                 dien_thoai_driver = driver.find_elements(By.XPATH,"//table[@id='table-data']//tr/td[@class='d-none text-center d-sm-table-cell']")
    #                 dien_thoai = [driver.text for driver in dien_thoai_driver]
                    
    #                 for nb in range(len(nha_thuoc)):
    #                     dict_temp = {'Nha_thuoc': nha_thuoc[nb],
    #                                 'Dia_chi' : dia_chi[nb],
    #                                 'dien_thoai' : dien_thoai[nb],
    #                         }
    #                     print(dict_temp)
    #                     data = pd.DataFrame([dict_temp])
    #                     resutl_path = '/Users/dinhvan/Projects/Code/crawl/selenium/nha_thuoc/a_chau.csv'
    #                     data.to_csv(resutl_path, mode='a', header=not os.path.exists(resutl_path),index = False)
    #         except Exception as e:
    #             print(e)   
    #             continue
if __name__ == '__main__':
    crawl(options)