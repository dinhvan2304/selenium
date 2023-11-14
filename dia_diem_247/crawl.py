from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException, 
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

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--headless")   
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")

list_ttp = [
    'Hà Nội',
    'Hoà Bình', 
    'Bắc Ninh',
    'Bắc Kạn',
    'Lào Cai',
    'Lạng Sơn',
    'Bắc Giang',
    'Cao Bằng',
    'Thái Nguyên', 
    'Phú Thọ',
    'Tuyên Quang',
    'Yên Bái',
    'Sơn La',
    'Điện Biên',
    'Lai Châu',
    'Hà Giang',
    'Hà Nam',
    'Nam Định',
    'Thái Bình',
    'Hải Dương',
    'Hải Phòng', 
    'Quảng Ninh',
    'Vĩnh Phúc',
    'Hưng Yên',
    'Ninh Bình',
    'Thanh Hóa',
    'Nghệ An', 
    'Hà Tĩnh',
    'Quảng Bình',
    'Quảng Trị', 
    'Thừa Thiên-Huế',
    'Quảng Nam', 
    'Quảng Ngãi',
    'Bình Định',
    'Gia Lai',
    'Đắk Lắk',
    'Đắk Nông',
    'Phú Yên',
    'Khánh Hòa',
    'Kon Tum',
    'Đà Nẵng',
    'Lâm Đồng',
    'Bình Thuận',
    'Ninh Thuận',
    'TP Hồ Chí Minh',
    'Đồng Nai',
    'Bình Dương', 
    'Tây Ninh',
    'Bà Rịa-Vũng Tàu',
    'Bình Phước',
    'Long An',
    'Tiền Giang', 
    'Bến Tre',
    'Trà Vinh',
    'Vĩnh Long',
    'Cần Thơ',
    'Hậu Giang', 
    'Đồng Tháp',
    'An Giang',
    'Kiên Giang', 
    'Cà Mau',
    'Sóc Trăng',
    'Bạc Liêu'
    ]

def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s

def get_link(list_ttp):
    list_ttp_link, list_link = [],[]
    list_topic = [
                'spa-massage-c21.html', 
                'the-duc-tham-my-c22.html',
                'cham-soc-da-c24.html',
                'shop-hoa-my-pham-c25.html',
                'phong-kham-c30.html',
                'nha-thuoc-c32.html',
                'resort-c49.html'
                ]
    for city in list_ttp:
        list_ttp_link.append('https://diadiem247.com/' + no_accent_vietnamese(city.lower()).replace(' ','-'))
    
    # dict_ttp_link = {list_ttp[i]: list_ttp_link[i] for i in range(len(list_ttp))}
    list_link = []
    for ttp_link in list_ttp_link:
        for topic in list_topic:
            list_link.append(ttp_link + "/" + topic)
    
    return list_link

def main(link):
    list_link_full = []
    
    driver = webdriver.Chrome(
        service = Service(ChromeDriverManager().install()), 
        chrome_options= options
    )
    driver.get(link)
    time.sleep(1)
    
    """Scroll the web page to the end"""
    # html = driver.find_element(By.TAG_NAME, 'html')
    # html.send_keys(Keys.END)
    
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
                lastCount = lenOfPage
                time.sleep(2)
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                    match=True
                    
    result_number = int((WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='col-md-8 col-xs-12']/div[@class='row'][2]/div[@class='col-xs-12']/h2/b[2]")
                )
        ).text).replace(",",''))

    if result_number == 0:
        print('Không có kết quả tìm kiếmm !')
    elif result_number <= 8:
        list_xpath_value = driver.find_elements(By.XPATH,"//div[@class='col-md-8 col-xs-12']/div[@class='row']/div[@class='col-md-10 col-xs-9']/a")
        list_link_full = [value.get_attribute('href') for value in list_xpath_value]
    else:
        wait = WebDriverWait(driver, 10 )
        while True:
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='row main-content']/div[@class='col-md-8 col-xs-12']/a[@id='more-location']")))
                element.click()
            except (TimeoutException,ElementClickInterceptedException, ElementNotInteractableException):
                break
        list_xpath_value_1 = driver.find_elements(By.XPATH,"//div[@class='col-md-8 col-xs-12']/div[@class='row']/div[@class='col-md-10 col-xs-9']/a")
        list_xpath_value_2 = driver.find_elements(By.XPATH,"//div[@class='col-md-8 col-xs-12']/div[@class='row']/div[@class='col-md-10 col-xs-9']/div[@class='block-grid-v2-info rounded-bottom box-title']/a[1]")
        list_link_full_1 = [value.get_attribute('href') for value in list_xpath_value_1]
        list_link_full_2= [value.get_attribute('href') for value in list_xpath_value_2]
        list_link_full = list_link_full_1 + list_link_full_2
        
    url_df = pd.DataFrame()
    if len(list_link_full) == 0:
        print('Không có kết quả')
    else:
        url_df['url'] = pd.Series(list_link_full)
        url_df['url_source'] = link
    driver.close()
    return url_df
    
if __name__ == '__main__':
    # print(get_link(list_ttp))
    # print(main('https://diadiem247.com/ha-noi/dai-hoc-cao-dang-c33.html'))
    for link_ttp in get_link(list_ttp)[320:]:
        path = '/Users/dinhvan/Projects/Code/crawl/selenium/dia_diem_247/link.csv'
        data = main(link_ttp)
        data.to_csv(path, mode='a', header=not os.path.exists(path), index = False)
        print(get_link(list_ttp).index(link_ttp)+1)
        # print(data)
        # break
