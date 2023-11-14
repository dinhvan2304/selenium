from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
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
from sqlalchemy.dialects.mysql import LONGTEXT, JSON
from datetime import date, datetime, timedelta
import time
import re
import json
from sqlalchemy import create_engine
from urllib.parse import quote
import sys

missing_dict = {}

ma_ttp ={
    'hanoi': 'HNI', 
    'vinhphuc': 'VPC', 
    'hoabinh': 'HBH', 
    'bacninh': 'BNH', 
    'backan': 'BCN', 
    'laocai': 'LCI', 
    'langson': 'LSN', 
    'bacgiang': 'BGG', 
    'caobang': 'CBG', 
    'thainguyen': 'TNN', 
    'phutho': 'PTO', 
    'tuyenquang': 'TQG', 
    'yenbai': 'YBI', 
    'sonla': 'SLA', 
    'dienbien': 'DBN', 
    'laichau': 'LCU', 
    'hagiang': 'HGG', 
    'hanam': 'HNM', 
    'namdinh': 'NDH', 
    'thaibinh': 'TBH', 
    'haiduong': 'HDG', 
    'haiphong': 'HPG', 
    'quangninh': 'QNH', 
    'hungyen': 'HYN', 
    'ninhbinh': 'NBH', 
    'thanhhoa': 'THA', 
    'nghean': 'NAN', 
    'hatinh': 'HTH', 
    'quangbinh': 'QBH', 
    'quangtri': 'QTI', 
    'thuathien-hue': 'HUE', 
    'quangnam': 'QNM', 
    'quangngai': 'QNI', 
    'binhdinh': 'BDH', 
    'gialai': 'GLI', 
    'daklak': 'DLC', 
    'daknong': 'DKN', 
    'phuyen': 'PYN', 
    'khanhhoa': 'KHA', 
    'kontum': 'KTM', 
    'danang': 'DNG', 
    'lamdong': 'LDG', 
    'binhthuan': 'BTN', 
    'ninhthuan': 'NTN', 
    'hochiminh': 'HCM', 
    'dongnai': 'DNI', 
    'binhduong': 'BDG', 
    'tayninh': 'TNH', 
    'baria-vungtau': 'VTU', 
    'binhphuoc': 'BPC', 
    'longan': 'LAN', 
    'tiengiang': 'TGG', 
    'bentre': 'BTE', 
    'travinh': 'TVH', 
    'vinhlong': 'VLG', 
    'cantho': 'CTO', 
    'haugiang': 'HAG', 
    'dongthap': 'DTP', 
    'angiang': 'AGG', 
    'kiengiang': 'KGG', 
    'camau': 'CMU', 
    'soctrang': 'STG', 
    'baclieu': 'BLU'
    }

phone_prefix_vina = {
    "8496": "Viettel",
    "8497": "Viettel",
    "8498": "Viettel",
    "8432": "Viettel",
    "8433": "Viettel",
    "8434": "Viettel",
    "8435": "Viettel",
    "8436": "Viettel",
    "8437": "Viettel",
    "8438": "Viettel",
    "8439": "Viettel",
    "8486": "Viettel",
    "8490": "Mobifone",
    "8493": "Mobifone",
    "8470": "Mobifone",
    "8489": "Mobifone",
    "8477": "Mobifone",
    "8476": "Mobifone",
    "8478": "Mobifone",
    "8479": "Mobifone",
    "8491": "Vinaphone",
    "8494": "Vinaphone",
    "8481": "Vinaphone",
    "8482": "Vinaphone",
    "8483": "Vinaphone",
    "8484": "Vinaphone",
    "8485": "Vinaphone",
    "8488": "Vinaphone",
    "8499": "Gmobile",
    "8459": "Gmobile",
    "8492": "Vietnamobile",
    "8456": "Vietnamobile",
    "8458": "Vietnamobile",
}

