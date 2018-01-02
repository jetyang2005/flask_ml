#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sklearn.datasets import load_files
from pandas import read_csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from app.lib import sklearn_classification_lib as skclassification
from csv import reader
from sklearn.preprocessing import LabelEncoder
from app.lib import nltk_text_analyze_lib as textAnalyzer

# # 1) 导入数据
# categories = ['ham', 'spam']
# # # 导入训练数据
# train_path = 'data/email'
# dataset_train = load_files(container_path=train_path, categories=categories)
#
#
# # 2）数据准备与理解
#
# # 计算TF-IDF
# tf_transformer = TfidfVectorizer(stop_words='english', decode_error='ignore')
# X_train_counts_tf = tf_transformer.fit_transform(dataset_train.data)
#
# # 查看数据维度
# print(X_train_counts_tf.shape)
# print X_train_counts_tf.toarray()
# print dataset_train.target
#
#
# # sk分类算法计算各种算法的精确度
# skclassification.compareAlgorithm(X_train_counts_tf.toarray(), dataset_train.target)



def readData(filename):
    class_data_array = []
    feature_data_array = []
    f = open(filename)
    line = f.readline()
    while line:

        classValue = line[0:4].lower().strip()
        featureValue = line[4:].lower().strip()
        feature_data_array.append(featureValue)
        class_data_array.append(classValue)

        line = f.readline()

    f.close()

    print ('feature len is :%d, class len is %d' %(len(feature_data_array), len(class_data_array)))

    feature_datas = textAnalyzer.tfidf_vectorizer(feature_data_array)

    le = LabelEncoder()

    labelValues = le.fit_transform(class_data_array)

    return feature_datas, labelValues

train_filename = '../lib/data/email2/train_data2.txt'
test_filename = '../lib/data/email2/test_data2.txt'

train_datas , train_class = readData(train_filename)
test_datas, test_class = readData(test_filename)

print train_datas.shape
print train_class

# # sk分类算法计算各种算法的精确度
skclassification.compareAlgorithm_Ensemble(train_datas, train_class, test_datas, test_class)


