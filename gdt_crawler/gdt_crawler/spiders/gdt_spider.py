import scrapy
import pandas as pd
from scrapy.http import Request
from gdt_crawler.items import GdtCrawlerItem
import numpy as np
import os
from sqlalchemy import create_engine
from urllib.parse import quote

current_path = os.path.dirname(os.path.abspath(__file__))
# sqlEngine = create_engine(
#     "mysql+pymysql://root:%s@172.16.10.112:3306/hkd" % quote("Ptdl@123")
# )
sqlEngine = create_engine("mysql+pymysql://root:@127.0.0.1:3306/bid")

class GdtSpiderSpider(scrapy.Spider):
    name = "gdt_spider"
    # allowed_domains = ["https://www.gdt.gov.vn/wps/portal/home/hct"]
    # start_urls = ["http://https://www.gdt.gov.vn/wps/portal/home/hct/"]
    start_url = "http://https://www.gdt.gov.vn/wps/portal/home/hct/"

    custom_settings = {
        "ITEM_PIPELINES": {"gdt_crawler.pipelines.GdtCrawlerPipeline": 500},
        "ITEM_CLASS": "gdt_crawler.items.GdtCrawlerItem",
        # "FEED_URI": "TendersScope.csv",
        # "FEED_FORMAT": "csv",
    }

    def get_url_to_crawl(self, gdt_info, type):
        if type == "11":
            new_page = gdt_info["all_tax_new_page"]
            last_page = gdt_info["all_tax_last_page"]
        elif type == "10":
            new_page = gdt_info["tax_without_gtgt_new_page"]
            last_page = gdt_info["tax_without_gtgt_last_page"]
        elif type == "12":
            new_page = gdt_info["off_low_tax_new_page"]
            last_page = gdt_info["off_low_tax_last_page"]
        elif type == "04":
            new_page = gdt_info["off_tax_new_page"]
            last_page = gdt_info["off_tax_last_page"]
        elif type == "03":
            new_page = gdt_info["change_tax_new_page"]
            last_page = gdt_info["change_tax_last_page"]

        temp_url = list()
        if new_page > last_page:
            for page in range(last_page + 1, new_page + 1):
                url_to_crawl = "https://www.gdt.gov.vn/TTHKApp/jsp/results.jsp?maTinh={}&maHuyen={}&maXa={}&hoTen=&kyLb=&diaChi=&maSoThue=&searchType={}&uuid=7be821e5-6b35-4c87-bdfa-5eedc1e47a32&pageNumber={}".format(
                    gdt_info["ma tinh"],
                    gdt_info["ma huyen"],
                    gdt_info["ma xa"],
                    type,
                    page,
                )
                temp_url.append(url_to_crawl)
        return "_".join(temp_url)

    def start_requests(self):
        query_mst = "SELECT mst FROM gdt_origin"
        gdt_mst = pd.read_sql(query_mst, con=sqlEngine)
        self.gdt_mst_list = set(gdt_mst['mst'].values.tolist())

        gdt_url_info = pd.read_csv("./gdt_url.csv")
        gdt_tax_type = "11"
        gdt_tax_without_gtgt = "10"
        gdt_off_low_tax = "12"
        gdt_off_tax = "04"
        gdt_change_tax = "03"

        gdt_url_info["tax_url"] = gdt_url_info.apply(
            lambda x: self.get_url_to_crawl(x, gdt_tax_type), axis=1
        )
        gdt_url_info["tax_without_gtgt_url"] = gdt_url_info.apply(
            lambda x: self.get_url_to_crawl(x, gdt_tax_without_gtgt), axis=1
        )
        gdt_url_info["off_low_tax_url"] = gdt_url_info.apply(
            lambda x: self.get_url_to_crawl(x, gdt_off_low_tax), axis=1
        )
        gdt_url_info["off_tax_url"] = gdt_url_info.apply(
            lambda x: self.get_url_to_crawl(x, gdt_off_tax), axis=1
        )
        gdt_url_info["change_tax_url"] = gdt_url_info.apply(
            lambda x: self.get_url_to_crawl(x, gdt_change_tax), axis=1
        )
        gdt_to_crawl = [
            t
            for t in zip(
                gdt_url_info["tinh"],
                gdt_url_info["huyen"],
                gdt_url_info["xa"],
                gdt_url_info["ma xa"],
                gdt_url_info["tax_url"],
                gdt_url_info["tax_without_gtgt_url"],
                gdt_url_info["off_low_tax_url"],
                gdt_url_info["off_tax_url"],
                gdt_url_info["change_tax_url"],
            )
        ]
        requests = list()

        # for info in gdt_to_crawl:
        #     tinh = info[0]
        #     huyen = info[1]
        #     xa = info[2]
        #     ma_xa = info[3]
        #     urls_tax = info[4].split("_")
        #     urls_tax_without_gtgt = info[5].split("_")
        #     urls_off_low_tax = info[6].split("_")
        #     urls_off_tax = info[7].split("_")
        #     urls_change_tax = info[8].split("_")
        #     for url in urls_tax:
        #         if "https" in url:
        #             requests.append(
        #                 Request(
        #                     url=url,
        #                     dont_filter=True,
        #                     callback=self.parse,
        #                     meta={
        #                         "tinh": tinh,
        #                         "huyen": huyen,
        #                         "xa": xa,
        #                         "ma_xa": ma_xa,
        #                         "gdt_type": gdt_tax_type,
        #                         # "playwright": True,
        #                     },
        #                 )
        #             )
        #     for url in urls_tax_without_gtgt:
        #         if "https" in url:
        #             requests.append(
        #                 Request(
        #                     url=url,
        #                     dont_filter=True,
        #                     callback=self.parse,
        #                     meta={
        #                         "tinh": tinh,
        #                         "huyen": huyen,
        #                         "xa": xa,
        #                         "ma_xa": ma_xa,
        #                         "gdt_type": gdt_tax_without_gtgt,
        #                         # "playwright": True,
        #                     },
        #                 )
        #             )
        #     for url in urls_off_low_tax:
        #         if "https" in url:
        #             requests.append(
        #                 Request(
        #                     url=url,
        #                     dont_filter=True,
        #                     callback=self.parse,
        #                     meta={
        #                         "tinh": tinh,
        #                         "huyen": huyen,
        #                         "xa": xa,
        #                         "ma_xa": ma_xa,
        #                         "gdt_type": gdt_off_low_tax,
        #                         # "playwright": True,
        #                     },
        #                 )
        #             )
        #     for url in urls_off_tax:
        #         if "https" in url:
        #             requests.append(
        #                 Request(
        #                     url=url,
        #                     dont_filter=True,
        #                     callback=self.parse,
        #                     meta={
        #                         "tinh": tinh,
        #                         "huyen": huyen,
        #                         "xa": xa,
        #                         "ma_xa": ma_xa,
        #                         "gdt_type": gdt_off_tax,
        #                         # "playwright": True,
        #                     },
        #                 )
        #             )
        #     for url in urls_change_tax:
        #         if "https" in url:
        #             requests.append(
        #                 Request(
        #                     url=url,
        #                     dont_filter=True,
        #                     callback=self.parse,
        #                     meta={
        #                         "tinh": tinh,
        #                         "huyen": huyen,
        #                         "xa": xa,
        #                         "ma_xa": ma_xa,
        #                         "gdt_type": gdt_change_tax,
        #                         # "playwright": True,
        #                     },
        #                 )
        #             )
        requests.append(
            
            Request(
                url="https://www.gdt.gov.vn/TTHKApp/jsp/results.jsp?maTinh=209&maHuyen=20909&maXa=2090931&hoTen=&kyLb=&diaChi=&maSoThue=&searchType=04&uuid=7be821e5-6b35-4c87-bdfa-5eedc1e47a32&pageNumber=4",
                dont_filter=True,
                callback=self.parse,
                meta={
                    "tinh": "209",
                    "huyen": "20909",
                    "xa": "2090931",
                    "ma_xa": "2090931",
                    "gdt_type": gdt_off_tax,
                    # "playwright": True,
                },
            )
        )
        return requests

    def parse(self, response):
        xstr = lambda s: "" if s is None else str(s)
        gdt_tax_type = "11"
        gdt_tax_without_gtgt = "10"
        gdt_off_low_tax = "12"
        gdt_off_tax = "04"
        gdt_change_tax = "03"

        tinh = response.meta.get("tinh")

        huyen = response.meta.get("huyen")
        xa = response.meta.get("xa")
        ma_xa = response.meta.get("ma_xa")
        page = response.url.split("=")[-1]
        type = response.meta.get("gdt_type")
        gdt_items = GdtCrawlerItem()
        gdt_items["tax_all_info"] = list()
        gdt_items["tax_without_gtgt"] = list()
        gdt_items["tax_low_off"] = list()
        gdt_items["tax_off"] = list()
        gdt_items["tax_changed"] = list()
        
        gdt_origin = list()

        if type == gdt_tax_type:
            # Crawl all tax
            number_gdt_rows = response.xpath(
                "//table[@class='ta_border']//tr/td[2]"
            ).extract()

            tax_all_info = list()
            for col in range(3, len(number_gdt_rows) + 3):
                name = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[2]/text()".format(col)
                    ).extract_first()
                )
                mst = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='mst'][1]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                
                ky_lap_bo = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='mst'][2]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                dia_chi = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[5]/text()".format(col)
                    ).extract_first()
                )
                nganh_nghe = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[6]/text()".format(col)
                    ).extract_first()
                )
                doanh_thu_thang = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='money'][1]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                tong_thue = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='money'][2]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                thue_gtgt = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[3]/td[@class='money'][3]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                thue_tncn = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='money'][4]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                thue_ttdb = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='money'][5]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                thue_tn = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='money'][6]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                thue_bvmt = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='money'][7]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                phi_bvmt = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='money'][8]/text()".format(
                            col
                        )
                    ).extract_first()
                )

                dv_tinh = xstr(
                    response.xpath("//html/body/div[2]/text()").extract_first()
                )
                if dv_tinh != "":
                    dv_tinh = dv_tinh.split(":")[-1].strip()

                tax_all_info.append(
                    (
                        tinh,
                        huyen,
                        xa,
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
                            tinh,
                            huyen,
                            xa,
                            name,
                            mst,
                            dia_chi,
                            nganh_nghe
                        )
                    )
                    self.gdt_mst_list.add(mst)
            
            gdt_items["gdt_origin"] = gdt_origin

            # update page crawed to db
            gdt_items["gdt_type"] = gdt_tax_type

            # push data to db
            gdt_items["tax_all_info"] = tax_all_info
        elif type == gdt_tax_without_gtgt:
            # Crawl tax without gtgt
            number_gdt_rows = response.xpath(
                "//table[@class='ta_border']//tr/td[2]"
            ).extract()

            tax_without_gtgt = list()
            for col in range(1, len(number_gdt_rows) + 1):
                name = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[2]/text()".format(col)
                    ).extract_first()
                )
                mst = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='mst'][1]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                ky_lap_bo = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='mst'][2]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                dia_chi = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[5]/text()".format(col)
                    ).extract_first()
                )
                nganh_nghe = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[6]/text()".format(col)
                    ).extract_first()
                )
                doanh_thu_thang = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='money']/text()".format(
                            col
                        )
                    ).extract_first()
                )
                dv_tinh = xstr(
                    response.xpath("//html/body/div[2]/text()").extract_first()
                )
                if dv_tinh != "":
                    dv_tinh = dv_tinh.split(":")[-1].strip()

                tax_without_gtgt.append(
                    (
                        tinh,
                        huyen,
                        xa,
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
                            tinh,
                            huyen,
                            xa,
                            name,
                            mst,
                            dia_chi,
                            nganh_nghe
                        )
                    )
                    self.gdt_mst_list.add(mst)
            
            gdt_items["gdt_origin"] = gdt_origin
            # update page crawed to db
            gdt_items["gdt_type"] = gdt_tax_without_gtgt

            gdt_items["tax_without_gtgt"] = tax_without_gtgt
        elif type == gdt_off_low_tax:
            # Crawl low off tax
            number_gdt_rows = response.xpath(
                "//table[@class='ta_border']//tr/td[2]"
            ).extract()

            tax_low_off = list()
            for col in range(3, len(number_gdt_rows) + 3):
                name = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[2]/text()".format(col)
                    ).extract_first()
                )
                mst = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='mst'][1]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                ky_lap_bo = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='mst'][2]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                dia_chi = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[5]/text()".format(col)
                    ).extract_first()
                )
                nganh_nghe = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[6]/text()".format(col)
                    ).extract_first()
                )
                off_date_from = response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[7]/text()".format(col)
                    ).extract_first()
                
                off_date_to =response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[8]/text()".format(col)
                    ).extract_first()

                dv_tinh = xstr(
                    response.xpath("//html/body/div[2]/text()").extract_first()
                )
                if dv_tinh != "":
                    dv_tinh = dv_tinh.split(":")[-1].strip()
                
                if off_date_from != None and "/" in off_date_from:
                    date_list_from = off_date_from.split("/")
                    off_date_from = date_list_from[-1] + "-" + date_list_from[-2] + "-" + date_list_from[0]
                
                if off_date_to != None and "/" in off_date_to:
                    date_list_to = off_date_to.split("/")
                    off_date_to = date_list_to[-1] + "-" + date_list_to[-2] + "-" + date_list_to[0] 

                tax_low_off.append(
                    (
                        tinh,
                        huyen,
                        xa,
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
                            tinh,
                            huyen,
                            xa,
                            name,
                            mst,
                            dia_chi,
                            nganh_nghe
                        )
                    )
                    self.gdt_mst_list.add(mst)
            
            gdt_items["gdt_origin"] = gdt_origin
            # update page crawed to db
            gdt_items["gdt_type"] = gdt_off_low_tax
            gdt_items["tax_low_off"] = tax_low_off
        elif type == gdt_off_tax:
            # Crawl off tax
            number_gdt_rows = response.xpath(
                "//table[@class='ta_border']//tr/td[2]"
            ).extract()

            tax_off = list()
            for col in range(1, len(number_gdt_rows) + 1):
                name = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[2]/text()".format(col)
                    ).extract_first()
                )
                mst = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='mst'][1]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                ky_lap_bo = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='mst'][2]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                dia_chi_lh = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[5]/text()".format(col)
                    ).extract_first()
                )
                dia_chi_kd = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[6]/text()".format(col)
                    ).extract_first()
                )
                nganh_nghe = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[7]/text()".format(col)
                    ).extract_first()
                )
                off_date_to = response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[8]/text()".format(col)
                    ).extract_first()

                dv_tinh = xstr(
                    response.xpath("//html/body/div[2]/text()").extract_first()
                )
                if dv_tinh != "":
                    dv_tinh = dv_tinh.split(":")[-1].strip()

                if off_date_to != None and "/" in off_date_to:
                    date_list_to = off_date_to.split("/")
                    off_date_to = date_list_to[-1] + "-" + date_list_to[-2] + "-" + date_list_to[0] 

                tax_off.append(
                    (
                        tinh,
                        huyen,
                        xa,
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
                            tinh,
                            huyen,
                            xa,
                            name,
                            mst,
                            dia_chi_kd,
                            nganh_nghe
                        )
                    )
                    self.gdt_mst_list.add(mst)
            
            gdt_items["gdt_origin"] = gdt_origin
            # update page crawed to db
            gdt_items["gdt_type"] = gdt_off_tax
            gdt_items["tax_off"] = tax_off
        elif type == gdt_change_tax:
            # Crawl off tax
            number_gdt_rows = response.xpath(
                "//table[@class='ta_border']//tr/td[2]"
            ).extract()

            tax_changed = list()
            for col in range(3, len(number_gdt_rows) + 3):
                name = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[2]/text()".format(col)
                    ).extract_first()
                )
                mst = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='mst'][1]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                ky_lap_bo = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='mst'][2]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                dia_chi_kd_cu = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[5]/text()".format(col)
                    ).extract_first()
                )
                dia_chi_kd_moi = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[6]/text()".format(col)
                    ).extract_first()
                )
                nganh_nghe_cu = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[7]/text()".format(col)
                    ).extract_first()
                )
                nganh_nghe_moi = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[8]/text()".format(col)
                    ).extract_first()
                )
                doanh_thu_cu = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='money'][1]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                doanh_thu_moi = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='money'][2]/text()".format(
                            col
                        )
                    ).extract_first()
                )

                tong_thue = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='money'][3]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                thue_gtgt = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[3]/td[@class='money'][4]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                thue_tncn = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='money'][5]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                thue_ttdb = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='money'][6]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                thue_tn = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='money'][7]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                thue_bvmt = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='money'][8]/text()".format(
                            col
                        )
                    ).extract_first()
                )
                phi_bvmt = xstr(
                    response.xpath(
                        "//table[@class='ta_border']//tr[{}]/td[@class='money'][9]/text()".format(
                            col
                        )
                    ).extract_first()
                )

                dv_tinh = xstr(
                    response.xpath("//html/body/div[2]/text()").extract_first()
                )
                if dv_tinh != "":
                    dv_tinh = dv_tinh.split(":")[-1].strip()

                tax_changed.append(
                    (
                        tinh,
                        huyen,
                        xa,
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
                            tinh,
                            huyen,
                            xa,
                            name,
                            mst,
                            dia_chi_kd_moi,
                            nganh_nghe_moi
                        )
                    )
                    self.gdt_mst_list.add(mst)
            
            gdt_items["gdt_origin"] = gdt_origin
            # update page crawed to db
            gdt_items["gdt_type"] = gdt_change_tax
            gdt_items["tax_changed"] = tax_changed

        gdt_items["ma_xa"] = ma_xa
        gdt_items["page_crawled"] = page

        if gdt_items != None:
            yield gdt_items
        else:
            pass
