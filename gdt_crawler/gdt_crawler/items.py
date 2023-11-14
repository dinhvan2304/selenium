# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GdtCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tax_all_info = scrapy.Field()
    tax_without_gtgt = scrapy.Field()
    tax_low_off = scrapy.Field()
    tax_off = scrapy.Field()
    tax_changed = scrapy.Field()
    ma_xa = scrapy.Field()
    page_crawled = scrapy.Field()
    gdt_type = scrapy.Field()
    gdt_origin = scrapy.Field()
