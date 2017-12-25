#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 1 查询上下文中，查询操作不仅仅会进行查询，还会计算分值，用于确定相关度；在过滤器上下文中，查询操作仅判断是否满足查询条件
# 2 过滤器上下文中，查询的结果可以被缓存。

from  app.lib.elasticsearch_util import Elasticsearch_Util
from datetime import datetime
import xlrd
import app.lib.apriori as apriori

es_util = Elasticsearch_Util()

es_index_name = "elast-alert-20171208"
es_type_name = "elast-alert"

test_index_mapping = {
    "mappings": {
            "elast-alert": {
                "properties": {
                    "@timestamp": {
                        "type": "date",
                        "format": "yyyy-MM-dd'T'HH:mm:ss"
                    },
                    "schedule_batchid": {
                        "type": "keyword"
                    },
                    "msgId": {
                        "type": "keyword"
                    },
                    "remindName": {
                        "type": "keyword"
                    },
                    "searchCondition": {
                        "type": "keyword"
                    },
                    "searchIndex": {
                        "type": "keyword"
                    },
                    "remindPerson": {
                        "type": "keyword"
                    },
                    "remindEmail": {
                        "type": "keyword"
                    },
                    "remindStatus": {
                        "type": "keyword"
                    },
                    "remindType": {
                        "type": "keyword"
                    },
                    "remindWay": {
                        "type": "keyword"
                    },
                    "remindMessage": {
                        "type": "string",
                        "index": "analyzed",
                        "analyzer": "ik_max_word"
                    }
                }
            }
        }
}



# 从excel批量导入数据
def insert_data_from_xls():
    data = xlrd.open_workbook('/Users/yangwm/log/exceldata/elast-alert.xls')  # 打开xls文件
    table = data.sheets()[0]  # 打开第一张表
    esdatas = []
    nrows = table.nrows  # 获取表的行数
    for i in range(nrows):  # 循环逐行打印

        rows = table.row_values(i)

        esdata = {
            "_index": es_index_name,
            "_type": es_type_name,
            "_id": i,
            "_source": {
                "@timestamp": datetime.strptime(str(rows[0]), '%Y/%m/%d %H:%M:%S'),
                "schedule_batchid": str(rows[1]),
                "msgId": str(rows[2]),
                "remindName": str(rows[3]),
                "searchCondition": str(rows[4]),
                "searchIndex": str(rows[5]),
                "remindPerson": rows[6],
                "remindEmail": str(rows[7]),
                "remindStatus": str(rows[8]),
                "remindType": str(rows[9]),
                "remindWay": str(rows[10]),
                "remindMessage": str(rows[11])
            }
        }
        esdatas.append(esdata)
    es_util.insert_bulk_data(esdatas)
    # print str(esdatas)


def getAlertDataFromES():
    # 最大查询10000条数据
    query_data = {  "from" :0,
                    "size" :10000,
                    "sort" : [{ "@timestamp" : {"order" : "asc"}}],
                    "query": {
                        "match_all": {}
                    }
                 }

    print es_util.query_count(es_index_name,es_type_name)

    res = es_util.query(es_index_name, es_type_name, query_data)

    data = [doc for doc in res['hits']['hits']]
    frequency_items = {}
    search_conditions = ""
    for doc in res['hits']['hits']:
        print("%s) %s %s %s " % (doc['_id'], doc['_source']['@timestamp'], doc['_source']['schedule_batchid'], doc['_source']['searchCondition']))
        schedule_patch_id = doc['_source']['schedule_batchid']
        search_condition = doc['_source']['searchCondition']

        if frequency_items.has_key(schedule_patch_id):
            frequency_items[schedule_patch_id] = frequency_items[schedule_patch_id] + ',' + search_condition
        else:
            frequency_items[schedule_patch_id] = search_condition

    print frequency_items

    for item in frequency_items.values():
        print item
        record = frozenset(item.split(','))
        yield record

# es_util.delete_index(es_index_name)
#
# es_util.create_index(es_index_name, test_index_mapping)
#
# insert_data_from_xls()

items, rules = apriori.runApriori(getAlertDataFromES(), 0.01, 0.6)
apriori.printResults(items, rules)
