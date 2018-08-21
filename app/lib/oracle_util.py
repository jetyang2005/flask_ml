# -*- coding: utf-8 -*-
import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
# os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import sys
import importlib
importlib.reload(sys)

import cx_Oracle
from sqlalchemy import Column, String, create_engine
import pandas as pd


# stock_dict = {}
#
##connStr_now = 'riskcontrol/000000@10.0.0.99:1521/FOTIC'
##db = cx_Oracle.connect(connStr_now)
# db = cx_Oracle.connect('ccbtrust4', '123456', '10.0.0.99/FOTIC')
# cursor = db.cursor()
##strsql = "select * from AC_APPLICATION"
# strsql=" select USERNAME,ACCOUNT_STATUS,PASSWORD_VERSIONS from dba_users"
#
# cursor.execute(strsql)
# """
# =========================one=========================
# """
## while (1):
##    row = cursor.fetchone()
##    if row == None:
##        break
##    key = int("%s"%row[5])
##    value = int("%s"%row[3])
##    stock_dict[key] = value
#
## =========================all=========================
#
# rows = cursor.fetchall()
# for row in rows:
#    print row
#    #print "%d, %s, %s, %s" % (row[0], row[1], row[2], row[3])


class cxOracle():
    """
    对cxoracle的简单封装
    tns的取值tnsnames.ora对应的配置项的值，如：
    tns = '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=10.16.18.23)(PORT=1521)))(CONNECT_DATA=(SERVICE_NAME=MYDB)))'
    """

    def __init__(self, user, pwd, tns):
        self.user = user
        self.pwd = pwd
        self.tns = tns

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        self.conn = cx_Oracle.connect(self.user, self.pwd, self.tns)
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def ExecQuery(self, sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        # 查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecQueryTodf(self, sql):
        """
        sql to dataframe
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        fields = cur.description
        column_list = []  # 定义字段名的列表
        for i in fields:
            # print i[0]
            column_list.append(i[0])

        records = []
        for record in resList:
            # for i in range(0,len(record)):
            # field0 = record[0]
            # field1 = record[1]
            # field2 = record[2]
            # field3 = record[3].decode('gbk').encode('utf-8')
            # field4 = record[4]

            # fields = (field0, field1, field2, field3, field4)
            # print fields
            # records.append(fields)
            fields = []
            for i in range(0, len(record)):
                # try:
                field_val = record[i]
                # except (UnicodeDecodeError, UnicodeEncodeError):
                #   field_val = record[i].decode('gbk').encode('utf-8')
                #   print field_val
                if isinstance(field_val, basestring):
                    field_val = field_val.decode('gbk').encode('utf-8')
                fields.append(field_val)
            #print fields
            records.append(tuple(fields))
        print ("数据总条数:", len(records))
        # Prepare the records into a single DataFrame
        df = None
        if records:
            df = pd.DataFrame(records, columns=column_list)

        # 查询完毕后必须关闭连接
        self.conn.close()
        return df


# def main():
#    db = cxOracle('ccbtrust4', '123456', '10.0.0.99/FOTIC')
#    # strsql = "select * from AC_APPLICATION"
#    strsql = " select USERNAME,ACCOUNT_STATUS,PASSWORD_VERSIONS from dba_users"
#    rows = db.ExecQuery(strsql)
#    for row in rows:
#        print row


# if __name__ == '__main__':
#    main()

"""
创建数据库连接的三种方式：
方法一：用户名、密码和监听分开写
import cx_Oracle
db = cx_Oracle.connect('username/password@host/orcl')
db.close()

方法二：用户名、密码和监听写在一起
import cx_Oracle
db = cx_Oracle.connect('username', 'password', 'host/orcl')
db.close()

方法三：配置监听并连接
import cx_Oracle
tns = cx_Oracle.makedsn('host', 1521, 'orcl')
db = cx_Oracle.connect('username', 'password', tns)
db.close()
"""
