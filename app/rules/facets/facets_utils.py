# -*- coding: UTF-8 -*-
import MySQLdb as mdb
import pandas as pd
from app.lib.mysql_util import Mysql_Util
from app.lib.elasticsearch_util import Elasticsearch_Util

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
     数据库类型的查询，需要将其中的一个时间字段做进一步处理 unix_timestamp(stat_period) as timestamps,
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

    jdbclist = jdbcurl.split("//")[1].split("/")
    host = jdbclist[0].split(":")[0]
    db = jdbclist[1]

    data_json = None
    for indexs in dataset_df.index:
        data_json = dataset_df.loc[indexs, "data_json"]
    paramDict_dataset = parse_js(data_json)
    sqlhead = "select * from ("

    print paramDict_dataset["query"]

    sql = paramDict_dataset["query"]["sql"]

    if sql.endswith(";"):
        sql = sql[0:-1]
    sqlend = ') as a where a.timestamps >= unix_timestamp(\"'+beginTime+'\") and a.timestamps <= unix_timestamp(\"'+endTime+'\") limit 10000;'
    sqlstr = '%s%s%s' % (sqlhead, sql, sqlend)

    print sqlstr

    df = select_nocolumns(host=host, user=username, passwd=password, db=db, sqlstr=sqlstr)
    return df


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
        "size": 10000
    }
    df = es_util.es_read_querybody(indexName, typeName, query_data)
    return df


def select_nocolumns(host, user, passwd, db, sqlstr):
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
