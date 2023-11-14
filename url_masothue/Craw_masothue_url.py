from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
)
import os
import time
from datetime import date, datetime, timedelta
import shutil
from pathlib import Path
import pandas as pd
import re
from sqlalchemy import create_engine, text
from urllib.parse import quote
import time


current_path = os.path.dirname(os.path.abspath(__file__))
company_file_path = os.path.join(current_path, "bocao_new.csv")
masothue_path = os.path.join(current_path, "masothue_url.csv")
# current_date = datetime.now()
start_date = datetime.now() - timedelta(14)
current_date = datetime.now() - timedelta(1)
province = {
    "88": "An Giang",
    "89": "Vũng Tàu",
    "90": "Bắc Giang",
    "91": "Bắc Kạn",
    "92": "Bạc Liêu",
    "93": "Bắc Ninh",
    "94": "Bến Tre",
    "95": "Bình Định",
    "96": "Bình Dương",
    "97": "Bình Phước",
    "98": "Bình Thuận",
    "99": "Cà Mau",
    "100": "Cao Bằng",
    "101": "Đắk Lắk",
    "102": "Đắk Nông",
    "103": "Điện Biên",
    "104": "Đồng Nai",
    "105": "Đồng Tháp",
    "106": "Gia Lai",
    "107": "Hà Giang",
    "108": "Hà Tĩnh",
    "109": "Hải Dương",
    "110": "Hậu Giang",
    "111": "Hòa Bình",
    "112": "Hưng Yên",
    "113": "Khánh Hòa",
    "114": "Kiên Giang",
    "115": "KonTum",
    "116": "Lai Châu",
    "117": "Lâm Đồng",
    "118": "Lạng Sơn",
    "119": "Lào Cai",
    "120": "Long An",
    "121": "Nam Định",
    "122": "Nghệ An",
    "123": "Ninh Bình",
    "124": "Ninh Thuận",
    "125": "Phú Thọ",
    "126": "Phú Yên",
    "127": "Quảng Bình",
    "128": "Quảng Nam",
    "129": "Quảng Ngãi",
    "130": "Quảng Ninh",
    "131": "Quảng Trị",
    "132": "Sóc Trăng",
    "133": "Sơn La",
    "134": "Tây Ninh",
    "135": "Thái Bình",
    "136": "Thái Nguyên",
    "137": "Thanh Hoá",
    "138": "Thừa Thiên-Huế",
    "139": "Tiền Giang",
    "140": "Trà Vinh",
    "141": "Tuyên Quang",
    "142": "Vĩnh Long",
    "143": "Vĩnh Phúc",
    "144": "Yên Bái",
    "145": "Hà Nam",
    "81": "Cần Thơ",
    "82": "Đà Nẵng",
    "83": "Hà Nội",
    "86": "Hải Phòng",
    "87": "Hồ Chí Minh",
}

province_data_crawled = {}

def check_exists_by_xpath(browser, xpath):
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/", "_blank")
    return driver.execute_script(
        """
        var elements = document.querySelector('downloads-manager')
        .shadowRoot.querySelector('#downloadsList')
        .items
        if (elements.every(e => e.state === 'COMPLETE'))
        return elements.map(e => e.filePath || e.file_path || e.fileUrl || e.file_url);
        """
    )


