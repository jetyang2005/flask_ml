# -*- coding: UTF-8 -*-
import json
import collections
#s = 'mississippi'
#d = collections.defaultdict(int)
#for k in s:
#  d[k] += 1
#print(d)

s = [('red', 1), ('blue', 2), ('red', 3), ('blue', 4), ('red', 1), ('blue', 4)]
d = collections.defaultdict(set)
for k, v in s:
    d[k].add(v)

print(d)

def parse_js(expr):
    """
    解析非标准JSON的Javascript字符串，等同于json.loads(JSON str)
    :param expr:非标准JSON的Javascript字符串
    :return:Python字典
    """
    obj = eval(expr, type('Dummy', (dict,), dict(__getitem__=lambda s, n: n))())
    return obj


# line=""
# parse_js()


parmStr = """
    {
	"datasourceId": "11",
	"datasetId": "11",
    "beginTime": "2011-03-30T10:44:00.000+08:00",
    "time_stampFlag": false,
	"endTime": "2011-03-31T10:44:00.000+08:00",
	"queryType": "overview"
    }
    """
#  	"beginTime": "2011-03-30T10:44:00.000+08:00",
print parmStr

paramDict = json.loads(parmStr)
datasourceId = paramDict['datasourceId']
datasetId = paramDict['datasetId']
time_stampFlag = paramDict['time_stampFlag']
beginTime = paramDict['beginTime']
endTime = paramDict['endTime']
queryType = paramDict['queryType']
if time_stampFlag is False:
    print (datasourceId, datasetId, beginTime, time_stampFlag, endTime, queryType)
