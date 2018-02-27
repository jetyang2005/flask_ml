# -*- coding: UTF-8 -*-
import MySQLdb as mdb
import pandas as pd
from app.lib.mysql_util import Mysql_Util
from app.lib.elasticsearch_util import Elasticsearch_Util
from app.lib.ms_sqlserver_util import MSSQL
from app.lib.oracle_util import cxOracle

"""
为了使用数据集分析功能，数据集需要做如下处理：
如果数据源为mysql，则需要在查询字段中添加 unix_timestamp(datatime) as time_stamp，其中datatime为表中的时间字段；
如果数据源为oracle，则需要在查询字段中添加 TO_NUMBER(TO_DATE(datatime,'YYYY') - TO_DATE('1970-01-01 8:0:0','YYYY-MM-DD HH24:MI:SS'))*24*60*60*1000 as time_stamp，
其中datatime为表中的时间字段，‘YYYY’代表时间格式，可以根据datatime的格式进行自定义。
"""
def configanalysis(datasourceId, datasetId, beginTime, endTime):
    """
    从数据库中读取数据源于数据集中的配置信息
    :param datasourceId:
    :param datasetId:
    :param beginTime:
    :param endTime:
    :return:
    """
    mysqlselect = Mysql_Util()
    # 读取数据源中的配置信息
    datasource_sqlstr = "select source_type,config from linkdata_datasource where datasource_id=" + datasourceId
    datasource_columns = ["source_type", "config"]
    datasource_df = mysqlselect.select(sqlstr=datasource_sqlstr, columns=datasource_columns)

    # 读取数据集中的配置信息
    dataset_sqlstr = "select data_json from linkdata_dataset where dataset_id=" + datasetId
    dataset_columns = ["data_json"]
    dataset_df = mysqlselect.select(sqlstr=dataset_sqlstr, columns=dataset_columns)

    return datasetAnalysis(datasource_df, dataset_df, beginTime, endTime)


def datasetAnalysis(datasource_df, dataset_df, beginTime, endTime):
    """
    根据数据源的类型选择不同的解析方式
    :param datasource_df:
    :param dataset_df:
    :param beginTime:
    :param endTime:
    :return:
    """
    for indexs in datasource_df.index:
        source_type = datasource_df.loc[indexs, "source_type"]
        config = datasource_df.loc[indexs, "config"]
        if source_type.lower() == "jdbc":
            return jdbcconfiganalysis(config, dataset_df, beginTime, endTime)
        elif source_type.lower() == "linkesdata":
            return linkESDatacconfiganalysis(config, beginTime, endTime)
        else:
            return "datasetAnalysis is exception"


def parse_js(expr):
    """
    解析非标准JSON的Javascript字符串，等同于json.loads(JSON str)
    :param expr:非标准JSON的Javascript字符串
    :return:Python字典
    """
    obj = eval(expr, type('Dummy', (dict,), dict(__getitem__=lambda s, n: n))())
    return obj


def jdbcconfiganalysis(parmStr, dataset_df, beginTime, endTime):
    """
     解析jdbc类型的json
     数据库类型的查询，需要将其中的一个时间字段做进一步处理 unix_timestamp(stat_period) as time_stamp,
     :param parmStr:非标准JSON的字符串
     :param dataset_df:从数据库中查询出的数据集的配置
     :return:Python Dataframe
    """
    paramDict = parse_js(parmStr)
    # resultPart2 = json.dumps(parmStr2)
    # print resultPart2["type"]
    # parmStr.decode('utf-8').replace("'", "\"")
    # paramDict = json.loads(resultPart2)
    # print eval(paramDict)
    print "jdbc:", paramDict
    type = paramDict["type"]
    jdbcurl = paramDict["jdbcurl"]
    driver = paramDict["driver"]
    username = paramDict["username"]
    password = paramDict["password"]

    if type.lower() == "mysql":
        return mysqlconfiganalysis(jdbcurl, username, password, dataset_df, beginTime, endTime)
    elif type.lower() == "oracle":
        return oracleconfiganalysis(jdbcurl, username, password, dataset_df, beginTime, endTime)
    elif type.lower() == "sql server":
        return sqlserverconfiganalysis(jdbcurl, username, password, dataset_df, beginTime, endTime)
    else:
        return "database type is error"


