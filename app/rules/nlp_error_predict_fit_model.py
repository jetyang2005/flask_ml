#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier

from app import config, Elasticsearch_Util
from sklearn.preprocessing import LabelEncoder
from app.lib import nltk_text_analyze_lib as textAnalyzer
from app.lib import sklearn_classification_lib as skclassification

import pandas as pd
# import time
import datetime

# print time.time()
# print time.localtime(time.time())
# print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


starttime = datetime.datetime.now()
print ("当前的日期和时间是 %s" % starttime)


def getDataFromES(es_util, index, type, beginTime, endTime, fromnum, size, source_include):
    # 最大查询10000条数据
    query_data = {
        "from": fromnum,
        "size": size,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "from": beginTime,
                                "to": endTime
                            }
                        }
                    }
                ],
            }
        },
        "_source": {
            "includes": source_include
            # [include_field01, include_field02
            # "title", "question"
            # "system.diskio.name", "metricset.rtt"]
            ,
            "excludes": []
        },
        "sort": [
            {
                "@timestamp": {
                    "order": "desc"
                }
            }
        ]
    }
    # print es_util.query_count(es_index_name, es_type_name)
    res = es_util.query(index, type, query_data)
    # print res

    df = None
    records = []
    for doc in res['hits']['hits']:
        # print("%s %s %s " % (doc['_id'], doc['_source']['question'], doc['_source']['title']))
        records.append(doc['_source'])
    if records:
        df = pd.DataFrame(records)
        # .fillna(value=np.nan)
        # df = df.reindex_axis(sorted(df.columns), axis=1)
    return df


def scanDataFromES2(es_util, index, type, source_include, scroll, beginTime, endTime):
    query_data = {
        "from": fromnum,
        "size": size,
        "query": {
            "range": {
                "@timestamp": {
                    "gte": beginTime,
                    "lte": endTime
                }
            }
            # "bool": {
            #    "must": [
            #        {
            #            "range": {
            #                "@timestamp": {
            #                    "from": beginTime,
            #                    "to": endTime
            #                }
            #            }
            #        }
            #    ],
            # "filter": [
            # {
            #    "term": {
            #        "status": "published"
            #    }
            # },
            # {
            #    "range": {
            #        "@timestamp": {
            #            "gte": "2015-01-01"
            #        }
            #    }
            # }
            # ]
            # }
        },
        "_source": {
            "includes": source_include,
            "excludes": []
        },
        # "sort": [
        #    {
        #        "@timestamp": {
        #            "order": "desc"
        #        }
        #    }
        # ]
    }
    res = es_util.query_more(index, type, query_data, scroll=scroll)
    # print res
    df = None
    records = []
    for item in res:
        # print item
        records.append(item['_source'])
        # print item['_source']
    print ('数据条数：%s' % (len(records)))
    if records:
        df = pd.DataFrame(records)
    return df


# 获取10000条以上的数据
def scanDataFromES(es_util, index, type, source_include, scroll):
    query_data = {
        "query": {
            "match_all": {}
        },
        "_source": {
            "includes": source_include,
            "excludes": []
        }
    }
    res = es_util.query_more(index, type, query_data, scroll=scroll)
    # print res
    df = None
    records = []
    for item in res:
        # print item
        records.append(item['_source'])
        # print item['_source']
    print ('数据条数：%s' % (len(records)))
    if records:
        df = pd.DataFrame(records)
    return df


es_util = Elasticsearch_Util()

#   查询45个分片中用的45个,12734命中,耗时0.02秒
# beginTime = "2018-01-03T00:00:00.000+08:00"
# endTime = "2018-01-05T00:00:00.000+08:00"

# getDataFromES(es_util, beginTime, endTime)
# index = "1012-knowledgelibrary-*"
# type = "knowledgeLibrary"

index = "1012-knowledge_training-*"
type = "knowledge_training"
beginTime = "2018-01-10T00:00:00.000+08:00"
endTime = "2018-01-11T00:00:00.000+08:00"
fromnum = 0
size = 100
tag = "isException"
logmsg = "logBody"
source_include = [tag, logmsg]

scroll = "5m"

# train_data = scanDataFromES2(es_util, index=index, type=type, source_include=source_include, scroll=scroll,
#                             beginTime=beginTime, endTime=endTime)

# train_data = scanDataFromES(es_util, index=index, type=type, source_include=source_include, scroll=scroll)

train_data = getDataFromES(es_util, index=index, type=type,
                           beginTime=beginTime, endTime=endTime,
                           fromnum=fromnum, size=size,
                           source_include=source_include)
feature_data_array = train_data[logmsg]
class_data_array = train_data[tag]
# print feature_data_array
# print class_data_array


# 提取特征
tf_transformer = TfidfVectorizer(tokenizer=textAnalyzer.tokenize, stop_words='english', decode_error='ignore')
feature_datas = tf_transformer.fit_transform(feature_data_array)
# joblib.dump(tf_transformer, 'knowledge_tf_transformer.pkl')

# 将类别转化为数字标签
le = LabelEncoder()
train_labelValues = le.fit_transform(class_data_array)
# joblib.dump(le, 'knowledge_labelencoder.pkl')

# model = DecisionTreeClassifier()
# model.fit(feature_datas, train_labelValues)
# joblib.dump(model, 'knowledge_cart.pkl')

skclassification.compareAlgorithm(X_train=feature_datas, Y_train=train_labelValues, X_validation=feature_datas,
                                  Y_validation=train_labelValues)
# =====================================================
endtime = datetime.datetime.now()
print ("当前的日期和时间是 %s" % endtime)

print ('时间差：%s' % ((endtime - starttime).microseconds))
print '============='
