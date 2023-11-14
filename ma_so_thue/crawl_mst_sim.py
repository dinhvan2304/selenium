# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# import time
# import pandas as pd
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import json
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.chrome.service import Service


# def check_exists_by_xpath(browser,xpath):
#     try:
#         browser.find_element(By.XPATH,xpath)
#     except NoSuchElementException:
#         return False
#     return True

# def restart_sim(options):
#     driver = webdriver.Chrome(
#         service=Service(ChromeDriverManager().install()), 
#         chrome_options=options
#     )
#     driver.get(
#         "http://192.168.8.1/html/index.html"
#     )

#     WebDriverWait(driver, 60).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']")
#                 )
#         ) 

#     pass_elem = driver.find_element(
#         By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']")
#     pass_elem.send_keys("Qtcd@123")

#     login_btn = driver.find_element(By.ID, "login_btn")
#     WebDriverWait(driver, 60).until(
#             EC.element_to_be_clickable(
#                 (By.ID, "login_btn")
#                 )
#         )
#     login_btn.click()

#     WebDriverWait(driver, 60).until(
#             EC.presence_of_element_located(
#                 (By.CLASS_NAME, "ic_reboot")
#                 )
#         )
#     WebDriverWait(driver, 60).until(
#             EC.element_to_be_clickable(
#                 (By.CLASS_NAME, "ic_reboot")
#                 )
#         ).click()
#     WebDriverWait(driver, 60).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, "//div[2]/div[@class='btn_normal_short pull-left margin_left_12']")
#                 )
#         )
#     WebDriverWait(driver, 60).until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, "//div[2]/div[@class='btn_normal_short pull-left margin_left_12']")
#                 )
#         ).click() 
    
#     WebDriverWait(driver, 600).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']")
#                 )
#         )
#     driver.quit()

# def crawl_mst_info(list_input):
#     global dataFrame
#     i = len(list_input)
#     for element in list_input:
#         print('-------------------------Còn {} mã số thuế nữa !!!--------------------------'.format(i))
#         i -= 1
#         try:
                
#             options = Options()
#             options.add_argument("--no-sandbox")
#             # options.add_argument("--headless")
#             options.add_argument("--disable-dev-shm-usage")
#             options.add_argument("--disable-setuid-sandbox")
                        
#             capabilities = DesiredCapabilities.CHROME.copy()
#             capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

#             driver = webdriver.Chrome(
#                 service=Service(ChromeDriverManager().install()), 
#                 chrome_options=options, 
#                 desired_capabilities=capabilities
#             )
            
#             driver.get("https://masothue.com/")
                        
#             WebDriverWait(driver, 30).until(
#                 EC.presence_of_element_located(
#                     (By.XPATH, "//input[@id='search']")
#                     )
#                 ).send_keys('{}'.format(element)
#                                 )
                        
#             WebDriverWait(driver, 30).until(
#                 EC.presence_of_element_located(
#                     (By.XPATH,"(//button[@class='btn btn-secondary btn-search-submit'])")
#                     )
#                 ).click()
                
#             time.sleep(2)
            
#             if check_exists_by_xpath(driver, "//div[@class='modal-content']/div[@class='modal-body']"):
#                 time.sleep(1)
#                 body_model = driver.find_element(
#                     By.XPATH, "//div[@class='modal-content']/div[@class='modal-body']"
#                     )
#                 body_text = body_model.text
#                 if 'Truy cập bị từ chối' in body_text:
#                     print("---------------------- Starting restart sim !----------------------")
#                     restart_sim(options)
#                     print("---------------------- Starting restart sim done !----------------------")

#                 list_keys = []
#                 list_values = []
#                 list_keys.append('Tên công ty')
#                 list_values.append(
#                     driver.find_element(
#                         By.XPATH,"//table[@class='table-taxinfo']/thead/tr/th"
#                         ).text
#                     )

#                 table_keys = driver.find_elements(
#                     By.XPATH,"//table[@class='table-taxinfo']//tr/td[1]"
#                     )
#                 for key in table_keys:
#                     list_keys.append(key.text)

#                 table_values = driver.find_elements(
#                     By.XPATH,"//table[@class='table-taxinfo']//tr/td[2]"
#                     )
#                 for value in table_values:
#                     list_values.append(value.text)
                        
