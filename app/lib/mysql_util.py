# -*- coding: UTF-8 -*-
# 安装 MYSQL DB for python
import pymysql as mdb
import pandas as pd
import sys
import app.config as config
import importlib
importlib.reload(sys)



class Mysql_Util():
    #def __int__(self):
    #    self.host = config.DB_HOST
    #    self.port = config.DB_PORT
    #    self.user = config.DB_USER
    #    self.passwd = config.DB_PASSWORD
    #    self.db = config.DB_DB

    def select(self, sqlstr, columns):
        con = None
        try:
            # 连接 mysql 的方法： connect('ip','user','password','dbname')
            con = mdb.connect(host=config.DB_HOST, user=config.DB_USER, passwd=config.DB_PASSWORD, db=config.DB_DB, charset='utf8')
            # 所有的查询，都在连接 con 的一个模块 cursor 上面运行的
            cur = con.cursor()
            # 执行一个查询
            # cur.execute("SELECT VERSION()")
            # 取得上个查询的结果，是单个结果
            # data = cur.fetchone()
            # print "Database version : %s " % data
            # cur.execute("CREATE TABLE IF NOT EXISTS \
            # Writers(Id INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(25))")
            # 以下插入了 5 条数据
            # cur.execute("INSERT INTO Writers(Name) VALUES('Jack London')")
            # cur.execute("INSERT INTO Writers(Name) VALUES('Honore de Balzac')")
            # cur.execute("INSERT INTO Writers(Name) VALUES('Lion Feuchtwanger')")
            # cur.execute("INSERT INTO Writers(Name) VALUES('Emile Zola')")
            # cur.execute("INSERT INTO Writers(Name) VALUES('Truman Capote')")
            # 类似于其他语言的 query 函数， execute 是 python 中的执行查询函数
            cur.execute(sqlstr)
            # 使用 fetchall 函数，将结果集（多维元组）存入 rows 里面
            rows = cur.fetchall()
            # 依次遍历结果集，发现每个元素，就是表中的一条记录，用一个元组来显示
            records = []
            for record in rows:
                records.append(record)
            #print "数据总条数:",len(records)
            # Prepare the records into a single DataFrame
            df = None
            if records:
                df = pd.DataFrame(records, columns=columns)
                # .fillna(value=np.nan)
                # df = df.reindex(sorted(df.columns), axis=1)
                # print df
            return df
        except Exception as e:
            print(e)
            con.rollback()
        finally:
            if con:
                # 无论如何，连接记得关闭
                cur.close()
                con.commit()
                con.close()