def crawl_bocao_data(province, mst_existed_list):
    lost_province_array = {}
    province_data = province
    for province_key, province_value in province_data.items():

        # Initial_path = (
        #     "/home/data/Documents/Crawl_data/Crawl_info/temp/"
        #     + current_date.strftime("%Y_%m_%d")
        #     + "/"
        #     + province_value
        # )
        Initial_path = os.path.join(
            "/home/data/Documents/Crawl_data/Crawl_info/temp",
            current_date.strftime("%Y_%m_%d"),
            province_value,
        )

        #Initial_path = (
        #   "/Users/tuanpt/Desktop/Crawl_info/temp/"
        #   + current_date.strftime("%Y_%m_%d")
        #   + "/"
        #   + province_value
        #)

        options = Options()
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": Initial_path,
                # "download.default_directory": "/Users/tuanpt/Desktop/Crawl_info/temp/"
                # + current_date.now().strftime("%m_%d_%Y")
                # + "/"
                # + province_value,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
            },
        )

        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")

        #browser = webdriver.Chrome(
        #   executable_path="gdt_crawler/gdt_crawler/chromedriver",
        #   chrome_options=options,
        #)
        browser = webdriver.Chrome(
            executable_path="/usr/bin/chromedriver", chrome_options=options
        )

        browser.get(
            "https://bocaodientu.dkkd.gov.vn/egazette/Forms/Egazette/ANNOUNCEMENTSListingInsUpd.aspx"
        )

        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "herbas"))
        )

        

        try:
            table_info = browser.find_element_by_xpath(
                "//div[@id='header']/div[@class='centraldiv']/div[@class='centraldivf']/div[@class='MenuHome']/input[@id='ctl00_imgHome']"
            )

            Path(Initial_path).mkdir(parents=True, exist_ok=True)

            select_type = Select(
                browser.find_element_by_id("ctl00_C_ANNOUNCEMENT_TYPE_IDFilterFld")
            )
            select_type.select_by_value("NEW")

            start_date_elem = browser.find_element_by_id(
                "ctl00_C_PUBLISH_DATEFilterFldFrom"
            )
            end_date_elem = browser.find_element_by_id(
                "ctl00_C_PUBLISH_DATEFilterFldTo"
            )

            start_date_elem.clear()
            end_date_elem.clear()
            # start_date_elem.send_keys("{}/{}/{}".format(start_date.date, start_date.month, start_date.year))
            start_date_elem.send_keys(start_date.strftime("%d/%m/%Y"))
            print("start date: {}".format(start_date.strftime("%d/%m/%Y")))
            print("{}/{}/{}".format(start_date.date, start_date.month, start_date.year))
            # end_date_elem.send_keys("{}/{}/{}".format(current_date.date, current_date.month, current_date.year))
            end_date_elem.send_keys(current_date.strftime("%d/%m/%Y"))

            select_province = Select(
                browser.find_element_by_id("ctl00_C_HO_PROVINCE_IDFld")
            )
            select_province.select_by_value(province_key)

            # time.sleep(3.0)

            btn_file = browser.find_element_by_id("ctl00_C_BtnFilter").click()
            delay = 10  # seconds

            myElem = WebDriverWait(browser, delay).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//table[@id='ctl00_C_CtlList']")
                )
            )
            company_numb = browser.find_element_by_xpath(
                "//div[@id='ctl00_C_PnlListResult']/fieldset/table[@class='center']//tr/td/i/b"
            ).text

            print(
                "Province: {} _ Company count: {}".format(province_value, company_numb)
            )

            number_page = 0

            print(
                "before: {} _ {}".format(
                    int(company_numb) % 20, int(company_numb) // 20
                )
            )
            if int(company_numb) % 20 > 0:
                number_page = int(company_numb) // 20 + 1
            else:
                number_page = int(company_numb) // 20

            print("after: {}".format(number_page))

            if number_page != 0:
                index_page = 1
                page_clicked = 0
                while True:
                    index_page += 1
                    page_clicked += 1
                    if page_clicked <= number_page:
                        company_name = browser.find_elements_by_xpath(
                            "//table[@id='ctl00_C_CtlList']//tr/td[4]/p[@class='enterprise_name']"
                        )
                        company_mst = browser.find_elements_by_xpath(
                            "//table[@id='ctl00_C_CtlList']//tr/td[4]/div[@class='enterprise_code']/span"
                        )
                        
                        with open(company_file_path, "a+") as fp:
                            for mst_text in company_mst:
                                mst = re.findall(r'\d+', mst_text.text)
                                if mst[0] not in mst_existed_list:
                                    fp.write(mst[0] + "\n")
                        # if check_exists_by_xpath(
                        #     "//table[@id='ctl00_C_CtlList']//tr/td[7]/input"
                        # ):

                            # btns_pdf = browser.find_elements_by_xpath(
                            #     "//table[@id='ctl00_C_CtlList']//tr/td[7]/input"
                            # )
                            # for index, btn_pdf in enumerate(btns_pdf):
                            #     btn_pdf.click()
                            #     time.sleep(3)
                            #     filename = max(
                            #         [
                            #             os.path.join(Initial_path, f)
                            #             for f in os.listdir(Initial_path)
                            #         ],
                            #         key=os.path.getctime,
                            #     )
                            #     shutil.move(
                            #         filename,
                            #         os.path.join(
                            #             Initial_path,
                            #             current_date.strftime("%d_%m_%Y")
                            #             + "_"
                            #             + str(page_clicked)
                            #             + "_"
                            #             + str(index)
                            #             + ".pdf",
                            #         ),
                            #     )
                            # waits for all the files to be completed and returns the paths
                            # WebDriverWait(browser, 60, 1).until(every_downloads_chrome)
                            # print("Download company info in page {} done".format(index))
                            # time.sleep(5)
                            # if check_exists_by_xpath("//table[@id='ctl00_C_CtlList']/tbody/tr[@class='Pager']/td/table/tbody/tr/td[" + str(index) + "]/a"):
                            #     next_page_click = browser.find_element_by_xpath("//table[@id='ctl00_C_CtlList']/tbody/tr[@class='Pager']/td/table/tbody/tr/td[" + str(index) + "]/a")
                            #     print(next_page_click.text)
                            #     if next_page_click.text == "...":
                            #             index = 3
                            #     if next_page_click is not None:
                            #         next_page_click.click()
                            #         WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//table[@id='ctl00_C_CtlList']")))
                        WebDriverWait(browser, delay).until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    "//table[@id='ctl00_C_CtlList']/tbody/tr[@class='Pager']/td/table/tbody/tr/td["
                                    + str(index_page)
                                    + "]/a",
                                )
                            )
                        )
                        next_page_click = browser.find_element_by_xpath(
                            "//table[@id='ctl00_C_CtlList']/tbody/tr[@class='Pager']/td/table/tbody/tr/td["
                            + str(index_page)
                            + "]/a"
                        )
                        print(next_page_click.text)
                        if next_page_click.text == "...":
                            next_page_click = browser.find_element_by_xpath(
                                "//table[@id='ctl00_C_CtlList']/tbody/tr[@class='Pager']/td/table/tbody/tr/td["
                                + str(index_page)
                                + "]/a"
                            )
                            index_page = 3
                        if next_page_click is not None:
                            next_page_click.click()
                            WebDriverWait(browser, delay).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, "//table[@id='ctl00_C_CtlList']")
                                )
                            )
                        print(index_page)
                    else:
                        province_data_crawled[province_key] = province_value
                        lost_province_array.pop(province_key, None)
                        # try:
                        #     del province[province_key]
                        # except KeyError as ex:
                        #     print("No such key: '%s'" % ex.message)
                        browser.close()
                        break
        except ElementNotInteractableException as err:
            pass
        except NoSuchElementException as err:
            print(err)
            print(province_value)
            lost_province_array[province_key] = province_value
            browser.close()
            pass
        except TimeoutException:
            print("Loading took too much time!")
            pass
        except Exception as e:
            print(e)
            pass

    return lost_province_array

