# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 系统库
from collections import OrderedDict

# 第三方库
from pymongo import MongoClient

# 项目内部库
from scrapy.conf import settings


class AlipayScrapyPipeline(object):
    def __init__(self):
        # Host地址
        self.host = settings["MONGODB_HOST"]
        # 端口号
        self.port = settings["MONGODB_PORT"]
        # 数据库名字
        self.db_name = settings["MONGODB_DB_NAME"]
        # 集合名
        self.collection_name = settings["MONGODB_COLLECTION"]

        # 数据库连接
        self.client = MongoClient(host=self.host, port=self.port)

        # 指定数据库
        self.db = self.client[self.db_name]

        # 指定集合名
        # self.collection = self.db[self.collection_name]

    def process_item(self, item, spider):
        if len(item) == 6:
            collection = self.db['c_user_info']
            collection.insert(dict(item))
        elif len(item) != 6:
            collection = self.db[self.collection_name]
            collection.insert(dict(item))
        return item
