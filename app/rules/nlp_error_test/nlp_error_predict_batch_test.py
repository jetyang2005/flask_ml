# -*- coding: UTF-8 -*-
from app.lib.elasticsearch_util import Elasticsearch_Util


def es_read_scroll_scan(self, index, doc_type, querybody, size):
    # Initialize the scroll
    page = self.es.search(
        index=index,
        doc_type=doc_type,
        scroll='2m',
        size=size,
        body=querybody)
    sid = page['_scroll_id']
    scroll_size = page['hits']['total']

    # Start scrolling
    while (scroll_size > 0):
        print "Scrolling..."
        page = self.es.scroll(scroll_id=sid, scroll='2m')
        # Update the scroll ID
        sid = page['_scroll_id']
        # Get the number of results that we returned in the last scroll
        scroll_size = len(page['hits']['hits'])
        print "scroll size: " + str(scroll_size)
        # Do something with the obtained page
        batchdata = page['hits']['hits']
        esdata_parse(batchdata, 'ActualElapsedTime')


def readDataLine(lineStr):
    if len(lineStr) == 0:
        return
    else:
        feature_data_array = []
        featureValue = lineStr.lower().strip()
        feature_data_array.append(featureValue)
        return feature_data_array


def esdata_parse(batchdata, logbody):
    # errors = []
    for item in batchdata:
        # print item
        id = item['_id']
        logBody = item['_source'][logbody]
        test_datas = readDataLine(logBody)
        # test_feature_datas = tf_transformer.transform(test_datas)
        # pred = model.predict(test_feature_datas)
        # guess = le.inverse_transform(pred)
        # if (guess[0] == "1")):
        # errors.append((id, guess[0]))
        print '%s:%s' % (id, logBody)




es_util = Elasticsearch_Util()
index = "1007-airlinedata-20171124"
doc_type = "airlinedata"
querybody = {
    "query": {
        "match_all": {}
    },
    "_source": {
        "includes": [],
        "excludes": []
    }
}
size = 500
es_read_scroll_scan(es_util, index=index, doc_type=doc_type, querybody=querybody, size=size)
