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

import os
import pandas as pd
from datetime import date, datetime, timedelta
import time
import re
import requests
import json
from sqlalchemy import create_engine
from urllib.parse import quote
import logging
import numpy as np
from pathlib import Path
import sys
from scrapy.cmdline import execute
import shutil


sys.path.append(os.path.dirname(os.path.abspath(__file__+"/../")))

TYPE_DNM = "new"
TYPE_DNGT = "crash"
PROCESS_CRAWL_MST = "crawl_mst"
PROCESS_CRAWL_URL = "crawl_url"

missing_dict = {}

ma_ttp ={
    'Hà Nội'       : 'HNI', 
    'Vĩnh Phúc'    : 'VPC', 
    'Hoà Bình'     : 'HBH', 
    'Bắc Ninh'     : 'BNH', 
    'Bắc Kạn'      : 'BCN', 
    'Lào Cai'      : 'LCI', 
    'Lạng Sơn'     : 'LSN', 
    'Bắc Giang'    : 'BGG', 
    'Cao Bằng'     : 'CBG', 
    'Thái Nguyên'  : 'TNN', 
    'Phú Thọ'      : 'PTO', 
    'Tuyên Quang'  : 'TQG', 
    'Yên Bái'      : 'YBI', 
    'Sơn La'       : 'SLA', 
    'Điện Biên'    : 'DBN', 
    'Lai Châu'     : 'LCU', 
    'Hà Giang'     : 'HGG', 
    'Hà Nam'       : 'HNM', 
    'Nam Định'     : 'NDH', 
    'Thái Bình'    : 'TBH', 
    'Hải Dương'    : 'HDG', 
    'Hải Phòng'    : 'HPG', 
    'Quảng Ninh'   : 'QNH', 
    'Hưng Yên'     : 'HYN', 
    'Ninh Bình'    : 'NBH', 
    'Thanh Hóa'    : 'THA', 
    'Nghệ An'      : 'NAN', 
    'Hà Tĩnh'      : 'HTH', 
    'Quảng Bình'   : 'QBH', 
    'Quảng Trị'    : 'QTI', 
    'Thừa Thiên - Huế': 'HUE', 
    'Quảng Nam'    : 'QNM', 
    'Quảng Ngãi'   : 'QNI', 
    'Bình Định'    : 'BDH', 
    'Gia Lai'      : 'GLI', 
    'Đắk Lắk'      : 'DLC', 
    'Đắk Nông'     : 'DKN', 
    'Phú Yên'      : 'PYN', 
    'Khánh Hòa'    : 'KHA', 
    'Kon Tum'      : 'KTM', 
    'Đà Nẵng'      : 'DNG', 
    'Lâm Đồng'     : 'LDG', 
    'Bình Thuận'   : 'BTN', 
    'Ninh Thuận'   : 'NTN', 
    'Hồ Chí Minh'  : 'HCM', 
    'Đồng Nai'     : 'DNI', 
    'Bình Dương'   : 'BDG', 
    'Tây Ninh'     : 'TNH', 
    'Bà Rịa - Vũng Tàu': 'VTU', 
    'Bình Phước'   : 'BPC', 
    'Long An'      : 'LAN', 
    'Tiền Giang'   : 'TGG', 
    'Bến Tre'      : 'BTE', 
    'Trà Vinh'     : 'TVH', 
    'Vĩnh Long'    : 'VLG', 
    'Cần Thơ'      : 'CTO', 
    'Hậu Giang'    : 'HAG', 
    'Đồng Tháp'    : 'DTP', 
    'An Giang'     : 'AGG', 
    'Kiên Giang'   : 'KGG', 
    'Cà Mau'       : 'CMU', 
    'Sóc Trăng'    : 'STG', 
    'Bạc Liêu'     : 'BLU',
    'Không xác định'    : '000'
    }

