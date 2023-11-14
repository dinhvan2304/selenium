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
import numpy as np

def restart_sim(options):
    driver = webdriver.Chrome(
            executable_path="/usr/bin/local/chromedriver",
            chrome_options=options, 
        )
    driver.get(
        "http://192.168.8.1/html/index.html"
    )

    WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH,"//div[@id='login_password_close']/input[@id='login_password']")
                )
        ) 

    pass_elem = driver.find_element(
        By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']")
    pass_elem.send_keys("Qtcd@123")

    login_btn = driver.find_element(
        By.ID, "login_btn")
    WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(
                (By.ID, "login_btn")
                )
        )
    login_btn.click()

    WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "ic_reboot")
                )
        )
    WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "ic_reboot")
                )
        ).click()
    WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[2]/div[@class='btn_normal_short pull-left margin_left_12']")
                )
        )
    WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[2]/div[@class='btn_normal_short pull-left margin_left_12']")
            )
        ).click() 
    
    WebDriverWait(driver, 600).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']")
                )
        )
    driver.quit()

def check_exists_by_xpath(driver, xpath):
        try:
            driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

def crawl_host_record(domain):
    
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless") 
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-setuid-sandbox")
    options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": '/home/ptdl/Documents/Projects/host_records/Result',
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
            },
        )
    
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
    # restart_sim(options)
    driver = webdriver.Chrome(
            executable_path="/usr/bin/local/chromedriver",
            chrome_options=options, 
        )
    
    try:
        driver.get(
                "https://dnsdumpster.com/"
                )
        
        input_search = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@id='hideform']/form/div[@class='form-group']/div[@class='col-md-6']/input[@id='regularInput']")
                    )
                )
                                                                                                               
        input_search.send_keys('{}'.format(domain))
        time.sleep(1)
        
        element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@id='hideform']/form/div[@id='formsubmit']/button[@class='btn btn-default']")
                    )
                )

        element.click();
        time.sleep(2)
        check = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='container'][1]/div[@class='row']/div[@class='col-md-12']/p")
                    )
                ).text
        domain_status = []
        if (check_exists_by_xpath(driver,"//div[@class='container'][1]/div[@class='row']/div[@class='col-md-12']/p")) and ('Too many requests from your IP address' in check):
            # driver.close()
            time.sleep(2)
            print('Starting restart sim !')
            restart_sim(options)
            print('Restart sim done !')
        # else:
            # WebDriverWait(driver, 20).until(
            #     EC.presence_of_element_located(
            #         (By.XPATH, "//div[@class='table-responsive'][4]/div/a[1]/button[@class='btn btn-default']")
            #         )
            #     )
            # if(check_exists_by_xpath(driver,"//div[@class='table-responsive'][4]/div/a[1]/button[@class='btn btn-default']")):
            #     download_button = driver.find_element(By.XPATH, "//div[@class='table-responsive'][4]/div/a[1]/button[@class='btn btn-default']")
            #     download_button.click()
            #     time.sleep(5)
            # else:
            #     print('Không có bản download')
        elif (check_exists_by_xpath(driver,"//div[@class='container'][1]/div[@class='row']/div[@class='col-md-12']/p")) and ('There was an error getting results' in check):
            domain_status.append('Không có kết quả tìm kiếm !')
            
        else:
            if check_exists_by_xpath(driver,"//div[@class='table-responsive'][4]/table[@class='table']//tr/td[@class='col-md-4']") == False:
                domain_status.append('Không có kết quả !')
            else:
                domain_status = [host.text for host in (driver.find_elements(By.XPATH,"//div[@class='table-responsive'][4]/table[@class='table']//tr/td[@class='col-md-4']"))]
                domain_status = [(host.split('\n'))[0] for host in domain_status]
                # print(domain_status)
     
        dict_result = {
            'domain': domain,
            'host'  : domain_status
            }

        data = pd.DataFrame([dict_result])
     
     
    except Exception as e:
        print('Domain error !')
        
    driver.close()
    print(domain)
    return data
        
if __name__ == '__main__':
    # domain = pd.read_excel('/home/ptdl/Documents/Projects/host_records/dai hoc_cao dang.xlsx', dtype = str)
    # domain['WEBSITE'] = domain["WEBSITE"].replace('',None)
    # domain.dropna(subset=['WEBSITE'], inplace=True)
    # domain['WEBSITE'] = domain["WEBSITE"].str.strip()
    # domain['WEBSITE'] = (domain['WEBSITE'].str.split('//')).str[1]
    # domain['WEBSITE'] = domain["WEBSITE"].str.replace('/','')
    # domain['WEBSITE'] = domain["WEBSITE"].str.replace('www.','')

    # list_domain = domain['WEBSITE'].values.tolist()
    list_domain = ['dav.edu.vn','cit.udn.vn','caodangnghebacgiang.edu.vn']
    for domain in list_domain:
        print(crawl_host_record(domain))