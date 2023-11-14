from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException, TimeoutException, InvalidSessionIdException
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

class Ttdn_Scraper():
    def __init__(self, headless=False, delay_time=3, current_date=None, current_path=None):
        super().__init__()
        self.parent_path = os.path.dirname(os.path.abspath(__file__ + "/../"))
        self.current_date = current_date
        self.current_path = current_path
        # self.Initial_path = (
        #     "/home/data/Documents/Crawl_info/temp/"+self.current_date
        # )
        self.Initial_path = os.path.join(self.current_path, "temp", self.current_date)

        # self.Initial_path = (
        #     "/Users/tuanpt/Documents/projects/PHP/ptdl_khdn/Projects/sme/masothue_crawl/temp/"+self.current_date
        # )
        self.options = Options()
        self.options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": self.Initial_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
            },
        )
        
        self.headless = headless
        if self.headless:
            self.options.add_argument("--headless=new")
            # self.options.add_argument("--no-sandbox")
            # self.options.add_argument("--disable-dev-shm-usage")
        
            
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
 
        self.delay = delay_time
        

        self.browser_all = webdriver.Chrome(
            # executable_path=os.path.join(self.parent_path, "chromedriver"),
            executable_path="/usr/bin/chromedriver",
            options =self.options,
            desired_capabilities=capabilities
        )

    def _save_data(self, list_ttdn, ttdn_dir):
        if not os.path.exists(ttdn_dir):
            csv_header = np.array([["created_date", "MST"]])
            df = pd.DataFrame(data=csv_header)
            df.to_csv(ttdn_dir, index=False, header=False)
            df_data = pd.DataFrame(data=list_ttdn)
            df_data.to_csv(ttdn_dir, index=False, header=False, mode="a")
        else:
            df = pd.DataFrame(data=list_ttdn)
            df.to_csv(ttdn_dir, index=False, header=False, mode="a")

    def check_exists_by_xpath(self, browser, xpath):
        try:
            browser.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    def restart_sim(self, options):
        self.browser_all = webdriver.Chrome(
            # executable_path=os.path.join(self.parent_path, "chromedriver"),
            executable_path="/usr/bin/chromedriver",
            options=options,
            desired_capabilities=self.capabilities
        )
        self.browser_all.get(
            "http://192.168.8.1/html/index.html"
        )

        WebDriverWait(self.browser_all, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']"))
            ) 

        pass_elem = self.browser_all.find_element(By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']")
        pass_elem.send_keys("Ptdl@2020")

        login_btn = self.browser_all.find_element(By.ID, "login_btn")
        WebDriverWait(self.browser_all, 60).until(
                EC.element_to_be_clickable((By.ID, "login_btn"))
            )
        login_btn.click()

        WebDriverWait(self.browser_all, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ic_reboot"))
            )
        WebDriverWait(self.browser_all, 60).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "ic_reboot"))
            ).click()
        WebDriverWait(self.browser_all, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[2]/div[@class='btn_normal_short pull-left margin_left_12']"))
            )
        WebDriverWait(self.browser_all, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//div[2]/div[@class='btn_normal_short pull-left margin_left_12']"))
            ).click() 
        
        WebDriverWait(self.browser_all, 600).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']"))
            )
        self.browser_all.quit()

    def crawl_masothue(self, mst_list, mst_path):
        mst_new_list = mst_list
        print(self.browser_all.get_window_size())
        for mst in mst_new_list:
            if mst.isnumeric():
                print(mst)
                # mst = '0' + mst	
                if len(mst) == 9:
                    mst = '0' + mst
                try:
                    self.browser_all.get(
                        "https://masothue.com/"
                    )
                    logs = self.browser_all.get_log('performance')
                    print(self.get_status(logs))
                    if self.get_status(logs) == 200 and mst != "":
                        print("Waiting search element") 
                        time.sleep(2)
                        WebDriverWait(self.browser_all, 15).until(
                            EC.presence_of_element_located((By.XPATH, "//*[@id='search']"))
                        ) 
                        print("Found search element")
                        mst_search_elem = self.browser_all.find_element(By.XPATH,
                            "//*[@id='search']"
                        )
                        mst_search_elem.send_keys(mst)
                        btns_pdf = self.browser_all.find_element(By.XPATH,
                            "//button[@class='btn btn-secondary btn-search-submit']"
                        )
                        btns_pdf.click()
                        try:
                            WebDriverWait(self.browser_all, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@class='modal-header']/h5[@id='exampleModalLabel']")))
                            if self.check_exists_by_xpath(self.browser_all, "//div[@class='modal-content']/div[@class='modal-body']"):
                                time.sleep(1)
                                body_model = self.browser_all.find_element(By.XPATH, "//div[@class='modal-content']/div[@class='modal-body']")
                                body_text = body_model.text
                                print(body_text)
                                
                                if 'Truy cập bị từ chối' in body_text:
                                    print("Starting restart sim")
                                    self.restart_sim(self.options)
                                    self.browser_all = webdriver.Chrome(
                                        # executable_path=os.path.join(self.parent_path, "chromedriver"),
                                        executable_path="/usr/bin/chromedriver",
                                        options=self.options,
                                        desired_capabilities=self.capabilities
                                    )
                                    mst_search_elem.clear()
                                    if mst != "":
                                        mst_search_elem.send_keys(mst)
                                        btns_pdf.click() 
                                    break
                                
                        except Exception as e:
                            print(e)
                            
                        WebDriverWait(self.browser_all, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "table-taxinfo")))
                        with open(mst_path, "a+") as fp:
                            fp.write(mst + "," + self.browser_all.current_url + "\n")
                            
						# Parse detail masothue
						
                        time.sleep(2)
                        
                    else:
                        self.browser_all.close()
                        
                except InvalidSessionIdException as e:
                    print("Catch invalid session id exception")
                    self.browser_all.quit()
                    print("Start restart sim")
                    self.restart_sim(self.options)
                    self.browser_all = webdriver.Chrome(
                        # executable_path=os.path.join(self.parent_path, "chromedriver"),
                        executable_path="/usr/bin/chromedriver",
                        options=self.options,
                        desired_capabilities=self.capabilities
                    )
                    continue
                except TimeoutException as e:
                    print("Catch timeout exception") 
                    if "r=" in self.browser_all.current_url:
                        self.browser_all.quit()
                        print("Start restart sim")
                        self.restart_sim(self.options)
                        self.browser_all = webdriver.Chrome(
                            # executable_path=os.path.join(self.parent_path, "chromedriver"),
                            executable_path="/usr/bin/chromedriver",
                            options=self.options,
                            desired_capabilities=self.capabilities
                        )
                    continue
                except Exception as e:
                    print("Catch exception: {}".format(e))
                    self.browser_all.quit()
                    self.browser_all = webdriver.Chrome(
                        # executable_path=os.path.join(self.parent_path, "chromedriver"),
                        executable_path="/usr/bin/chromedriver",
                        options=self.options,
                        desired_capabilities=self.capabilities
                    )
                    continue

        self.browser_all.quit()
        return "done"

    def _start_crawl(self, type_crawl):
        self.browser_all.maximize_window()
        self.browser_all.get(
                "https://bocaodientu.dkkd.gov.vn/egazette/Forms/Egazette/DefaultAnnouncements.aspx"
            )
        
        try:
            WebDriverWait(self.browser_all, self.delay).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "Pager")
                    )
            )
            if type_crawl == TYPE_DNGT:
                print("Starting crawl dngt")
                js_script = '''\
                                document.getElementById('ipcc_chat_iframe').style.display = 'none';
                                '''
                self.browser_all.execute_script(js_script)
                WebDriverWait(self.browser_all, self.delay).until(
                    EC.element_to_be_clickable((By.ID, "ctl00_C_RptProdGroups_ctl05_EGZDivItem"))
                ).click()
                ttdn_dir = os.path.join(self.current_path, "mst_dngt_crawed.csv")
            elif type_crawl == TYPE_DNM:
                print("Start crawl dnm")
                ttdn_dir = os.path.join(self.current_path, "mst_dnm_crawed.csv") 
            
            today_crawed_list = list() 
            if os.path.exists(ttdn_dir):
                mst_crawed = pd.read_csv(ttdn_dir, dtype=object)
                if mst_crawed.shape[0] > 0:
                    today_crawed_list = mst_crawed['MST'].values.tolist()

            list_date_elems = self.browser_all.find_elements(By.XPATH, "//table[@id='ctl00_C_CtlList']//tr/td[1]")
            list_date = [datetime.strptime(i.text.split(" ")[0], "%d/%m/%Y").strftime("%Y_%m_%d") for i in list_date_elems[:20]]
            list_mst_elems = self.browser_all.find_elements(By.XPATH, "//table[@id='ctl00_C_CtlList']//tr/td/div[@class='enterprise_code']/span")
            list_raw_mst = [i.text.split(" ")[-1] for i in list_mst_elems]
            list_date_mst = list(zip(list_date, list_raw_mst))
            list_mst = [(crawed_date,mst) for crawed_date,mst in list_date_mst if mst not in today_crawed_list]
            
            if len(list_mst) > 0:
                list_ttdn = [(date, mst) for date,mst in list_mst]
                list_mst_crawed = [mst for date,mst in list_ttdn]
                self._save_data(list_ttdn, ttdn_dir)

                if type_crawl == TYPE_DNM: 
                    btns_pdf = self.browser_all.find_elements_by_xpath(
                        "//table[@id='ctl00_C_CtlList']//tr/td[5]/input"
                    )
                    btns_pdf = btns_pdf[:20]
                    list_city_elems = self.browser_all.find_elements_by_xpath(
                        "//table[@id='ctl00_C_CtlList']//tr/td[3]"
                    )
                    list_city = [i.text for i in list_city_elems[:20]]

                    list_btns = list(zip(list_raw_mst, list_date, btns_pdf, list_city))
                    list_btns = [btn for btn in list_btns if btn[0] not in today_crawed_list]
                    for index, (mst, date, btn_pdf, city) in enumerate(list_btns):
                        if "chí minh" in city.lower():
                            city_dir = "Hồ Chí Minh"
                        elif "huế" in city.lower():
                            city_dir = "Thừa Thiên-Huế"
                        else:
                            name_list = city.split(" ")
                            city_dir = " ".join(name_list[-2:])

                        abs_city_dir = self.current_path+"/temp/"+date+"/"+city_dir
                        Path(abs_city_dir).mkdir(parents=True, exist_ok=True)
                        
                        btn_pdf.click()
                        time.sleep(5)
                        filename = max(
                            [
                                os.path.join(self.Initial_path, f)
                                for f in os.listdir(self.Initial_path)
                            ],
                            key=os.path.getctime,
                        )
                        # print(filename)
                        if "new_announcement" in filename:
                            suffix = datetime.now().strftime("%y%m%d_%H%M%S")
                            shutil.move(
                                filename,
                                os.path.join(
                                    abs_city_dir,
                                    city
                                    + "_"
                                    + suffix
                                    + ".pdf",
                                ),
                            )
                            # print(os.path.join(
                            #         abs_city_dir,
                            #         city
                            #         + "_"
                            #         + suffix
                            #         + ".pdf",
                            #     ))
                today_crawed_list = today_crawed_list+list_mst_crawed

            is_last_slide_page = False
            is_middel_slide_page = False
            end_crawl = False
            current_page_crawled = 0
            old_page_crawled = 0
            while True:
                try:
                    list_page_elems = self.browser_all.find_elements(By.XPATH, "//table[@id='ctl00_C_CtlList']//tr[@class='Pager']/td/table//tr/td/a")
                    if list_page_elems[-1].text.isnumeric():
                        temp_page_elems = list_page_elems
                        is_last_slide_page = True
                    else:
                        temp_page_elems = list_page_elems[:-1] 
                    
                    if list_page_elems[1].text == "...":
                        temp_page_elems = temp_page_elems[2:]
                        is_middel_slide_page = True

                    temp_list_page_elems = [i.text for i in temp_page_elems]
                    current_page_crawled += len(temp_list_page_elems)
                    
                    for index, page in enumerate(temp_list_page_elems):
                        logging.info("Crawling page {}".format(page))
                        if old_page_crawled != 0:
                            page_to_crawl = old_page_crawled
                            old_page_crawled = 0
                        else:
                            if is_middel_slide_page or is_last_slide_page:
                                page_to_crawl = index + 4
                            else:
                                page_to_crawl = index + 2

                        js_script = '''\
                            document.getElementById('return').style.display = 'none';
                            '''
                        self.browser_all.execute_script(js_script)
                        if page != "":
                            print("Crawl page {}".format(page))
                            WebDriverWait(self.browser_all, self.delay).until(
                                EC.element_to_be_clickable((By.XPATH, "//table[@id='ctl00_C_CtlList']//tr[@class='Pager']/td/table//tr/td["+ str(page_to_crawl) + "]/a"))
                            ).click()

                            WebDriverWait(self.browser_all, self.delay).until(
                                EC.presence_of_element_located((By.XPATH, "//table[@id='ctl00_C_CtlList']//tr[2]/td[1]"))
                            )
                            list_date_elems = self.browser_all.find_elements(By.XPATH, "//table[@id='ctl00_C_CtlList']//tr/td[1]")
                            list_date = [datetime.strptime(i.text.split(" ")[0], "%d/%m/%Y").strftime("%Y_%m_%d") for i in list_date_elems[:20]]
                            list_mst_elems = self.browser_all.find_elements(By.XPATH, "//table[@id='ctl00_C_CtlList']//tr/td/div[@class='enterprise_code']/span")
                            list_raw_mst = [i.text.split(" ")[-1] for i in list_mst_elems]
                            list_date_mst = list(zip(list_date, list_raw_mst))
                            list_mst = [(date,mst) for date,mst in list_date_mst if mst not in today_crawed_list]
                            if len(list_mst) > 0:
                                list_ttdn = [(date, mst) for date,mst in list_mst]
                                list_mst_crawed = [mst for date,mst in list_ttdn]
                                self._save_data(list_ttdn, ttdn_dir)
                                
                                if type_crawl == TYPE_DNM: 
                                    btns_pdf = self.browser_all.find_elements_by_xpath(
                                        "//table[@id='ctl00_C_CtlList']//tr/td[5]/input"
                                    )
                                    list_city_elems = self.browser_all.find_elements_by_xpath(
                                        "//table[@id='ctl00_C_CtlList']//tr/td[3]"
                                    )
                                    list_city = [i.text for i in list_city_elems[:20]]

                                    list_btns = list(zip(list_raw_mst, list_date, btns_pdf, list_city))
                                    list_btns = [btn for btn in list_btns if btn[0] not in today_crawed_list]
                                    for index, (mst, date, btn_pdf, city) in enumerate(list_btns):
                                        if "chí minh" in city.lower():
                                            city_dir = "Hồ Chí Minh"
                                        elif "huế" in city.lower():
                                            city_dir = "Thừa Thiên-Huế"
                                        else:
                                            name_list = city.split(" ")
                                            city_dir = " ".join(name_list[-2:])

                                        abs_city_dir = self.current_path+"/temp/"+date+"/"+city_dir
                                        Path(abs_city_dir).mkdir(parents=True, exist_ok=True)

                                        btn_pdf.click()                                        
                                        time.sleep(5)
                                        filename = max(
                                            [
                                                os.path.join(self.Initial_path, f)
                                                for f in os.listdir(self.Initial_path)
                                            ],
                                            key=os.path.getctime,
                                        )
                                        # print(filename)
                                        suffix = datetime.now().strftime("%y%m%d_%H%M%S")
                                        shutil.move(
                                            filename,
                                            os.path.join(
                                                abs_city_dir,
                                                city
                                                + "_"
                                                + suffix
                                                + ".pdf",
                                            ),
                                        )
                                        # print(os.path.join(
                                        #     abs_city_dir,
                                        #     city
                                        #     + "_"
                                        #     + suffix
                                        #     + ".pdf",
                                        # ))

                                        
                                today_crawed_list = today_crawed_list+list_mst_crawed
                        else:
                            break
                        if index == len(temp_list_page_elems)-1:
                                break
                    
                    if (is_last_slide_page and index == len(temp_page_elems) - 1):
                        end_crawl = True
                        break
                    
                    WebDriverWait(self.browser_all, self.delay).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "Pager"))
                    )

                    if end_crawl:
                        break  

                except ElementClickInterceptedException as e:
                    logging.error(e)
                    js_script = '''\
                            document.getElementById('ipcc_chat_iframe').style.display = 'none';
                            '''
                    self.browser_all.execute_script(js_script)
                    old_page_crawled = page_to_crawl
                    pass
                except TimeoutException as e:
                    old_page_crawled = page_to_crawl
                    pass
            result = "done"
        except TimeoutException as e:
            logging.error("Timeout Exception: Can't load ttdn page")
            result = "exception"
            pass
        except ElementClickInterceptedException as e:
            logging.error("ElementClickInterceptedException: Can't load ttdn page")
            result = "exception"
            pass

        self.browser_all.quit()
        return result

        
