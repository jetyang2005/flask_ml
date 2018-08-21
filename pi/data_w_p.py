from  app.lib.elasticsearch_util import Elasticsearch_Util

#输入源
es_util=Elasticsearch_Util()
type = "data_w_p"
index = type+"-20180820"
column_names=['class','wind_speed','power']
size=5000
data=es_util.getMoreDataFromES(index, type, column_names, size)

#切分训练集与测试集
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(data[column_names[1:3]],data[column_names[0]],test_size=0.5,random_state=33)


print (Y_train.value_counts())
print (Y_test.value_counts())


#归一化
from sklearn.preprocessing import StandardScaler
ss=StandardScaler()
X_train=ss.fit_transform(X_train)
X_test=ss.transform(X_test)


#逻辑回归
from sklearn.linear_model import LogisticRegression
lr=LogisticRegression()
lr.fit(X_train,Y_train)
lr_y_predict=lr.predict(X_test)


#模型评估
from sklearn.metrics import classification_report
print ('Accuracy of LR Classifier:',lr.score(X_test,Y_test))
print (classification_report(Y_test,lr_y_predict,target_names=['no ice','icing']))