khdn_tinh_id = {
    "HNI": "21",
    "VPC": "58",
    "HBH": "65",
    "BNH": "5",
    "BCN": "4",
    "LCI": "34",
    "LSN": "33",
    "BGG": "3",
    "CBG": "12",
    "TNN": "61",
    "PTO": "59",
    "TQG": "56",
    "YBI": "60",
    "SLA": "49",
    "DBN": "22",
    "LCU": "32",
    "HGG": "20",
    "HNM": "25",
    "NDH": "37",
    "TBH": "51",
    "HDG": "27",
    "HPG": "26",
    "QNH": "45",
    "HYN": "24",
    "NBH": "39",
    "THA": "52",
    "NAN": "38",
    "HTH": "23",
    "QBH": "42",
    "QTI": "46",
    "HUE": "53",
    "QNM": "43", 
    "QNI": "44",
    "BDH": "6",
    "GLI": "19",
    "DLC": "16",
    "DKN": "64",
    "PYN": "41",
    "KHA": "29",
    "KTM": "31",
    "DNG": "15",
    "LDG": "35",
    "BTN": "10",
    "NTN": "40",
    "HCM": "28",
    "DNI": "17",
    "BDG": "8",
    "TNH": "50",
    "VTU": "2",
    "BPC": "9",
    "LAN": "36",
    "TGG": "54",
    "BTE": "7",
    "TVH": "55",
    "VLG": "57",
    "CTO": "13",
    "HAG": "66",
    "DTP": "18",
    "AGG": "1",
    "KGG": "30",
    "CMU": "14",
    "STG": "47",
    "BLU": "11",
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
    "TNN": "TN",
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
}

khdn_tinh_code = {
    'an giang':'1',
    'bình dương':'8',
    'bình phước':'9',
    'bình thuận':'10',
    'bình định':'6',
    'bạc liêu':'11',
    'bắc cạn':'4',
    'bắc giang':'3',
    'bắc ninh':'5',
    'bến tre':'7',
    'cao bằng':'12',
    'cà mau':'14',
    'cần thơ':'13',
    'gia lai':'19',
    'huế':'53',
    'hà giang':'20',
    'hà nam':'25',
    'hà nội':'21',
    'hà tĩnh':'23',
    'hòa bình':'65',
    'hưng yên':'24',
    'hải dương':'27',
    'hải phòng':'26',
    'hậu giang':'66',
    'khánh hoà':'29',
    'không xác định':'99',
    'kiên giang':'30',
    'kon tum':'31',
    'lai châu':'32',
    'long an':'36',
    'lào cai':'34',
    'lâm đồng':'35',
    'lạng sơn':'33',
    'nam định':'37',
    'net':'67',
    'nghệ an':'38',
    'ninh bình':'39',
    'ninh thuận':'40',
    'phú thọ':'59',
    'phú yên':'41',
    'quảng bình':'42',
    'quảng nam':'43',
    'quảng ngãi':'44',
    'quảng ninh':'45',
    'quảng trị':'46',
    'quốc tế (vti)':'98',
    'sóc trăng':'47',
    'sơn la':'49',
    'chí minh':'28',
    'đà nẵng':'15',
    'thanh hoá':'52',
    'thái bình':'51',
    'thái nguyên':'61',
    'tiền giang':'54',
    'trà vinh':'55',
    'tuyên quang':'56',
    'tây ninh':'50',
    'điện biên':'22',
    'vinaphone':'100',
    'vĩnh long':'57',
    'vĩnh phúc':'58',
    'vũng tàu':'2',
    'yên bái':'60',
    'đắk lắk':'16',
    'đắk nông':'64',
    'đồng nai':'17',
    'đồng tháp':'18',
}

