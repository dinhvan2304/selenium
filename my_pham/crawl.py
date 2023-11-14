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

def main():
    driver = webdriver.Chrome(
        service = Service(ChromeDriverManager().install()), 
        chrome_options= options
    )
    driver.get(
        "https://www.google.com/search?tbs=lf:1,lf_ui:10&tbm=lcl&sxsrf=APwXEdds8N-i550U3G6gthXB_ftITOZlSQ:1687322137001&q=c%E1%BB%ADa+h%C3%A0ng+m%E1%BB%B9+ph%E1%BA%A9m&rflfq=1&num=10&rllag=21034824,105785545,498&sa=X&ved=2ahUKEwjfxuPkxNP_AhWZ_WEKHa_bDKgQjGp6BAgYEAE&biw=1440&bih=764&dpr=2#rlfi=hd:;si:4457411337329438109,l,Chdj4butYSBow6BuZyBt4bu5IHBo4bqpbVoZIhdj4butYSBow6BuZyBt4bu5IHBo4bqpbZIBD2Nvc21ldGljc19zdG9yZaoBaAoJL20vMDE0dHJsEAEqGyIXY-G7rWEgaMOgbmcgbeG7uSBwaOG6qW0oQjIfEAEiG78szMgmZ1e6bnTri3_I7ugQ010s8gzkonC4qzIbEAIiF2Phu61hIGjDoG5nIG3hu7kgcGjhuqlt;mv:[[21.070477409233824,105.857793822968],[20.97289344767196,105.77419473239183]]"
    )

if __name__ == '__main__':
    main()