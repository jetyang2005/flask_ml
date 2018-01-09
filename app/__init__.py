#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for, redirect, send_from_directory
import os
import uuid
import pandas as pd
import base64

from app.lib.elasticsearch_util import Elasticsearch_Util
from app.facets_overview.python.generic_feature_statistics_generator import GenericFeatureStatisticsGenerator

db = SQLAlchemy()

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    es_util = Elasticsearch_Util()
    print '当前路径',os.getcwd()

    # %%============================================================================
    # upload file config
    # ==============================================================================
    ALLOWED_EXTENSIONS = set(['csv'])
    app.config['UPLOAD_FOLDER'] = os.getcwd() + "/data"
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    html = '''
        <!DOCTYPE html>
        <title>Upload File</title>
        <link rel="shortcut icon" href="static/favicon.ico">
        <h1>文件上传</h1>
        <form method=post enctype=multipart/form-data>
             <input type=file name=file>
             <input type=submit value=上传>
             <br><br>
             <input type=radio name='select' value='facets-overview' checked> facets-overview
             <input type=radio name='select' value='facets-dive'> facets-dive

             <br><br><br><br>
             目前上传文件只支持.csv格式的文件，文件包含标题，并且列与列之间用,隔开
        </form>
        '''

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    # %%============================================================================
    # add google-facets
    # ==============================================================================
    def fun_facets_overview(file_url):
        gfsg = GenericFeatureStatisticsGenerator()
        train_data = pd.read_csv(file_url, sep=r'\s*,\s*', engine='python', na_values='?')
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

        html_name = "./static/Overview_html/" + uuidStr + ".html"
        return redirect(html_name)

    def fun_facets_dive(file_url):
        jsonstr = pd.read_csv(file_url, sep=r'\s*,\s*', engine='python', na_values='?').to_json(orient='records')

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

        html_name = "./static/Dive_html/" + uuidStr + ".html"
        return redirect(html_name)

    # %%============================================================================
    # flask app route
    # ==============================================================================

    @app.route(app.config['UPLOAD_FOLDER'] + '/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                                   filename)

    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = str(uuid.uuid4()) + '.csv'
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_url = url_for('uploaded_file', filename=filename)

                if request.form['select'] == 'facets-overview':
                    return fun_facets_overview(file_url)
                if request.form['select'] == 'facets-dive':
                    return fun_facets_dive(file_url)
        return html

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response

    from app.users.model import db
    db.init_app(app)

    # 注册用户API接口
    from app.users.api import init_api
    init_api(app)

    # 注册规则API接口
    from app.rules.esapi import init_api
    init_api(app, es_util)

    # 注册关联分析
    from app.rules.alert_assotiation import init_api
    init_api(app, es_util)

    # 注册数据预览和深潜接口
    from app.rules.rule_data_overview_dive import init_api
    init_api(app, es_util)

    return app
