#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import division
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from app import config, Elasticsearch_Util
from sklearn.preprocessing import LabelEncoder
from app.lib import nltk_text_analyze_lib as textAnalyzer
import pandas as pd
import datetime

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
            "includes": source_include,
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


def readDataLine(lineStr):
    if len(lineStr) == 0:
        return
    else:
        feature_data_array = []
        featureValue = lineStr.lower().strip()
        feature_data_array.append(featureValue)
        return feature_data_array


index = "1008-syslog-*"
type = "syslog"
beginTime = "2017-12-15T00:00:00.000+08:00"
endTime = "2017-12-16T00:00:00.000+08:00"
fromnum = 0
size = 1000
tag = "level"
logmsg = "logmsg"
source_include = [tag, logmsg]

es_util = Elasticsearch_Util()
train_data = getDataFromES(es_util, index=index, type=type,
                           beginTime=beginTime, endTime=endTime,
                           fromnum=fromnum, size=size,
                           source_include=source_include)
print '数据总条数:%s' % len(train_data)

# feature_data_array = train_data[logmsg]
# class_data_array = train_data[tag]
# print len(feature_data_array)
# print len(class_data_array)

# 提取特征
# tf_transformer = TfidfVectorizer(tokenizer=textAnalyzer.tokenize, stop_words='english', decode_error='ignore')
# feature_datas = tf_transformer.fit_transform(feature_data_array)
# print feature_datas.toarray()
# print tf_transformer.get_feature_names()

# 将类别转化为数字标签
# le = LabelEncoder()
# train_labelValues = le.fit_transform(class_data_array)
# model = DecisionTreeClassifier()
# model.fit(feature_datas, train_labelValues)

# othertestdata
model = joblib.load(r'modelspkl\teststack0_130\knowledge_cart.pkl')
tf_transformer = joblib.load(r'modelspkl\teststack0_130\knowledge_tf_transformer.pkl')
le = joblib.load(r'modelspkl\teststack0_130\knowledge_labelencoder.pkl')

errors = []
for indexs in train_data.index:
    logBody = train_data.loc[indexs, logmsg]
    isException = train_data.loc[indexs, tag]

    test_datas = readDataLine(logBody)
    test_feature_datas = tf_transformer.transform(test_datas)
    pred = model.predict(test_feature_datas)
    guess = le.inverse_transform(pred)
    # print ('correct:%s, guess:%s,logmsg:%s' % (isException, guess[0], logBody))
    # if guess[0] != isException:
    if (guess[0] == "1") and (isException.strip().lower() != "error"):
        errors.append((isException, guess[0], logBody))
    elif (guess[0] == "0") and (isException.strip().lower() == "error"):
        errors.append((isException, guess[0], logBody))

print '预测结果异常总条数:%s' % len(errors)
print '预测异常比:%s' % (len(errors) / len(train_data))

for (tag, guess, name) in sorted(errors):
    print 'correct=%-8s guess=%-8s name=%-30s' % (tag, guess, name)

# =====================================================
endtime = datetime.datetime.now()
print ("当前的日期和时间是 %s" % endtime)

print '时间差：%s' % (endtime - starttime).microseconds
print '============='
