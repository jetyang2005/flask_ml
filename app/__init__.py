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
    print ('当前路径',os.getcwd())

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

    # # 注册日志异常检测API接口
    #from app.rules.nlp_error_predict import init_api
    #init_api(app, es_util)

    return app
