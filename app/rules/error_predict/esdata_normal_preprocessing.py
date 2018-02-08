
# coding: utf-8

# In[1]:



import sys
import os       
import pandas as pd
import datetime
os.chdir('D:/zxdf/Workspaces/PycharmProjects/flask_ml')
from app import config, Elasticsearch_Util

starttime = datetime.datetime.now()
print ("当前的日期和时间是 %s" % starttime)


# In[2]:


#def getDataFromES2(es_util, index, es_type, beginTime, endTime, fromnum, size, source_include):
#    # 最大查询10000条数据
#    query_data = {
#        "from": fromnum,
#        "size": size,
#        "query": {
#            "bool": {
#                "must": [
#                    {
#                        "range": {
#                            "@timestamp": {
#                                "from": beginTime,
#                                "to": endTime
#                            }
#                        }
#                    }
#                ],
#            }
#        },
#        "_source": {
#            "includes": source_include,
#            "excludes": []
#        },
#        "sort": [
#            {
#                "@timestamp": {
#                    "order": "desc"
#                }
#            }
#        ]
#    }
#    res = es_util.query(index, es_type, query_data)
#    df = None
#    records = []
#    for doc in res['hits']['hits']:
#        source=doc['_source']
#        source["id"]=doc['_id']
#        records.append(source)
#    if records:
#        df = pd.DataFrame(records)
#    return df


# In[3]:


#def getDataFromES(es_util, index, es_type, beginTime, endTime, fromnum, size, source_include):
#    # 最大查询10000条数据
#    query_data = {
#        "from": fromnum,
#        "size": size,
#        "query": {
#            "bool": {
#                "must": [
#                    {
#                        #"match":{
#                        #    "isException":"0"
#                        #}
#                        "range": {
#                            "@timestamp": {
#                                "from": beginTime,
#                                "to": endTime
#                            }
#                        }
#                    }
#                ],
#            }
#        },
#        "_source": {
#            "includes": source_include,
#            "excludes": []
#        },
#        "sort": [
#            {
#                "@timestamp": {
#                    "order": "desc"
#                }
#            }
#        ]
#    }
#
#    res = es_util.query(index, es_type, query_data)
#    df = None
#    records = []
#    for doc in res['hits']['hits']:
#        source=doc['_source']
#        source["id"]=doc['_id']
#        source["index"]=doc['_index']
#        records.append(source)
#    if records:
#        df = pd.DataFrame(records)
#    return df


# In[4]:


def getMoreDataFromES(self, index, doc_type,beginTime, endTime, source_include,size):
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
    print "Initialize the scroll"
    page = self.es.search(
        index=index,
        doc_type=doc_type,
        scroll='2m',
        size=size,
        body=querybody)
    sid = page['_scroll_id']
    scroll_size = page['hits']['total']

    print "sid: " + str(sid)
    print "scroll size: " + str(scroll_size)

    records = []
    for doc in page['hits']['hits']:
            source=doc['_source']
            source["id"]=doc['_id']
            source["index"]=doc['_index']
#            if doc['_source']['logBody']!=None and doc['_source']['logBody']!="":
            records.append(source)

    df = None
   #Start scrolling
    while (scroll_size > 0):
        print "Scrolling..."
        page = self.es.scroll(scroll_id=sid, scroll='2m')
        # Update the scroll ID
        sid = page['_scroll_id']
        print "sid: " + str(sid)
        # Get the number of results that we returned in the last scroll
        scroll_size = len(page['hits']['hits'])

        for doc in page['hits']['hits']:
            source=doc['_source']
            source["id"]=doc['_id']
            source["index"]=doc['_index']
#            if doc['_source']['logBody']!=None and doc['_source']['logBody']!="":
            records.append(source)

        print "scroll size: " + str(scroll_size)

    if records:
        df = pd.DataFrame(records)
        # Do something with the obtained page
    return df


# In[5]:


