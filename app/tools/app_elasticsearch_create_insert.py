#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 1 查询上下文中，查询操作不仅仅会进行查询，还会计算分值，用于确定相关度；在过滤器上下文中，查询操作仅判断是否满足查询条件
# 2 过滤器上下文中，查询的结果可以被缓存。

from  lib.elasticsearch_util import Elasticsearch_Util
from datetime import datetime

es_util = Elasticsearch_Util()

es_index_name = "index-student"
es_type_name = "type_student"

test_index_mapping = {
    "mappings": {
            "type_student": {
                "properties": {
                    "studentNo": {
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "name": {
                        "type": "string",
                        "index": "analyzed",
                        "analyzer": "ik"
                    },
                    "male": {
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "age": {
                        "type": "integer"
                    },
                    "birthday": {
                        "type": "date",
                        "format": "yyyy-MM-dd"
                    },
                    "address": {
                        "type": "string",
                        "index": "analyzed",
                        "analyzer": "ik"
                    },
                    "classNo": {
                        "type": "string",
                        "index": "not_analyzed "
                    },
                    "isLeader": {
                        "type": "boolean"
                    }
                }
            }
        }
}

es_util.create_index(es_index_name, test_index_mapping)

es_sample_data =   {
                "studentNo": '4',
                "name":'test',
                "male": 'male',
                "age": 20,
                "birthday": datetime.now().strftime( "%Y-%m-%dT%H:%M:%S.000+0800" ),
                "classNo": 'c100',
                "address": 'liaoning',
                "isLeader": 'true'
                }



print "begin time is ："+datetime.now().strftime( "%Y-%m-%dT%H:%M:%S.000+0800" )
es_util.insert_single_data(es_index_name, es_type_name ,es_sample_data)
print "end time is ："+datetime.now().strftime( "%Y-%m-%dT%H:%M:%S.000+0800" )

# 查询全部
query_data = {"query": {
                    "match_all": {}
                }
             }

es_util.query(es_index_name, es_type_name, query_data)