def crawl_masothue(mst_path):
    # with open(mst_path, 'r') as f:
    #     mst_new_list = f.read().splitlines()
    mst_new_list = mst_path
    options = Options()

    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")

    
    browser = webdriver.Chrome(
        executable_path="/usr/bin/chromedriver", chrome_options=options
    )
    
    # browser = webdriver.Chrome(
    #     executable_path="gdt_crawler/gdt_crawler/chromedriver",
    #     chrome_options=options,
    # )
    
    for mst in mst_new_list:
        # mst = '0' + mst	
        if len(mst) == 9:
            mst = '0' + mst
        
        browser.get(
            # "https://checkmst.com/"
            "https://masothue.com/"
        )

        WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.XPATH, "//form[@class='navbar-search tax-search']/div[@class='input-group']/input[@id='search']"))
        ) 

        mst_search_elem = browser.find_element_by_xpath(
            "//form[@class='navbar-search tax-search']/div[@class='input-group']/input[@id='search']"
        )
        
        mst_search_elem.send_keys(mst)
        # btns_pdf = browser.find_element_by_xpath(
        #     "//button[@class='btn btn-secondary btn-search-submit']"
        # )
        # btns_pdf.click()
        try:
            # WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@class='modal-header']/h5[@id='exampleModalLabel']")))
            # if check_exists_by_xpath(browser, "//div[@class='modal-content']/div[@class='modal-body']"):
            #     time.sleep(1)
            #     btn_close_model = browser.find_element_by_xpath("//div[@class='modal-footer']/button[@class='btn btn-secondary']")
            #     btn_close_model.click() 
            #     mst = '0' + mst	
            #     mst_search_elem.clear()
            #     mst_search_elem.send_keys(mst)
            #     btns_pdf.click() 
            WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "table-taxinfo")))
            with open(masothue_path, "a+") as fp:
                fp.write(mst + "," + browser.current_url + "\n")
        except Exception as e:    
            print(e)

    browser.close()
        
if __name__ == "__main__":
    sqlEngine = create_engine(
        "mysql+pymysql://root:%s@172.16.10.112:3306/hkd" % quote("Ptdl@123")
    )
    # # sqlEngine = create_engine("mysql+pymysql://root:@127.0.0.1:3306/bid")
    # query_origin = "SELECT DISTINCT mst FROM clients"

    mst_existed = pd.read_csv("mst_crawl.csv")
    mst_existed['MST'] = mst_existed['MST'].str.lstrip("'")
    mst_existed_list = mst_existed['MST'].values.tolist()

    crawl_masothue(mst_existed_list)

    # lost_province_array = crawl_bocao_data(province,mst_existed_list)

    # while True:
    #    if len(province_data_crawled) > 0:
    #        print(province_data_crawled)
    #        for key in province_data_crawled.keys():
    #            try:
    #                del province[key]
    #            except KeyError as xp:
    #                pass

    #    print(lost_province_array)

    #    if len(lost_province_array) == 0:
    #        crawl_masothue(company_file_path)
    #        break
    #    else:
    #        lost_province_array = crawl_bocao_data(lost_province_array,mst_existed_list)

