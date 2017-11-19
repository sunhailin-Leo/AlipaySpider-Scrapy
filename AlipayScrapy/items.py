# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AlipayBillItem(scrapy.Item):
    transfer_ymd = scrapy.Field()
    transfer_hms = scrapy.Field()
    transfer_memo = scrapy.Field()
    transfer_name = scrapy.Field()
    transfer_seller_code = scrapy.Field()
    transfer_transfer_code = scrapy.Field()
    transfer_serial_num = scrapy.Field()
    transfer_opposite = scrapy.Field()
    transfer_money = scrapy.Field()
    transfer_status = scrapy.Field()
    transfer_username = scrapy.Field()
    transfer_tag = scrapy.Field()


class AlipayUserItem(scrapy.Item):
    user = scrapy.Field()
    user_rest_huabei = scrapy.Field()
    user_total_huabei = scrapy.Field()
    user_yeb_rest = scrapy.Field()
    user_yeb_earn = scrapy.Field()
    create_time = scrapy.Field()
