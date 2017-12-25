#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from zipfile_util import ZFile
from csv_util import CSVUitl
from kafka_util import KafkaUtil

Const_Image_Format = [".csv"]

class DIRUitl(object):

    fileList = [""]
    counter = 0

    def __init__(self):
        self.kafka_util = KafkaUtil()

    def FindFile(self, dirr, filtrate=1):
        global Const_Image_Format
        for s in os.listdir(dirr):
            newDir = os.path.join(dirr, s)
            if os.path.isfile(newDir):
                if filtrate:
                    if newDir and (os.path.splitext(newDir)[1] in Const_Image_Format):
                        self.fileList.append(newDir)
                        self.counter += 1
                else:
                    self.fileList.append(newDir)
                    self.counter += 1


if __name__ == "__main__":

    b = DIRUitl()
    # b.FindFile(dirr="/home/linkdata/airline_data/csvs")
    b.FindFile(dirr="/Users/yangwm/log/exceldata/csvs")

    print(b.counter)
    for k in b.fileList:
        if (k != ''):
            print k
            csv_util = CSVUitl()
            csv_util.dictReadCSVFile(k, b.kafka_util)

        # if(k!=''):
        #     print k
        #     zipfile = ZFile(k)
        #     zipfile.extract_to('/home/linkdata/airline_data/csvs')
