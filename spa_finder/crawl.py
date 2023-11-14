from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
    
def crawl(path):
    driver = webdriver.Chrome(
        service = Service(ChromeDriverManager().install()), 
        chrome_options= options
    )
    try:
        driver.get(
            path
        )
        time.sleep()
        try:
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            while True:
                    list_href = driver.find_elements(By.XPATH,"//div[@class='card-container col col-12 col-sm-6 col-md-4 pa-0 custom-card-breakpoints']/a[@class='card v-card v-card--link v-sheet theme--light elevation-1']/div[@class='v-card__title']/div[@class='mt-2 mb-2']/div[@class='body-1 cursor-pointer vue-line-clamp']")
                    lastCount = lenOfPage
                    time.sleep(10)
                    print(len(list_href))
                    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                    if lastCount==lenOfPage or len(list_href) == 1100:
                        break
        except:           
            print("Done")
            
        time.sleep(10)
        list_href = driver.find_elements(By.XPATH,"//div[@class='card-container col col-12 col-sm-6 col-md-4 pa-0 custom-card-breakpoints']/a[@class='card v-card v-card--link v-sheet theme--light elevation-1']/div[@class='v-card__title']/div[@class='mt-2 mb-2']/div[@class='body-1 cursor-pointer vue-line-clamp']")
        for nb in range(1,len(list_href),1):
            name = driver.find_element(By.XPATH,"//div[@class='card-container col col-12 col-sm-6 col-md-4 pa-0 custom-card-breakpoints'][{}]/a[@class='card v-card v-card--link v-sheet theme--light elevation-1']/div[@class='v-card__title']/div[@class='mt-2 mb-2']/div[@class='body-1 cursor-pointer vue-line-clamp']".format(nb)).text
            href_name =  driver.find_element(By.XPATH,"//div[@class='card-container col col-12 col-sm-6 col-md-4 pa-0 custom-card-breakpoints'][{}]/a[@class='card v-card v-card--link v-sheet theme--light elevation-1']".format(nb)).get_attribute('href')
            dict_temp = {
                'name': name,
                'href': href_name
            }
            data = pd.DataFrame([dict_temp])
            result_path = "/Users/dinhvan/Projects/Code/web_scraping/selenium/spa_finder/href.csv"
            data.to_csv(result_path, mode='a', header=not os.path.exists(result_path), index = False)

        driver.close()
    except Exception as e:
        driver.close()
        print(e)

if __name__ == '__main__':
    path = 'https://www.spafinder.com/search?size=12&sort=relevance&distance=50&location=Thanh%20Xu%C3%A2n,%20VN'
    crawl(path)
