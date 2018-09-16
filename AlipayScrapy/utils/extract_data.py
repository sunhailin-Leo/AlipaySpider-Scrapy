# -*- coding: utf-8 -*- #
"""
Created on 2018年9月16日
@author: Leo
"""
# 暂时没用的代码(可以用来解析账单数据导出的csv结果从pandas dataframe -> MongoDB数据库中)
"""
import os
import json
import zipfile
import pandas as pd
from pymongo import MongoClient

path = "../.././static/temp_file/alipay_record_20180916_0109_1.csv"


class MongoBase:
    def __init__(self, collection):
        self.collection = collection
        self.open_mgo()

        self.conn = None
        self.db = None

    def open_mgo(self):
        self.conn = MongoClient(host="127.0.0.1", port=27017)
        self.db = self.conn['test']
        self.collection = self.db[self.collection]


def unzip_file_and_read():
    # 解压路径
    unzip_path = "../.././static/temp_file/"
    # 获取压缩文件
    f_list = os.listdir(path=unzip_path)
    # 压缩包路径
    zip_path = unzip_path + f_list[0]
    # 解压
    z = zipfile.ZipFile(zip_path, 'r')
    z.extractall(path=unzip_path)
    z.close()
    # 删除压缩包
    os.remove(path=zip_path)
    # 读取压缩包中的csv文件
    read_csv(csv_path=unzip_path + os.listdir(path=unzip_path)[0])


def read_csv(csv_path: str):
    # 读取数据
    df = pd.read_csv(path, header=3, encoding="GBK", skiprows=[3], skipfooter=7)
    # 重命名列名(存在空格)
    df = df.rename(columns=lambda x: x.strip())
    # 去除多余的列
    last_col_name = df.columns.tolist()[-1]
    del df[last_col_name]
    # 去除交易号、商户订单号的制表符
    for i in range(2):
        df[df.columns.tolist()[i]] = df[df.columns.tolist()[i]].apply(lambda x: x.replace('\t', ""))
    for i in range(2, len(df.columns.tolist())):
        if i != 9 and i != 12 and i != 13:
            df[df.columns.tolist()[i]] = df[df.columns.tolist()[i]].apply(lambda x: str(x).strip())
        else:
            df[df.columns.tolist()[i]] = df[df.columns.tolist()[i]].apply(lambda x: str(x).strip()).astype('float')
    # 删除csv
    # os.remove(path=csv_path)
    # 写入到MongoDB
    mongo = MongoBase('test')
    mongo.collection.insert(json.loads(df.T.to_json(force_ascii=False)).values())


if __name__ == '__main__':
    # unzip_file_and_read()
    read_csv(csv_path="")
"""