#                 del list_keys[-2:]
                        
#                 list_keys.append('Ngành nghề kinh doanh')
#                 element_strong = "//table[@class='table']//tr/td[2]/strong"
#                 if check_exists_by_xpath(driver,element_strong):
#                     list_values.append(
#                         driver.find_element(
#                             By.XPATH,"//table[@class='table']//tr/td[2]/strong/a"
#                             ).text
#                         )
#                 else:
#                     list_values.append(None)
                        
#                 dict_result = dict(zip(list_keys,list_values))
#                 print(dict_result)
#                 # dataFrame_temp = pd.DataFrame([dict_result])
#                 # dataFrame  = pd.concat([dataFrame,dataFrame_temp],ignore_index= True)
#                 # dataFrame.to_csv('/Users/dinhvan/Documents/Projects/Crawl/selenium/masothue/data_output/Raw_23_11.csv', index = False, sep= ',')
#                 driver.close()
#         except Exception as e:
#             print(e)
#             print(element)
#             driver.close()
        
        
# if __name__ == '__main__':
#     # dataFrame = pd.DataFrame()
#     # data_input = pd.read_csv("/home/ptdl/Documents/Projects/chinhanh/SOE2_lost.csv",dtype = str)
#     # data_input.drop(data_input.loc[data_input['Mã số thuế SOE2'].isna()].index,inplace=True)
#     # data_input['Mã số thuế SOE2'] = data_input['Mã số thuế SOE2'].str.strip()
#     # data_input.drop(data_input.loc[data_input['Mã số thuế SOE2'].isna()].index,inplace=True)
#     # list_input = data_input['Mã số thuế SOE2'].values.tolist()
#     # list_input = list_input[765:]
#     # list_input = ['0305173688','0104093672','0102409426']
#     # crawl_mst_info(list_input)
    
    
#     pass

        
import requests
import json
import re
import pandas as pd
import numpy as np
import re 
import glob
import os
import time
#Library_selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service


khdn_quan_path = "/home/data/Documents/Crawl_info/khdn_data/quan"
khdn_phuong_path = "/home/data/Documents/Crawl_info/khdn_data/phuong"
gdt_province_path = "/home/data/Documents/Projects/get_customer_error/gdt_province.csv"

NUMBER_PAGE_SIZE = 10
PAGE_INDEX = 1
NUMBER_REQUEST = 1