if __name__ == "__main__":
    args = sys.argv
    type_crawl = args[1] # "new" or "crash"
    process_type = args[2] # "crawl_mst" or "crawl_url"
    current_path = os.path.dirname(os.path.abspath(__file__))
    # process_type = PROCESS_CRAWL_MST
    # process_type = PROCESS_CRAWL_URL
    # type_crawl = "new"
    current_date = datetime.now()
    #  - timedelta(1)
    current_date = current_date.strftime("%Y_%m_%d")
    
    if process_type == PROCESS_CRAWL_MST:
        logging.basicConfig(filename=os.path.join(current_path,"ttdn_mst_scraper.log"), filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        logging.warning('This will get logged to a file')
        while True:
            print("Crawl info at {}".format(datetime.now()))
            msc_scrap = Ttdn_Scraper(headless = True, delay_time = 15, current_date = current_date, current_path =current_path)
            result = msc_scrap._start_crawl(type_crawl=type_crawl)
            # result = msc_scrap._start_crawl(type_crawl=TYPE_DNM)
            logging.info("MST Scraper result: {} at {}".format(result,current_date))
            if result == "done":
                break
    elif process_type == PROCESS_CRAWL_URL:
        logging.basicConfig(filename=os.path.join(current_path,"ttdn_url_scraper.log"), filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        logging.warning('This will get logged to a file')
        masothue_path = os.path.join(current_path, "masothue_crawl/masothue_url.csv")
        
        mst_existed = pd.read_csv(os.path.join(current_path, "mst_dnm_crawed.csv"), dtype=object)
        # mst_existed = mst_existed[mst_existed['created_date'] < "2022-10-14"]
        mst_existed = mst_existed[mst_existed['created_date'] < current_date]
        mst_query = "SELECT DISTINCT mst FROM clients"
        sqlEngine = create_engine(
            "mysql+pymysql://root:%s@172.16.10.144:3306/hkd" % quote("Ptdl@123")
        )
        mst_db = pd.read_sql(mst_query, con=sqlEngine)
        mst_db['mst'] = mst_db['mst'].str.lstrip("'")
        mst_not_in_db = mst_existed[~mst_existed['MST'].isin(mst_db['mst'])]

        if os.path.exists(masothue_path):
            mst_url_df = pd.read_csv(masothue_path, names=['mst','url'], dtype=object)
            mst_not_in_db = mst_not_in_db[~mst_not_in_db['MST'].isin(mst_url_df['mst'])]

        mst_existed_list = mst_not_in_db['MST'].values.tolist()
        if len(mst_existed_list) > 0:
            msc_scrap = Ttdn_Scraper(headless=True, delay_time=15, current_date=current_date, current_path=current_path)
            result = msc_scrap.crawl_masothue(mst_list=mst_existed_list, mst_path=masothue_path)
            if result == "done":
                try:
                    os.chdir(os.path.join(current_path, "masothue_crawl"))
                    execute(
                        [
                            "scrapy",
                            "crawl",
                            "masothue_tablets",
                        ]
                    )
                except SystemExit:
                    pass
