#!/usr/bin/env python
# -*- coding:utf-8 -*-

from elasticsearch import Elasticsearch
from elasticsearch import helpers
import logging
import sys
import json
import app.config as config


reload(sys)
sys.setdefaultencoding( "utf-8" )

class Elasticsearch_Util():

    def __init__(self):

        # 日志基本配置，将日志文件输出到当前目录下的elastticsearch_sample.log文件中
        logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='log/elastticsearch_sample.log',
                filemode='w')

        # 将日志打印在屏幕上

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

        self.elastalert_logger = logging.getLogger('Elasticsearch_Util')

        # 连接elasticsearch

        self.es = Elasticsearch([config.ES_HOST],
                                http_auth=('admin', 'admin'),
                                port=config.ES_PORT)

    # 查询方法
    def query(self, index_name, type_name, querybody):

        res = self.es.search(index=index_name, doc_type=type_name, body=querybody)

        # print(" res value is : "+str(res).decode("unicode_escape").encode("utf8"))
        # result = json.dumps(res, indent=4)
        return res
        # self.elastalert_logger.info(str(res).decode("unicode_escape").encode("utf8"))

    # 查询并过滤结果显示字段方法
    def query_and_filter(self, index_name, type_name, querybody,result_filter):

        res = self.es.search(index=index_name, doc_type=type_name, body=querybody,filter_path=[result_filter])

        # print(" res value is : "+str(res).decode("unicode_escape").encode("utf8"))
        print json.dumps(res, indent=4)
        # self.elastalert_logger.info(str(res).decode("unicode_escape").encode("utf8"))

    def query_index(self, index_name, querybody):

        res = self.es.search(index=index_name, body=querybody)
        print(" res value is : "+str(res).decode("unicode_escape").encode("utf8"))

    def query_count(self, index_name , type_name):

        res = self.es.search(index=index_name, doc_type=type_name, body={"query":{"match_all":{}}})

        print(index_name +" Got %d Hits: " % res.get("hits").get("total"))


    #创建索引
    def create_index(self, index_name,mapping_body ):

            # processdefine
            if self.es.indices.exists(index=index_name) :
                self.es.indices.delete(index_name)

            processdef_index_mapping = mapping_body

            self.es.indices.create(index=index_name, ignore=400,
                                       body=mapping_body)
    # 单条插入数据
    def insert_single_data(self, index_name, typep_name , esdata):
        self.elastalert_logger.info(str(esdata).decode("unicode_escape").encode("utf8"))
        self.es.index(index=index_name, doc_type=typep_name, body=esdata,refresh='true')

    # 批量插入数据
    def insert_bulk_data(self, esdatas):
        self.elastalert_logger.info(str(esdatas).decode("unicode_escape").encode("utf8"))
        helpers.bulk(self.es, esdatas)

    # 删除索引
    def delete_index(self, index_name):
        self.es.indices.delete(index=index_name, ignore=[400, 404])