ma_mien = {
    "HNI": "MB",
    "VPC": "MB",
    "HBH": "MB",
    "BNH": "MB",
    "BCN": "MB",
    "LCI": "MB",
    "LSN": "MB",
    "BGG": "MB",
    "CBG": "MB",
    "TNN": "MB",
    "PTO": "MB",
    "TQG": "MT",
    "YBI": "MB",
    "SLA": "MB",
    "DBN": "MB",
    "LCU": "MB",
    "HGG": "MB",
    "HNM": "MB",
    "NDH": "MB",
    "TBH": "MB",
    "HDG": "MB",
    "HPG": "MT",
    "QNH": "MB",
    "HYN": "MB",
    "NBH": "MT",
    "THA": "MB",
    "NAN": "MT",
    "HTH": "MT",
    "QBH": "MT",
    "QTI": "MT",
    "HUE": "MT",
    "QNM": "MT",
    "QNI": "MT",
    "BDH": "MT",
    "GLI": "MT",
    "DLC": "MT",
    "DKN": "MT",
    "PYN": "MT",
    "KHA": "MT",
    "KTM": "MT",
    "DNG": "MT",
    "LDG": "MN",
    "BTN": "MN",
    "NTN": "MN",
    "HCM": "MN",
    "DNI": "MN",
    "BDG": "MN",
    "TNH": "MN",
    "VTU": "MN",
    "BPC": "MN",
    "LAN": "MN",
    "TGG": "MN",
    "BTE": "MN",
    "TVH": "MN",
    "VLG": "MN",
    "CTO": "MN",
    "HAG": "MN",
    "DTP": "MN",
    "AGG": "MN",
    "KGG": "MN",
    "CMU": "MN",
    "STG": "MN",
    "BLU": "MN",
    "000": "00"
}

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
    'Thừa Thiên - Huế',
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
    'Hồ Chí Minh',
    'Đồng Nai',
    'Bình Dương', 
    'Tây Ninh',
    'Bà Rịa - Vũng Tàu',
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

def get_city_name(location, list_ttp):
    location = no_accent_vietnamese(location)
    location = location.lower()
    location = location.replace(' ','')
    
    list_ttp_solved = [get_location_name(city.lower()) for city in list_ttp]
    list_ttp_solved = [no_accent_vietnamese(city_lower) for city_lower in list_ttp_solved]
    list_ttp_solved = [city_lower.replace(' ','') for city_lower in list_ttp_solved]
    
    list_index = [location.rfind(city) for city in list_ttp_solved ]
    max_value = max(list_index)
    if max_value == -1:
        return 'Không xác định'
    else:
        index_max_value = list_index.index(max_value)
        return list_ttp[index_max_value]

def get_city_code(city, ma_ttp):
    return ma_ttp[city]

def get_city_area(city_code, ma_mien):
    return ma_mien[city_code]

def get_location_name(s):
    s = re.sub(r'^thành phố|^huyện|^thị xã|^tx|^tt|^xã|^thị trấn|^tp|^tỉnh', '', s)
    s = s.strip()
    return s

