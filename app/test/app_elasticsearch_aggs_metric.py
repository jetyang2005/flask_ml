#!/usr/bin/env python
# -*- coding:utf-8 -*-
from  app.lib.elasticsearch_util import Elasticsearch_Util
import json

es_util = Elasticsearch_Util()

es_index_name = "1007-linux-system-cpu*"
es_type_name = "linux-system-cpu"


# Metric统计，计算平均数
query_avg_data = {
                      "size":0,
                      "query": {
                        "match_all": {}
                      },

                      "aggs": {
                        "avg_field_name": {
                          "avg": {
                            "field": "metricset.rtt"
                          }
                        }
                      }
                }

#result = json.dumps(es_util.query(es_index_name, es_type_name, query_avg_data), indent=4)

# Metric统计，计算最小值
query_max_and_min_data = {
                      "size": 0,
                      "query": {

                           "match_all": {}

                      },
                      "aggs": {

                        "min_value": {
                          "min": {
                            "field": "metricset.rtt"
                          }
                        }
                          ,
                        "max_value": {
                            "max": {
                                "field": "metricset.rtt"
                            }
                        }
                     }
                }

#result = json.dumps(es_util.query(es_index_name, es_type_name, query_max_and_min_data), indent=4)


# Metric统计，stats
query_stats_data = {  "size": 0,
                      "aggs": {
                        "stats_value": {
                          "stats": {
                            "field": "metricset.rtt"
                          }
                        }
                     }
                }

#result = json.dumps(es_util.query(es_index_name, es_type_name, query_stats_data), indent=4)


# Metric统计，top hits
query_top_hits_data = {      "size": 0,
                              "aggs": {
                                "top_value": {
                                  "top_hits": {
                                      "sort":[
                                          {
                                                "metricset.rtt":{
                                                    "order": "desc"
                                                }
                                            }
                                        ],
                                      #指定返回字段名称
                                      "_source": {
                                              "include": [
                                              "metricset.rtt"
                                            ]
                                        },
                                        #取前两条
                                        "size": 2
                                  }
                                }
                             }
                        }

result = json.dumps(es_util.query(es_index_name, es_type_name, query_top_hits_data), indent=4)



print result
