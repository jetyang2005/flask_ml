# -*- coding: UTF-8 -*-
from flask import jsonify, request
from sklearn.externals import joblib
from app.auth.auths import Auth
import json


def init_api(app, es_util):
    # 加载.pkl
    model = joblib.load(r'app\rules\modelspkl\knowledge_cart.pkl')
    tf_transformer = joblib.load(r'app\rules\modelspkl\knowledge_tf_transformer.pkl')
    le = joblib.load(r'app\rules\modelspkl\knowledge_labelencoder.pkl')

    @app.route('/ml_error_predict', methods=['POST'])
    def error_predict():
        parmStr = request.get_data()
        # paramDict = json.loads(parmStr)
        # testline = paramDict['logBody']
        testline = parmStr
        """
        获取用户信息
        :return: json
        """
        auth = Auth()
        result = auth.identify(request)

        if (result['status']):
            test_datas = readDataLine(testline)
            test_feature_datas = tf_transformer.transform(test_datas)
            # 进行预测
            pred = model.predict(test_feature_datas)
            result = le.inverse_transform(pred)
            print ('预测结果:%s,预测内容:%s' % (result[0], testline))
            return result[0]
        else:
            return jsonify(result)


def readDataLine(lineStr):
    feature_data_array = []
    featureValue = lineStr.lower().strip()
    feature_data_array.append(featureValue)
    return feature_data_array