def get_district_town_name(city,location,info_full):
    town, district = '',''
    
    full_district = info_full.loc[info_full['Tỉnh Thành Phố'] == city]
    full_district = full_district.drop_duplicates(subset=['Quận Huyện'], keep='first', ignore_index=True)
    
    list_district = full_district['Quận Huyện'].values.tolist()
    list_district.sort(key=lambda s: len(s))
    list_district_lower = [get_location_name(district.lower()) for district in list_district]
    list_district_lower = [no_accent_vietnamese(district) for district in list_district_lower]
    list_district_lower = [district.replace(' ','') for district in list_district_lower]
    
    city_solved = city.lower()
    city_solved = get_location_name(city_solved)
    city_solved = no_accent_vietnamese(city_solved)
    city_solved = city_solved.replace(' ','')
    
    location = location.lower()
    location = location.replace(' ','')
    # index_city = location.rfind(city_solved)
    location = no_accent_vietnamese(location)
    index_city = location.rfind(city_solved)
    # location = location.replace(' ','')
    
    if index_city == -1:
        return ['','']
    else: 
        location = location[:index_city]
    
        list_index_district = [location.rfind(value) for value in list_district_lower]
 
        if len(list_index_district) <= 1:
            return ['','']
        else:
            max_value_district = max(list_index_district)
            if max_value_district == -1:
                return ['','']
            else:
                index_max_value_district = [index for index, item in enumerate(list_index_district) if item == max_value_district][-1]
                district = list_district[index_max_value_district]

                full_town = info_full.loc[(info_full['Tỉnh Thành Phố'] == city) & (info_full['Quận Huyện'] == district)]
                
                list_town = full_town['Phường Xã'].values.tolist()
                list_town.sort(key=lambda s: len(s))
                list_town_solved = [get_location_name(town.lower()) for town in list_town]
                list_town_solved = [no_accent_vietnamese(town) for town in list_town_solved]
                list_town_solved = [town.replace(' ','') for town in list_town_solved]
                
                district_solve = get_location_name(district.lower())
                district_solve = no_accent_vietnamese(district_solve)
                district_solve = district_solve.replace(' ','')
                
                index_district = location.rfind(district_solve)
                location = location[:index_district]
                
                list_index_town= [location.rfind(value) for value in list_town_solved]
                
                if len(list_index_town) <= 1:
                    return [district,'']
                else:
                    max_value_town = max(list_index_town)
                    if max_value_town == -1:
                        return [district,'']
                    else:
                        index_max_value_town = [index for index, item in enumerate(list_index_town) if item == max_value_town][-1]
                        town = list_town[index_max_value_town]
                        return [district,town]

def connect_database():
    sqlEngine = create_engine(
        "mysql+pymysql://root:%s@localhost:3306/hkd" % quote("Van230420."))
    query_origin = "SELECT DISTINCT mst FROM gdt_origin LIMIT 150"
    mst_origin_sql = pd.read_sql(query_origin, con=sqlEngine)
    return mst_origin_sql['mst'].values.tolist()
    
def matchingKeys(dictionary, searchString):
        return [
            key for key, val in dictionary.items() if any(searchString in s for s in val)
        ]
        
nganh_chinh_code = {
    "A": [str(i).zfill(2) for i in range(1, 4)],
    "B": [str(i).zfill(2) for i in range(5, 10)],
    "C": [str(i).zfill(2) for i in range(10, 34)],
    "D": [str(35).zfill(2)],
    "E": [str(i).zfill(2) for i in range(36, 40)],
    "F": [str(i).zfill(2) for i in range(41, 44)],
    "G": [str(i).zfill(2) for i in range(45, 48)],
    "H": [str(i).zfill(2) for i in range(49, 54)],
    "I": [str(i).zfill(2) for i in range(55, 57)],
    "J": [str(i).zfill(2) for i in range(58, 64)],
    "K": [str(i).zfill(2) for i in range(64, 67)],
    "L": [str(68).zfill(2)],
    "M": [str(i).zfill(2) for i in range(69, 76)],
    "N": [str(i).zfill(2) for i in range(77, 83)],
    "O": [str(84).zfill(2)],
    "P": [str(85).zfill(2)],
    "Q": [str(i).zfill(2) for i in range(86, 89)],
    "R": [str(i).zfill(2) for i in range(90, 94)],
    "S": [str(i).zfill(2) for i in range(94, 97)],
    "T": [str(i).zfill(2) for i in range(97, 99)],
    "U": [str(99).zfill(2)],
}

def get_nganh_nghe_by_id(id):
    result = "Khác"
    if 1 <= id <= 3:
        result = "Nông nghiệp"
    elif 49 <= id <= 53:
        result = "Vận tải và Logictic"
    elif 5 <= id <= 43:
        result = "Công nghiệp và xây dựng"
    elif 86 <= id <= 88:
        result = "Y tế"
    elif id == 85:
        result = "Giáo dục"
    elif 45 <= id <= 47:
        result = "Phân phối, bán lẻ"
    elif id == 55 or id == 56 or id == 79:
        result = "Du lịch"
    return result

