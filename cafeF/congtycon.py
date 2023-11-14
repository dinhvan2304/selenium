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
from selenium.webdriver.common.action_chains import ActionChains

def check_exists_by_xpath(broswer,xpath):
    try:
        broswer.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return True

def cafeF_crawl(element):
        global dataFrame
    # try:
        options = Options()
        # options.headless = True
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--disable-setuid-sandbox")
            
        driver = webdriver.Chrome(
            options=options, 
            executable_path='/usr/local/bin/chromedriver')
        driver.get(
            "https://s.cafef.vn/hose/VIC-tap-doan-vingroup-cong-ty-co-phan.chn")

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@id='CafeF_SearchKeyword_Company']")
                )
            )
        
        ActionChains(driver).double_click(driver.find_element(By.ID,"CafeF_SearchKeyword_Company")).perform()
        
        # WebDriverWait(driver, 5).until(
        #     EC.element_to_be_clickable(
        #         (By.XPATH, "//input[@id='CafeF_SearchKeyword_Company']")
        #         )
        #     )
        
        query = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@id='CafeF_SearchKeyword_Company']")
                )
            )
        query.send_keys(element)
        WebDriverWait(driver, 5).until(lambda driver: query.get_attribute('value') == element)
        
        driver.find_element(
            By.CLASS_NAME,"s-submit"
            ).click()
            
        time.sleep(5)
        
        check_1 = "//div[@class='dulieu']/div[@class='dl-title clearfix']/div[@id='symbolbox']"
        check_2 = "//div[@class='contentMainV1']/div[@id='contentV1']/div[@class='btopheader']/div[@class='symbol']"
        check_3 = "//div[@class='contentMainV1']/div[@id='contentV1']/h1/span[1]"
        
        if check_exists_by_xpath(driver,check_1):
            driver.find_element(By.XPATH,
                    "//div[@class='dulieu']/div[@class='hosocongty']/ul[@class='tabs4']/li[@id='liTabCongTy4CT']"
                    ).click()
            time.sleep(2)
            check_exists_1 = "//table//tr[2]/td/table[@class='congtycon']//tr/td[1]"
            check_exists_2 = "//table//tr[4]/td/table[@class='congtycon']//tr/td[1]"
            
            if check_exists_by_xpath(driver,check_exists_1):
                table_1 = driver.find_elements(By.XPATH,check_exists_1)
                for i in range(2,len(table_1)):
                    dict_values = { 'mck_cong_ty_me': element,
                                    'ten_cong_ty_con': driver.find_element(
                                        By.XPATH,"//table//tr[2]/td/table[@class='congtycon']//tr[{}]/td[1]".format(i)).text,
                                    'von_dieu_le': driver.find_element(
                                        By.XPATH,"//table//tr[2]/td/table[@class='congtycon']//tr[{}]/td[2]".format(i)).text,
                                    'vong_gop': driver.find_element(
                                        By.XPATH,"//table//tr[2]/td/table[@class='congtycon']//tr[{}]/td[3]".format(i)).text,
                                    'ty_le_so_huu': driver.find_element(
                                        By.XPATH,"//table//tr[2]/td/table[@class='congtycon']//tr[{}]/td[4]".format(i)).text,
                                    'loai_hinh_doanh_nghiep' : 'Công ty con'
                    }
                    print(dict_values)
                
                # dataFrame_temp = pd.DataFrame([dict_values])
                # dataFrame  = pd.concat([dataFrame,dataFrame_temp],ignore_index= True)
                # dataFrame.to_csv('/Users/dinhvan/Documents/Projects/Crawl/selenium/chinhanh/chi_nhanh_HO_1.csv',index = False)
            if check_exists_by_xpath(driver,check_exists_2):
                table_2 = driver.find_elements(By.XPATH,check_exists_2)
                for i in range(2,len(table_2)):
                    dict_values = { 'mck_cong_ty_me': element,
                                    'ten_cong_ty_con': driver.find_element(
                                        By.XPATH,"//table//tr[4]/td/table[@class='congtycon']//tr[{}]/td[1]".format(i)).text,
                                    'von_dieu_le': driver.find_element(
                                        By.XPATH,"//table//tr[4]/td/table[@class='congtycon']//tr[{}]/td[2]".format(i)).text,
                                    'vong_gop': driver.find_element(
                                        By.XPATH,"//table//tr[4]/td/table[@class='congtycon']//tr[{}]/td[3]".format(i)).text,
                                    'ty_le_so_huu': driver.find_element(
                                        By.XPATH,"//table//tr[4]/td/table[@class='congtycon']//tr[{}]/td[4]".format(i)).text,
                                    'loai_hinh_doanh_nghiep' : 'Công ty liên kết'
                        }
                    print(dict_values)
                    
                # dataFrame_temp = pd.DataFrame([dict_values])
                # dataFrame  = pd.concat([dataFrame,dataFrame_temp],ignore_index= True)
                # dataFrame.to_csv('/Users/dinhvan/Documents/Projects/Crawl/selenium/chinhanh/chi_nhanh_HO_1.csv',index = False)
            
        elif check_exists_by_xpath(driver,check_2):
            print(2)
        elif check_exists_by_xpath(driver,check_3):
            print(3)
        else:
            print(4)
            
        
            # list_result = []
            # list_result.append('mck')
            # list_result.append(element)
            # list_result.append('url')
            # list_result.append(driver.current_url)
            
            # check1 = "//div[@id='content']/div[@class='dulieu']/div[@class='hosocongty']/h2[@id='taichinh']"
        
            # check2 ="//div[@id='container']/div[@class='contentMainV1']/div[@id='contentV1']/div[@class='contentbox'][5]/div[@class='contentheader']"
                    
        
            # if(check_exists_by_xpath(driver,check1)):
            #     print(1)
            # if(check_exists_by_xpath(driver,check2)):
            #     print(2)
            
        #     if(check == 'Thông tin tài chính'):
        #         WebDriverWait(driver, 10).until(
        #             EC.element_to_be_clickable(
        #                 (By.XPATH,"//div[@class='hosocongty']/ul[@class='tabs4']/li[@id='liTabCongTy1CT']/a[@id='lsTab1CT']")
        #             )
        #         ).click()
        #         WebDriverWait(driver, 10).until(
        #             EC.element_to_be_clickable(
        #                 (By.XPATH,"//div[@class='phanchia clearfix']/div[@class='l']/a[@id='idTabTaiChinhNam']")
        #             )
        #         ).click()

        #     else:
        #         WebDriverWait(driver, 10).until(
        #             EC.element_to_be_clickable(
        #                 (By.XPATH,"//div[@class='hosocongty']/ul[@class='tabs4']/li[@id='liTabCongTy2CT'] | //div[@class='otherInfo clearfix']/ul[@class='tabs4']/li[4]")
        #                 )
        #             ).click()
            
        #         driver.find_element(
        #             By.XPATH,"/html/body/form[@id='aspnetForm']/div[3]/div[@id='pagewrap']/div[@id='container']/div[@class='botop']/div[@class='contentMain']/div[@id='content']/div[@class='dulieu']/div[@class='hosocongty']/div[@class='phanchia clearfix']/div[@id='divStart']/div[@class='hosocongty']/div[@class='phanchia clearfix']/div[@class='l']/a[@id='idTabTaiChinhNam']"
        #             ).click()
                
        #     list_year = []
        #     list_nam_xpath = WebDriverWait(driver, 10).until(
        #             EC.presence_of_all_elements_located(
        #                 (By.XPATH,"//div[@id='thongtintaichinh']/div[@class='hosocongty']/div[@id='divHoSoCongTyAjax']/table//tr/th")
        #                 )
        #             ).click()
        #     for i in list_nam_xpath:
        #         list_year.append(i.text)
        #     for i in range(len(list_year)):
        #         list_year[i] = list_year[i].replace('\n(Đã kiểm toán)','')
                
        #     result_temp = driver.find_elements(By.XPATH,"//div[@class='hosocongty']/div[@id='divHoSoCongTyAjax']/table//tr[@id='rptNhomChiTieu_ctl00_rptData_ctl00_TrData']/td")
                                            
        #     list_result_temp = [i.text for i in result_temp] 
        #     list_result = []
        #     list_result.append('MCK')
        #     list_result.append(element)
            
        #     list_result.append('DT_2020')
        #     if 'Năm 2020' in list_year:
        #         list_result.append(list_result_temp[list_year.index('Năm 2020')])
        #     else :
        #         list_result.append(None)
        #     list_result.append('DT_2021')
            
        #     if 'Năm 2021' in list_year:
        #         list_result.append(list_result_temp[list_year.index('Năm 2021')])
        #     else :
        #         list_result.append(None)
            
        #     dict_result = {}
        #     for result in range(0,len(list_result)):
        #         if(result%2 == 0):
        #             dict_result['{}'.format(list_result[result])] = list_result[result+1]
        #     print(list_year)
        #     print(list_result_temp)
        #     print(dict_result)
        #     dataFrame_temp = pd.DataFrame([dict_result])
        #     dataFrame  = pd.concat([dataFrame,dataFrame_temp],ignore_index= True)
        #     dataFrame.to_csv('link_vnr_500_doanh_thu.csv',index = False)
        # driver.close()
    # except Exception as e:
    #     print(e)
    #     driver.close()
        
if __name__ == '__main__':
    
    dataFrame = pd.DataFrame()
    # data_input = pd.read_csv('/Users/dinhvan/Documents/Projects/Crawl/selenium/cafeF/machungkhoan_vnr_500.csv',dtype={'Mã chứng khoán': np.str})
    # list_input = data_input['Mã chứng khoán'].to_list()
    list_input = ['VIC','TR1']
    for element in list_input:
        cafeF_crawl(element)
