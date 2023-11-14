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
import pandas as pd
import numpy as np
import time

def scrap_info(browser):
	
	# WebDriverWait(browser, 15).until(
	# 	EC.presence_of_element_located((By.XPATH, "//div[@class='bxh']"))
	# )
	
	stt_elems = browser.find_elements(By.XPATH,
                                "//div[@id='dataTables-search_wrapper']/table[@id='dataTables-search']//tr/th[@class='sorting_1']"
                            )
	stt_list = [i.text for i in stt_elems]

	name_elems = browser.find_elements(By.XPATH,
                                    "//div[@id='dataTables-search_wrapper']/table[@id='dataTables-search']//tr/th[2]/span/span[@class='name_1']/a")
	name_list = [i.text for i in name_elems]

	ceo_name_elems = browser.find_elements(By.XPATH,"//div[@id='dataTables-search_wrapper']/table[@id='dataTables-search']//tr/th[2]/span/div[@class='row']/span[@class='col-xs-12 col-sm-6 mst']/span[@class='ceo']/a")
	ceo_name_list = [i.text for i in ceo_name_elems]

	mst_elems = browser.find_elements(By.XPATH,
                                   "//div[@id='dataTables-search_wrapper']/table[@id='dataTables-search']/tbody/tr/th[2]/span/div[@class='row']/span[@class='col-xs-12 col-sm-6 mst']/span[2]")
	mst_list = [i.text for i in mst_elems]

	nganhnghe_elems = browser.find_elements(By.XPATH,
                                         "//div[@id='dataTables-search_wrapper']/table[@id='dataTables-search']/tbody/tr/th[2]/span/div[@class='row']/span[@class='col-xs-12 col-sm-6 nganh-nghe']/span/a[2]")
	nganhnghe_list = [i.text for i in nganhnghe_elems]

	vnr_500_list = list(zip(stt_list, name_list, ceo_name_list, mst_list, nganhnghe_list))

	vnr_500_df = pd.DataFrame(vnr_500_list)


	ocr_dir = "vnr_profit_500_1.csv"


	if not os.path.exists(ocr_dir):
		csv_header = np.array(
			[
				[
					'STT', 'Company', 'CEO', 'MST', 'NGANH_NGHE'
				]
			]
		)
		df = pd.DataFrame(data=csv_header)
		df.to_csv(ocr_dir, index=False, header=False)

		df_data = pd.DataFrame(data=vnr_500_df)
		df_data.to_csv(
			ocr_dir, index=False, header=False
		)
	else:
		df = pd.DataFrame(data=vnr_500_df)
		df.to_csv(
			ocr_dir,
			index=False,
			header=False,
			mode="a",
		)

def check_exists_by_xpath(browser, xpath):
	try:
		elem = browser.find_element(By.CLASS_NAME,xpath)
	except NoSuchElementException:
		return None
	return elem

def crawl_vnr500():
	# current_path = os.path.dirname(os.path.abspath(__file__))
	options = Options()
	# options.add_argument("--no-sandbox")
	# options.add_argument("--headless")
	# options.add_argument("--disable-dev-shm-usage")
	browser = webdriver.Chrome(
            executable_path=r'/Users/dinhvan/Downloads/chromedriver',
            chrome_options=options,
        )
	browser.get(
            "https://vnr500.com.vn/Charts/Index?chartId=2&year=2021"
        )

	range_page = 11
	click_gg_ads = False
	for _ in range(range_page):
		scrap_info(browser)
		time.sleep(2)
		if click_gg_ads == False:
			gg_ads_btn = check_exists_by_xpath(browser, "grippy-host")
			if gg_ads_btn:
				gg_ads_btn.click()
				click_gg_ads = True
				time.sleep(2)
			
		pages = browser.find_elements(By.CLASS_NAME,
                                "paginate_button")
		for index, page in enumerate(pages):
			page_class = page.get_attribute("class")
			if "current" in page_class:
				page_to_click = pages[index+1]
				page_to_click.click()
				time.sleep(2)
				break

if __name__ == "__main__":
	crawl_vnr500()