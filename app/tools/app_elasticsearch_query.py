#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 1 查询上下文中，查询操作不仅仅会进行查询，还会计算分值，用于确定相关度；在过滤器上下文中，查询操作仅判断是否满足查询条件
# 2 过滤器上下文中，查询的结果可以被缓存。

from  lib.elasticsearch_util import Elasticsearch_Util

es_util = Elasticsearch_Util()

es_index_name = "1007-linux-system-cpu*"
es_type_name = "linux-system-cpu"

# 查询全部
query_data = {"query": {
                    "match_all": {}
                }
             }

#es_util.query(es_index_name, es_type_name, query_data)

#Term 查询
query_term_data = {"query":{
                            "term":{
                                "beat.hostname" : "WIN-KGQBA6FBL1A"
                            }
                        }
                    }

#es_util.query(es_index_name, es_type_name, query_term_data)

#Terms 查询
query_terms_data = {
                    "query":{
                        "terms":{
                            "beat.hostname":[
                               "WIN-KGQBA6FBL1A"
                            ]
                        }
                    }
                }

#es_util.query(es_index_name, es_type_name, query_terms_data)

# match:匹配name包含python关键字的数据
query_match_data = {
                        "query":{
                            "match":{
                                "beat.hostname" : "WIN-KGQBA6FBL1A"
                            }
                        }
                    }
# 查询name包含python关键字的数据
#es_util.query(es_index_name, es_type_name, query_match_data)


# multi_match:在name和addr里匹配包含关键字的数据
query_multi_match_data = {
                            "query":{
                                "multi_match":{
                                    "query":"WIN-KGQBA6FBL1A",
                                    "fields":["beat.hostname"]
                                }
                            }
                        }
# 查询name和addr包含""关键字的数据
#es_util.query(es_index_name, es_type_name, query_multi_match_data)

# 查询某一索引及类型的ID符合条件的数据
query_ids_data = {
    "query":{
        "ids":{
            "type":es_type_name,
            "values":[
                "AV-uPtsDCzML6CkCgfem","AV-uPtsDCzML6CkCgfej"
            ]
        }
    }
}
# 搜索出id为1或2d的所有数据
#es_util.query(es_index_name, es_type_name, query_ids_data)

# 复合查询
query_bool_data = {
                    "query":{
                        "bool":{
                            "must":[
                                {
                                    "term":{
                                        "beat.hostname":"WIN-KGQBA6FBL1A"
                                    }
                                },
                                {
                                    "term":{
                                        "metricset.module":"system"
                                    }
                                }
                            ]
                        }
                    }
                }
# 获取name="python"并且age=18的所有数据
#es_util.query(es_index_name, es_type_name, query_bool_data)

# 切片式查询
query_slice_data = { "query": {
                            "match_all":{}
                        },
                        "from":2 ,   # 从第二条数据开始
                        "size":4    # 获取4条数据
                    }
# 从第2条数据开始，获取4条数据
#es_util.query(es_index_name, es_type_name, query_slice_data)

# 范围查询
query_range_data = {
                        "query":{
                            "range":{
                                "metricset.rtt":{
                                    "gte":1,       # >=18
                                    "lte":1000        # <=30
                                }
                            }
                        }
                    }
# 查询18<=age<=30的所有数据
#es_util.query(es_index_name, es_type_name, query_range_data)

#前缀查询
query_preifix_data = {
                        "query":{
                            "prefix":{
                                "beat.hostname":""
                            }
                        }
                    }
# 查询前缀为"赵"的所有数据
#es_util.query(es_index_name, es_type_name, query_preifix_data)

#通配符查询
query_wildcard_data = {
    "query":{
        "wildcard":{
            "beat.hostname":"*KGQBA6FBL1A"
        }
    }
}
# 查询name以id为后缀的所有数据
#es_util.query(es_index_name, es_type_name, query_wildcard_data)

#查询排序
query_orderby_data = {
                        "query":{
                            "match_all":{}
                        },
                        "sort":{
                            "metricset.rtt":{                 # 根据age字段升序排序
                                "order":"desc"       # asc升序，desc降序
                            }
                        }
                    }
#es_util.query(es_index_name, es_type_name, query_orderby_data)


#查询排序,并控制输出条数
query_orderby_data = {
                        "query":{
                            "match_all":{}
                        },
                        "size":2,
                        "sort":{
                            "metricset.rtt":{                 # 根据age字段升序排序
                                "order":"desc"       # asc升序，desc降序
                            }
                        }
                    }
es_util.query_and_filter(es_index_name, es_type_name, query_orderby_data,"hits.hits._id")