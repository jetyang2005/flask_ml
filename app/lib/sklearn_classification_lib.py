#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 导入类库
from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier

# 导入数据
filename = 'data/iris.data.csv'
names = ['separ-length', 'separ-width', 'petal-length', 'petal-width', 'class']
dataset = read_csv(filename, names=names)

def showInfo(dataset):
    #显示数据维度
    print('数据维度: 行 %s，列 %s' % dataset.shape)
    # 查看数据的前10行
    print(dataset.head(10))
    # 统计描述数据信息
    print(dataset.describe())
    # 分类分布情况
    print(dataset.groupby('class').size())

# showInfo(dataset)

def showGraph(dataset):
    # 箱线图
    dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
    pyplot.show()

    # 直方图
    dataset.hist()
    pyplot.show()

    # 散点矩阵图
    scatter_matrix(dataset)
    pyplot.show()

# showGraph(dataset)

def compareAlgorithm(dataset, classPosition, validationSizeRatio=0.2, num_folds=10, seed=7, scoring='accuracy'):
    # 分离数据集
    array = dataset.values
    X = array[:, 0:classPosition]
    Y = array[:, classPosition]
    validation_size = validationSizeRatio

    X_train, X_validation, Y_train, Y_validation = \
        train_test_split(X, Y, test_size=validation_size, random_state=seed)

    # 算法审查
    models = {}
    models['LR'] = LogisticRegression()
    models['LDA'] = LinearDiscriminantAnalysis()
    models['KNN'] = KNeighborsClassifier()
    models['CART'] = DecisionTreeClassifier()
    models['NB'] = GaussianNB()
    models['SVM'] = SVC()

    # 评估算法
    results = []
    for key in models:
        kfold = KFold(n_splits=num_folds, random_state=seed)
        cv_results = cross_val_score(models[key], X_train, Y_train, cv=kfold, scoring=scoring)
        results.append(cv_results)
        print('%s: %f (%f)' %(key, cv_results.mean(), cv_results.std()))
    return models, results

# compareAlgorithm(dataset, 4, 0.2)


def compareAlgorithm_Pipelines(dataset, classPosition, validationSizeRatio=0.2, num_folds=10, seed=7, scoring='accuracy'):
    # 分离数据集
    array = dataset.values
    X = array[:, 0:classPosition]
    Y = array[:, classPosition]
    validation_size = validationSizeRatio

    X_train, X_validation, Y_train, Y_validation = \
        train_test_split(X, Y, test_size=validation_size, random_state=seed)
    # 评估算法 - 正态化数据
    pipelines = {}
    pipelines['ScalerLR'] = Pipeline([('Scaler', StandardScaler()), ('LR', LogisticRegression())])
    pipelines['ScalerLDA'] = Pipeline([('Scaler', StandardScaler()), ('LDA', LinearDiscriminantAnalysis())])
    pipelines['ScalerKNN'] = Pipeline([('Scaler', StandardScaler()), ('KNN', KNeighborsClassifier())])
    pipelines['ScalerCART'] = Pipeline([('Scaler', StandardScaler()), ('CART', DecisionTreeClassifier())])
    pipelines['ScalerNB'] = Pipeline([('Scaler', StandardScaler()), ('NB', GaussianNB())])
    pipelines['ScalerSVM'] = Pipeline([('Scaler', StandardScaler()), ('SVM', SVC())])
    results = []
    for key in pipelines:
        kfold = KFold(n_splits=num_folds, random_state=seed)
        cv_results = cross_val_score(pipelines[key], X_train, Y_train, cv=kfold, scoring=scoring)
        results.append(cv_results)
        print('%s : %f (%f)' % (key, cv_results.mean(), cv_results.std()))

    return pipelines, results

# compareAlgorithm_Pipelines(dataset, 4, 0.2)

def compareAlgorithm_Ensemble(dataset, classPosition, validationSizeRatio=0.2, num_folds=10, seed=7, scoring='accuracy'):
    # 分离数据集
    array = dataset.values
    X = array[:, 0:classPosition]
    Y = array[:, classPosition]
    validation_size = validationSizeRatio

    X_train, X_validation, Y_train, Y_validation = \
        train_test_split(X, Y, test_size=validation_size, random_state=seed)

    # 集成算法
    ensembles = {}
    ensembles['ScaledAB'] = Pipeline([('Scaler', StandardScaler()), ('AB', AdaBoostClassifier())])
    ensembles['ScaledGBM'] = Pipeline([('Scaler', StandardScaler()), ('GBM', GradientBoostingClassifier())])
    ensembles['ScaledRF'] = Pipeline([('Scaler', StandardScaler()), ('RFR', RandomForestClassifier())])
    ensembles['ScaledET'] = Pipeline([('Scaler', StandardScaler()), ('ETR', ExtraTreesClassifier())])

    results = []
    for key in ensembles:
        kfold = KFold(n_splits=num_folds, random_state=seed)
        cv_result = cross_val_score(ensembles[key], X_train, Y_train, cv=kfold, scoring=scoring)
        results.append(cv_result)
        print('%s: %f (%f)' % (key, cv_result.mean(), cv_result.std()))
    return ensembles, results