def mysqlconfiganalysis(jdbcurl, username, password, dataset_df, beginTime, endTime):
    """
    查询mysql中的数据
    驱动类:com.mysql.jdbc.Driver
    JDBC连接URL:jdbc:mysql://127.0.0.1:3306/dbname
    """
    jdbclist = jdbcurl.split("//")[1].split("/")
    host = jdbclist[0].split(":")[0]
    db = jdbclist[1]
    sqlhead = "select * from ("
    sql = datasetconfigTosql(dataset_df)
    sqlend = ') as a where a.time_stamp >= unix_timestamp(\"' + beginTime + '\") and a.time_stamp <= unix_timestamp(\"' + endTime + '\") limit 10000;'
    sqlstr = '%s%s%s' % (sqlhead, sql, sqlend)
    print sqlstr
    df = mysql_select(host=host, user=username, passwd=password, db=db, sqlstr=sqlstr)
    return df


def sqlserverconfiganalysis(jdbcurl, username, password, dataset_df, beginTime, endTime):
    """
    查询sqlserver中的数据
    驱动类:com.microsoft.sqlserver.jdbc.SQLServerDriver
    JDBC连接URL:jdbc:sqlserver://127.0.0.1:1433;DatabaseName=dbname;SelectMethod=Cursor
    """
    jdbclist = jdbcurl.split("//")[1].split(";")
    host = jdbclist[0].split(":")[0]
    db = jdbclist[1].split("=")[1]
    sqlhead = "select * from ("
    sql = datasetconfigTosql(dataset_df)
    sqlend = ') as a where a.time_stamp >= DATEDIFF(ss,\'1970-01-01 00:00:00+08:00\',\"' + beginTime + '\") and a.time_stamp <= DATEDIFF(ss, \'1970-01-01 00:00:00+08:00\',\"' + endTime + '\") limit 10000;'
    sqlstr = '%s%s%s' % (sqlhead, sql, sqlend)
    print sqlstr
    df = sqlserver_select(host=host, user=username, pwd=password, db=db, sqlstr=sqlstr)
    return df


def oracleconfiganalysis(jdbcurl, username, password, dataset_df, beginTime, endTime):
    """
    查询oracle中的数据
    驱动类:oracle.jdbc.driver.OracleDriver
    JDBC连接URL:jdbc:oracle:thin:@127.0.0.1:1521:sid
    """
    jdbclist = jdbcurl.split("@")[1].split(":")
    host = jdbclist[0]
    service_name = jdbclist[2]
    tns = host + "/" + service_name

    """
      select CREATETIME from LINK_ACTIVITYINST 
      where to_char(CREATETIME,'YYYY-MM-DD HH24:MI:SS' )>='2014-10-13 18:27:53'  and   to_char(CREATETIME,'YYYY-MM-DD HH24:MI:SS' )<='2014-10-13 18:27:53';
    
    TO_NUMBER(TO_DATE('1970-01-01 08:00:01', 'YYYY-MM-DD HH24:MI:SS') -      
                TO_DATE('1970-01-01 8:0:0', 'YYYY-MM-DD HH24:MI:SS')) * 24 * 60 * 60 * 1000
    """
    # "beginTime": "2011-03-30T10:44:00.000+08:00",

    beginTime1 = beginTime[0:10] + " " + beginTime[11:19]
    beginTime2 = "TO_NUMBER(TO_DATE(\'" + beginTime1 + "\', 'YYYY-MM-DD HH24:MI:SS') -  TO_DATE('1970-01-01 8:0:0', 'YYYY-MM-DD HH24:MI:SS')) * 24 * 60 * 60 * 1000"

    endTime1 = endTime[0:10] + " " + endTime[11:19]
    endTime2 = "TO_NUMBER(TO_DATE(\'" + endTime1 + "\', 'YYYY-MM-DD HH24:MI:SS') -  TO_DATE('1970-01-01 8:0:0', 'YYYY-MM-DD HH24:MI:SS')) * 24 * 60 * 60 * 1000"
    sqlhead = "select * from ("
    sql = datasetconfigTosql(dataset_df)
    sqlend = ') a where a.time_stamp >= ' + beginTime2 + ' and a.time_stamp <= ' + endTime2 + ' and rownum<= 10000'

    sqlstr = '%s%s%s' % (sqlhead, sql, sqlend)
    print sqlstr

    # sql2 = "select ID,ORG_ID from T_MDL_HIS_PROPERTYTAX where tax_year>'2016' and rownum<= 10"
    df = oracle_select(user=username, passwd=password, tns=tns, sqlstr=sqlstr)
    return df


