#!/usr/bin/env python
# -*- coding:utf-8 -*-

from kafka import KafkaProducer
import json

import codecs
import logging
import app.config as config

logging.basicConfig(level = logging.INFO)

def create_producer():
    producer = KafkaProducer(bootstrap_servers=config.KAFKA_HOST_PORT)
    return producer

# 生产kafka数据，通过字符串形式
def produce_kafka_data(producer, topic, message):
    producer.send(topic, message)
    producer.flush()


def produce_kafka_dataframe(producer,  topic, dataset):

    # df_json = dataset.head(2).to_json(orient='records')
    df_json = dataset.to_json(orient='records')

    # print df.dtypes
    df_list = json.loads(df_json)
    num=0
    for i in df_list:
        message = json.dumps(i)
        producer.send(topic, message)
        producer.flush()
        num=num+1
    print '发送数据总条数：', num

