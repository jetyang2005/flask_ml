#coding=utf-8
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name: pymssqlTest.py
# Purpose: 测试 pymssql库，该库到这里下载：http://www.lfd.uci.edu/~gohlke/pythonlibs/#pymssql
#
# Author: scott
#
# Created: 04/02/2012
#-------------------------------------------------------------------------------

import pymssql
#from  Python_Elasticsearch import ElasticsearchOperate
#from  Process_Stat import Process_Stat
import logging
import sys
import time
import pandas as pd

reload(sys)
sys.setdefaultencoding( "utf-8" )


class MSSQL:
    """
    对pymssql的简单封装
    pymssql库，该库到这里下载：http://www.lfd.uci.edu/~gohlke/pythonlibs/#pymssql
    使用该库时，需要在Sql Server Configuration Manager里面将TCP/IP协议开启

    用法：

    """

    def __init__(self, host, user, pwd, db):
        # 日志基本配置，将日志文件输出到当前目录下的elastticsearch_sample.log文件中
        logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='sqlserver_import_logger.log',
                filemode='w')

        self.sqlserver_import_logger = logging.getLogger('MSSQL')

        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def ExecQuery(self, sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段

        调用示例：
                ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
                resList = ms.ExecQuery("SELECT id,NickName FROM WeiBoUser")
                for (id,NickName) in resList:
                    print str(id),NickName
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        # 查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        """
        执行非查询语句

        调用示例：
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

#def main2():
#
# # ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
# # #返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
# # ms.ExecNonQuery("insert into WeiBoUser values('2','3')")
#
#    ms = MSSQL(host="10.0.0.29", user="sa", pwd="sysadmin", db="ZHONGZI")
#
# # 流程定义表
#    processdefineList = ms.ExecQuery(
#        "select processdefname, processchname, versionsign,createtime from link_processdefine")
#    processdefines = []
#    for (processdefname, processchname, versionsign, createtime) in processdefineList:
#        esdata = {"_index": "index_stat_processdefine",
#              "_type": "type_stat_processdefine",
#              "_source": {
#                  "processdefname": processdefname,
#                  "processchname": processchname,
#                  "versionsign": versionsign,
#                  "createtime": str(createtime),
#              }
#              }
#        processdefines.append(esdata)
#
#    # 流程实例表
#    process_processinstList = ms.ExecQuery("select processinstid, processinstname, processdefname, processchname, versionsign,currentstate, createtime, endtime, subtime from link_processinst")
#    process_processinsts = []
#    for (processinstid, processinstname, processdefname, processchname, versionsign, currentstate, createtime, endtime, subtime) in process_processinstList:
#        esdata = {"_index": "index_stat_process_processinst",
#                  "_type": "type_stat_process_processinst",
#                  "_source": {
#                    "processinstid": processinstid,
#                    "processinstname": processinstname,
#                    "processdefname": processdefname,
#                    "processchname": processchname,
#                      "versionsign": versionsign,
#                    "currentstate": currentstate,
#                    "createtime":  str(createtime),
#                    "endtime": str(endtime),
#                    "subtime": subtime
#                        }
#                }
#        process_processinsts.append(esdata)
#
#    #环节实例表
#    activityinstList = ms.ExecQuery("select processinstid, processinstname, processdefname, processchname, versionsign,activityinstid,activityinstname, currentstate, createtime, endtime, subtime from link_activityinst")
#    activityinsts = []
#    for (processinstid, processinstname, processdefname, processchname, versionsign,activityinstid,activityinstname, currentstate, createtime, endtime, subtime) in activityinstList:
#        esdata = {"_index": "index_stat_process_activityinst",
#                  "_type": "type_stat_process_activityinst",
#                  "_source": {
#                    "processinstid": processinstid,
#                    "processinstname": processinstname,
#                    "processdefname": processdefname,
#                    "processchname": processchname,
#                      "versionsign": versionsign,
#                    "activityinstid": activityinstid,
#                    "activityinstname": activityinstname,
#                      "currentstate": currentstate,
#                    "createtime":  str(createtime),
#                    "endtime": str(endtime),
#                    "subtime": subtime
#                    }
#                }
#        activityinsts.append(esdata)
#
#
#    #工作项表
#    workitemList = ms.ExecQuery("select processinstid, processinstname, processdefname, processchname,workitemid,workitemname,istimeout,timeoutnum,activityinstid,activityinstname, currentstate, createtime, endtime, userid,orgid,orgname from link_workitem")
#    workitems = []
#    for (processinstid, processinstname, processdefname, processchname,workitemid,workitemname,istimeout,timeoutnum,activityinstid,activityinstname, currentstate, createtime, endtime, userid,orgid,orgname) in workitemList:
#        esdata = {"_index": "index_stat_process_workitem",
#                  "_type": "type_stat_process_workitem",
#                  "_source": {
#                    "processinstid": processinstid,
#                    "processinstname": processinstname,
#                    "processdefname": processdefname,
#                    "processchname": processchname,
#                    "workitmeid": workitemid,
#                    "workitemname": workitemname,
#                    "istimeout": istimeout,
#                    "timeoutnum": timeoutnum,
#                    "currentstate": currentstate,
#                    "activityinstid": activityinstid,
#                    "activityinstname": activityinstname,
#                    "createtime":  str(createtime),
#                    "endtime": str(endtime),
#                      "userid": userid,
#                      "orgid": orgid,
#                      "orgname": orgname
#                        }
#                }
#        workitems.append(esdata)
#
#
#
#    process_stat = Process_Stat()
#    process_stat.create_index()
#
#    process_stat.create_data(processdefines)
#    process_stat.create_data(process_processinsts)
#    process_stat.create_data(activityinsts)
#    process_stat.create_data(workitems)
#
#
#    process_stat.query_count("index_stat_process_activityinst", "type_stat_process_activityinst")
#    process_stat.query_count("index_stat_process_processinst", "type_stat_process_processinst")
#    process_stat.query_count("index_stat_processdefine", "type_stat_processdefine")
#    process_stat.query_count("index_stat_process_workitem", "type_stat_process_workitem")




#if __name__ == '__main__':
#    main()