from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from sqlalchemy import create_engine
from urllib.parse import quote
import mysql.connector

def connect_databasae():
    sqlEngine = create_engine("mysql+pymysql://vantt:%s@172.16.10.144:3306/hkd" % quote("Ptdl@123"))
    query_origin = "SELECT DISTINCT mst as mst_check FROM clients"
    mst_existed = pd.read_sql(query_origin, con=sqlEngine)
    print(mst_existed.head())


def restart_sim(options):
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        chrome_options=options
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
    pass_elem.send_keys("Qtcd@123")

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


def check_exists_by_xpath(browser,xpath):
    try:
        browser.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return True


def crawl_HDDT(list_input):
    global dataFrame
    for element in list_input:
        try:
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-setuid-sandbox")
                            
            capabilities = DesiredCapabilities.CHROME.copy()
            capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), 
                chrome_options=options, 
                desired_capabilities=capabilities
            )
                
            driver.get("https://masothue.com/")
                
            window_before = driver.window_handles[0]
                    
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@id='search']")
                    )
                ).send_keys('{}'.format(element)
                            )
                
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='input-group-btn']/button[@class='btn btn-secondary btn-search-submit']")
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
                    driver.close()
                    print("---------------------- Starting restart sim !----------------------")
                    restart_sim(options)
                    print("---------------------- Starting restart sim done !----------------------")
                    
            
            list_keys = []
            list_values = []
                    
            list_keys.append('url_DN_1')
            list_values.append(driver.current_url)
                    
            list_keys.append('name_company_1')
            list_values.append(WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH,"//table[@class='table-taxinfo']/thead/tr/th/span[@class='copy']")
                    )
                ).text
                               )
            check_exist = "//div[@id='primary']/main[@id='main']/section[@class='animate-in-view fadeIn animated'][1]/div[@class='container']/div[@class='alert alert-success']"
            list_keys.append('invoice_status')
                
            if(check_exists_by_xpath(driver,check_exist)):
                
                #? Add invoice_status
                if(driver.find_element(By.XPATH,check_exist).text == 'Doanh nghiệp đang sử dụng HOÁ ĐƠN TỰ IN.'):
                    list_values.append('Hoá đơn tự in')
                elif(driver.find_element(By.XPATH,check_exist).text == 'Doanh nghiệp sử dụng HOÁ ĐƠN ĐIỆN TỬ của .'):
                    list_values.append('Không xác định')
                else:
                    invoice_info = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH,"//div[@id='primary']/main[@id='main']/section[@class='animate-in-view fadeIn animated'][1]/div[@class='container']/div[@class='alert alert-success']")
                            )
                        ).text
                
                    if 'HOÁ ĐƠN GIẤY' in invoice_info:
                        list_values.append("Hoá đơn giấy")
                    else:
                        list_values.append("Hoá đơn điện tử")
                    
                    # print(invoice_info)
                #? Add invoice_company_name
                    list_keys.append("invoice_company_name")
                    list_values.append(WebDriverWait(driver, 30).until(
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
                        
                    list_keys.append('url_DN_2')
                    list_values.append(driver.current_url)
                            
                    list_keys.append('name_company_2')
                    list_values.append(
                        WebDriverWait(driver,30).until(
                            EC.presence_of_element_located(
                                (By.XPATH,"//table[@class='table-taxinfo']/thead/tr/th/span[@class='copy']")
                                    )
                                ).text
                            )
                    header = driver.find_elements(
                        By.XPATH,"//table[@class='table-taxinfo']//tr/td[1]")
                    for key in header:
                        list_keys.append(key.text)
                    if('Cập nhật mã số thuế' in list_keys[-2]):
                        del list_keys[-2:]
                    
                    values = driver.find_elements(
                        By.XPATH,"//table[@class='table-taxinfo']//tr/td[2]")
                    for value in values:
                        list_values.append(value.text)
                    
                    #? Add code_main_bussiness
                    list_keys.append('code_main_bussiness')
                    if check_exists_by_xpath(driver,"//table[@class='table']//tr/td[1]/strong/a"):
                        list_values.append(
                            driver.find_element(
                                By.XPATH,"//table[@class='table']//tr/td[1]/strong/a").text
                                )
                    else:
                        list_values.append(None)
                     
                    #? Add main_bussiness
                    list_keys.append('main_bussiness')
                    if check_exists_by_xpath(driver,"//table[@class='table']//tr/td[2]/strong/a"):
                        list_values.append(
                            driver.find_element(
                                By.XPATH,"//table[@class='table']//tr/td[2]/strong/a").text
                                )
                    else:
                        list_values.append(None)
                            
                    driver.close()
                    driver.switch_to.window(window_before)
            else:
                list_values.append('Không xác định')


            dict_result = dict(zip(list_keys,list_values))
            dict_update = {'invoice_status': dict_result.get('invoice_status'),
                           'invoice_company_name' : dict_result.get('invoice_company_name') if dict_result.get('invoice_company_name') is not None else None,
                           'invoice_company_mst' : dict_result.get('Mã số thuế') if dict_result.get('Mã số thuế') is not None else None}
            print(dict_update)
            # connect_databasae()
            
            
            dataFrame_temp = pd.DataFrame([dict_result])
            dataFrame  = pd.concat([dataFrame,dataFrame_temp],ignore_index= True)
            # dataFrame.to_csv('/Users/dinhvan/Document/Projects/crawl_data/selenium/hoa_don/Test_output.csv', index = False)
            driver.close()
        except Exception as e:
            print(e)
            print('Error: ' + str(element))
            driver.close()

            
if __name__ == "__main__":
    # data_input = pd.read_csv('/Users/dinhvan/Documents/Projects/Crawl/selenium/HDDT/data_input/test_input.csv',dtype = {'mst': str})
    # data_input['mst'] = data_input['mst'].str.strip()
    # list_input = data_input['mst'].values.tolist()
    

    # list_input =['4900755586','2901296620','4601576589','2500665870']
    # dataFrame = pd.DataFrame()
    # crawl_HDDT(list_input)
    connect_databasae()
    
    
    
    
    