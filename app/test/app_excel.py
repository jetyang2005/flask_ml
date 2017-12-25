#! /usr/bin/env python
# -*- coding: utf-8 -*-

#from __future__ import unicode_literals

import datetime
import json


from app.lib.mysql_connectionpool_util import Mysql
import re


'''
#################################################################
# 查询widget表                                       #
#################################################################
'''
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


mysql = Mysql()
now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")

# query_widgets_sql = "select * from linkdata_widget"
# widgets = mysql.getAll(query_widgets_sql)  # 数据库查询的接收者
# for widget in widgets:
#     jsonObj =  json.loads(widget['data_json'])
#     widget_id =  widget['widget_id']
#     if widget_id != 113 :
#         print widget['widget_id'], jsonObj['datasetId']
#
#         update_widget_sql =  "update linkdata_widget set dataset_id = %s , category_id = %s " \
#                              "where widget_id = %s "
#         update_widget_data = [jsonObj['datasetId'], 1, widget_id]
#         mysql.update(update_widget_sql, update_widget_data )

# update_board_sql =  "update linkdata_board set board_type = %s where board_id >= 113"
# update_board_data = ['screenBoard']
# mysql.update(update_board_sql, update_board_data )

# query_dataset_sql = 'select * from linkdata_dataset'
# datasets = mysql.getAll(query_dataset_sql)  # 数据库查询的接收者
# for dataset in datasets:
#     regex = re.compile(r'\\(?![/u"])')
#     fixed = regex.sub(r"\\\\", dataset['data_json'])
#     jsonObj = json.loads(fixed,strict=False)
# #    print dataset['dataset_id'],jsonObj['datasource']
#
#     update_dataset_sql =  "update linkdata_dataset set datasource_id = %s "  \
#                          "where dataset_id = %s  "
#
#     update_dataset_data = [jsonObj['datasource'], dataset['dataset_id']]
#
#     mysql.update(update_dataset_sql, update_dataset_data )

mysql.dispose()





