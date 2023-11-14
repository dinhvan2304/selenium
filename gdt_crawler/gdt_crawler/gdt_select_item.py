from selenium import webdriver
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
from urllib.parse import quote
import os
import time
from datetime import date, datetime, timedelta
import ast
import numpy as np
import pandas as pd
import re
from sqlalchemy import create_engine

current_path = os.path.dirname(os.path.abspath(__file__))


def check_exists_by_xpath(browser, xpath):
    try:
        browser.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return True


def extract_select_item(current_path, browser):

    url_tinh = "https://www.gdt.gov.vn/TTHKApp/jsp/json.jsp?cmd=GET_DS_TINH"
    browser.get(url_tinh)
    WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "pre"))
    )
    pre_elem = browser.find_element_by_tag_name("pre")
    options_matinh = ast.literal_eval(pre_elem.text)
    for tinh in options_matinh:
        value_tinh = tinh["id"]
        title_tinh = tinh["title"]
        url_huyen = "https://www.gdt.gov.vn/TTHKApp/jsp/json.jsp?cmd=GET_DS_HUYEN&maTinh={}".format(
            value_tinh
        )
        browser.get(url_huyen)
        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "pre"))
        )
        pre_elem = browser.find_element_by_tag_name("pre")
        options_mahuyen = ast.literal_eval(pre_elem.text)
        for huyen in options_mahuyen:
            xa_info = []
            value_huyen = huyen["id"]
            title_huyen = huyen["title"]
            url_xa = "https://www.gdt.gov.vn/TTHKApp/jsp/json.jsp?cmd=GET_DS_XA&maCQThue={}".format(
                value_huyen
            )
            browser.get(url_xa)
            WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "pre"))
            )
            pre_elem = browser.find_element_by_tag_name("pre")
            options_maxa = ast.literal_eval(pre_elem.text)
            for xa in options_maxa:
                value_xa = xa["id"]
                title_xa = xa["title"]
                xa_info.append(
                    [
                        title_tinh,
                        value_tinh,
                        title_huyen,
                        value_huyen,
                        title_xa,
                        value_xa,
                    ]
                )
            xa_np_array = np.array(xa_info)
            if not os.path.exists(os.path.join(current_path, "gdt_province.csv")):
                csv_header = np.array(
                    [["tinh", "ma tinh", "huyen", "ma huyen", "xa", "ma xa"]]
                )
                csv_all_data = np.concatenate((csv_header, xa_np_array))
                df = pd.DataFrame(data=csv_all_data)
                df.to_csv(
                    os.path.join(current_path, "gdt_province.csv"),
                    index=False,
                    header=False,
                )
            else:
                df = pd.DataFrame(data=xa_np_array)
                df.to_csv(
                    os.path.join(current_path, "gdt_province.csv"),
                    index=False,
                    header=False,
                    mode="a",
                )


def get_last_page(url, browser):
    print(url)
    try:
        browser.get(url)
        WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "titleMsg"))
        )
        try:
            end_page_elem = browser.find_element(By.XPATH,
                "//a[@id='endPage']"
            ).get_attribute("href")
            last_pages = re.findall(r"\d+", end_page_elem)
            last_page = last_pages[0]
        except NoSuchElementException:
            last_page = "1"
    except TimeoutException:
        with open(current_path + "/not_found_url.txt", "a+") as f:
            f.write(url + "\n")
        last_page = "0"
    return last_page


