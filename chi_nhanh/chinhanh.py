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


def check_exists_by_xpath(browser,xpath):
    try:
        browser.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return True

def restart_sim(options):
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        chrome_options=options
    )
    driver.get(
        "http://192.168.8.1/html/index.html"
    )

    WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']"))
        ) 

    pass_elem = driver.find_element(By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']")
    pass_elem.send_keys("Qtcd@123")

    login_btn = driver.find_element(By.ID, "login_btn")
    WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "login_btn"))
        )
    login_btn.click()

    WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ic_reboot"))
        )
    WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ic_reboot"))
        ).click()
    WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//div[2]/div[@class='btn_normal_short pull-left margin_left_12']"))
        )
    WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//div[2]/div[@class='btn_normal_short pull-left margin_left_12']"))
        ).click() 
    
    WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']"))
        )
    driver.quit()

def crawl_chi_nhanh(list_input):
    global dataFrame
    i = len(list_input)
    for element in list_input:
        print('-------------------------Còn {} mã số thuế nữa !!!--------------------------'.format(i))
        i -= 1
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
                
                        
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@id='search']")
                    )
                ).send_keys('{}'.format(element)
                                )
                        
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH,"(//button[@class='btn btn-secondary btn-search-submit'])")
                    )
                ).click()
                
            time.sleep(2)
            
            # WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@class='modal-header']/h5[@id='exampleModalLabel']")))
            
            if check_exists_by_xpath(driver, "//div[@class='modal-content']/div[@class='modal-body']"):
                time.sleep(1)
                body_model = driver.find_element(By.XPATH, "//div[@class='modal-content']/div[@class='modal-body']")
                body_text = body_model.text
                if 'Truy cập bị từ chối' in body_text:
                    print("---------------------- Starting restart sim !----------------------")
                    restart_sim(options)
                    print("---------------------- Starting restart sim done !----------------------")

                if(check_exists_by_xpath(driver,"//table[@class='table']//tr/td[2]/strong/a")):
                    nganh_nghe_HO = driver.find_element(
                                    By.XPATH,"//table[@class='table']//tr/td[2]/strong/a").text
                else:
                    nganh_nghe_HO = 'Không xác định'
                    
                check_exist_xpath = "//section[@class='animate-in-view fadeIn animated'][2]/div[@class='container']/header/h2[@class='h1']"
                if(check_exists_by_xpath(driver,check_exist_xpath) and (driver.find_element(By.XPATH,check_exist_xpath).text == 'Mã số thuế chi nhánh')):
                    table = driver.find_elements(By.XPATH,"//div[@id='primary']/main[@id='main']/section[@class='animate-in-view fadeIn animated'][2]/div[@class='container']/div[@class='tax-listing']/div")
                            
                    for i in range(1,len(table)+1):
                        dict_values = { 'url_HO': driver.current_url,
                                        'mst_HO': element,
                                        'nganh_nghe_HO': nganh_nghe_HO ,
                                        'ten_chi_nhanh': driver.find_element(
                                            By.XPATH,"//div[@id='primary']/main[@id='main']/section[@class='animate-in-view fadeIn animated'][2]/div[@class='container']/div[@class='tax-listing']/div[{}]/h3/a".format(i)).text,
                                        'mst_chi_nhanh': driver.find_element(
                                            By.XPATH,"//div[@class='container']/div[@id='primary']/main[@id='main']/section[@class='animate-in-view fadeIn animated'][2]/div[@class='container']/div[@class='tax-listing']/div[{}]/div/a".format(i)).text,
                                        'CEO_chi_nhanh': driver.find_element(
                                            By.XPATH,"//div[@id='content']/div[@class='container']/div[@id='primary']/main[@id='main']/section[@class='animate-in-view fadeIn animated'][2]/div[@class='container']/div[@class='tax-listing']/div[{}]/div/em/a".format(i)).text,
                                        'Dia_chi_chi_nhanh': driver.find_element(
                                            By.XPATH,"//div[@id='content']/div[@class='container']/div[@id='primary']/main[@id='main']/section[@class='animate-in-view fadeIn animated'][2]/div[@class='container']/div[@class='tax-listing']/div[{}]/address".format(i)).text}
                            
                        dataFrame_temp = pd.DataFrame([dict_values])
                        dataFrame  = pd.concat([dataFrame,dataFrame_temp],ignore_index= True)
                        dataFrame.to_csv('/home/ptdl/Documents/Projects/chinhanh/Chi_nhanh_SOE2_bonus_1.csv',index = False,sep = ',')
                        print (dict_values) 
                else:
                    dict_values = { 'url_HO': driver.current_url,
                                    'mst_HO': element,
                                    'nganh_nghe_HO': nganh_nghe_HO,
                                    'ten_chi_nhanh': None,
                                    'mst_chi_nhanh': None,
                                    'CEO_chi_nhanh': None,
                                    'Dia_chi_chi_nhanh': None}
                        
                    dataFrame_temp = pd.DataFrame([dict_values])
                    dataFrame  = pd.concat([dataFrame,dataFrame_temp],ignore_index= True)
                    dataFrame.to_csv('/home/ptdl/Documents/Projects/chinhanh/Chi_nhanh_SOE2_bonus_1.csv',index = False)
                    # print(dict_values)
                driver.close()
        except Exception as e:
            print(e)
            print(element)
            driver.close()
        
        
if __name__ == '__main__':
    dataFrame = pd.DataFrame()
    data_input = pd.read_csv("/home/ptdl/Documents/Projects/chinhanh/SOE2_lost.csv",dtype = str)
    # data_input.drop(data_input.loc[data_input['Mã số thuế SOE2'].isna()].index,inplace=True)
    # data_input['Mã số thuế SOE2'] = data_input['Mã số thuế SOE2'].str.strip()
    # data_input.drop(data_input.loc[data_input['Mã số thuế SOE2'].isna()].index,inplace=True)
    list_input = data_input['Mã số thuế SOE2'].values.tolist()
    list_input = list_input[765:]
    # list_input = ['01022669569']
    
    crawl_chi_nhanh(list_input)

        
        