def datasetconfigTosql(dataset_df):
    """
    dataset从解析sql语句
    :param dataset_df:
    :return:
    """
    data_json = None
    for indexs in dataset_df.index:
        data_json = dataset_df.loc[indexs, "data_json"]
    paramDict_dataset = parse_js(data_json)
    print paramDict_dataset["query"]
    sql = paramDict_dataset["query"]["sql"]
    if sql.endswith(";"):
        sql = sql[0:-1]
    return sql


def linkESDatacconfiganalysis(parmStr, beginTime, endTime):
    es_util = Elasticsearch_Util()
    paramDict = parse_js(parmStr)
    print "linkESData:", paramDict
    syscode = paramDict["syscode"]
    filename = paramDict["filename"]

    indexName = syscode + "-" + filename + "-*"
    typeName = filename

    # 查询全部
    query_data = {
        "query": {
            "bool":
                {"must":
                    [
                        {"range":
                             {"@timestamp":
                                  {"from": beginTime,
                                   "to": endTime
                                   }
                              }
                         }
                    ]
                }
        },
        "_source": {
            "includes": [],
            "excludes": ["_sysNo_", "_nodeName_", "_ip_", "_port_", "_createDate_"]
        },
        "size": 10000
    }
    df = es_util.es_read_querybody(indexName, typeName, query_data)
    return df


def mysql_select(host, user, passwd, db, sqlstr):
    con = None
    try:
        # 连接 mysql 的方法： connect('ip','user','password','dbname')
        con = mdb.connect(host=host, user=user, passwd=passwd, db=db, charset='utf8')
        # 所有的查询，都在连接 con 的一个模块 cursor 上面运行的
        cur = con.cursor()
        cur.execute(sqlstr)
        rows = cur.fetchall()
        records = []
        for record in rows:
            # print record
            records.append(record)
        print "数据总条数:", len(records)
        # Prepare the records into a single DataFrame
        df = None
        if records:
            df = pd.DataFrame(records)
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


def sqlserver_select(host, user, passwd, db, sqlstr):
    # #返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
    # ms = MSSQL(host="127.0.0.1", user="sa", pwd="123456", db="ZHONGZI")
    ms = MSSQL(host=host, user=user, pwd=passwd, db=db)
    # sqlstr="select processchname, versionsign,createtime from link_processdefine"
    rows = ms.ExecQuery(sqlstr)
    records = []
    for record in rows:
        print record
        records.append(record)
    print "数据总条数:", len(records)
    # Prepare the records into a single DataFrame
    df = None
    if records:
        df = pd.DataFrame(records)
    return df


def oracle_select(user, passwd, tns, sqlstr):
    db = cxOracle(user=user, pwd=passwd, tns=tns)
    rows = db.ExecQuery(sqlstr)
    records = []
    for record in rows:
        print record
        records.append(record)
    print "数据总条数:", len(records)
    # Prepare the records into a single DataFrame
    df = None
    if records:
        df = pd.DataFrame(records)
    return df