# compareAlgorithm_Ensemble(dataset, 4, 0.2)

def compareAlgorithm_BoxLine(models, results):
    # 箱线图比较算法
    fig = pyplot.figure()
    fig.suptitle('Algorithm Comparison')
    ax = fig.add_subplot(111)
    pyplot.boxplot(results)
    ax.set_xticklabels(models.keys())
    pyplot.show()

# models, results = compareAlgorithm_Ensemble(dataset, 4, 0.2, 10, 7, 'accuracy')
# compareAlgorithm_BoxLine(models, results)

# 分离数据集
def optimizeAlgorithm_KNN(dataset, classPosition, validationSizeRatio=0.2, num_folds=10, seed=7, scoring='accuracy'):

    array = dataset.values
    X = array[:, 0:classPosition]
    Y = array[:, classPosition]
    validation_size = validationSizeRatio
    X_train, X_validation, Y_train, Y_validation = \
        train_test_split(X, Y, test_size=validation_size, random_state=seed)

    # 调参改进算法 - KNN
    scaler = StandardScaler().fit(X_train)
    rescaledX = scaler.transform(X_train)
    param_grid = {'n_neighbors': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]}
    model = KNeighborsClassifier()
    kfold = KFold(n_splits=num_folds, random_state=seed)
    grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring=scoring, cv=kfold)
    grid_result = grid.fit(X=rescaledX, y=Y_train)

    print('最优：%s 使用%s' % (grid_result.best_score_, grid_result.best_params_))
    cv_results = zip(grid_result.cv_results_['mean_test_score'],
                     grid_result.cv_results_['std_test_score'],
                     grid_result.cv_results_['params'])
    for mean, std, param in cv_results:
        print('%f (%f) with %r' % (mean, std, param))

# optimizeAlgorithm_KNN(dataset, 4)

# 调参改进算法 - SVM
def optimizeAlgorithm_SVM(dataset, classPosition, validationSizeRatio=0.2, num_folds=10, seed=7, scoring='accuracy'):

    # 分离数据集
    array = dataset.values
    X = array[:, 0:classPosition]
    Y = array[:, classPosition]
    validation_size = validationSizeRatio
    X_train, X_validation, Y_train, Y_validation = \
        train_test_split(X, Y, test_size=validation_size, random_state=seed)

    scaler = StandardScaler().fit(X_train)
    rescaledX = scaler.transform(X_train).astype(float)
    param_grid = {}
    param_grid['C'] = [0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.3, 1.5, 1.7, 2.0]
    param_grid['kernel'] = ['linear', 'poly', 'rbf', 'sigmoid']
    model = SVC()
    kfold = KFold(n_splits=num_folds, random_state=seed)
    grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring=scoring, cv=kfold)
    grid_result = grid.fit(X=rescaledX, y=Y_train)

    print('最优：%s 使用%s' % (grid_result.best_score_, grid_result.best_params_))
    cv_results = zip(grid_result.cv_results_['mean_test_score'],
                     grid_result.cv_results_['std_test_score'],
                     grid_result.cv_results_['params'])
    for mean, std, param in cv_results:
        print('%f (%f) with %r' % (mean, std, param))

optimizeAlgorithm_SVM(dataset, 4)

# 调参改进算法 - SVM
def optimizeAlgorithm_GradientBoosting(dataset, classPosition, validationSizeRatio=0.2, num_folds=10, seed=7, scoring='neg_mean_squared_error'):

    # 分离数据集
    array = dataset.values
    X = array[:, 0:classPosition]
    Y = array[:, classPosition]
    validation_size = validationSizeRatio
    X_train, X_validation, Y_train, Y_validation = \
        train_test_split(X, Y, test_size=validation_size, random_state=seed)

    scaler = StandardScaler().fit(X_train)
    rescaledX = scaler.transform(X_train)
    param_grid = {'n_estimators': [10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900]}
    model = GradientBoostingClassifier()
    kfold = KFold(n_splits=num_folds, random_state=seed)
    grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring=scoring, cv=kfold)
    grid_result = grid.fit(X=rescaledX, y=Y_train)
    print('最优：%s 使用%s' % (grid_result.best_score_, grid_result.best_params_))


# optimizeAlgorithm_GradientBoosting(dataset, 4)

def algorithm_SVM(dataset, classPosition, validationSizeRatio=0.2, seed=7):

    # 分离数据集
    array = dataset.values
    X = array[:, 0:classPosition]
    Y = array[:, classPosition]
    validation_size = validationSizeRatio
    X_train, X_validation, Y_train, Y_validation = \
        train_test_split(X, Y, test_size=validation_size, random_state=seed)

    # 模型最终化
    scaler = StandardScaler().fit(X_train)
    rescaledX = scaler.transform(X_train)
    model = SVC(C=0.8, kernel='linear')
    model.fit(X=rescaledX, y=Y_train)

    # 评估模型
    rescaled_validationX = scaler.transform(X_validation)
    predictions = model.predict(rescaled_validationX)
    print(accuracy_score(Y_validation, predictions))
    print(confusion_matrix(Y_validation, predictions))
    print(classification_report(Y_validation, predictions))

algorithm_SVM(dataset, 4)
