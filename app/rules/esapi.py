#-*- coding: UTF-8 -*-
from flask import jsonify, request
from app.users.model import Users
from app.auth.auths import Auth
from .. import common
import json


def init_api(app, es_util):

    @app.route('/estest', methods=['POST'])
    def queryESTest():
        """
        获取用户信息
        :return: json
        """
        auth = Auth()
        result = auth.identify(request)
        if (result['status']):
          print 'hello'

          es_index_name = "1007-linux-system-cpu*"
          es_type_name = "linux-system-cpu"

          # 查询全部
          query_data = {"query": {
            "match_all": {}
            }
          }

          response = es_util.query(es_index_name, es_type_name, query_data)

          result_list = []
          # 存放键值
          key_name = response['hits']['hits'][0]["_source"].keys()

          result_list.append(key_name)

          for hit in response['hits']['hits']:
              # 存放value
              result_list.append(hit["_source"].values())
              # print(hit["_source"].values())

          result = json.dumps(result_list, indent=4)
          print result
          return result

        else:
          return jsonify(result)
