from re import escape
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    ElementNotInteractableException, 
    NoSuchElementException,
    TimeoutException)
import pandas as pd
import numpy as np
import re


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

def check_exists_by_xpath(driver,xpath):
    try:
        driver.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return True

def crawl(element):
    global dataFrame
    try:
        options = Options()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-setuid-sandbox")
        driver = webdriver.Chrome(
            options=options, 
            executable_path='/usr/local/bin/chromedriver')
        driver.get("https://www.tratencongty.com/")
        
        
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH,"//input[@class='form-control input-lg']")
                )
            ).send_keys('{}'.format(element)
                        )
            
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@class='btn btn-default btn-lg']")
                )
            ).click()
        
        result_number = (WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='col-xs-12 col-sm-9']/div[3]/h4")
                )
            ).text).split(" ")[1]

        list_key    = []
        list_value  = []
        
        list_key.append("name_input")
        list_value.append(element)
        
        list_key.append('name_result')
        if( result_number == '0'):
            list_value.append('Không có kết quả tìm kiếm !')
            
        elif(result_number == '1'):
            list_driver_temp = driver.find_element(By.XPATH,"//div[@class='col-xs-12 col-sm-9']/div[3]/div[@class='search-results']").text
            list_result_temp_split = list_driver_temp.split('\n')
            
            list_value.append(list_result_temp_split[0])
            
            list_key.append('mst')
            list_value.append(driver.find_element(By.XPATH,"//div[@class='col-xs-12 col-sm-9']/div[3]/div[@class='search-results'][1]/p/a").text)
            
            list_key.append('address')
            list_value.append(list_result_temp_split[2])
            
        else:
            list_driver_company = driver.find_elements(By.XPATH,"//div[@class='col-xs-12 col-sm-9']/div[3]/div[@class='search-results']")
            list_company = [i.text for i in list_driver_company]
            
            
            list_company_split = []
            for company in list_company:
                company_temp = company.split('\n')
                for i in range(3):
                    list_company_split.append(company_temp[i])
                    
            list_company_split_solved = []
            for value in list_company_split:
                list_company_split_solved.append(no_accent_vietnamese(value))
            
            set_company = set()
            for name_company in range(0,len(list_company_split_solved),3):
                set_company.add(list_company_split_solved[name_company])
        
            
            if len(set_company) < int(result_number):
                noti = 'Kết quả tìm kiếm trùng nhau : ' + str(int(result_number) - len(set_company))
                list_value.append(noti)
            else:
                
                list_len = []
                for value in range(0,len(list_company_split_solved),3):
                    list_len.append(len(list_company_split_solved[value]))
                    
                value = min(list_len)
                print(list_len)
                index_result = 3*list_len.index(value)
                print(index_result)
                
                list_value.append(list_company_split[index_result])
                list_key.append('mst')
                list_value.append(list_company_split[index_result+1])
                
                list_key.append('address')
                list_value.append(list_company_split[index_result+2])
                
                
        dict_result = dict(zip(list_key,list_value))
        print(dict_result)
        dataFrame_temp = pd.DataFrame([dict_result])
        dataFrame  = pd.concat([dataFrame,dataFrame_temp],ignore_index= True)
        dataFrame.to_csv('/Users/dinhvan/Documents/Projects/Crawl/selenium/SOE/result/SOE2/Result_search_CTC_plus.csv',index = False)
        driver.close()
    except  Exception as e:
        print(e)
        driver.close()
if __name__ == '__main__':
    
    dataFrame = pd.DataFrame()
    data_input  = pd.read_csv('/Users/dinhvan/Documents/Projects/Crawl/selenium/SOE/result/SOE2/Nhieu_ket_qua.csv',error_bad_lines=False)
    list_input = data_input['name_input'].values.tolist()
    # list_input = ['CÔNG TY TNHH MỘT THÀNH VIÊN VÀNG BẠC ĐÁ QUÝ NGÂN HÀNG THƯƠNG MẠI CỔ PHẦN CÔNG THƯƠNG VIỆT NAM']
    # list_input = ['CÔNG TY TNHH THIẾT BỊ PHỤ TÙNG HÒA PHÁT']
    count = len(list_input)
    for value in list_input:
        print(count)
        crawl(value)
        count -= 1