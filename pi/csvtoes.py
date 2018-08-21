
import pandas as pd

#file_name=""
#names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']
#data = pd.read_csv(file_name, names=names)
#print(data.shape)



from  app.lib.elasticsearch_util import Elasticsearch_Util
import xlrd

es_util = Elasticsearch_Util()
type = "data_w_p"
index = type+"-20180820"

mapping = {
    "mappings": {
            type: {
                "properties": {
                    "class": {
                        "type": "keyword"
                    },
                    "wind_speed": {
                        "type": "keyword"
                    },
                    "power": {
                        "type": "keyword"
                    }
                }
            }
        }
}



def insert_data_from_xls():
    #column_names = ['class', 'wind_speed', 'power']
    #data = pd.read_excel('E:\zxdf\电科院\北科大\王玉峰\模型案例\设备级\data_w_p.xlsx', names=column_names)  # 读文件
    #print(data)

    data = xlrd.open_workbook('E:\zxdf\电科院\北科大\王玉峰\模型案例\设备级\data_w_p.xlsx')  # 打开xls文件
    table = data.sheets()[0]  # 打开第一张表
    esdatas = []
    nrows = table.nrows  # 获取表的行数
    for i in range(nrows):  # 循环逐行打印
        rows = table.row_values(i)
        esdata = {
            "_index": index,
            "_type": type,
            "_id": i,
            "_source": {
                "class": str(rows[0]),
                "wind_speed": str(rows[1]),
                "power": str(rows[2])
            }
        }
        esdatas.append(esdata)
    es_util.insert_bulk_data(esdatas)
    # print str(esdatas)

def getDataFromES():
    # 最大查询10000条数据
    query_data = {  "from" :0,
                    "size" :10000,
                    #"sort" : [{ "@timestamp" : {"order" : "asc"}}],
                    "query": {
                        "match_all": {}
                    }
                 }

    #print (es_util.query_count(index,type))

    #res = es_util.query(index, type, query_data)
    res =es_util.es_read_querybody(index, type, query_data)


def getMoreDataFromES(self, index, doc_type, source_include, size):
    querybody = {
        "query": {
            "match_all": {}
        },
        "_source": {
            "includes": source_include,
            "excludes": []
        }
    }
    # Initialize the scroll
    print ("Initialize the scroll")

    page = self.es.search(
        index=index,
        doc_type=doc_type,
        scroll='2m',
        size=size,
        body=querybody)
    sid = page['_scroll_id']
    scroll_size = page['hits']['total']

    print("sid: " + str(sid))
    print("scroll size: " + str(scroll_size))
    records = []
    for doc in page['hits']['hits']:
        source = doc['_source']
        #source["id"] = doc['_id']
        #source["index"] = doc['_index']
        #            if doc['_source']['logBody']!=None and doc['_source']['logBody']!="":
        records.append(source)

    df = None
    # Start scrolling
    while (scroll_size > 0):
        print ("Scrolling...")
        page = self.es.scroll(scroll_id=sid, scroll='2m')
        # Update the scroll ID
        sid = page['_scroll_id']
        print ("sid: " + str(sid))
        # Get the number of results that we returned in the last scroll
        scroll_size = len(page['hits']['hits'])

        for doc in page['hits']['hits']:
            source = doc['_source']
            source["id"] = doc['_id']
            source["index"] = doc['_index']
            #            if doc['_source']['logBody']!=None and doc['_source']['logBody']!="":
            records.append(source)

        print ("scroll size: " + str(scroll_size))
    if records:
        df = pd.DataFrame(records)
        # Do something with the obtained page
    return df

# es_util.delete_index(es_index_name)
#
es_util.create_index(index, mapping)
insert_data_from_xls()


#getDataFromES()

#beginTime = "2018-02-05T00:00:00.000+08:00"
#endTime = "2018-02-06T00:00:00.000+08:00"
#size = 10000
#source_include = ["class", "wind_speed","power"]

#print (getMoreDataFromES( es_util,index, type, source_include, size))