vung_ttp = {
    "MB": "Lào Cai,  Điện Biên, Hòa Bình, Lai Châu, Sơn La, Hà Giang, Cao Bằng, Bắc Kạn, Lạng Sơn, Tuyên Quang, Thái Nguyên, Phú Thọ, Bắc Giang, Quảng Ninh, Bắc Ninh, Hà Nam, Hà Nội, Hải Dương, Thanh Hoá, Hưng Yên,  Nam Định, Thái Bình, Vĩnh Phúc",
    "MT": "Yên Bái, Nghệ An, Ninh Bình, Tuyên Quang, Hà Tĩnh , Quảng Bình,  Quảng Trị, Thừa Thiên-Huế, Đà Nẵng, Quảng Nam, Quảng Ngãi, Bình Định, Phú Yên, Khánh Hòa, KonTum, Gia Lai, Đắk Lắk, Đắk Nông, Hải Phòng",
    "MN": "Bình Phước, Ninh Thuận, Bình Thuận, Bình Dương, Đồng Nai, Tây Ninh, Bà Rịa-Vũng Tàu, Thành phố Hồ Chí Minh, Long An, Đồng Tháp, Tiền Giang, An Giang, Bến Tre, Vĩnh Long, Trà Vinh, Hậu Giang, Kiên Giang, Sóc Trăng, Bạc Liêu, Cà Mau, Thành phố Cần Thơ, Lâm Đồng",
}

def get_city_name(location):
    location = no_accent_vietnamese(location)
    location = location.lower()
    
    city_name = ''
    if 'ho chi minh' in location or 'hcm' in location:
        city_name = 'Hồ Chí Minh'
    elif 'ha noi' in location:
        city_name ='Hà Nội'
    elif 'dan ang' in location:
        city_name ='Đà Nẵng'
    elif 'hai phong' in location:
        city_name ='Hải Phòng'
    elif 'thanh hoa' in location:
        city_name = 'Thanh Hoá'
    elif 'hung yen' in location:
        city_name ='Hưng Yên'
    elif 'vung tau' in location:
        city_name ='Bà Rịa - Vũng Tàu' 
    elif 'bac giang' in location:
        city_name ='Bắc Giang'
    elif 'thai nguyen' in location:
        city_name ='Thái Nguyên' 
    elif 'bac kan' in location:
        city_name ='Bắc Kạn'  
    elif 'bac lieu' in location:
        city_name ='Bạc Liêu' 
    elif 'bac ninh' in location:
        city_name ='Bắc Ninh'
    elif 'ben tre' in location:
        city_name ='Bến Tre'
    elif 'binh dinh' in location:
        city_name ='Bình Định' 
    elif 'binh duong' in location:
        city_name ='Bình Dương'  
    elif 'binh phuoc' in location:
        city_name ='Bình Phước'
    elif 'binh thuan' in location:
        city_name ='Bình Thuận'
    elif 'ca mau' in location:
        city_name ='Cà Mau' 
    elif 'can tho' in location:
        city_name ='Cần Thơ'
    elif 'cao bang' in location:
        city_name ='Cao Bằng'
    elif 'dak lak' in location:
        city_name ='Đắk Lắk'
    elif 'dak nong' in location:
        city_name ='Đắk Nông' 
    elif 'dong nai' in location:
        city_name ='Đồng Nai'
    elif 'dong thap' in location:
        city_name ='Đồng Tháp'
    elif 'gia lai' in location:
        city_name ='Gia Lai'
    elif 'ha giang' in location:
        city_name ='Hà Giang'
    elif 'ha nam' in location:
        city_name ='Hà Nam'
    elif 'ha tinh' in location:
        city_name ='Hà Tĩnh'
    elif 'hai duong' in location:
        city_name ='Hải Dương'  
    elif 'hau giang' in location:
        city_name ='Hậu Giang' 
    elif 'hoa binh' in location:
        city_name ='Hòa Bình' 
    elif 'khanh hoa' in location:
        city_name ='Khánh Hòa' 
    elif 'kien giang' in location:
        city_name ='Kiên Giang' 
    elif 'kon tum' in location:
        city_name ='Kon Tum'
    elif 'lai chau' in location:
        city_name ='Lai Châu' 
    elif 'lam dong' in location:
        city_name ='Lâm Đồng' 
    elif 'lang son' in location:
        city_name ='Lạng Sơn' 
    elif 'lao cai' in location:
        city_name ='Lào Cai'
    elif 'lon gan' in location:
        city_name ='Long An'
    elif 'nam dinh' in location:
        city_name ='Nam Định'
    elif 'nghe an' in location:
        city_name ='Nghệ An'
    elif 'ninh binh' in location:
        city_name ='Ninh Bình'
    elif 'ninh thuan' in location:
        city_name ='Ninh Thuận' 
    elif 'phu tho' in location:
        city_name ='Phú Thọ'
    elif 'phu yen' in location:
        city_name ='Phú Yên'
    elif 'quang binh' in location:
        city_name ='Quảng Bình'
    elif 'quang nam' in location:
        city_name ='Quảng Nam'
    elif 'quang ngai' in location:
        city_name ='Quảng Ngãi'
    elif 'quang ninh' in location:
        city_name ='Quảng Ninh'
    elif 'quang tri' in location:
        city_name ='Quảng Trị'
    elif 'soc trang' in location:
        city_name ='Sóc Trăng'
    elif 'son la' in location:
        city_name ='Sơn La'
    elif 'tay ninh' in location:
        city_name ='Tây Ninh'
    elif 'thua thien' in location:
        city_name ='Thừa Thiên - Huế'
    elif 'tien giang' in location:
        city_name ='Tiền Giang'
    elif 'tra vinh' in location:
        city_name ='Trà Vinh'
    elif 'tuyen quang' in location:
        city_name ='Tuyên Quang'
    elif 'vinh long' in location:
        city_name ='Vĩnh Long'
    elif 'vinh phuc' in location:
        city_name ='Vĩnh Phúc'
    elif 'yen bai' in location:
        city_name ='Yên Bái'
    elif 'thai binh' in location:
        city_name ='Thái Bình'
    elif 'dien bien' in location:
        city_name ='Điện Biên'
    elif 'an giang' in location:
        city_name ='An Giang'
    else:
        city_name = 'Không xác định'
    return city_name

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