dict_province_id = {
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
    'hồ chí minh':'28',
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

def check_exists_by_xpath(browser,xpath):
    try:
        browser.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return True

def restart_sim(options):
    print("Starting restart sim !")
    # options = Options()
    # options.add_argument("--no-sandbox")
    # options.add_argument("--headless")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-setuid-sandbox")
    
    driver = webdriver.Chrome(
        executable_path = "/usr/bin/chromedriver", 
        chrome_options = options
    )
    driver.get(
        "http://192.168.8.1/html/index.html"
    )

    WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']")
                )
        ) 

    pass_elem = driver.find_element(
        By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']")
    pass_elem.send_keys("Ptdl@2020")

    login_btn = driver.find_element(By.ID, "login_btn")
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
    print("Restarting sim done !")

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

def get_data_API():
    url = "http://10.156.4.137:5000/mapi/services/get_customer_error"

    payload = json.dumps({
      "username": "api_new_khdn",
      "password": "Api_New_KHDN_@02#",
      "page_size": NUMBER_PAGE_SIZE,
      "page_index": PAGE_INDEX
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers = headers, data = payload)
    list_data_API = response.json()['Data']
    df_data_API = pd.DataFrame(list_data_API)
    return df_data_API
    
def get_location_name(s):
    s = re.sub(r'^thành phố|^quận|^huyện|^thị xã|^xã|^phường|^thị trấn|^tp', '', s)
    s = s.strip()
    return s

def get_town_name(location):
    location_lower = location.lower()
    
    number_of_comma = location.count(',')
    number_of_dash  = location.count('-')
    
    location_split = []
    location_split_solved = []
    if number_of_comma < number_of_dash :
        location_split = location.split('-')
    else:
        location_split = location.split(',')
        
    location_split_solved = [i.lower() for i in location_split]
    
    if 'phường' in location_lower:
        index = [idx for idx, s in enumerate(location_split_solved) if 'phường' in s][0]
        town_name =  get_location_name(location_split[index])
        town_name = re.sub(' +',' ', town_name)
        town_name = town_name.strip()
        return town_name
    
    elif 'xã' in location_lower:
        index = [idx for idx, s in enumerate(location_split_solved) if 'xã' in s][0]
        town_name =  get_location_name(location_split[index])
        town_name = re.sub(' +',' ', town_name)
        town_name = town_name.strip()
        return town_name
    
    else:
        return 'không xác định'
    
def get_district_name(town_name,location,data_district):
    location_lower = location.lower()
    location_lower = location_lower.replace(' ','')

    town_name_lower = town_name.lower()
    
    data_district['xa'] = data_district['xa'].str.lower()
    district_info = data_district[data_district['xa'].str.contains(town_name_lower)]
    
    district_name = ''
    district_code = 0
    for index, row in district_info.iterrows():
        check_exist = row['huyen']
        check_exist = check_exist.lower()
        check_exist = check_exist.replace(' ','')
        if check_exist in location_lower:
            district_name = row['huyen']
            district_name = re.sub(' +',' ', district_name)
            district_name = district_name.strip()
            district_code = row['ma huyen']
            break
        else:
            district_name = 'không xác định'
    return district_name, district_code
    
def get_province_name(district_code, data_province):
    province_name = data_province['tinh'].loc[data_province['ma huyen'] == district_code]
    province_name = province_name.iloc[0]
    return province_name

def get_province_id(province_name):
    province_name = province_name.lower()
    province_name_solved = get_location_name(province_name)
    
    province_id = dict_province_id[province_name_solved]
    return province_id 
    
def get_district_id(province_id, district_name):
    district_id = 0
    district_df = None
    district_file_path = khdn_quan_path + "/{}.csv".format(province_id)
    try:
        district_df = pd.read_csv(district_file_path)
    except Exception as e:
        print("File khdn_quan_path not found: {}".format(khdn_quan_path))
    if district_df is not None:
        district_name = no_accent_vietnamese(district_name)
        district_name = district_name.lower()
        district_name = district_name.strip()
        district_info = district_df[district_df['NAME'].str.contains(district_name)]
        if len(district_info) > 0:
            district_id = district_info.iloc[0]['ID']
    return district_id

def get_town_id(district_name, town_name):
    district_name_solved = district_name.lower()
    district_name_solved = get_location_name(district_name_solved)
    district_name_solved = no_accent_vietnamese(district_name_solved)
    district_name_solved = district_name_solved + ".csv"

    town_id = 0
    town_df = None
    for district_path in glob.glob(khdn_phuong_path + "/*"):
        district_name_path = district_path.split("/")[-1]
        if district_name_solved in district_name_path:
            town_name_path = os.path.join(khdn_phuong_path,district_name_path)
    
    if town_name_path != "":
        try:
            town_df = pd.read_csv(town_name_path)
        except Exception as e:
            print("File khdn_quan_path not found: {}".format(khdn_phuong_path))
        if town_df is not None:
            town_name = no_accent_vietnamese(town_name)
            town_name = town_name.lower()
            town_name = town_name.strip()
            town_info = town_df[town_df['NAME'].str.contains(town_name)]
            if len(town_info) > 0:
                town_id = town_info.iloc[0]['ID']
    return town_id

def crawl_mst_error(element):
    dict_result = {}
    dataFrame = pd.DataFrame()
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--start-maximized")
                        
    driver = webdriver.Chrome(
        executable_path = "/usr/bin/chromedriver", 
        chrome_options = options
        )
    
    try:               
        driver.get("https://masothue.com/")
                        
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@id='search']")
                )
            ).send_keys('{}'.format(element)
        )
                        
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH,"(//button[@class='btn btn-secondary btn-search-submit'])")
                )
            ).click()
                
        time.sleep(2)
            
        if check_exists_by_xpath(driver, "//div[@class='modal-content']/div[@class='modal-body']"):
            time.sleep(1)
            body_model = driver.find_element(
                By.XPATH, "//div[@class='modal-content']/div[@class='modal-body']"
                )
            body_text = body_model.text
            if 'Truy cập bị từ chối' in body_text:
                driver.quit()
                restart_sim(options)
                    
            else:
                list_keys = []
                list_values = []
                
                list_keys.append('Tên công ty')
                list_values.append(
                    driver.find_element(
                        By.XPATH,"//table[@class='table-taxinfo']/thead/tr/th"
                        ).text
                    )

                table_keys = driver.find_elements(
                    By.XPATH,"//table[@class='table-taxinfo']//tr/td[1]"
                    )
                
                for key in table_keys:
                    list_keys.append(key.text)
                
                table_values = driver.find_elements(
                    By.XPATH,"//table[@class='table-taxinfo']//tr/td[2]"
                    )
                
                for value in table_values:
                    list_values.append(value.text)
                
                del list_keys[-2:]
                        
                list_keys.append('Ngành nghề kinh doanh')
                element_strong = "//table[@class='table']//tr/td[2]/strong"
                if check_exists_by_xpath(driver,element_strong):
                    list_values.append(
                        driver.find_element(
                            By.XPATH,"//table[@class='table']//tr/td[2]/strong/a"
                            ).text
                        )
                else:
                    list_values.append(None)
                        
                dict_temp = dict(zip(list_keys,list_values))
                
                location = dict_temp.get("Địa chỉ")
                town = get_town_name(location)
                
                district = get_district_name(town,location,data_province_full)[0]
                district_code = get_district_name(town,location,data_province_full)[1]
                
                province = get_province_name(district_code, data_province_full)
                province_id = get_province_id(province)
                
                district_id = get_district_id(province_id, district)
                town_id = get_town_id(district,town)
                
                manager = dict_temp.get("Người đại diện")
                if '\n' in manager:
                    manager_solved = manager.split('\n')
                    manager_solved = manager_solved[0]
                else:
                    manager_solved = manager
                
                dict_result = {'MST': dict_temp.get('Mã số thuế'),
                               'COMPANY_NAME' : dict_temp.get("Tên công ty"),
                               'TOWN' : town,
                               'TOWN_ID' : town_id,
                               'DISTRICT' : district,
                               'DISTRICT_ID' : district_id,
                               'PROVINCE' : province,
                               'PROVINCE_ID' : province_id,
                               'MAIN_BUSSINESS' : dict_temp.get('Ngành nghề kinh doanh'),
                               'PHONE' : dict_temp.get('Điện thoại'),
                               'MANAGER' : manager_solved
                               }
                print(dict_result)
                dataFrame = pd.DataFrame([dict_result])
                # dataFrame  = pd.concat([dataFrame,dataFrame_temp],ignore_index= True)
                # dataFrame.to_csv('/Users/dinhvan/Documents/Projects/Crawl/selenium/masothue/data_output/Raw_23_11.csv', index = False, sep= ',')
                driver.close()
    except Exception as e:
        print(e)
        print(element)
        driver.close()
        
    return dataFrame

if __name__ == "__main__":
    
    data_API = get_data_API()
    list_mst_error = data_API['MST'].values.tolist()
    data_province_full = pd.read_csv(gdt_province_path, dtype = str)
    
    print(crawl_mst_error("0302160137-003"))
    # restart_sim()
    
    # data_province_full = pd.read_csv(gdt_province_path, dtype = str)
    # location = "Thửa đất số 388, Tờ bản đồ số 58, Tổ 5, khu phố 9, đường Nguyễn Thị Minh Khai, Phường Phú Hòa, Thành phố Thủ Dầu Một, Tỉnh Bình Dương, Việt Nam"
    # town_name = get_town_name(location)
    # print(town_name)
    # district_name = get_district_name(town_name,location,data_province_full)[0]
    # district_code = get_district_name(town_name,location,data_province_full)[1]
    # print(district_name)
    # province_name = get_province_name(district_code, data_province_full)
    # print(province_name)
    # province_id = get_province_id(province_name)
    # print(province_id)
    # district_id = get_district_id(province_id, district_name)
    # print(district_id)
    # town_id = get_town_id(district_name,town_name)
    # print(town_id)