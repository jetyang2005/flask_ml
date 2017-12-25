#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import json




class CSVUitl(object):

    def __init__(self):
        pass


    def dictReadCSVFile(self, file_path, kafka_util):
        with open(file_path) as f:
            reader = csv.DictReader(f)
            for row in reader:

                #jsonObj = json.loads(row)                # 循环遍历字典中的值
                # for key,value in row.items():
                #     print "key is :"+key , "value is :"+value

                #删除字典中value为空的元素
                for k, v in row.items():
                    if not k: row.pop(k)

                row['@timestamp']=row['FlightDate']+' '+row['CRSDepTime'][0:2]+':'+row['CRSDepTime'][2:4]+':00'+' 000'
                print row['@timestamp']
                #获取字典中的元素数量
                # print len(row)linkdata__1007__node__airlinedata
                # print json.dumps(row)
                message_json = json.dumps(row)
                print message_json
                kafka_util.produce_kafka_data('linkdata__1007__node__airlinedata',message_json)

        # kafka_util.colse_producer()


    def readCSVFile(self, file_path):
        with open(file_path) as f:
            reader = csv.reader(f)
            for row in reader:
                # Max TemperatureF是表第一行的某个数据，作为key
                print(row)

# csv_util = CSVUitl()
# csv_util.dictReadCSVFile('/Users/yangwm/log/exceldata/On_Time_On_Time_Performance_1987_10/On_Time_On_Time_Performance_1987_10.csv')
