# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import logging


class GdtCrawlerPipeline:
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWD"],
            charset="utf8mb4",
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        # run the db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        # d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        # d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        d.addCallback(self._handle_error)

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        query = ""

        if len(item["tax_all_info"]) > 0:
            conn.executemany(
                """
                    INSERT INTO gdt_tax_all(tinh, huyen, xa, name, mst, ky_lap_bo, dia_chi, nganh_nghe, doanh_thu_thang, tong_thue, thue_gtgt, thue_tncn, thue_ttdb, thue_tn, thue_bvmt, phi_bvmt, don_vi_tinh) VALUES(%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s)
                """,
                item["tax_all_info"],
            )
            query = "INSERT INTO gdt_crawled_page (ma_xa, all_tax_last_page) VALUES (%s, %s) ON DUPLICATE KEY UPDATE all_tax_last_page =VALUES(all_tax_last_page)"

        if len(item["tax_without_gtgt"]) > 0:
            conn.executemany(
                """
                    INSERT INTO gdt_tax_without_gtgt(tinh, huyen, xa, name, mst, ky_lap_bo, dia_chi, nganh_nghe, doanh_thu_thang, don_vi_tinh) VALUES(%s,%s, %s,%s, %s,%s, %s,%s, %s, %s)
                """,
                item["tax_without_gtgt"],
            )
            query = "INSERT INTO gdt_crawled_page (ma_xa, tax_without_gtgt_last_page) VALUES (%s, %s) ON DUPLICATE KEY UPDATE tax_without_gtgt_last_page =VALUES(tax_without_gtgt_last_page)"

        if len(item["tax_low_off"]) > 0:
            conn.executemany(
                """
                    INSERT INTO gdt_tax_low_off(tinh, huyen, xa, name, mst, ky_lap_bo, dia_chi, nganh_nghe, off_date_from, off_date_to, don_vi_tinh) VALUES(%s,%s, %s,%s, %s,%s, %s,%s, %s, %s, %s)
                """,
                item["tax_low_off"],
            )
            query = "INSERT INTO gdt_crawled_page (ma_xa, off_low_tax_last_page) VALUES (%s, %s) ON DUPLICATE KEY UPDATE off_low_tax_last_page =VALUES(off_low_tax_last_page)"

        if len(item["tax_off"]) > 0:
            conn.executemany(
                """
                    INSERT INTO gdt_tax_off(tinh, huyen, xa, name, mst, ky_lap_bo, dia_chi_lh, dia_chi_kd, nganh_nghe, off_date_to, don_vi_tinh) VALUES(%s,%s, %s,%s, %s,%s, %s,%s, %s, %s, %s)
                """,
                item["tax_off"],
            )
            query = "INSERT INTO gdt_crawled_page (ma_xa, off_tax_last_page) VALUES (%s, %s) ON DUPLICATE KEY UPDATE off_tax_last_page =VALUES(off_tax_last_page)"

        if len(item["tax_changed"]) > 0:
            conn.executemany(
                """
                    INSERT INTO gdt_tax_changed(tinh, huyen, xa, name, mst, ky_lap_bo, dia_chi_kd_cu, dia_chi_kd_moi, nganh_nghe_cu, nganh_nghe_moi, doanh_thu_cu,doanh_thu_moi,tong_thue,thue_gtgt,thue_tncn, thue_ttdb, thue_tn, thue_bvmt, phi_bvmt,don_vi_tinh) VALUES(%s,%s, %s,%s, %s,%s, %s,%s, %s, %s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s)
                """,
                item["tax_changed"],
            )
            query = "INSERT INTO gdt_crawled_page (ma_xa, change_tax_last_page) VALUES (%s, %s) ON DUPLICATE KEY UPDATE change_tax_last_page =VALUES(change_tax_last_page)"

        if query != "":
            conn.execute(
                query,
                (
                    item["ma_xa"],
                    item["page_crawled"],
                ),
            )
        
        if len(item["gdt_origin"]) > 0:
            conn.executemany(
                """
                    INSERT INTO gdt_origin(tinh, huyen, xa, name, mst, dia_chi_kd, nganh_nghe) VALUES(%s,%s, %s,%s, %s,%s, %s)
                """,
                item["gdt_origin"],
            )

        return item

    def _handle_error(self, failure):
        """Handle occurred on db interaction."""
        # do nothing, just log
        print(failure)
