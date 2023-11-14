
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

# options.add_argument("--no-sandbox")
# options.add_argument("--headless")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-setuid-sandbox")
# options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options, executable_path= "/Users/dinhvan/Downloads/chromedriver")
driver.get("https://finance.vietstock.vn/doanh-nghiep-a-z/danh-sach-niem-yet?page=1")
# print('Headless is running !')
time.sleep(1)
def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return True

# Log in
WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable(
        (By.XPATH,"//div[@class='navbar-right hidden-xs hidden-sm navbar-login']/a[@class='title-link btnlogin']"))).click()
username_input = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//div[@id='content-login-form-input']/div[@class='input-group'][1]/input[@id='txtEmailLogin']")))
username_input.send_keys('dinhvan2304@gmail.com')
password_input = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//div[@id='content-login-form']/div[@id='content-login-form-input']/div[@class='input-group'][2]/input[@id='txtPassword']")))
password_input.send_keys('Van23042000.')
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located(
        (By.XPATH,"//div[@class='modal-content']/form[@id='form1']/div[@id='content-login-form']/div[@id='content-login-form-button']/div[1]/button[@id='btnLoginAccount']"))).click()
print('Logged in successfully !')
time.sleep(1)

dataFrame = pd.DataFrame()
def result_total(result_number):
    global dataFrame
    dict_result = dict.fromkeys(['mck','ten_cong_ty','doanh_thu_quy_1','doanh_thu_quy_2'])

    mck = driver.find_element(By.XPATH,"//table[@class='table table-striped table-bordered table-hover table-middle pos-relative m-b']//tr[{}]/td[@class='text-center'][2]/a[@class='title-link']".format(result_number)).text
    ten = driver.find_element(By.XPATH,"//table[@class='table table-striped table-bordered table-hover table-middle pos-relative m-b']//tr[{}]/td[3]".format(result_number)).text

    driver.execute_script("arguments[0].click();",driver.find_element(By.XPATH,"//table[@class='table table-striped table-bordered table-hover table-middle pos-relative m-b']//tr[{}]/td[@class='text-center'][2]/a[@class='title-link']".format(result_number)))

    active_tab_name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,"//div[@class='p-t']/div[@class='row'][1]/div[@class='btn-group col-sm-16 m-b']/a[@class='btn bg active']"))).text
    if (active_tab_name == 'Xem theo năm'):
        result_tab_link = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,"//div[@class='p-t']/div[@class='row'][1]/div[@class='btn-group col-sm-16 m-b']/a[@class='btn btn-default']")))
        webdriver.ActionChains(driver).move_to_element(result_tab_link).click(result_tab_link).perform()
    time.sleep(1)

    dt_quy_1 = ''
    dt_quy_2 = ''
    list_dt = []
    list_quy = []

    check_xpath = "//div[@class='auto-resize']/div[@class='p-t']/div[@class='pos-relative']/h3"
    if(check_exists_by_xpath(check_xpath)):
        dt_quy_1 = "Chưa có dữ liệu"
        dt_quy_2 = "Chưa có dữ liệu"
    else:
        list_quy_xpath = driver.find_elements(By.XPATH,"//table[@id='table-0']/thead/tr/th[@class='text-center col-100 al-middle']/b")
        for i in list_quy_xpath:
            list_quy.append(i.text)
        dt = driver.find_elements(By.XPATH,"//table[@id='table-0']/tbody/tr[@class='Normal'][1]/td[@class='text-right']")
        for i in dt:
            list_dt.append(i.text)
        if ('Quý 1/2022' in list_quy) and (list_dt[list_quy.index('Quý 1/2022')] != '') :
                dt_quy_1 = list_dt[list_quy.index('Quý 1/2022')]
        else:
            dt_quy_1 = "Chưa có dữ liệu"

        if ('Quý 2/2022' in list_quy) and (list_dt[list_quy.index('Quý 2/2022')] != ''):
            dt_quy_2 = list_dt[list_quy.index('Quý 2/2022')]
        else:
            dt_quy_2 = "Chưa có dữ liệu"
        # dt = driver.find_elements(By.XPATH,"//table[@id='table-0']/tbody/tr[@class='Normal'][1]/td[@class='text-right']")
        # for i in dt:
        #     list_dt.append(i.text)
        # if(len(list_dt)== 1):
        #     dt_quy_2 = list_dt[-1]
        # else:
        #     dt_quy_1 = list_dt[-2]
        #     dt_quy_2 = list_dt[-1]

    # driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH,"//a[contains(text(),'Đăng ký KD')]"))
    # time.sleep(0.5)
    # mst_raw = driver.find_element(By.XPATH,"//div[@id='profile-3']/p[2]").text.split(':')
    # mst = mst_raw[-1].strip()

    # driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH,"//div[@class='m-b']/ul[@id='view-tab']/li[5]/a"))
    # time.sleep(1)

    # xpath_ctc = "//div[@class='col-xs-24 col-sm-16']/div[@id='cong-ty-con-lien-ket']/div[@class='headline bb3 red']/h4[@class='text-link']/a[@class='title-link']"
    # if(check_exists_by_xpath(xpath_ctc)):
    #     ctc = driver.find_elements(By.XPATH,"(//table[@class='table table-striped table-hover table-middle no-m-b']//tr[@class='i-b']/td[@class='padder-h-xs']/span) | (//table[@class='table table-striped table-hover table-middle no-m-b']/tbody/tr[@class='i-b']/td[@class='padder-h-xs']/a[@class='title-link']/span[1])")
    #     list_ctc = [i.text for i in ctc]
    # else:
    #     list_ctc.append(None)

    dict_result['mck'] = mck
    dict_result['ten_cong_ty'] = ten
    dict_result['doanh_thu_quy_1'] = dt_quy_1
    dict_result['doanh_thu_quy_2'] = dt_quy_2
    # dict_result['mst'] = mst
    # dict_result['cong_ty_con'] = list_ctc

    dataFrame = dataFrame.append(dict_result,ignore_index = True)
    dataFrame.to_csv('vietStock_dt_quy_6.csv')
    print(dict_result)

