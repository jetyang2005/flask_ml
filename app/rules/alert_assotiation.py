#-*- coding: UTF-8 -*-
from flask import jsonify, request
from app.auth.auths import Auth
import app.lib.apriori as apriori
import json



def init_api(app, es_util):

    @app.route('/ml_alert_association', methods=['POST'])
    def queryAlertAssociation():
        parmStr = request.get_data()
        paramDict = json.loads(parmStr)
        timeRange = paramDict['timerange']
        #timeRange = "[2017-12-07T00:00:00.000+08:00 TO 2017-12-13T00:00:00.000+08:00]"
        # beginTime = str(timeRange[1:30])
        # endTime = str(timeRange[-30:-1])
        beginTime = str(timeRange[1:20])
        endTime = str(timeRange[-30:-11])
        """
        获取用户信息
        :return: json
        """
        auth = Auth()
        result = auth.identify(request)

        if (result['status']):

            items, rules = apriori.runApriori(getAlertDataFromES(es_util,beginTime,endTime), paramDict["minSupport"], paramDict["minConfidence"])
            result = apriori.printResults(items, rules)

            print result
            return result

        else:
          return jsonify(result)


def getAlertDataFromES(es_util,beginTime,endTime):
    es_index_name = "1-elast-alert-*"
    es_type_name = "elast-alert"
    # 最大查询10000条数据
    query_data = {  "from" :0,
                    "size" :10000,
                    "sort" : [{ "@timestamp" : {"order" : "asc"}}],
                    "query" : {
                        "bool" : {
                            "must" : [{
                                "range" : {
                                    "@timestamp" : {
                                        "from" : beginTime,
                                        "to" : endTime
                                    }
                                }
                            }
                        ]
                      }
                   }
                 }

    print es_util.query_count(es_index_name, es_type_name)

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
