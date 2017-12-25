#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from app.lib.elasticsearch_util import Elasticsearch_Util

db = SQLAlchemy()

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    es_util = Elasticsearch_Util()

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

    # 注册规则API接口
    from app.rules.alert_assotiation import init_api
    init_api(app, es_util)

    return app
