#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import pandas as pd
import datetime

os.chdir('D:/zxdf/Workspaces/PycharmProjects/flask_ml')
from app import config, Elasticsearch_Util
#from app.lib import nltk_text_analyze_lib as textAnalyzer
#from app.lib import sklearn_classification_lib as skclassification

starttime = datetime.datetime.now()
print ("当前的日期和时间是 %s" % starttime)

def getDataFromES():
    df = None
    records = [
        {"isException" : 0, "logBody" :"-Mapped java.lang.StringIndexOutOfBoundsException: String index out of range: 0 String String"},
        {"isException" : 1, "logBody" :"-Mapped java.lang.StringIndexOutOfBoundsException:  index out of range: 0"  }
    ]
    if records:
        df = pd.DataFrame(records)
    return df

from sklearn.preprocessing import LabelEncoder

tag = "isException"
logmsg = "logBody"

train_data = getDataFromES()
feature_data_array = train_data[logmsg]
class_data_array = train_data[tag]
print len(feature_data_array)
print len(class_data_array)
# 将类别转化为数字标签
#le = LabelEncoder()
#train_labelValues = le.fit_transform(class_data_array)


#训练数据日志体
for indexs in train_data.index:
    print "%s%s" %(train_data.loc[indexs].values[0:1],train_data.loc[indexs].values[1:2])

import nltk
import string
from nltk.corpus import stopwords


# 训练数据关键词提取列表
def tokenize(text):
    tokens = nltk.word_tokenize(text)
    tokens2 = []
    for w in tokens:
        if w[0] == '-':
            tokens2.append(w[1:])
        elif w[0] == "'":
            tokens2.append(w[1:])
        else:
            tokens2.append(w)

    stopword_tokens = [i for i in tokens2 if i not in string.punctuation]
    stopword_tokens2 = [w for w in stopword_tokens if w not in stopwords.words('english')]

    stopwords_custom = ["''", "``", "||", "'/", "'/'", u"'0x0", "'2", "'=", "'s", '**', '***', '***.***',
                        '**constraint.unique_wt**', '**failed', '**method', '--',
                        '-1', '-297991290629036654', '-614', '-6182496564283649260', '-6787310117729693199', '-8',
                        '-999999999', u'-e',
                        '..', '...', '.\\xxx\\xxx.txt', '/*', '/**', '/c', '/p', '0', '1', '==', 'b', 'c', 'e', 'x',
                        '===',
                        'v'
                        ]
    stopword_tokens3 = [w for w in stopword_tokens2 if w not in stopwords_custom]

    print  "%s" % (stopword_tokens3)
    return stopword_tokens3


from sklearn.feature_extraction.text import CountVectorizer
#tokenizer=tokenize,
vectorizer=CountVectorizer( stop_words='english', decode_error='ignore')
csr_mat = vectorizer.fit_transform(feature_data_array)
# 获取词袋模型中的所有词
wordlist = vectorizer.get_feature_names()
# tf矩阵 元素a[i][j]表示j词在i类文本中的tf
countlist = csr_mat.toarray()

#对应文档的关键词词频统计
# 打印每类文本的tf词语词频，第一个for遍历所有文本，第二个for便利某一类文本下的词频
for i in range(len(countlist)):
    print "%s"%"---------------------------------------------------line",i,"---------------------------------------------------"
    for j in range(len(wordlist)):
            if  countlist[i][j]>0:
                print "%s" %  "keyword[",wordlist[j],"] tf[",countlist[i][j],"]"

# 提取特征
from sklearn.feature_extraction.text import TfidfTransformer
tf_transformer=TfidfTransformer(norm=None)
feature_datas= tf_transformer.fit_transform(csr_mat)
weighttlist = feature_datas.toarray()

#获得倒序的词频统计列表（词总数，词，所有出现改词的文档列表（文档id，词数））
listtext=[]
for j in range(len(wordlist)):
    lineidcountarray=[]
    count=0
    for i in range(len(weighttlist)):
        if countlist[i][j]>0:
            count+=countlist[i][j]
            lineidcountmap=(i,countlist[i][j])
            lineidcountarray.append(lineidcountmap)
    textcontent=(count,wordlist[j],lineidcountarray)
    listtext.append(textcontent)
listtext=sorted(listtext, reverse=True)
for text in listtext:
    print  text


#所有对应文档的tf与tf-idf
for i in range(len(weighttlist)):
    print "%s"%"---------------------------------------------------line",i,"---------------------------------------------------"
    for j in range(len(wordlist)):
            if  countlist[i][j]>0:
                print "%s" %  "keyword[",wordlist[j],"] tf[",countlist[i][j],"],tf-idf[", weighttlist[i][j],"]"


from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier()
model.fit(feature_datas, class_data_array)


testline='-Mapped java.lang.StringIndexOutOfBoundsException: String index out of range: 0  '

test_datas = []
featureValue = testline.lower().strip()
test_datas.append(featureValue)
#test_feature_datas = tf_transformer.transform(test_datas)
test_vect_datas=vectorizer.transform(test_datas)
test_feature_datas= tf_transformer.transform(test_vect_datas)
model.predict(test_feature_datas)