index = "1012-knowledge_training_normal-*"
es_type = "knowledge_training_normal"
beginTime = "2018-02-05T00:00:00.000+08:00"
endTime = "2018-02-06T00:00:00.000+08:00"
size = 10000
#1085  804:281
tag = "isException"
logmsg = "logBody"
source_include = [tag, logmsg]

es_util = Elasticsearch_Util()
train_data = getMoreDataFromES(es_util, index=index, doc_type=es_type,
                           beginTime=beginTime, endTime=endTime,
                           size=size,
                           source_include=source_include)


# In[6]:


#index = "1012-knowledge_training-*"
#es_type = "knowledge_training"
#index = "1012-knowledge_training_normal-*"
#es_type = "knowledge_training_normal"
#beginTime = "2018-01-30T00:00:00.000+08:00"
#endTime = "2018-02-07T00:00:00.000+08:00"
#fromnum = 0
#size = 10000
##1085  804:281
#tag = "isException"
#logmsg = "logBody"
#source_include = [tag, logmsg]
#
#es_util = Elasticsearch_Util()
#train_data = getDataFromES(es_util, index=index, es_type=es_type,
#                           beginTime=beginTime, endTime=endTime,
#                           fromnum=fromnum, size=size,
#                           source_include=source_include)


# In[7]:


len(train_data)


# In[8]:


feature_data_array = train_data[logmsg]
class_data_array = train_data[tag]
print len(feature_data_array)
print len(class_data_array)


# In[9]:


#import codecs
#训练数据日志体
#f = codecs.open(r"E:\zxdf\ml\linkdata-log\dataset\testrecord\logbody.txt", "w", encoding='unicode')
f = open(r"E:\zxdf\ml\linkdata-log\dataset\testrecord\logbody.txt", "w")
for indexs in train_data.index:
    print >> f, "%s%s%s%s" %(train_data.loc[indexs].values[0:1],train_data.loc[indexs].values[1:2],train_data.loc[indexs].values[2:3],train_data.loc[indexs].values[3:4])
    #f.write(content)
f.close()


# In[10]:


import nltk
import string
from nltk.corpus import stopwords

#训练数据关键词提取列表
def tokenize(text):
    f = open(r"E:\zxdf\ml\linkdata-log\dataset\testrecord\keyword_logbody.txt", "a+")
    #stopword_tokens3 =[]
    
    #if text !=None:
    tokens = nltk.word_tokenize(text)
    tokens2=[]
    for w in tokens:
        if w[0]=='-':
            tokens2.append(w[1:])
        elif w[0]=="'":
            tokens2.append(w[1:])    
        else:
            tokens2.append(w)
    
    stopword_tokens = [i for i in tokens2 if i not in string.punctuation]
    stopword_tokens2 = [w for w in stopword_tokens if w not in stopwords.words('english')]
    
    stopwords_custom=["''", "``","||","'/","'/'",u"'0x0","'2","'=","'s",'**','***','***.***','**constraint.unique_wt**','**failed','**method','--',
                      '-1','-297991290629036654','-614','-6182496564283649260','-6787310117729693199','-8','-999999999',u'-e',
                      '..','...','.\\xxx\\xxx.txt','/*','/**','/c','/p','0','1','==','b','c','e','x','===',
                      'v'
                     ]
    stopword_tokens3 = [w for w in stopword_tokens2 if w not in stopwords_custom]    
            
    print >> f, "%s" %(stopword_tokens3)
    f.close()
    return stopword_tokens3 


# In[11]:


from sklearn.feature_extraction.text import CountVectorizer
vectorizer=CountVectorizer(tokenizer=tokenize, stop_words='english', decode_error='ignore')
csr_mat = vectorizer.fit_transform(feature_data_array)
# 获取词袋模型中的所有词
wordlist = vectorizer.get_feature_names()  
# tf矩阵 元素a[i][j]表示j词在i类文本中的tf
countlist = csr_mat.toarray()


# In[12]:


len(wordlist)


# In[13]:


