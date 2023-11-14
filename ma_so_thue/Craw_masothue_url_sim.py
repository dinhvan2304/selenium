from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
    InvalidSessionIdException,
)
import os
import time
from datetime import date, datetime, timedelta
import shutil
from pathlib import Path
import pandas as pd
import re
from sqlalchemy import create_engine, text
from urllib.parse import quote
import json
from webdriver_manager.chrome import ChromeDriverManager

#from fake_useragent import UserAgent


current_path = os.path.dirname(os.path.abspath(__file__))
company_file_path = os.path.join(current_path, "bocao_new.csv")
masothue_path = os.path.join(current_path, "masothue_url.csv")
# current_date = datetime.now()
start_date = datetime.now() - timedelta(14)
current_date = datetime.now() - timedelta(1)

province = {
    "88": "An Giang",
    "89": "Vũng Tàu",
    "90": "Bắc Giang",
    "91": "Bắc Kạn",
    "92": "Bạc Liêu",
    "93": "Bắc Ninh",
    "94": "Bến Tre",
    "95": "Bình Định",
    "96": "Bình Dương",
    "97": "Bình Phước",
    "98": "Bình Thuận",
    "99": "Cà Mau",
    "100": "Cao Bằng",
    "101": "Đắk Lắk",
    "102": "Đắk Nông",
    "103": "Điện Biên",
    "104": "Đồng Nai",
    "105": "Đồng Tháp",
    "106": "Gia Lai",
    "107": "Hà Giang",
    "108": "Hà Tĩnh",
    "109": "Hải Dương",
    "110": "Hậu Giang",
    "111": "Hòa Bình",
    "112": "Hưng Yên",
    "113": "Khánh Hòa",
    "114": "Kiên Giang",
    "115": "KonTum",
    "116": "Lai Châu",
    "117": "Lâm Đồng",
    "118": "Lạng Sơn",
    "119": "Lào Cai",
    "120": "Long An",
    "121": "Nam Định",
    "122": "Nghệ An",
    "123": "Ninh Bình",
    "124": "Ninh Thuận",
    "125": "Phú Thọ",
    "126": "Phú Yên",
    "127": "Quảng Bình",
    "128": "Quảng Nam",
    "129": "Quảng Ngãi",
    "130": "Quảng Ninh",
    "131": "Quảng Trị",
    "132": "Sóc Trăng",
    "133": "Sơn La",
    "134": "Tây Ninh",
    "135": "Thái Bình",
    "136": "Thái Nguyên",
    "137": "Thanh Hoá",
    "138": "Thừa Thiên-Huế",
    "139": "Tiền Giang",
    "140": "Trà Vinh",
    "141": "Tuyên Quang",
    "142": "Vĩnh Long",
    "143": "Vĩnh Phúc",
    "144": "Yên Bái",
    "145": "Hà Nam",
    "81": "Cần Thơ",
    "82": "Đà Nẵng",
    "83": "Hà Nội",
    "86": "Hải Phòng",
    "87": "Hồ Chí Minh",
}

province_data_crawled = {}

def check_exists_by_xpath(browser, xpath):
    try:
        browser.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return True

def restart_sim(options):
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), chrome_options=options
    )
    browser.get(
        "http://192.168.8.1/html/index.html"
    )

    WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']"))
        ) 

    pass_elem = browser.find_element(By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']")
    pass_elem.send_keys("Qtcd@123")

    login_btn = browser.find_element(By.ID, "login_btn")
    WebDriverWait(browser, 60).until(
            EC.element_to_be_clickable((By.ID, "login_btn"))
        )
    login_btn.click()

    WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ic_reboot"))
        )
    WebDriverWait(browser, 60).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ic_reboot"))
        ).click()
    WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.XPATH, "//div[2]/div[@class='btn_normal_short pull-left margin_left_12']"))
        )
    WebDriverWait(browser, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//div[2]/div[@class='btn_normal_short pull-left margin_left_12']"))
        ).click() 
    
    WebDriverWait(browser, 600).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']"))
        )
    browser.quit()
    
def get_status(logs):
    for log in logs:
        if log['message']:
            d = json.loads(log['message'])
            try:
                content_type = 'text/html' in d['message']['params']['response']['headers']['content-type']
                response_received = d['message']['method'] == 'Network.responseReceived'
                if content_type and response_received:
                    return d['message']['params']['response']['status']
            except:
                pass

def crawl_masothue(mst_path):
    mst_new_list = mst_path
    options = Options()

    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), chrome_options=options, desired_capabilities=capabilities
    )
    
    mst_search_elem = None

    for mst in mst_new_list:
        if mst.isnumeric():
            print(mst)
            # mst = '0' + mst	
            if len(mst) == 9:
                mst = '0' + mst
            try:    
                browser.get(
                    "https://masothue.com/"
                )
                logs = browser.get_log('performance')
                print(get_status(logs))
                if get_status(logs) == 200:
                    WebDriverWait(browser, 60).until(
                        EC.presence_of_element_located((By.XPATH, "//form[@class='navbar-search tax-search']/div[@class='input-group']/input[@id='search']"))
                    ) 
                    mst_search_elem = browser.find_element(By.XPATH,
                        "//form[@class='navbar-search tax-search']/div[@class='input-group']/input[@id='search']"
                    )
                    if mst != "":
                        mst_search_elem.send_keys(mst)
                        btns_pdf = browser.find_element(By.XPATH,
                            "//button[@class='btn btn-secondary btn-search-submit']"
                        )
                        btns_pdf.click()
                    try:
                        WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@class='modal-header']/h5[@id='exampleModalLabel']")))
                        if check_exists_by_xpath(browser, "//div[@class='modal-content']/div[@class='modal-body']"):
                            time.sleep(1)
                            body_model = browser.find_element(By.XPATH, "//div[@class='modal-content']/div[@class='modal-body']")
                            body_text = body_model.text
                            print(body_text)
                            if 'Truy cập bị từ chối' in body_text:
                                print("Start restart sim")
                                restart_sim(options)
                                browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options, desired_capabilities=capabilities)
                                mst_search_elem.clear()
                                if mst != "":
                                    mst_search_elem.send_keys(mst)
                                    btns_pdf.click() 
                                break
                    except Exception as e:
                        print(e)
                    WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "table-taxinfo")))
                    with open(masothue_path, "a+") as fp:
                        fp.write(mst + "," + browser.current_url + "\n")
                    time.sleep(2)   
            except InvalidSessionIdException as e:
                browser.quit()
                browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options, desired_capabilities=capabilities)
            except Exception as e:    
                print(e)
                continue
                    
        else:
            browser.close()

    browser.quit()
        
if __name__ == "__main__":
    # sqlEngine = create_engine(
    #     "mysql+pymysql://root:%s@172.16.10.112:3306/hkd" % quote("Ptdl@123")
    # )
    # # sqlEngine = create_engine("mysql+pymysql://root:@127.0.0.1:3306/bid")
    # query_origin = "SELECT DISTINCT mst FROM clients"
    current_path = os.path.dirname(os.path.abspath(__file__))
    mst_existed = pd.read_csv(os.path.join(current_path, "all_mst.csv"), converters={'MST':str})
    url_crawed = pd.read_csv(os.path.join(current_path,"masothue_url.csv"), names=['mst', 'url'], converters={'mst':str})
    mst_existed = mst_existed[~mst_existed['MST'].isin(url_crawed['mst'])]
    mst_existed_list = mst_existed['MST'].values.tolist()

    crawl_masothue(mst_existed_list)

