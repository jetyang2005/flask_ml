#!/usr/bin/env python
# -*- coding:utf-8 -*-
from  lib.elasticsearch_util import Elasticsearch_Util

es_util = Elasticsearch_Util()

es_index_name = "1007-linux-system-cpu*"
es_type_name = "linux-system-cpu"


# Metric统计，计算平均数
query_data = {
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

#es_util.query(es_index_name, es_type_name, query_data)

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


es_util.query(es_index_name, es_type_name, query_datehistogram_data)