def create_gdt_url(current_path, browser):
    gdt_tax_type = "11"
    gdt_tax_without_gtgt = "10"
    gdt_off_low_tax = "12"
    gdt_off = "04"
    gdt_change_tax = "03"
    url_first_page = "https://www.gdt.gov.vn/TTHKApp/jsp/results.jsp?maTinh={}&maHuyen={}&maXa={}&hoTen=&kyLb=&diaChi=&maSoThue=&searchType={}&uuid=7be821e5-6b35-4c87-bdfa-5eedc1e47a32"
    provine_file_path = os.path.join(current_path, "gdt_province.csv")
    province_info = pd.read_csv(provine_file_path)

    province_info["url_gdt_tax_type"] = province_info.apply(
        lambda x: url_first_page.format(
            x["ma tinh"], x["ma huyen"], x["ma xa"], gdt_tax_type
        ),
        axis=1,
    )
    province_info["url_gdt_tax_without_gtgt"] = province_info.apply(
        lambda x: url_first_page.format(
            x["ma tinh"], x["ma huyen"], x["ma xa"], gdt_tax_without_gtgt
        ),
        axis=1,
    )
    province_info["url_gdt_off_low_tax"] = province_info.apply(
        lambda x: url_first_page.format(
            x["ma tinh"], x["ma huyen"], x["ma xa"], gdt_off_low_tax
        ),
        axis=1,
    )
    province_info["url_gdt_off"] = province_info.apply(
        lambda x: url_first_page.format(
            x["ma tinh"], x["ma huyen"], x["ma xa"], gdt_off
        ),
        axis=1,
    )
    province_info["url_gdt_change_tax"] = province_info.apply(
        lambda x: url_first_page.format(
            x["ma tinh"], x["ma huyen"], x["ma xa"], gdt_change_tax
        ),
        axis=1,
    )
    # gán column page đã crawl đến
    sqlEngine = create_engine("mysql+pymysql://root:%s@127.0.0.1:3306/hkd" % quote("Ptdl@123"))
    # sqlEngine = create_engine(
    #     "mysql+pymysql://root:%s@172.16.10.112:3306/alert" % quote("Ptdl@123")
    # )
    query = "SELECT * FROM gdt_crawled_page"
    crawled_page = pd.read_sql(query, con=sqlEngine)
    crawled_page.rename({"ma_xa": "ma xa"}, axis=1, inplace=True)
    crawled_page.drop(["id"], axis=1, inplace=True)
    province_info = pd.merge(province_info, crawled_page, on="ma xa")
    province_info.fillna(0, inplace=True)

    # gán column last page sẽ crawl
    province_info["all_tax_new_page"] = province_info["url_gdt_tax_type"].apply(
        lambda x: get_last_page(x, browser)
    )
    province_info["tax_without_gtgt_new_page"] = province_info[
        "url_gdt_tax_without_gtgt"
    ].apply(lambda x: get_last_page(x, browser))
    province_info["off_low_tax_new_page"] = province_info["url_gdt_off_low_tax"].apply(
        lambda x: get_last_page(x, browser)
    )
    province_info["off_tax_new_page"] = province_info["url_gdt_off"].apply(
        lambda x: get_last_page(x, browser)
    )
    province_info["change_tax_new_page"] = province_info["url_gdt_change_tax"].apply(
        lambda x: get_last_page(x, browser)
    )

    url_file_path = os.path.join(current_path, "gdt_url.csv")
    province_info.to_csv(url_file_path)


if __name__ == "__main__":
    gdt_province_file_path = os.path.join(current_path, "gdt_province.csv")
    options = Options()
    options.add_experimental_option(
        "prefs",
        {
            # "download.default_directory": Initial_path,
            # "download.default_directory": "/Users/tuanpt/Desktop/Crawl_info/temp/" + current_date.now().strftime("%m_%d_%Y") + "/" + province_value,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")

    #browser = webdriver.Chrome(executable_path=current_path + "/chromedriver 2", chrome_options=options)
    browser  = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    if not os.path.exists(gdt_province_file_path):
        extract_select_item(current_path, browser)
	

    if not os.path.exists(os.path.join(current_path, "gdt_url.csv")):
        create_gdt_url(current_path, browser)

    # init crawed gdt page
    # sqlEngine = create_engine(
    #         "mysql+pymysql://root:%s@127.0.0.1:3306/hkd" % quote("Ptdl@123")
    # )
    # province_info = pd.read_csv(current_path + "/gdt_province.csv")
    # ma_xa = province_info["ma xa"]
    # ab = pd.DataFrame()
    # ab["ma_xa"] = ma_xa
    # ab.to_sql(name="gdt_crawled_page", con=sqlEngine, if_exists="replace")