def callback_click():
    driver.execute_script("arguments[0].click();",driver.find_element(By.XPATH,"//a[normalize-space()='{}']".format(alphabet)))
    time.sleep(1)
list_alphabet = ['W','X','Y']
# ,'C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y'
for alphabet in list_alphabet:
    driver.execute_script("arguments[0].click();",driver.find_element(By.XPATH,"//a[normalize-space()='{}']".format(alphabet)))
    time.sleep(1)
    record_number_total = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,"//div[@id='az-container']/div[1]/div[@class='pull-left']/div[@class='m-t']"))).text.split(" ")
    record_number = int(record_number_total[2])
    page_numbers = 1
    if(record_number % 50 != 0 and record_number > 0): page_numbers = int(record_number / 50) + 1
    else: page_numbers = int(record_number / 50)

    if page_numbers == 1:
        for result_number in range(1,record_number+1,1):
            try:
                driver.execute_script("arguments[0].click();",WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//a[normalize-space()='{}']".format(alphabet)))))
                time.sleep(1)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"(//option[@value='50'][normalize-space()='50'])[2]"))).click()
                time.sleep(1)
                result_total(result_number)
                print('Pass :' + str(result_number))
                driver.get("https://finance.vietstock.vn/doanh-nghiep-a-z/danh-sach-niem-yet?page=1")
            except Exception as e:
                print(e)
                driver.get("https://finance.vietstock.vn/doanh-nghiep-a-z/danh-sach-niem-yet?page=1")
    else:
        for page_number in range(1,page_numbers+1,1):
            if page_number == page_numbers :
                for result_number in range(1,(record_number-((page_numbers-1)*50))+1,1):
                    try:
                        driver.execute_script("arguments[0].click();",WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//a[normalize-space()='{}']".format(alphabet)))))
                        time.sleep(1.5)
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"(//option[@value='50'][normalize-space()='50'])[2]"))).click()
                        time.sleep(1.5)
                        for click in range(page_numbers-1):
                            driver.execute_script("arguments[0].click();",driver.find_element(By.XPATH,"//div[@class='auto-resize']/div/div[@id='az-container']/div[3]/div[@class='pull-right']/div[@class='form-group']/div[@class='btn-group m-l']/button[@id='btn-page-next']"))
                            time.sleep(1.5)
                        result_total(result_number)
                        print('Pass :' + str(result_number))
                        driver.get("https://finance.vietstock.vn/doanh-nghiep-a-z/danh-sach-niem-yet?page=1")
                    except Exception as e:
                        print(e)
                        driver.get("https://finance.vietstock.vn/doanh-nghiep-a-z/danh-sach-niem-yet?page=1")
            else:
                if page_number == 1:
                    for result_number in range(1,51,1):
                        try:
                            driver.execute_script("arguments[0].click();",WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//a[normalize-space()='{}']".format(alphabet)))))
                            time.sleep(1.5)
                            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"(//option[@value='50'][normalize-space()='50'])[2]"))).click()
                            time.sleep(1.5)
                            result_total(result_number)
                            print('Pass :' + str(result_number))
                            driver.get("https://finance.vietstock.vn/doanh-nghiep-a-z/danh-sach-niem-yet?page=1")
                        except Exception as e:
                            print(e)
                            driver.get("https://finance.vietstock.vn/doanh-nghiep-a-z/danh-sach-niem-yet?page=1")

                else:
                    for result_number in range(1,51,1):
                        try:
                            driver.execute_script("arguments[0].click();",WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//a[normalize-space()='{}']".format(alphabet)))))
                            time.sleep(1.5)
                            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"(//option[@value='50'][normalize-space()='50'])[2]"))).click()
                            time.sleep(1.5)
                            for click_page in range(page_number-1):
                                driver.execute_script("arguments[0].click();",driver.find_element(By.XPATH,"//div[@class='auto-resize']/div/div[@id='az-container']/div[3]/div[@class='pull-right']/div[@class='form-group']/div[@class='btn-group m-l']/button[@id='btn-page-next']"))
                                time.sleep(1.5)
                            result_total(result_number)
                            print('Pass :' + str(result_number))
                            driver.get("https://finance.vietstock.vn/doanh-nghiep-a-z/danh-sach-niem-yet?page=1")
                        except Exception as e:
                            print(e)
                            driver.get("https://finance.vietstock.vn/doanh-nghiep-a-z/danh-sach-niem-yet?page=1")
# driver.execute_script("arguments[0].click();",driver.find_element(By.XPATH,"//a[normalize-space()='D']"))
# result_total(3)
driver.quit()