#获得词频统计列表（包含该词的文档数，词，所有出现改词的文档列表[(文档index,文档id)]）
def wordcount(wordlist,countlist,train_data):
    wclist=[]
    for j in range(len(wordlist)):    
        esidarray=[]
        for i in range(len(countlist)):
            if countlist[i][j]>0:
                esidarray.append((train_data["index"][i],train_data["id"][i]))
        #（包含该词的文档数，词，所有出现改词的文档列表[文档id]）        
        textcontent=(len(esidarray),wordlist[j],esidarray)       
        wclist.append(textcontent)
    return  wclist   


# In[14]:


wclist=wordcount(wordlist,countlist,train_data)


# In[15]:


#获得倒序的词频统计列表
f = open(r"E:\zxdf\ml\linkdata-log\dataset\testrecord\tf_tfidfs.txt", "w")
for text in sorted(wclist, reverse=True):
    print >> f, text
f.close()  


# In[16]:


#获取要删除的高频词所对应的文档id列表
def delword(wclist,delwordnum):
    dellist=[]
    for i in range(len(wclist)):
         if wclist[i][0] >= delwordnum:
                dellist.append(wclist[i])
    return dellist


# In[17]:


#获得超过指定词频的列表（包含该词的文档数，词，所有出现改词的文档列表[文档id]）   
delwordnum=20
#2
#5
#10
#20
#50
#17954
#10028
#17635
#17954
#9024
dellist=delword(wclist,delwordnum)


# In[18]:


#dellist[0][2][0]
len(dellist)


# In[19]:


#def getDataFromESbyid(esid):
#    # 最大查询10000条数据
#    query_data ={
#        "query":{
#            "bool":{
#                "must":[
#                    {
#                        "match":{
#                            "_id":esid
#                        }
#                    }
#                ]
#            }
#        }
#    }
#    return query_data


# In[20]:


from elasticsearch import Elasticsearch
es = Elasticsearch([config.ES_HOST],
                   http_auth=('admin', 'admin'),
                   port=config.ES_PORT)
#esid="AWEwSCqvLBpMZiso47WP"
#res = es_util.query(index, es_type, getDataFromESbyid(esid)) 
#index = res["hits"]["hits"][0]["_index"]

#index = "1012-knowledge_training-20180130"
#es_type = "knowledge_training"

#index = "1012-knowledge_training_normal-20180131"
#es_type = "knowledge_training_normal"

#res=es.exists(index=index, doc_type=es_type, id=esid)
#resget = es.get_source(index=index, doc_type=es_type, id=esid)
#res2 = es.delete(index, doc_type=es_type, id=esid)


# In[21]:


#import sys  
#reload(sys)  
sys.setdefaultencoding('utf8')

everdellist=[]
#获删除高频词所对应的文档id列表
def delid(index,es_type,dellist,delidnum):
    for i in range(len(dellist)):
        delesids= dellist[i][2]
        #print '%s' % '=====================',dellist[i][1],'========================='
        for j in range(len(delesids)):
            if j>= delidnum:
                if not delesids[j] in everdellist: 
                    #print delesids[j][0],delesids[j][1]
                    result =es.delete(delesids[j][0], doc_type=es_type, id=delesids[j][1])
                    if result["result"]=="deleted":
                        everdellist.append(delesids[j])
                        print "%s" % 'success delid:',delesids[j],';result:',result
                    else:
                        print "%s" % 'faile delid:',delesids[j],';result:',result
                
                
                
#{u'_type': u'knowledge_training_normal', u'_index': u'1012-knowledge_training_normal-20180131', u'_shards': {u'successful': 1, u'failed': 0, u'total': 2}, u'_version
#': 2, u'result': u'deleted', u'found': True, u'_id': u'AWFKeRaILBpMZisoN8iF'}                


# In[22]:


#everdellist


# In[23]:


#test={u'_type': u'knowledge_training_normal', u'_index': u'1012-knowledge_training_normal-20180131', u'_shards': {u'successful': 1, u'failed': 0, u'total': 2}, u'_version': 2, u'result': u'deleteds', u'found': True, u'_id': u'AWFKeRaILBpMZisoN8iF'}


# In[24]:


delidnum=20
delid(index,es_type,dellist,delidnum)


# In[ ]:




