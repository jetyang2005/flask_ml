#!/usr/bin/env python
# -*- coding:utf-8 -*-

from app.lib import sklearn_classification_lib as classification
from pandas import read_csv
import seaborn as sns
import matplotlib.pyplot as plt
import warnings # current version of seaborn generates a bunch of warnings that we'll ignore
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

sns.set(style="white", color_codes=True)
# 导入数据
filename = 'data/iris.data.csv'
names = ['separ-length', 'separ-width', 'petal-length', 'petal-width', 'class']
dataset = read_csv(filename, names=names)

# classification.showInfo(dataset)

# print dataset["class"].value_counts()
#
# print(dataset.groupby('class').size())
#
# classification.showGraph(dataset)

# dataset.plot(kind='scatter', x='petal-length', y='petal-width')

sns.jointplot(x="separ-length", y="separ-width", data=dataset, size=5)
