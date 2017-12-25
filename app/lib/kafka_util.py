#!/usr/bin/env python
# -*- coding:utf-8 -*-



from kafka import KafkaProducer

import codecs
import logging
import config

logging.basicConfig(level = logging.INFO)



class KafkaUtil(object):

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=config.KAFKA_HOST_PORT)



    # 生产kafka数据，通过字符串形式
    def produce_kafka_data(self, topic, message):
        self.producer.send(topic, message)
        self.producer.flush()

