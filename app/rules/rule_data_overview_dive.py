#-*- coding: UTF-8 -*-
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for, redirect, send_from_directory
import os
import uuid
import pandas as pd
import base64
import json

from app.lib.elasticsearch_util import Elasticsearch_Util
from app.facets_overview.python.generic_feature_statistics_generator import GenericFeatureStatisticsGenerator

def init_api(app, es_util):

    @app.route('/showOverviewAndDive', methods=['POST'])
    def showOverviewAndDive():
        parmStr = request.get_data()
        paramDict = json.loads(parmStr)
        indexName = paramDict['indexName']
        typeName = paramDict['typeName']
        beginTime = paramDict['beginTime']
        endTime = paramDict['endTime']
        queryType = paramDict['queryType']

        returnUrl = ""

        # 查询全部
        query_data = {
            "query": {
                "bool" :
                    { "must" :
                          [
                              { "range" :
                                    { "@timestamp" :
                                          { "from" : beginTime,
                                            "to" : endTime
                                          }
                                    }
                              }
                          ]
                    }
        },
            "size": 1000
        }

        df = es_util.es_read_querybody(indexName, typeName, query_data)

        if(queryType == 'overview'):
            returnUrl = fun_facets_overview(df)
        if(queryType == 'dive'):
            returnUrl = fun_facets_dive(df)


        return returnUrl


# %%============================================================================
# add google-facets
# ==============================================================================
def fun_facets_overview(train_data):
    gfsg = GenericFeatureStatisticsGenerator()
    proto = gfsg.ProtoFromDataFrames([{'name': 'train', 'table': train_data}])
    protostr = base64.b64encode(proto.SerializeToString()).decode("utf-8")

    HTML_TEMPLATE = """ 
    <link rel="import" href="../facets-jupyter.html" >
    <facets-overview id="elem" height="100%"></facets-overview>
    <script>
        document.querySelector("#elem").protoInput = "{protostr}";
    </script>"""

    uuidStr = str(uuid.uuid4())

    html = HTML_TEMPLATE.format(protostr=protostr)
    html_write_name = "./app/static/Overview_html/" + uuidStr + ".html"

    with open(html_write_name, "w") as fout:
        fout.write(html)

    html_name = "/static/Overview_html/" + uuidStr + ".html"
    return html_name

def fun_facets_dive(train_data):
    jsonstr = train_data.to_json(orient='records')

    HTML_TEMPLATE = """<link rel="import" href="../facets-jupyter.html">
        <facets-dive id="elem" height="100%"></facets-dive>
        <script>
          var data = {jsonstr};
          document.querySelector("#elem").data = data;
        </script>"""

    html = HTML_TEMPLATE.format(jsonstr=jsonstr)

    uuidStr = str(uuid.uuid4())

    html_write_name = "./app/static/Dive_html/" + uuidStr + ".html"

    with open(html_write_name, "w") as fout:
        fout.write(html)

    html_name = "/static/Dive_html/" + uuidStr + ".html"
    return html_name
