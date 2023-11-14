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
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import pandas as pd
import os

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--headless")   
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")

def check_exists_by_xpath(driver, xpath):
        try:
            driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True
    
def crawl_href():
    driver = webdriver.Chrome(
        service = Service(ChromeDriverManager().install()), 
        chrome_options= options
    )
    driver.get(
        "https://www.pharmaceutical-technology.com/company-a-z/"
    )
    WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//section[@id='s']/div[@class='cell feature grid-x border-bottom u-mb-3'][70]/div[@class='cell large-8 articles']/h3[@class='wp-noreslt']/a")
                )
            )
    path = "//div[@class='cell feature grid-x border-bottom u-mb-3']/div[@class='cell large-8 articles']/h3[@class='wp-noreslt']/a"
    list_href = [value.get_attribute('href') for value in driver.find_elements(By.XPATH,path)]
    driver.close()
    return list_href

def crawl_result(path):

    driver = webdriver.Chrome(
        service = Service(ChromeDriverManager().install()), 
        chrome_options= options
    )
    driver.get(
        path
    )
    # dict_tmp = dict.fromkeys(['web','email','address','phone'])
    try:
        driver.execute_script("arguments[0].click();",driver.find_element(By.XPATH,"//button[normalize-space()='Contact Details']"))
        time.sleep(1)
        header  = driver.find_element(By.XPATH, "//header[@class='header-category']/h1").text
        if check_exists_by_xpath(driver,"//div[@class='grid-x']/div[@class='cell medium-3'][1]/div[@class='description'][1]/a"):
            web = driver.find_element(By.XPATH,"//div[@class='grid-x']/div[@class='cell medium-3'][1]/div[@class='description'][1]/a").get_attribute('href')
        else: 
            web = ''
        if check_exists_by_xpath(driver,"//div[@class='grid-x']/div[@class='cell medium-3'][1]/div[@class='description'][2]/a"):
            email = driver.find_element(By.XPATH,"//div[@class='grid-x']/div[@class='cell medium-3'][1]/div[@class='description'][2]/a").text
        else:
            email = ''
        if check_exists_by_xpath(driver,"//div[@class='grid-x']/div[@class='cell medium-3 '][1]/div[@class='description'][1]"):
            address = driver.find_element(By.XPATH,"//div[@class='grid-x']/div[@class='cell medium-3 '][1]/div[@class='description'][1]").text
            address = address.replace("\n",'')
        else:
            address = ''
        
        if check_exists_by_xpath(driver,"//div[@class='grid-x']/div[@class='cell medium-3 '][1]/div[@class='description'][2]/a"):

            phone = driver.find_element(By.XPATH,"//div[@class='grid-x']/div[@class='cell medium-3 '][1]/div[@class='description'][2]/a").text
        else:
            phone = ''
        if check_exists_by_xpath(driver,"//div[@class='grid-x']/div[@class='cell medium-3'][2]/div[@class='description'][3]/a[@class='c-post-content__excerpt']"):
            fax = driver.find_element(By.XPATH,"//div[@class='grid-x']/div[@class='cell medium-3'][2]/div[@class='description'][3]/a[@class='c-post-content__excerpt']").text
        else:
            fax = ''
        dict_tmp = {'header': header,
                    'web': web,
                    'email': email,
                    'address' : address,
                    'phone': phone,
                    'fax': fax
                    }
        data = pd.DataFrame([dict_tmp])
        result_path = "/Users/dinhvan/Projects/Code/crawl/selenium/pharmaceutical_technology/pharmaceutical_technology.csv"
        data.to_csv(result_path, mode='a', header=not os.path.exists(result_path), index = False)
        driver.close()
        # return dict_tmp
    except Exception as e:
        driver.close()
        print(e)
if __name__ == '__main__':
    # href = 'https://www.pharmaceutical-technology.com/contractors/clinical-it-systems/5k-pharma-consulting-services/'
    for href in crawl_href():
        crawl_result(href)  
        print(href)     