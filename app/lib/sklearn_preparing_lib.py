#!/usr/bin/env python
# -*- coding:utf-8 -*-


from sklearn.model_selection import train_test_split


def splitTrainAndTestData(dataset, classPosition, validationSizeRatio=0.2, seed=7):

    # 分离数据集
    array = dataset.values
    X = array[:, 0:classPosition]
    Y = array[:, classPosition]
    validation_size = validationSizeRatio
    X_train, X_validation, Y_train, Y_validation = \
        train_test_split(X, Y, test_size=validation_size, random_state=seed)
    return X_train, X_validation, Y_train, Y_validation

# 算法审查，数据集分为两个参数，其中训练数据集和测试数据集是和在一起的
def splitTrainAndTestData_XY(X, Y, validationSizeRatio=0.2, seed=7):
    # 分离数据集
    validation_size = validationSizeRatio
    X_train, X_validation, Y_train, Y_validation = \
        train_test_split(X, Y, test_size=validation_size, random_state=seed)

    return X_train, X_validation, Y_train, Y_validation
