#!/usr/bin/env python
# -*- coding:utf-8 -*-
from  app.lib.elasticsearch_util import Elasticsearch_Util
import json

es_util = Elasticsearch_Util()

es_index_name = "1007-airlinedata*"
es_type_name = "airlinedata"

# bucket统计，按照terms进行统计

query_terms_data = {
                              "aggs": {
                                "terms_FlightDate": {
                                  "terms": {
                                    "field": "FlightDate",
                                    "order": {
                                      "_count": "desc"
                                    },
                                    "size": 2
                                  }
                                }
                              }
                            }

#result = json.dumps(es_util.query(es_index_name, es_type_name, query_datehistogram_data), indent=4)

# bucket后统计
query_terms_cardinality_data = {
                                "size":0,
                                "query":{
                                    "bool":{
                                        "filter":[]
                                    }
                                },
                                "aggregations":{
                                    "FlightDate":{
                                        "terms":{
                                            "field":"FlightDate",
                                            "size":1000,
                                            "missing":"#NULL"
                                        },
                                        "aggregations":{
                                            "ce292785":{
                                                "cardinality":{
                                                    "field":"UniqueCarrier"
                                                }
                                            }
                                        }
                                    }
                                }
                            }

result = json.dumps(es_util.query(es_index_name, es_type_name, query_terms_cardinality_data), indent=4)


# Metric统计，按照时间进行直方图统计
query_datehistogram_data = {


                            "size": 0,
                            "query": {
                                "bool": {
                                    "filter": []
                                }
                            },
                            "aggregations": {
                                "@timestamp": {
                                    "date_histogram": {
                                        "field": "@timestamp",
                                        "format": "yyyy-MM-dd HH:mm:ss",
                                        "interval": "2563m",
                                        "time_zone": "Asia/Shanghai",
                                        "min_doc_count": 0,
                                        "extended_bounds": {}
                                    },
                                    "aggregations": {
                                        "9c8b054f": {
                                            "value_count": {
                                                "field": "metricset.rtt"
                                            }
                                        }
                                    }
                                }
                            }
                        }



#result = json.dumps(es_util.query(es_index_name, es_type_name, query_datehistogram_data), indent=4)


print result