def no_accent_vietnamese(s):
    s = re.sub('[áàảãạăắằẳẵặâấầẩẫậ]', 'a', s)
    s = re.sub('[ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬ]', 'A', s)
    s = re.sub('[éèẻẽẹêếềểễệ]', 'e', s)
    s = re.sub('[ÉÈẺẼẸÊẾỀỂỄỆ]', 'E', s)
    s = re.sub('[óòỏõọôốồổỗộơớờởỡợ]', 'o', s)
    s = re.sub('[ÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢ]', 'O', s)
    s = re.sub('[íìỉĩị]', 'i', s)
    s = re.sub('[ÍÌỈĨỊ]', 'I', s)
    s = re.sub('[úùủũụưứừửữự]', 'u', s)
    s = re.sub('[ÚÙỦŨỤƯỨỪỬỮỰ]', 'U', s)
    s = re.sub('[ýỳỷỹỵ]', 'y', s)
    s = re.sub('[ÝỲỶỸỴ]', 'Y', s)
    s = re.sub('đ', 'd', s)
    s = re.sub('Đ', 'D', s)
    return s

def get_location_name_detail(location):
    location_lower = location.lower()
    
    number_of_comma = location.count(',')
    number_of_dash  = location.count('-')
    
    location_split = []
    location_split_solved = []
    
    if number_of_comma < number_of_dash :
        location_split = location.split('-')
    else:
        location_split = location.split(',')
    
    
    town, district, city = '','',''
    if(len(location_split) >= 3):
        location_split_solved = [i.lower() for i in location_split]
        if ('phường' in location_lower) or ('xã' in location_lower) or ('thị trấn' in location_lower):
            index_town = [idx for idx, s in enumerate(location_split_solved) if ('phường' in s) or ('xã' in s) or ('thị trấn' in s)][0]
            town = location_split[index_town].strip()
            location_detail = ['quận', 'huyện', 'thành phố', 'tp']
            if any([value in location_lower for value in location_detail]):
                index_district = [idx for idx, s in enumerate(location_split_solved) if ('quận' in s) or ('huyện' in s) or ('tp' in s) or ('thành phố' in s)][0]
                if(index_district > index_town) : 
                    district = location_split[index_district].strip()
                if(index_district < len(location_split)-1) and ('việt nam' not in location_split[index_district+1]):
                    city = location_split[index_district+1].strip()
    return [town, district]
    
