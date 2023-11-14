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
import re
import requests

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--headless")   
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")

import requests

from bs4 import BeautifulSoup as bs

import re

 

# def main(url):

 

#     response = requests.get(url)

 

#     if response.status_code == 200:

#         text = response.text

#         soup = str(bs(text,'html.parser').body)

#         emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+',soup)

#         emails_set= set(emails)
#         if len(emails_set)==0:
#             print('Email not exist')
#         else:
#             data = pd.DataFrame(emails_set, columns=['email'])
#             data['link'] = url
#             print(data)
#     else:
#         print('Website not connect')

# if __name__ == '__main__':
#     main('https://serenisalon.com/')


def get_email(url):
    driver = webdriver.Chrome(
        service = Service(ChromeDriverManager().install()), 
        chrome_options= options
    )
    try:
        driver.get(
            url
        )
        email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,4}"
        html = driver.page_source
        emails = re.findall(email_pattern, html)
        if len(emails)>0:
            for email in emails:
                if '.io' in email or '.png' in email:
                    emails.remove(email)
        emails = set(emails)
        data = pd.DataFrame(emails, columns=['email'])
        data['link'] = url
        
        result_path = "/Users/dinhvan/Projects/Code/web_scraping/selenium/get_email/email.csv"
        data.to_csv(result_path, mode='a', header=not os.path.exists(result_path), index = False)
        print(emails)

    except:
        print('Error')
    driver.close()
    
if __name__ == '__main__':
    data_url = pd.read_csv('/Users/dinhvan/Projects/Strong Body/data/send/XNK/spa_week.csv', dtype = str)
    urls = data_url['web'].values.tolist()
    # url = 'https://serenisalon.com/'
    for url in urls:
        if url is not None:
            get_email(url)