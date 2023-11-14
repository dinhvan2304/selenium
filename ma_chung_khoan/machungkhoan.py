from re import escape
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.common.exceptions import TimeoutException
import pandas as pd
import numpy as np

options = Options()
# options.headless = True
driver = webdriver.Chrome(options=options, executable_path=r'/Users/dinhvan/Downloads/chromedriver')
driver.get("https://masothue.com/")