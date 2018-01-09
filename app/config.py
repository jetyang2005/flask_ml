# -*- coding:utf-8 -*-

# 配置当前应用端口号及IP地址
DEBUG = True
PORT = 3333
HOST = "10.0.0.188"

# 关系型数据库配置，此数据库配置需要与springboot平台数据库保持一致
DB_USER = 'root'
DB_PASSWORD = '123456'
DB_HOST = '10.0.0.188'
DB_DB = 'linkdata20171030'
DB_PORT = 3306
DB_CHAR = "utf8"


# SpringBoot平台Token秘钥
SECRET_KEY = "adsfialle323klsflADASF"

# Elasticsearch配置信息
ES_HOST = '10.0.0.188'
ES_PORT = 9200

# Kafka配置信息，可以在python中向kafka发送内容
KAFKA_HOST_PORT = '10.0.0.188:9092'

# SQLALCHEMY配置路径，此路径无需修改
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_DB

# elasticsearch基础类库日志
ELASTICSEARCH_LOG_DIR = '/Users/yangwm/flask/linkdata_api_py/log/elastticsearch.log'