def restart_sim(options):
    driver = webdriver.Chrome(
        service = Service(ChromeDriverManager().install()), 
        chrome_options=options
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

def crawl_dnm_info(mst):
    try:
        Initial_path = os.path.join(current_path, "temp", current_date)
    
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless") 
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
        options.add_experimental_option(
                "prefs",
                {
                    "download.default_directory": Initial_path,
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": True,
                },
            )
        driver = webdriver.Chrome(
            executable_path="/usr/bin/local/chromedriver",
            chrome_options=options, 
        )
        
        data = pd.DataFrame()
        missing_mst = pd.DataFrame()
        dict_temp = {}
        global columns
        
        driver.get(
            "https://masothue.com/"
            )
        window_before = driver.window_handles[0]

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@id='search']")
                )
            ).send_keys('{}'.format(mst)
        )
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH,"(//button[@class='btn btn-secondary btn-search-submit'])")
                )
            ).click()
        time.sleep(2)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@class='modal-header']/h5[@id='exampleModalLabel']")
                )
            )
        if check_exists_by_xpath(driver, "//div[@class='modal-content']/div[@class='modal-body']"):
            time.sleep(1)
            body_model = driver.find_element(
                By.XPATH,"//div[@class='modal-content']/div[@class='modal-body']")
            body_text = body_model.text

        #? Restarting sim !
            if 'Truy cập bị từ chối' in body_text:
                missing_dict_temp = {'mst' : mst,
                                    'error' : 'Restart sim'
                                        }
                
                missing_mst = pd.DataFrame([missing_dict_temp])
                print("Starting restart sim !")
                restart_sim(options)
                print("Restart sim done !")
                
            # elif 'chưa có mã số thuế cá nhân' in body_text:
            #     dict_temp = {
            #         'Mã số thuế' : mst,
            #         'Trạng thái' : 'Mã số thuế chưa có mã số thuế cá nhân'
            #     }
            elif 'Không có kết quả! Vui lòng thử từ khóa tìm kiếm khác.' in body_text:
                dict_temp = {
                    'Mã số thuế' : mst,
                    'Trạng thái' : 'Không có kết quả'
                }
            else:
                list_keys,list_values = [],[]
                list_keys.append('Tên công ty')
                list_values.append(
                    driver.find_element(
                        By.XPATH,"//table[@class='table-taxinfo']/thead/tr/th"
                        ).text
                    )

                table_keys = driver.find_elements(
                    By.XPATH,"//table[@class='table-taxinfo']//tr/td[1]"
                    )
                [list_keys.append(key.text) for key in table_keys]
                        
                table_values = driver.find_elements(
                    By.XPATH,"//table[@class='table-taxinfo']//tr/td[2]"
                    )
                [list_values.append(value.text) for value in table_values]

                if len(list_keys) > 0:
                    del list_keys[-2:]
                
                #? Append main business 
                list_keys.extend(['Ngành nghề kinh doanh chính','Loại ngành nghề', 'Mã ngành nghề'])

                if check_exists_by_xpath(driver,"//table[@class='table']//tr/td[2]/strong"):
                    main_business = driver.find_element(
                            By.XPATH,"//table[@class='table']//tr/td[2]/strong/a"
                            ).text + ' ' + driver.find_element(
                            By.XPATH,"//table[@class='table']//tr/td[1]/strong/a"
                            ).text 
                    main_business_id_string = (driver.find_element(
                            By.XPATH,"//table[@class='table']//tr/td[1]/strong/a"
                            ).text)[:2]
                    main_business_id_int = int(main_business_id_string)
                    main_business_type = get_nganh_nghe_by_id(main_business_id_int)
                    main_business_code = matchingKeys(nganh_chinh_code,main_business_id_string)[0]
                    
                else:
                    main_business = ''
                    main_business_type = ''
                    main_business_code = ''
                list_values.extend([main_business,main_business_type,main_business_code])  

                #? Append business
                list_keys.append('Ngành nghề kinh doanh')
                list_business = []
                string_business = ''
                if check_exists_by_xpath(driver, "//div[@class='container']/h3[@class='h3']") and check_exists_by_xpath(driver, "//table[@class='table']/tbody/tr/td"):
                    table_business_elem = driver.find_elements(By.XPATH, "//table[@class='table']//tr/td/a")
                    table_business = [row.text for row in table_business_elem]
                    
                    number_business = len(table_business)
                    for index in range(0, number_business, 2):
                        list_business.append(table_business[index+1] + ' ' + table_business[index])
                        
                    if main_business != '':
                        list_business.append(main_business)
                    
                    for index, value in enumerate(list_business):
                        string_business += '{}. '.format(index+1) + value + '\n'  
                        
                    if(len(string_business) > 0):
                        string_business = string_business[:-1]
                        string_business = '"' + string_business + '"'

                list_values.append(string_business)

                #? Convert to dict
                dict_temp = dict(zip(list_keys,list_values))
                
                #? Solve location
                if('Địa chỉ' in dict_temp):
                    location = dict_temp.get('Địa chỉ')
                
                
                city = get_city_name(location,list_ttp)
                district, town = get_district_town_name(city,location,info_full)

                
                dict_temp['Phường/Xã'] = town
                dict_temp['Quận/Huyện'] = district
                dict_temp['Tỉnh/Thành Phố'] = city

                if city == '':
                    city_code = ''
                    city_id = ''
                else:
                    city_solved = get_location_name(city.lower())
                    city_solved = no_accent_vietnamese(city_solved)
                    city_solved = city_solved.replace(' ','')
                    city_solved = city_solved.replace('.','')
                    
                    city_code   = ma_ttp.get('{}'.format(city_solved))
                    city_id     = ma_mien.get('{}'.format(city_code))
                    
                dict_temp['Mã tỉnh'] = city_code
                dict_temp['Miền'] = city_id
                
                if ('Người đại diện' in dict_temp) and ('\n' in dict_temp['Người đại diện']):
                    dict_temp['Người đại diện'] = dict_temp['Người đại diện'].split('\n')[0]
                    
                # #? Add url to dict
                dict_temp['URL'] = driver.current_url
                # #? Add info company providing electronic invoices
                
                check_exist = "//div[@id='primary']/main[@id='main']/section[@class='animate-in-view fadeIn animated'][1]/div[@class='container']/div[@class='alert alert-success']"
                name_company_invoice,mst_invoice, url_invoice,status_invoice  = '','','',''      
                if(check_exists_by_xpath(driver,check_exist)):
                    #? Add invoice_status
                    if(driver.find_element(By.XPATH,check_exist).text == 'Doanh nghiệp đang sử dụng HOÁ ĐƠN TỰ IN.'):
                        status_invoice = 'Hoá đơn tự in'
                    elif(driver.find_element(By.XPATH,check_exist).text == 'Doanh nghiệp sử dụng HOÁ ĐƠN ĐIỆN TỬ của .'):
                        status_invoice = 'Không xác định'
                    else:
                        invoice_info = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH,"//div[@id='primary']/main[@id='main']/section[@class='animate-in-view fadeIn animated'][1]/div[@class='container']/div[@class='alert alert-success']")
                                    )
                                ).text
                        if 'HOÁ ĐƠN GIẤY' in invoice_info:
                            status_invoice = "Hoá đơn giấy"
                            name_company_invoice = (WebDriverWait(driver, 30).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH,"//div[@id='primary']/main[@id='main']/section[@class='animate-in-view fadeIn animated'][1]/div[@class='container']/div[@class='alert alert-success']/a")
                                    )
                                ).text
                                            )
                            driver.execute_script(
                                "arguments[0].click();",
                                driver.find_element(
                                    By.XPATH,"//div[@id='primary']/main[@id='main']/section[@class='animate-in-view fadeIn animated'][1]/div[@class='container']/div[@class='alert alert-success']/a")
                                    )
                            window_after = driver.window_handles[-1]
                            driver.switch_to.window(window_after)
                                
                            url_invoice = driver.current_url
                            mst_invoice = driver.find_element(By.XPATH,"//div[@class='container']/header/h1[@class='h1']").text
                            
                            driver.close()
                            driver.switch_to.window(window_before)
                        else:
                            status_invoice = "Hoá đơn điện tử"

                            #? Add invoice_company_name
                            name_company_invoice = (WebDriverWait(driver, 30).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH,"//div[@id='primary']/main[@id='main']/section[@class='animate-in-view fadeIn animated'][1]/div[@class='container']/div[@class='alert alert-success']/a")
                                    )
                                ).text
                                            )
                            
                            driver.execute_script(
                                "arguments[0].click();",
                                driver.find_element(
                                    By.XPATH,"//div[@id='primary']/main[@id='main']/section[@class='animate-in-view fadeIn animated'][1]/div[@class='container']/div[@class='alert alert-success']/a")
                                    )
                        
                            window_after = driver.window_handles[-1]
                            driver.switch_to.window(window_after)
                                
                            url_invoice = driver.current_url
                            mst_invoice = driver.find_element(By.XPATH,"//div[@class='container']/header/h1[@class='h1']").text
                            
                            driver.close()
                            driver.switch_to.window(window_before)
                else:
                    status_invoice = 'Không chứa thông tin hoá đơn'
                
                dict_temp['Trạng thái invoice'] = status_invoice
                dict_temp['URL invoice'] = url_invoice
                dict_temp['Tên invoice'] = name_company_invoice
                dict_temp['Mã số thuế invoice']  =  mst_invoice
                
                status = ''
                if check_exists_by_xpath(driver,"//div[@class='container']/div[@class='alert alert-danger']"):
                    status = driver.find_element(By.XPATH,"//div[@class='container']/div[@class='alert alert-danger']").text
                dict_temp['Cảnh báo'] = status
                 #? Convert to dataFrame
            data = pd.DataFrame([dict_temp])  
            data = data.reindex(columns=columns)

    except TimeoutException as e:
        print('TimeoutException')
        missing_dict_temp = {'mst' : mst,
                            'error' : 'TimeoutException'
                        }
        missing_mst = pd.DataFrame([missing_dict_temp])
        
        print("Starting restart sim !")
        restart_sim(options)
        print("Restart sim done !")

    except InvalidSessionIdException as e:
        print('InvalidSessionIdException')
        missing_dict_temp = {'mst' : mst,
                            'error' : 'InvalidSessionIdException' 
                        }
        missing_mst = pd.DataFrame([missing_dict_temp])
        
        print("Starting restart sim !")
        restart_sim(options)
        print("Restart sim done !")

    except NoSuchElementException as e:
        print('NoSuchElementException')
        missing_dict_temp = {'mst' : mst,
                            'error' : 'NoSuchElementException'
                        }
        missing_mst = pd.DataFrame([missing_dict_temp])
        
    except Exception as e:
        print('Exception')
        missing_dict_temp = {'mst' : mst,
                            'error' : 'Exception'
                        }
        missing_mst = pd.DataFrame([missing_dict_temp])
        
    driver.close()
    print(mst)
    return data, missing_mst
    
if __name__ == "__main__":
    current_date = datetime.now()
    current_date = current_date.strftime("%Y_%m_%d")
    current_path = os.path.dirname(os.path.abspath(__file__))
    
    info_full = pd.read_csv('/Users/dinhvan/Projects/Administrative Units/administrative_units.csv', dtype =str)
    
    """Fix columns"""
    columns = ['Tên công ty','Mã số thuế', 'Mã số thuế cá nhân','Địa chỉ','Người đại diện','Điện thoại','Ngày hoạt động','Quản lý bởi','Loại hình DN','Tình trạng','Ngành nghề kinh doanh chính','Loại ngành nghề','Mã ngành nghề','Ngành nghề kinh doanh','Phường/Xã','Quận/Huyện','Tỉnh/Thành Phố','Mã tỉnh','Miền','URL','Trạng thái invoice','URL invoice','Tên invoice','Mã số thuế invoice','Cảnh báo','Tên quốc tế','Tên viết tắt', 'Trạng thái']
    
    current_date = datetime.now()
    current_date = current_date.strftime("%Y_%m_%d")
    current_path = os.path.dirname(os.path.abspath(__file__))
    
    print(connect_database())