def get_location_name(s):
    s = re.sub(r'^thành phố|^quận|^huyện|^thị xã|^xã|^phường|^thị trấn|^tp|^tỉnh', '', s)
    s = s.strip()
    return s

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
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        chrome_options=options, 
        desired_capabilities=capabilities
    )
    
    try:
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
                
                town, district= get_location_name_detail(location)
                city = get_city_name(location)
                
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
                
                # #? Convert to dataFrame
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
   
    """Fix columns"""
    columns = ['Tên công ty','Mã số thuế', 'Mã số thuế cá nhân','Địa chỉ','Người đại diện','Điện thoại','Ngày hoạt động','Quản lý bởi','Loại hình DN','Tình trạng','Ngành nghề kinh doanh chính','Loại ngành nghề','Mã ngành nghề','Ngành nghề kinh doanh','Phường/Xã','Quận/Huyện','Tỉnh/Thành Phố','Mã tỉnh','Miền','URL','Trạng thái invoice','URL invoice','Tên invoice','Mã số thuế invoice','Cảnh báo','Tên quốc tế','Tên viết tắt', 'Trạng thái']
    
    """Get list 'mã số thuế' last using compare columns"""
    # sqlEngine = create_engine("mysql+pymysql://tuanpt:%s@123.31.19.244:3306/hkd" % quote("Data_2021"))
    # query_origin = "SELECT * from doanh_thu_dn"
    # data_for_comparison = pd.read_sql(query_origin, con=sqlEngine)
    # data_stop_working = data_for_comparison[['MST','TRANG_THAI']].loc[(data_for_comparison['TRANG_THAI'] == 'Đã giải thể, phá sản, chấm dứt tồn tại') | (data_for_comparison['TRANG_THAI'] == 'Tạm ngừng kinh doanh')]
    
    # data_crawled = pd.read_csv('/home/ptdl/Documents/Projects/masothue_crawl/dnm_update/result/output_dnm.csv',dtype = str)
    # print('Total crawled: ' + str(len(data_crawled)))
    # mst_last = data_crawled['Mã số thuế'].iloc[-1]

    mst_in_db_raw = pd.read_csv('/Users/dinhvan/Projects/Code/crawl_data/selenium/ma_so_thue/dnm/mst_in_db_2.csv', dtype = str)
    mst_in_db_raw['mst'] = mst_in_db_raw['mst'].str.lstrip("'")
    list_mst = mst_in_db_raw['mst'].values.tolist()
    # mst_removed = mst_in_db_raw[~mst_in_db_raw['mst'].isin(data_stop_working['MST'])]
    
    # list_mst_in_db_removed = mst_removed['mst'].values.tolist()
    # list_mst = list_mst_in_db_removed[list_mst_in_db_removed.index(mst_last):]
    
    # print(list_mst[:10])

    current_date = datetime.now()
    current_date = current_date.strftime("%Y_%m_%d")
    current_path = os.path.dirname(os.path.abspath(__file__))

    # list_mst = ['3700192431','0211411947']
    resutl_path='/Users/dinhvan/Projects/Code/crawl_data/selenium/ma_so_thue/dnm/output_dnm.csv'
    missing_mst_path='/Users/dinhvan/Projects/Code/crawl_data/selenium/ma_so_thue/dnm/output_dnm_missing.csv'
    for mst in list_mst[180000:]:
        data_total, missing_total = crawl_dnm_info(mst)

        data_total.to_csv(resutl_path, mode='a', header=not os.path.exists(resutl_path), index = False)
        if len(missing_total) != 0:
            missing_total.to_csv(missing_mst_path,mode='a', header=not os.path.exists(missing_mst_path), index = False)

