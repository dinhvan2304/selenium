# from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib.parse import quote
import os
import time
from datetime import date, datetime, timedelta
import ast
import numpy as np
import pandas as pd
import re
from sqlalchemy import create_engine
from urllib.parse import quote
import database_connect as dbc
from captcha_v2.captcha_solver import SolverManager

from seleniumwire import webdriver


current_path = os.path.dirname(os.path.abspath(__file__))
not_refresh = 0
refresh_captcha = 1
refresh_ip = 2
refresh_cookie = 3

gdt_tax_type = "11"
gdt_tax_without_gtgt = "10"
gdt_off_low_tax = "12"
gdt_off = "04"
gdt_change_tax = "03"

search_type_list = ["11", "10", "12", "04", "03"]

gdt_crawled_col = {
   "11": "all_tax_last_page",
   "10": "tax_without_gtgt_last_page",
   "12": "off_low_tax_last_page",
   "04": "off_tax_last_page",
   "03": "change_tax_last_page" 
}

gdt_table_dict = {
   "11": "gdt_tax_all",
   "10": "gdt_tax_without_gtgt",
   "12": "gdt_tax_low_off",
   "04": "gdt_tax_off",
   "03": "gdt_tax_changed" 
}

gdt_table_col_dict = {
    "00": ['tinh', 'huyen', 'xa','name','mst','dia_chi_kd', 'nganh_nghe'],
    "11": ['tinh', 'huyen', 'xa','name','mst','ky_lap_bo', 'dia_chi', 'nganh_nghe', 'doanh_thu_thang', 'tong_thue','thue_gtgt','thue_tncn','thue_ttdb','thue_tn','thue_bvmt','phi_bvmt', 'don_vi_tinh'],
    "10": ['tinh', 'huyen', 'xa','name','mst','ky_lap_bo', 'dia_chi', 'nganh_nghe', 'doanh_thu_thang', 'don_vi_tinh'],
    "12": ['tinh', 'huyen', 'xa','name','mst','ky_lap_bo', 'dia_chi', 'nganh_nghe','off_date_from', 'off_date_to', 'don_vi_tinh'],
    "04": ['tinh', 'huyen', 'xa','name','mst','ky_lap_bo', 'dia_chi_lh','dia_chi_kd','nganh_nghe','off_date_to','don_vi_tinh'],
    "03": ['tinh', 'huyen', 'xa','name','mst','ky_lap_bo','dia_chi_kd_cu','dia_chi_kd_moi','nganh_nghe_cu','nganh_nghe_moi','doanh_thu_cu','doanh_thu_moi','tong_thue','thue_gtgt','thue_tncn','thue_ttdb','thue_tn','thue_bvmt','phi_bvmt','don_vi_tinh']
}


