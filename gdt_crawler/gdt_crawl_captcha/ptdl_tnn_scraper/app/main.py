# -*- coding: utf-8 -*-

import logging
import logging.config
from pathlib import Path
from webdriver import BusinessProfileScraper, PersonalProfileScraper
from captcha_solver import SolverManager
from pathlib import Path
import os
import pandas as pd
import numpy as np
import time

logger = logging.getLogger(__name__)

def run(site, command, term, values):
    logger.info('Initialising webdriver...')
    if site == 'business':
        logger.info('Navigating to mstdn.jsp')
        run_driver = BusinessProfileScraper
    elif site == 'personal':
        logger.info('Navigating to mstcn.jsp')
        run_driver = PersonalProfileScraper
    with run_driver(solver=SolverManager(),
                    headless=True) as driver:
        logger.info('Start scraping...')
        result = driver.run(command, {term:values})
        # search_keys = str({term:value})
        # result = {search_keys:result}
        logger.info('Finished scraping. Spin down driver.')
    return result

def search(site, command, term, values):
    result = run(site, command, term, values)
    return result

def save_info_mstcn(names, output_path):
    name_result = search('personal', 'sweep', 'name', names)
    name_info = name_result['result']['outer']
    # name_info_df = pd.DataFrame(name_info)
    # name_info_df.to_csv(
    #     output_path, index=False, header=False, mode="a"
    # )

def save_info_mstdn(input_path, mstdn_path):
    mst_dhsxkd = pd.read_csv(mstdn_path)
    mst_list = mst_dhsxkd['mst'].values.tolist()
    outer_path = os.path.join(input_path, 'data/tnn_outer.csv')
    inner_path = os.path.join(input_path, 'data/tnn_inner.csv')
    for taxnum in mst_list:
        result = search('business', 'pinpoint', 'taxnum', taxnum)
        if "outer" in result['result'].keys():
            dn_info_outer = result['result']['outer']
            if os.path.exists(outer_path):
                dn_info_outer.to_csv(outer_path, index=False, mode="a", header=None)
            else:
                dn_info_outer.to_csv(outer_path, index=False) 
        if "inner" in result['result'].keys():
            dn_info_inner = result['result']['inner']
            if os.path.exists(inner_path):
                dn_info_inner.to_csv(inner_path, index=False, mode="a", header=None)
            else:
                dn_info_inner.to_csv(inner_path, index=False) 
        time.sleep(6)


def scrap_by_name(input_path, existed_name):
    mstcn_path = os.path.join(parent_path, 'data/mstcn.csv')
    f = lambda list1, list2: list(filter(lambda element: element not in list2, list1))
    # with open(os.path.join(input_path, 'data/boy.txt'), 'r') as rb:
    #     boys_name_all = rb.read().splitlines()
    #     boys_name = f(boys_name_all, existed_name)

    # with open(os.path.join(input_path, 'data/girl.txt'), 'r') as rb:
    #     girls_name_all = rb.read().splitlines()
    #     girls_name = f(girls_name_all, existed_name) 

    with open(os.path.join(input_path, 'data/mstcn_name.txt'), 'r') as rb:
        mstcn_name_all = rb.read().splitlines()
        mstcn_name = f(mstcn_name_all, existed_name)

    # save_info_mstcn(boys_name, mstcn_path)
    # save_info_mstcn(girls_name, mstcn_path)
    save_info_mstcn(mstcn_name, mstcn_path)

def _default_file_mstcn(path):
    existed_name = []
    if not os.path.exists(path):
        csv_header = np.array(
            [
                [
                    'STT', 'MST', 'Name', 'Office', 'CMT', 'Updated_date', 'Note', 'Search_name'
                ]
            ]
        )
        df = pd.DataFrame(data=csv_header)
        df.to_csv(path, index=False, header=False)
    else:
        mstcn_df = pd.read_csv(path)
        existed_name = mstcn_df['Search_name'].to_list()
    
    return existed_name

if __name__ == '__main__':
    parent_path = Path(__file__).resolve().parents[1]
    mstcn_path = os.path.join(parent_path, 'data/mstcn.csv')
    mstdn_path = os.path.join(parent_path, 'data/gdt_dhsxkd.csv')
    # existed_name = _default_file_mstcn(mstcn_path)
    # scrap_by_name(parent_path, existed_name)
    save_info_mstdn(parent_path,mstdn_path)