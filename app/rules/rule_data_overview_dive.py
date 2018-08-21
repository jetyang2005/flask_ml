# -*- coding: UTF-8 -*-
from flask import request
import uuid
import base64
import json

from app.facets_overview.python.generic_feature_statistics_generator import GenericFeatureStatisticsGenerator

from app.rules.facets import facets_utils

from app.lib import sqliteutils

def init_api(app, es_util):
    @app.route('/showOverviewAndDive', methods=['POST'])
    def showOverviewAndDive():
        parmStr = request.get_data()
        print ("请求json字符串：", parmStr)
        #paramDict = json.loads(parmStr.decode('utf-8'))
        #datasourceId = paramDict['datasourceId']
        #datasetId = paramDict['datasetId']
        #beginTime = paramDict['beginTime']
        #endTime = paramDict['endTime']
        #queryType = paramDict['queryType']
        queryType = 'overview'
        #time_stampFlag = paramDict['time_stampFlag']

        returnUrl = "NULL"

        #df = facets_utils.configanalysis(datasourceId, datasetId, beginTime, endTime, time_stampFlag)

        db_path='E://气象局//rdata.db'
        #exectCmd= "select FAULT_ID,PK_ID,MALFUNC_CODE from FAULT_REC"
        exectCmd = "select * from FAULT_REC"
        df=sqliteutils.sqlliteToDF(db_path,exectCmd)

        if df is None:
            return returnUrl

        if df.empty:
            return returnUrl

        if (queryType == 'overview'):
            returnUrl = fun_facets_overview(df)

        if (queryType == 'dive'):
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
