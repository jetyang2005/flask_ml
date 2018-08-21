#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import NotFoundError
import logging
import sys
import json
import app.config as config

import importlib
importlib.reload(sys)



class Elasticsearch_Util():

    def __init__(self):

        # 日志基本配置，将日志文件输出到当前目录下的elastticsearch.log文件中
        logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=config.ELASTICSEARCH_LOG_DIR,
                filemode='a')

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
        print (json.dumps(res, indent=4))
        # self.elastalert_logger.info(str(res).decode("unicode_escape").encode("utf8"))

    def query_index(self, index_name, querybody):

        res = self.es.search(index=index_name, body=querybody)
        print(" res value is : "+str(res).decode("unicode_escape").encode("utf8"))

    def query_count(self, index_name , type_name):

        res = self.es.search(index=index_name, doc_type=type_name, body={"query":{"match_all":{}}})

        print(index_name +" Got %d Hits: " % res.get("hits").get("total"))

    def getMoreDataFromES(self, index, doc_type, source_include, size):
        querybody = {
            "query": {
                "match_all": {}
            },
            "_source": {
                "includes": source_include,
                "excludes": []
            }
        }
        # Initialize the scroll
        print("Initialize the scroll")

        page = self.es.search(
            index=index,
            doc_type=doc_type,
            scroll='2m',
            size=size,
            body=querybody)
        sid = page['_scroll_id']
        scroll_size = page['hits']['total']

        print("sid: " + str(sid))
        print("scroll size: " + str(scroll_size))
        records = []
        for doc in page['hits']['hits']:
            source = doc['_source']
            # source["id"] = doc['_id']
            # source["index"] = doc['_index']
            #            if doc['_source']['logBody']!=None and doc['_source']['logBody']!="":
            records.append(source)

        df = None
        # Start scrolling
        while (scroll_size > 0):
            print("Scrolling...")
            page = self.es.scroll(scroll_id=sid, scroll='2m')
            # Update the scroll ID
            sid = page['_scroll_id']
            print("sid: " + str(sid))
            # Get the number of results that we returned in the last scroll
            scroll_size = len(page['hits']['hits'])

            for doc in page['hits']['hits']:
                source = doc['_source']
                #source["id"] = doc['_id']
                #source["index"] = doc['_index']
                #            if doc['_source']['logBody']!=None and doc['_source']['logBody']!="":
                records.append(source)

            print("scroll size: " + str(scroll_size))
        if records:
            df = pd.DataFrame(records)
            # Do something with the obtained page
        return df

    def es_read_scroll_scan(self, index, doc_type, querybody,size):
        # Initialize the scroll
        page = self.es.search(
            index=index,
            doc_type=doc_type,
            scroll='2m',
            size=size,
            body=querybody)
        sid = page['_scroll_id']
        scroll_size = page['hits']['total']

        # Start scrolling
        while (scroll_size > 0):
            print ("Scrolling...")
            page = self.es.scroll(scroll_id=sid, scroll='2m')
            # Update the scroll ID
            sid = page['_scroll_id']
            # Get the number of results that we returned in the last scroll
            scroll_size = len(page['hits']['hits'])
            print ("scroll size: " + str(scroll_size))
            # Do something with the obtained page

    def es_read_querybody(self, index, doc_type, querybody):
        """
        Read from an ElasticSearch index and return a DataFrame
        :param keys: a list of keys to extract in elasticsearch
        :param index: the ElasticSearch index to read
        :param doc_type: the ElasticSearch doc_type to read
        """
        self.successful_ = 0
        self.failed_ = 0

        # Collect records for all of the keys
        records = []

        res = self.es.search(index=index, doc_type=doc_type, body=querybody)

        for record in res['hits']['hits']:
            self.successful_ += 1
            if '_source' in record:
                #print record['_source']
                records.append(record['_source'])
        print ("es hit total:",len(records))
        # Prepare the records into a single DataFrame
        df = None
        if records:
            df = pd.DataFrame(records)
            #df = pd.DataFrame(records).fillna(value=np.nan)
            #df = df.reindex(sorted(df.columns), axis=1)
        return df

    def es_write(self, df, index, doc_type, uid_name='indexId'):
        """
        Insert a Pandas DataFrame into ElasticSearch
        :param df: the DataFrame, must contain the column 'indexId' for a unique identifier
        :param index: the ElasticSearch index
        :param doc_type: the ElasticSearch doc_type
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError('df must be a pandas DataFrame')

        if not self.client.indices.exists(index=index):
            print('index does not exist, creating index')
            self.client.indices.create(index)

        if not uid_name in df.columns:
            raise ValueError('the uid_name must be a column in the DataFrame')

        if len(df[uid_name]) != len(set(df[uid_name])):
            message = 'the values in uid_name must be unique to use as an ElasticSearch _id'
            raise ValueError(message)
        self.uid_name = uid_name

        def generate_dict(df):
            """
            Generator for creating a dict to be inserted into ElasticSearch
            for each row of a pd.DataFrame
            :param df: the input pd.DataFrame to use, must contain an '_id' column
            """
            records = df.to_dict(orient='records')
            for record in records:
                yield record

        # The dataframe should be sorted by column name
        df = df.reindex_axis(sorted(df.columns), axis=1)
        df = df.astype('str')

        data = ({'_index': index,
                 '_type': doc_type,
                 '_id': record[uid_name],
                 '_source': record}
                for record in generate_dict(df))
        helpers.bulk(self.client, data)

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
        self.elastalert_logger.info(str(esdatas))
        #.decode("unicode_escape").encode("utf8")
        helpers.bulk(self.es, esdatas)

    # 删除索引
    def delete_index(self, index_name):
        self.es.indices.delete(index=index_name, ignore=[400, 404])

