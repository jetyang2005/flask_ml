# -*- coding: UTF-8 -*-
from flask import request
import uuid
import base64
import json

from app.facets_overview.python.generic_feature_statistics_generator import GenericFeatureStatisticsGenerator

from app.rules.facets import facets_utils


def init_api(app, es_util):
    @app.route('/showOverviewAndDive', methods=['POST'])
    def showOverviewAndDive():
        parmStr = request.get_data()
        print ("请求json字符串：", parmStr)
        paramDict = json.loads(parmStr)
        datasourceId = paramDict['datasourceId']
        datasetId = paramDict['datasetId']
        beginTime = paramDict['beginTime']
        endTime = paramDict['endTime']
        queryType = paramDict['queryType']
        time_stampFlag = paramDict['time_stampFlag']

        returnUrl = "NULL"

        df = facets_utils.configanalysis(datasourceId, datasetId, beginTime, endTime, time_stampFlag)

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