class Gdt_Scraper(webdriver.Chrome):
    def __init__(self, delay_time=3, config=None, headless=True):
        
        self.options = Options()
        self.headless= headless
        # capabilities = DesiredCapabilities.CHROME.copy()
        if self.headless:
            self.options.add_argument("--window-size=1920x1080")
            self.options.add_argument('--disable-gpu')
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--headless")
            self.options.add_argument("--disable-dev-shm-usage")
            self.options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

        # self.options.add_argument('--ignore-certificate-errors')
        # self.options.add_argument("disable-blink-features")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option('useAutomationExtension', False)

        # capabilities['acceptSslCerts'] = True
        # capabilities['acceptInsecureCerts'] = True
        
        self.delay = delay_time
        self.config=config

        try:
            self.driverPath = "/usr/bin/chromedriver"
            # self.conn = dbc.Database_PD(username="tuanpt", host="localhost", db_name="hkd", password="Thanhtuan2")
            self.conn = dbc.Database_PD(username="root", host="localhost", db_name="hkd", password="Ptdl@123")
        except Exception as e:
            print(e)

        sl_options = {
            'verify_ssl': False
        }

        super().__init__(self.driverPath, options = self.options, seleniumwire_options=sl_options)
        self.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.solver=SolverManager()
        self.home_url = None
    
    def _get_captcha_image(self):
        
        """Capture the captcha returned by server, then decode and preprocess to a (1,64,128,1) Tensor"""
        for request in self.requests[::-1]:
            if 'captcha' in request.url:
                return request.response.body

    def _get_gdt_captcha(self, info, refresh=False):

        if refresh:
            time.sleep(15)
            try:
                self.refresh()
            except TimeoutException as e:
                self.delete_browser()

        else:
            try:
                if self.home_url == None:
                    self.home_url = self.get("https://www.gdt.gov.vn/wps/portal/home/hct")
                else:
                    self.get(self.home_url)
            
                WebDriverWait(self, self.delay*2).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="captchaCtn"]'))
                )
            except Exception as e:
                self._get_gdt_captcha(info, refresh=True)

        # Get captcha image
        answer = ""
                
        try:
            img = self._get_captcha_image()
            answer = self.solver.predict(img)
        except Exception as e:
            print(e)
            self._get_gdt_captcha(info, refresh=True)

        if answer == "":
            self._get_gdt_captcha(info, refresh=True)

        # if answer != "":
        #     try:	
        #         matinh_elem = Select(
        #             self.find_element(By.ID, "maTinh")
        #         )
        #         matinh_elem.select_by_value(str(info['ma tinh']))
        #         time.sleep(self.delay)

        #         WebDriverWait(self, self.delay*2).until(
        #             EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='{}']".format(info['ma huyen'])))
        #         )
        #         mahuyen_elem = Select(
        #             self.find_element(By.ID, "maHuyen")
        #         )
        #         mahuyen_elem.select_by_value(str(info['ma huyen']))
        #         time.sleep(self.delay)

        #         # WebDriverWait(self, 30).until(
        #         #     EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='{}']".format(info['ma xa'])))
        #         # )
        #         # maxa_elem = Select(
        #         #     self.find_element(By.ID, "maXa")
        #         # )
        #         # maxa_elem.select_by_value(str(info['ma xa']))
        #         # time.sleep(self.delay)

        #         captcha_elem = self.find_element(By.ID, "captcha")
        #         captcha_elem.send_keys(answer)
                
        #         time.sleep(self.delay)

        #         WebDriverWait(self, self.delay).until(
        #             EC.element_to_be_clickable((By.ID, "nttSearchButton"))
        #         ).click()
            
        #         WebDriverWait(self, self.delay).until(
        #             EC.element_to_be_clickable((By.CLASS_NAME, "titleMsg"))
        #         )
        #     except Exception as e:
        #         self._get_gdt_captcha(info, refresh=True) 
        # self.close()
        return answer

    def _get_page_html(self, maTinh, maHuyen, maXa, searchType, captcha, page=1):
        url = "https://www.gdt.gov.vn/TTHKApp/jsp/results.jsp?maTinh={}&maHuyen={}&maXa={}&hoTen=&kyLb=&diaChi=&maSoThue=&searchType={}&uuid=c86e16bd-c3be-45a4-9a92-02e4f571903a&captcha={}&pageNumber={}".format(maTinh, maHuyen, maXa, searchType, captcha, page)

        # Open a new window
        # self.execute_script("window.open('');")
        # # Switch to the new window
        # self.switch_to.window(self.window_handles[1])
        try:
            self.get(url)

            title_msg_elem = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.XPATH, '//html/body/div[1]'))
            )
        except Exception as e:
            body_err = self.find_element(By.XPATH, "//html/body")
            if '[Go Back]' in body_err.text:
                return refresh_cookie
            elif "Vui lòng nhập đúng mã xác nhận." in body_err.text:
                return refresh_captcha
        except TimeoutException as e:
            return refresh_captcha
        
        return not_refresh
    
    def _get_new_last_page(self):
        try:
            last_page_elem = self.find_element(By.XPATH,"//a[@id='endPage']"
            ).get_attribute("href")
            last_pages = re.findall(r"\d+", last_page_elem)
            last_page = int(last_pages[0])
        except Exception as e:
            last_page = 0
        return last_page
    
    def _check_elem_exist(self, xpath):
        try:
            WebDriverWait(self, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except Exception as e:
            return False
    
        return True
    
    def _parse_page(self, search_type, info):

        xstr = lambda s: "" if s is None else str(s)
        gdt_origin = list() 
        gdt_tax_info = list()
        if search_type == gdt_tax_type:
            if self._check_elem_exist("//table[@class='ta_border']//tr/td[2]"):
                number_gdt_rows = self.find_elements(By.XPATH, "//table[@class='ta_border']//tr/td[2]")
                number_gdt_rows = [gdt_row.text for gdt_row in number_gdt_rows]

                
                for col in range(3, len(number_gdt_rows) + 3):
                    name = xstr(
                        self.find_element(By.XPATH, "//table[@class='ta_border']//tr[{}]/td[2]".format(col)
                        ).text
                    )
                    mst = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='mst'][1]".format(
                                col
                            )
                        ).text
                    )
                    
                    ky_lap_bo = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='mst'][2]".format(
                                col
                            )
                        ).text
                    )
                    dia_chi = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[5]".format(col)
                        ).text
                    )
                    nganh_nghe = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[6]".format(col)
                        ).text
                    )
                    doanh_thu_thang = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='money'][1]".format(
                                col
                            )
                        ).text
                    )
                    tong_thue = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='money'][2]".format(
                                col
                            )
                        ).text
                    )
                    thue_gtgt = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[3]/td[@class='money'][3]".format(
                                col
                            )
                        ).text
                    )
                    thue_tncn = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='money'][4]".format(
                                col
                            )
                        ).text
                    )
                    thue_ttdb = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='money'][5]".format(
                                col
                            )
                        ).text
                    )
                    thue_tn = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='money'][6]".format(
                                col
                            )
                        ).text
                    )
                    thue_bvmt = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='money'][7]".format(
                                col
                            )
                        ).text
                    )
                    phi_bvmt = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='money'][8]".format(
                                col
                            )
                        ).text
                    )

                    dv_tinh = xstr(
                        self.find_element(By.XPATH,"//html/body/div[2]").text
                    )
                    if dv_tinh != "":
                        dv_tinh = dv_tinh.split(":")[-1].strip()

                    gdt_tax_info.append(
                        (
                            info['tinh'],
                            info['huyen'],
                            info['xa'],
                            name,
                            mst,
                            ky_lap_bo,
                            dia_chi,
                            nganh_nghe,
                            doanh_thu_thang,
                            tong_thue,
                            thue_gtgt,
                            thue_tncn,
                            thue_ttdb,
                            thue_tn,
                            thue_bvmt,
                            phi_bvmt,
                            dv_tinh,
                        )
                    )
                    if mst not in self.gdt_mst_list:
                        gdt_origin.append(
                            (
                                info['tinh'],
                                info['huyen'],
                                info['xa'],
                                name,
                                mst,
                                dia_chi,
                                nganh_nghe
                            )
                        )
                        self.gdt_mst_list.append(mst)
        elif search_type == gdt_tax_without_gtgt:
            # Crawl tax without gtgt
            if self._check_elem_exist("//table[@class='ta_border']//tr/td[2]"):
                number_gdt_rows = self.find_elements(By.XPATH,
                    "//table[@class='ta_border']//tr/td[2]"
                )
                number_gdt_rows = [gdt_row.text for gdt_row in number_gdt_rows]

                
                for col in range(1, len(number_gdt_rows) + 1):
                    name = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[2]".format(col)
                        ).text
                    )
                    mst = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='mst'][1]".format(
                                col
                            )
                        ).text
                    )
                    ky_lap_bo = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='mst'][2]".format(
                                col
                            )
                        ).text
                    )
                    dia_chi = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[5]".format(col)
                        ).text
                    )
                    nganh_nghe = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[6]".format(col)
                        ).text
                    )
                    doanh_thu_thang = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='money']".format(
                                col
                            )
                        ).text
                    )
                    dv_tinh = xstr(
                        self.find_element(By.XPATH,"//html/body/div[2]").text
                    )
                    if dv_tinh != "":
                        dv_tinh = dv_tinh.split(":")[-1].strip()

                    gdt_tax_info.append(
                        (
                            info['tinh'],
                            info['huyen'],
                            info['xa'],
                            name,
                            mst,
                            ky_lap_bo,
                            dia_chi,
                            nganh_nghe,
                            doanh_thu_thang,
                            dv_tinh,
                        )
                    )

                    if mst not in self.gdt_mst_list:
                        gdt_origin.append(
                            (
                                info['tinh'],
                                info['huyen'],
                                info['xa'],
                                name,
                                mst,
                                dia_chi,
                                nganh_nghe
                            )
                        )
                        self.gdt_mst_list.append(mst)
            
        elif search_type == gdt_off_low_tax:
            # Crawl low off tax
            if self._check_elem_exist("//table[@class='ta_border']//tr/td[2]"):
                number_gdt_rows = self.find_elements(By.XPATH,
                    "//table[@class='ta_border']//tr/td[2]"
                )
                number_gdt_rows = [gdt_row.text for gdt_row in number_gdt_rows]
                
                for col in range(3, len(number_gdt_rows) + 3):
                    name = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[2]".format(col)
                        ).text
                    )
                    mst = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='mst'][1]".format(
                                col
                            )
                        ).text
                    )
                    ky_lap_bo = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='mst'][2]".format(
                                col
                            )
                        ).text
                    )
                    dia_chi = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[5]".format(col)
                        ).text
                    )
                    nganh_nghe = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[6]".format(col)
                        ).text
                    )
                    off_date_from = self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[7]".format(col)
                        ).text
                    
                    off_date_to =self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[8]".format(col)
                        ).text

                    dv_tinh = xstr(
                        self.find_element(By.XPATH,"//html/body/div[2]").text
                    )
                    if dv_tinh != "":
                        dv_tinh = dv_tinh.split(":")[-1].strip()
                    
                    if off_date_from != None and "/" in off_date_from:
                        date_list_from = off_date_from.split("/")
                        off_date_from = date_list_from[-1] + "-" + date_list_from[-2] + "-" + date_list_from[0]
                    
                    if off_date_to != None and "/" in off_date_to:
                        date_list_to = off_date_to.split("/")
                        off_date_to = date_list_to[-1] + "-" + date_list_to[-2] + "-" + date_list_to[0] 

                    gdt_tax_info.append(
                        (
                            info['tinh'],
                            info['huyen'],
                            info['xa'],
                            name,
                            mst,
                            ky_lap_bo,
                            dia_chi,
                            nganh_nghe,
                            off_date_from,
                            off_date_to,
                            dv_tinh,
                        )
                    )
                    if mst not in self.gdt_mst_list:
                        gdt_origin.append(
                            (
                                info['tinh'],
                                info['huyen'],
                                info['xa'],
                                name,
                                mst,
                                dia_chi,
                                nganh_nghe
                            )
                        )
                        self.gdt_mst_list.append(mst)
            
        elif search_type == gdt_off:
            # Crawl off tax
            if self._check_elem_exist("//table[@class='ta_border']//tr/td[2]"):
                number_gdt_rows = self.find_elements(By.XPATH,
                    "//table[@class='ta_border']//tr/td[2]"
                )
                number_gdt_rows = [gdt_row.text for gdt_row in number_gdt_rows]

                
                for col in range(1, len(number_gdt_rows) + 1):
                    name = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[2]".format(col)
                        ).text
                    )
                    mst = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='mst'][1]".format(
                                col
                            )
                        ).text
                    )
                    ky_lap_bo = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='mst'][2]".format(
                                col
                            )
                        ).text
                    )
                    dia_chi_lh = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[5]".format(col)
                        ).text
                    )
                    dia_chi_kd = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[6]".format(col)
                        ).text
                    )
                    nganh_nghe = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[7]".format(col)
                        ).text
                    )
                    off_date_to = self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[8]".format(col)
                        ).text

                    dv_tinh = xstr(
                        self.find_element(By.XPATH,"//html/body/div[2]").text
                    )
                    if dv_tinh != "":
                        dv_tinh = dv_tinh.split(":")[-1].strip()

                    if off_date_to != None and "/" in off_date_to:
                        date_list_to = off_date_to.split("/")
                        off_date_to = date_list_to[-1] + "-" + date_list_to[-2] + "-" + date_list_to[0] 

                    gdt_tax_info.append(
                        (
                            info['tinh'],
                            info['huyen'],
                            info['xa'],
                            name,
                            mst,
                            ky_lap_bo,
                            dia_chi_lh,
                            dia_chi_kd,
                            nganh_nghe,
                            off_date_to,
                            dv_tinh,
                        )
                    )
                    if mst not in self.gdt_mst_list:
                        gdt_origin.append(
                            (
                                info['tinh'],
                                info['huyen'],
                                info['xa'],
                                name,
                                mst,
                                dia_chi_kd,
                                nganh_nghe
                            )
                        )
                        self.gdt_mst_list.append(mst)
        elif search_type == gdt_change_tax:
            # Crawl off tax
            if self._check_elem_exist("//table[@class='ta_border']//tr/td[2]"):
                number_gdt_rows = self.find_elements(By.XPATH,
                    "//table[@class='ta_border']//tr/td[2]"
                )
                number_gdt_rows = [gdt_row.text for gdt_row in number_gdt_rows]

                
                for col in range(3, len(number_gdt_rows) + 3):
                    name = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[2]".format(col)
                        ).text
                    )
                    mst = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='mst'][1]".format(
                                col
                            )
                        ).text
                    )
                    ky_lap_bo = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='mst'][2]".format(
                                col
                            )
                        ).text
                    )
                    dia_chi_kd_cu = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[5]".format(col)
                        ).text
                    )
                    dia_chi_kd_moi = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[6]".format(col)
                        ).text
                    )
                    nganh_nghe_cu = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[7]".format(col)
                        ).text
                    )
                    nganh_nghe_moi = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[8]".format(col)
                        ).text
                    )
                    doanh_thu_cu = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='money'][1]".format(
                                col
                            )
                        ).text
                    )
                    doanh_thu_moi = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='money'][2]".format(
                                col
                            )
                        ).text
                    )

                    tong_thue = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='money'][3]".format(
                                col
                            )
                        ).text
                    )
                    thue_gtgt = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[3]/td[@class='money'][4]".format(
                                col
                            )
                        ).text
                    )
                    thue_tncn = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='money'][5]".format(
                                col
                            )
                        ).text
                    )
                    thue_ttdb = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='money'][6]".format(
                                col
                            )
                        ).text
                    )
                    thue_tn = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='money'][7]".format(
                                col
                            )
                        ).text
                    )
                    thue_bvmt = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='money'][8]".format(
                                col
                            )
                        ).text
                    )
                    phi_bvmt = xstr(
                        self.find_element(By.XPATH,
                            "//table[@class='ta_border']//tr[{}]/td[@class='money'][9]".format(
                                col
                            )
                        ).text
                    )

                    dv_tinh = xstr(
                        self.find_element(By.XPATH,"//html/body/div[2]").text
                    )
                    if dv_tinh != "":
                        dv_tinh = dv_tinh.split(":")[-1].strip()

                    gdt_tax_info.append(
                        (
                            info['tinh'],
                            info['huyen'],
                            info['xa'],
                            name,
                            mst,
                            ky_lap_bo,
                            dia_chi_kd_cu,
                            dia_chi_kd_moi,
                            nganh_nghe_cu,
                            nganh_nghe_moi,
                            doanh_thu_cu,
                            doanh_thu_moi,
                            tong_thue,
                            thue_gtgt,
                            thue_tncn,
                            thue_ttdb,
                            thue_tn,
                            thue_bvmt,
                            phi_bvmt,
                            dv_tinh,
                        )
                    )
                    if mst not in self.gdt_mst_list:
                        gdt_origin.append(
                            (
                                info['tinh'],
                                info['huyen'],
                                info['xa'],
                                name,
                                mst,
                                dia_chi_kd_moi,
                                nganh_nghe_moi
                            )
                        )
                        self.gdt_mst_list.append(mst)    

        return gdt_tax_info, gdt_origin 
    
    def delete_browser(self):
        def restart_sim():
            self.get(
                "http://192.168.8.1/html/index.html"
            )

            WebDriverWait(self, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']"))
                ) 

            pass_elem = self.find_element(By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']")
            pass_elem.send_keys("Qtcd@123")

            login_btn = self.find_element(By.ID, "login_btn")
            WebDriverWait(self, 60).until(
                    EC.element_to_be_clickable((By.ID, "login_btn"))
                )
            login_btn.click()

            WebDriverWait(self, 60).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ic_reboot"))
                )
            WebDriverWait(self, 60).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "ic_reboot"))
                ).click()
            WebDriverWait(self, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//div[2]/div[@class='btn_normal_short pull-left margin_left_12']"))
                )
            WebDriverWait(self, 60).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[2]/div[@class='btn_normal_short pull-left margin_left_12']"))
                ).click() 
            
            WebDriverWait(self, 600).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']"))
                )

        self.conn.close_conn()
        restart_sim()
        self.close()
        self.quit()
    
    def refresh_browser(self, info, searchType, captcha):
        count_request = 0
        while True:
            print("Need to refresh browser: {}".format(str(count_request+1)))
            captcha = self._get_gdt_captcha(info, refresh=True)
            status = self._get_page_html(info['ma tinh'], info['ma huyen'], info['ma xa'], searchType, captcha)
            if status != refresh_captcha:
                break
            time.sleep(self.delay)
            if count_request == 6:
                self.delete_browser()
            count_request += 1
    
    def clear_cookie(self):
        print("Need to clear cookie")
        self.get('chrome://settings/clearBrowserData')
        WebDriverWait(self, self.delay).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="clearBrowsingDataConfirm"]'))
            )
        self.find_element(By.XPATH,'//*[@id="clearBrowsingDataConfirm"]').send_keys(Keys.ENTER)
        # self.close()
            
    def _start_crawl_gdt(self):

        def process_error_status_load_page(status, info, searchType, captcha):
            if status == refresh_captcha:
                self.refresh_browser(info, searchType, captcha) 
            elif status == refresh_ip:
                # Restart sim
                
                # Refresh browser
                self.refresh_browser(info, searchType, captcha) 
            elif status == refresh_cookie:
                self.clear_cookie()
                time.sleep(self.delay)
                self.refresh_browser(info, searchType, captcha)

        
        def save_to_db(gdt_tax_page, gdt_origin_page, gdt_page_crawed):
            gdt_tax_df = pd.DataFrame(gdt_tax_page, columns=gdt_table_col_dict[gdt_page_crawed['table_id']])
            gdt_origin_df = pd.DataFrame(gdt_origin_page, columns=gdt_table_col_dict["00"])
            gdt_page_df = pd.DataFrame([gdt_page_crawed])

            table_name = gdt_table_dict[gdt_page_crawed['table_id']]
            col_name = gdt_page_crawed['col_name']
            if gdt_tax_df.shape[0] > 0:
                self.conn.insert_data(table_name, gdt_tax_df, dtype=None)
                update_page_crawed_query = "UPDATE gdt_crawled_page as f INNER JOIN temp_gdt_crawled_page AS t ON t.ma_xa = f.ma_xa SET f.{} = t.paged WHERE f.ma_xa = t.ma_xa".format(col_name)
                self.conn.update_data('gdt_crawled_page', gdt_page_df, update_page_crawed_query, dtype=None)
            if gdt_origin_df.shape[0] > 0:
                self.conn.insert_data("gdt_origin", gdt_origin_df, dtype=None)
            
        current_path, _ = os.path.split(os.path.abspath(__file__))
        province_df = pd.read_csv(os.path.join(current_path,"gdt_province.csv"))
        if os.path.exists(os.path.join(current_path, "crawed_province.csv")):
            crawed_provice = pd.read_csv(os.path.join(current_path,"crawed_province.csv"), names=['ma_xa'])
            province_df = province_df[~province_df['ma xa'].isin(crawed_provice['ma_xa'])]
        
        # province_id_df = province_df[['ma tinh', 'ma huyen', 'ma xa']]
        province_id_dict = province_df.to_dict('records')

        gdt_mst_query = """SELECT mst FROM gdt_origin"""
        gdt_mst_df = self.conn.select_data(gdt_mst_query)
        self.gdt_mst_list = gdt_mst_df.mst.values.tolist()
                
        for info in province_id_dict:
            captcha = self._get_gdt_captcha(info)
            if captcha != "":
                last_page_query = """SELECT * FROM gdt_crawled_page"""
                last_page_df = self.conn.select_data(last_page_query)
                
                # Get crawled last page                    
                last_page_crawled = last_page_df[last_page_df['ma_xa'] == info['ma xa']]
                for searchType in search_type_list:
                    print("Start get data of {} - {} - {} with type: {} at: {}".format(info['tinh'], info['huyen'], info['ma xa'], gdt_table_dict[searchType], datetime.now()))
                    col_name = gdt_crawled_col[searchType]
                    last_page = last_page_crawled.iloc[0][col_name]
                    last_page = last_page.item()
                    
                    # Get new last page
                    status = self._get_page_html(info['ma tinh'], info['ma huyen'], info['ma xa'], searchType, captcha)
                    if status == not_refresh:
                        new_page_crawl = self._get_new_last_page()
                        if last_page < new_page_crawl:
                            for page in range(int(last_page)+1, int(new_page_crawl)):                                                    
                                status = self._get_page_html(info['ma tinh'], info['ma huyen'], info['ma xa'], searchType, captcha, page)
                                if status == not_refresh:
                                    gdt_tax_page, gdt_origin_page = self._parse_page(searchType, info)
                                    if len(gdt_tax_page) > 0:
                                        gdt_page_crawed = {'table_id': searchType, 'col_name': col_name, 'ma_xa': info['ma xa'], 'paged': page}
                                        save_to_db(gdt_tax_page, gdt_origin_page, gdt_page_crawed)
                                    else:
                                        break
                                else:
                                    process_error_status_load_page(status, info, searchType, captcha)
                                
                                time.sleep(self.delay)
                        # self.close()
                    else:
                        process_error_status_load_page(status, info, searchType, captcha)
                    time.sleep(self.delay)
                print("End get data of {} - {} - {} with type: {} at: {}".format(info['tinh'], info['huyen'], info['ma xa'], gdt_table_dict[searchType], datetime.now()))
                with open(os.path.join(current_path, 'crawed_province.csv'), 'a+') as f:
                    f.write(str(info['ma xa']) + "\n")
                    
            time.sleep(self.delay)
            
                                        
if __name__ == "__main__":
    
    gdt_scraper = Gdt_Scraper(headless=False)
    gdt_scraper._start_crawl_gdt()

    