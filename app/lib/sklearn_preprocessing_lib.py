#!/usr/bin/env python
# -*- coding:utf-8 -*-


import nltk
import math
import string
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.porter import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


# 最小化，去标点符号，分词
def get_tokens(text):
    lowers = text.lower()
    # remove the punctuation using the character deletion step of translate
    table = string.maketrans("", "")
    no_punctuation = lowers.translate(table, string.punctuation)
    tokens = nltk.word_tokenize(no_punctuation)
    return tokens



def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

# 分词，去除标点符号，提取词干
def tokenize(text):
    tokens = nltk.word_tokenize(text)
    tokens = [i for i in tokens if i not in string.punctuation]
    stemmer = PorterStemmer()
    stems = stem_tokens(tokens, stemmer)
    return stems


# 分词，词干提取（Stemming），Counter类的目的是用来跟踪值出现的次数。它是一个无序的容器类型，以字典的键值对形式存储，其中元素作为key，其计数作为value。计数值可以是任意的Interger（包括0和负数）。Counter类和其他语言的bags或multisets很相似。
def count_term(text):
    tokens = get_tokens(text)
    filtered = [w for w in tokens if not w in stopwords.words('english')]
    stemmer = PorterStemmer()
    stemmed = stem_tokens(filtered, stemmer)
    count = Counter(stemmed)
    return count

# （Term Frequency，TF）指的是某一个给定的词语在该文件中出现的频率。即词w在文档d中出现的次数count(w, d)和文档d中总词数size(d)的比值。
def tf(word, count):
    #print ('count is %d, containg is %d' % (count[word], sum(count.values())))
    return float(count[word]) / sum(count.values())

def n_containing(word, count_list):
    # print word
    value = sum(1 for count in count_list if word in count)
    return value

# 逆向文件频率（Inverse Document Frequency，IDF）是一个词语普遍重要性的度量。
# 某一特定词语的IDF，可以由总文件数目除以包含该词语之文件的数目，再将得到的商取对数得到。
# 即文档总数n与词w所出现文件数docs(w, D)比值的对数。
def idf(word, count_list):
    # print ('word is %s,len is :%d,  containg is %d' % (word,len(count_list), 1+(n_containing(word, count_list))))
    divideValue = float(len(count_list)) / float((n_containing(word, count_list)))
    #print 'divideValue is :', divideValue
    idfvalue = math.log(divideValue)
    #print 'idfvalue: ', idfvalue
    return idfvalue

# 某一特定文件内的高词语频率，以及该词语在整个文件集合中的低文件频率，可以产生出高权重的TF-IDF。
# 因此，TF-IDF倾向于过滤掉常见的词语，保留重要的词语。
def tfidf(word, count, count_list):
    tfidf_value =  tf(word, count) * idf(word, count_list)
    #print 'tfidf_value', tfidf_value
    #print ('tf is :%d, idf is :%d' %(tf(word, count), idf(word, count_list)))
    return tfidf_value

# 将文本中的词语转换为词频矩阵
def count_vectorizer(textArray):

    vectorizer = CountVectorizer(stop_words='english', decode_error='ignore')
    # 计算个词语出现的次数
    X = vectorizer.fit_transform(textArray)
    # 获取词袋中所有文本关键词
    word = vectorizer.get_feature_names()

    # 查看词频结果
    print X.toarray()
    return X.toarray()

# 计算TF-IDF
def tfidf_vectorizer(textArray):

    tf_transformer = TfidfVectorizer(tokenizer=tokenize,  stop_words='english', decode_error='ignore')
    X_train_counts_tf = tf_transformer.fit_transform(textArray)
    tfidfword = tf_transformer.get_feature_names()

    # 查看词频结果
    # print X_train_counts_tf.toarray()
    return X_train_counts_tf.toarray()


