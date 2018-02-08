# -*- coding: UTF-8 -*-
from flask import jsonify, request
from sklearn.externals import joblib
from app.auth.auths import Auth
import json
import logging
from app.lib import nltk_text_analyze_lib as textAnalyzer

# logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s | %(filename)s[line:%(lineno)d] | %(levelname)s | %(message)s',
#                    # datefmt='%a, %d %b %Y %H:%M:%S',
#                    filename='test_trace.log',
#                    filemode='a')

def init_api(app, es_util):
    # 加载.pkl
    # model = joblib.load(r'app\rules\modelspkl\knowledge_cart.pkl')
    # tf_transformer = joblib.load(r'app\rules\modelspkl\knowledge_tf_transformer.pkl')
    # le = joblib.load(r'app\rules\modelspkl\knowledge_labelencoder.pkl')

    # test100
    # model = joblib.load(r'app\rules\modelspkl\test100\knowledge_cart.pkl')
    # tf_transformer = joblib.load(r'app\rules\modelspkl\test100\knowledge_tf_transformer.pkl')
    # le = joblib.load(r'app\rules\modelspkl\test100\knowledge_labelencoder.pkl')

    # teststack100
    # model = joblib.load(r'app\rules\modelspkl\teststack100\knowledge_cart.pkl')
    # tf_transformer = joblib.load(r'app\rules\modelspkl\teststack100\knowledge_tf_transformer.pkl')
    # le = joblib.load(r'app\rules\modelspkl\teststack100\knowledge_labelencoder.pkl')

    # teststack50_132
    # model = joblib.load(r'app\rules\modelspkl\teststack50_132\knowledge_cart.pkl')
    # tf_transformer = joblib.load(r'app\rules\modelspkl\teststack50_132\knowledge_tf_transformer.pkl')
    # le = joblib.load(r'app\rules\modelspkl\teststack50_132\knowledge_labelencoder.pkl')

    # teststack130_0
    # model = joblib.load(r'app\rules\modelspkl\teststack130_0\knowledge_cart.pkl')
    # tf_transformer = joblib.load(r'app\rules\modelspkl\teststack130_0\knowledge_tf_transformer.pkl')
    # le = joblib.load(r'app\rules\modelspkl\teststack130_0\knowledge_labelencoder.pkl')

    # teststack130_1
    # model = joblib.load(r'app\rules\modelspkl\teststack130_1\knowledge_cart.pkl')
    # tf_transformer = joblib.load(r'app\rules\modelspkl\teststack130_1\knowledge_tf_transformer.pkl')
    # le = joblib.load(r'app\rules\modelspkl\teststack130_1\knowledge_labelencoder.pkl')

    # teststack0_130
    # model = joblib.load(r'app\rules\modelspkl\teststack0_130\knowledge_cart.pkl')
    # tf_transformer = joblib.load(r'app\rules\modelspkl\teststack0_130\knowledge_tf_transformer.pkl')
    # le = joblib.load(r'app\rules\modelspkl\teststack0_130\knowledge_labelencoder.pkl')

    # teststack1_130
    # model = joblib.load(r'app\rules\modelspkl\teststack1_130\knowledge_cart.pkl')
    # tf_transformer = joblib.load(r'app\rules\modelspkl\teststack1_130\knowledge_tf_transformer.pkl')
    # le = joblib.load(r'app\rules\modelspkl\teststack1_130\knowledge_labelencoder.pkl')

    # teststack_PorterStemmer_804_804
    # model = joblib.load(r'app\rules\modelspkl\teststack_PorterStemmer_804_804\knowledge_cart.pkl')
    # tf_transformer = joblib.load(r'app\rules\modelspkl\teststack_PorterStemmer_804_804\knowledge_tf_transformer.pkl')
    # le = joblib.load(r'app\rules\modelspkl\teststack_PorterStemmer_804_804\knowledge_labelencoder.pkl')

    # teststack_NOPorterStemmer_804_804
    #model = joblib.load(r'app\rules\modelspkl\teststack_NOPorterStemmer_804_804\knowledge_cart.pkl')
    #tf_transformer = joblib.load(r'app\rules\modelspkl\teststack_NOPorterStemmer_804_804\knowledge_tf_transformer.pkl')
    #le = joblib.load(r'app\rules\modelspkl\teststack_NOPorterStemmer_804_804\knowledge_labelencoder.pkl')

    #teststack4212_804
    #model = joblib.load(r'app\rules\modelspkl\teststack4212_804\knowledge_cart.pkl')
    #tf_transformer = joblib.load(r'app\rules\modelspkl\teststack4212_804\knowledge_tf_transformer.pkl')
    #le = joblib.load(r'app\rules\modelspkl\teststack4212_804\knowledge_labelencoder.pkl')

    # =============================================================================================================================
    # teststack6678_804
    #model = joblib.load(r'app\rules\modelspkl\teststack6678_804\knowledge_cart.pkl')
    #tf_transformer = joblib.load(r'app\rules\modelspkl\teststack6678_804\knowledge_tf_transformer.pkl')
    #le = joblib.load(r'app\rules\modelspkl\teststack6678_804\knowledge_labelencoder.pkl')

    # teststack2527_804
    #model = joblib.load(r'app\rules\modelspkl\teststack2527_804\knowledge_cart.pkl')
    #tf_transformer = joblib.load(r'app\rules\modelspkl\teststack2527_804\knowledge_tf_transformer.pkl')
    #le = joblib.load(r'app\rules\modelspkl\teststack2527_804\knowledge_labelencoder.pkl')

    # teststack1662_804
    #model = joblib.load(r'app\rules\modelspkl\teststack1662_804\knowledge_cart.pkl')
    #tf_transformer = joblib.load(r'app\rules\modelspkl\teststack1662_804\knowledge_tf_transformer.pkl')
    #le = joblib.load(r'app\rules\modelspkl\teststack1662_804\knowledge_labelencoder.pkl')

    # teststack489_804
    #model = joblib.load(r'app\rules\modelspkl\teststack489_804\knowledge_cart.pkl')
    #tf_transformer = joblib.load(r'app\rules\modelspkl\teststack489_804\knowledge_tf_transformer.pkl')
    #le = joblib.load(r'app\rules\modelspkl\teststack489_804\knowledge_labelencoder.pkl')

    # teststack290_804
    #model = joblib.load(r'app\rules\modelspkl\teststack290_804\knowledge_cart.pkl')
    #tf_transformer = joblib.load(r'app\rules\modelspkl\teststack290_804\knowledge_tf_transformer.pkl')
    #le = joblib.load(r'app\rules\modelspkl\teststack290_804\knowledge_labelencoder.pkl')

    # teststack150_804
    #model = joblib.load(r'app\rules\modelspkl\teststack150_804\knowledge_cart.pkl')
    #tf_transformer = joblib.load(r'app\rules\modelspkl\teststack150_804\knowledge_tf_transformer.pkl')
    #le = joblib.load(r'app\rules\modelspkl\teststack150_804\knowledge_labelencoder.pkl')
    # =============================================================================================================================
    # normal_preprocessing01\teststack22371_804
    #model = joblib.load(r'app\rules\modelspkl\normal_preprocessing01\teststack22371_804\knowledge_cart.pkl')
    #tf_transformer = joblib.load(r'app\rules\modelspkl\normal_preprocessing01\teststack22371_804\knowledge_tf_transformer.pkl')
    #le = joblib.load(r'app\rules\modelspkl\normal_preprocessing01\teststack22371_804\knowledge_labelencoder.pkl')

    # normal_preprocessing01\teststack773_804
    #model = joblib.load(r'app\rules\modelspkl\normal_preprocessing01\teststack773_804\knowledge_cart.pkl')
    #tf_transformer = joblib.load(r'app\rules\modelspkl\normal_preprocessing01\teststack773_804\knowledge_tf_transformer.pkl')
    #le = joblib.load(r'app\rules\modelspkl\normal_preprocessing01\teststack773_804\knowledge_labelencoder.pkl')

    # =============================================================================================================================
    # normal_preprocessing02\teststack1618_804
    #model = joblib.load(r'app\rules\modelspkl\normal_preprocessing02\teststack1618_804\knowledge_cart.pkl')
    #tf_transformer = joblib.load(r'app\rules\modelspkl\normal_preprocessing02\teststack1618_804\knowledge_tf_transformer.pkl')
    #le = joblib.load(r'app\rules\modelspkl\normal_preprocessing02\teststack1618_804\knowledge_labelencoder.pkl')

    # normal_preprocessing02\teststack1043_804
    #model = joblib.load(r'app\rules\modelspkl\normal_preprocessing02\teststack1043_804\knowledge_cart.pkl')
    #tf_transformer = joblib.load(r'app\rules\modelspkl\normal_preprocessing02\teststack1043_804\knowledge_tf_transformer.pkl')
    #le = joblib.load(r'app\rules\modelspkl\normal_preprocessing02\teststack1043_804\knowledge_labelencoder.pkl')

    # normal_preprocessing02\teststack692_804
    model = joblib.load(r'app\rules\modelspkl\normal_preprocessing02\teststack692_804\knowledge_cart.pkl')
    tf_transformer = joblib.load(r'app\rules\modelspkl\normal_preprocessing02\teststack692_804\knowledge_tf_transformer.pkl')
    le = joblib.load(r'app\rules\modelspkl\normal_preprocessing02\teststack692_804\knowledge_labelencoder.pkl')


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
        # auth = Auth()
        # result = auth.identify(request)

        # if (result['status']):
        # test_datas = readDataLine(testline)
        if len(testline) == 0:
            return "this is None"
        #elif len(testline) < 15:
        #    return "0"
        else:
            test_datas = []
            featureValue = testline.lower().strip()
            test_datas.append(featureValue)

            # if test_datas != None:
            test_feature_datas = tf_transformer.transform(test_datas)
            print tf_transformer.get_feature_names()
            print test_feature_datas.toarray()

            wordlist = tf_transformer.get_feature_names()  # 获取词袋模型中的所有词
            # tf-idf矩阵 元素a[i][j]表示j词在i类文本中的tf-idf权重
            weightlist = test_feature_datas.toarray()
            # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
            sortweight=[]
            for i in range(len(weightlist)):
                print "-------这里输出第", i, "类文本的词语tf-idf权重------"
                for j in range(len(wordlist)):
                    if weightlist[i][j] > 0:
                        sortweight.append((weightlist[i][j],wordlist[j]))
                        #print wordlist[j], weightlist[i][j]
            for wordweight in sorted(sortweight, reverse=True):
                print wordweight
            # 进行预测
            pred = model.predict(test_feature_datas)
            result = le.inverse_transform(pred)
            print ('预测结果:%s,预测内容:%s' % (result[0], testline))
            logging.debug('预测结果:%s,预测内容:%s' % (result[0], testline))

            # {"isException":"1","text":"关键词"}
            #keywords = textAnalyzer.tokenize(featureValue)
            #keytext = ''
            #for keys in keywords:
            #    keytext += keys + "|"

            #return_data ="{'isException':", result[0], "}"
            #print "%s" % "{'isException':'", result[0], "'}"
            return result[0]
        # return "this is None"


# else:
#    return jsonify(result)


def readDataLine(lineStr):
    # print lineStr
    if len(lineStr) == 0:
        return
    else:
        feature_data_array = []
        featureValue = lineStr.lower().strip()
        feature_data_array.append(featureValue)
        return feature_data_array
