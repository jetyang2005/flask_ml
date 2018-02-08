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

# text1 = "Natural language processing (NLP) is a field of computer science, artificial intelligence and computational linguistics concerned with the interactions between computers and human (natural) languages, and, in particular, concerned with programming computers to fruitfully process large natural language corpora. Challenges in natural language processing frequently involve natural language understanding, natural language generation (frequently from formal, machine-readable logical forms), connecting language and machine perception, managing human-computer dialog systems, or some combination thereof."
#
# text2 = "The Georgetown experiment in 1954 involved fully automatic translation of more than sixty Russian sentences into English. The authors claimed that within three or five years, machine translation would be a solved problem.[2] However, real progress was much slower, and after the ALPAC report in 1966, which found that ten-year-long research had failed to fulfill the expectations, funding for machine translation was dramatically reduced. Little further research in machine translation was conducted until the late 1980s, when the first statistical machine translation systems were developed."
#
# text3 = "During the 1970s, many programmers began to write conceptual ontologies, which structured real-world information into computer-understandable data. Examples are MARGIE (Schank, 1975), SAM (Cullingford, 1978), PAM (Wilensky, 1978), TaleSpin (Meehan, 1976), QUALM (Lehnert, 1977), Politics (Carbonell, 1979), and Plot Units (Lehnert 1981). During this time, many chatterbots were written including PARRY, Racter, and Jabberwacky"

def get_tokens(text):
    lowers = text.lower()
    # remove the punctuation using the character deletion step of translate
    table = string.maketrans("", "")
    no_punctuation = lowers.translate(table, string.punctuation)
    tokens = nltk.word_tokenize(no_punctuation)
    return tokens


# 去掉标点符号
# tokens = get_tokens(text2)
# count = Counter(tokens)
# print (count.most_common(10))

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def tokenize2(text):
    #f = open(r"E:\zxdf\ml\linkdata-log\dataset\testrecord\keyword_logbody.txt", "w")
    tokens = nltk.word_tokenize(text)
    tokens = [i for i in tokens if i not in string.punctuation]
    filtered = [w for w in tokens if w not in stopwords.words('english')]
    # stemmer = PorterStemmer()
    # stems = stem_tokens(filtered, stemmer)
    print ('关键词:%s,预测内容:%s' % (filtered, text))
    # return stems
    #print >> f, "%s %s" % (filtered, text)
    #f.close()
    return filtered


def tokenize(text):
    #f = open(r"E:\zxdf\ml\linkdata-log\dataset\testrecord\keyword_logbody.txt", "a+")
    tokens = nltk.word_tokenize(text)
    tokens2 = []
    for w in tokens:
        if w[0] == '-':
            tokens2.append(w[1:])
        elif w[0] == "'":
            tokens2.append(w[1:])
        else:
            tokens2.append(w)

    stopword_tokens = [i for i in tokens2 if i not in string.punctuation]
    stopword_tokens2 = [w for w in stopword_tokens if w not in stopwords.words('english')]

    stopwords_custom = ["''", "``", "||", "'/", "'/'", u"'0x0", "'2", "'=", "'s", '**', '***', '***.***',
                        '**constraint.unique_wt**', '**failed', '**method', '--',
                        '-1', '-297991290629036654', '-614', '-6182496564283649260', '-6787310117729693199', '-8',
                        '-999999999', u'-e',
                        '..', '...', '.\\xxx\\xxx.txt', '/*', '/**', '/c', '/p', '0', '1', '==', 'b', 'c', 'e', 'x',
                        '===',
                        'v'
                        ]
    # ,'mapped'
    stopword_tokens3 = [w for w in stopword_tokens2 if w not in stopwords_custom]

    #print >> f, "%s" % (stopword_tokens3)
    #f.close()
    return stopword_tokens3

# 完成了去停用词
# tokens = get_tokens(text2)
# filtered = [w for w in tokens if not w in stopwords.words('english')]
# count = Counter(filtered)
# print (count.most_common(10))


# 词干提取（Stemming）
def count_term(text):
    tokens = get_tokens(text)
    filtered = [w for w in tokens if not w in stopwords.words('english')]
    stemmer = PorterStemmer()
    stemmed = stem_tokens(filtered, stemmer)
    count = Counter(stemmed)
    return count


# （Term Frequency，TF）指的是某一个给定的词语在该文件中出现的频率。即词w在文档d中出现的次数count(w, d)和文档d中总词数size(d)的比值。
def tf(word, count):
    # print ('count is %d, containg is %d' % (count[word], sum(count.values())))
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
    # print 'divideValue is :', divideValue
    idfvalue = math.log(divideValue)
    # print 'idfvalue: ', idfvalue
    return idfvalue


# 某一特定文件内的高词语频率，以及该词语在整个文件集合中的低文件频率，可以产生出高权重的TF-IDF。
# 因此，TF-IDF倾向于过滤掉常见的词语，保留重要的词语。
def tfidf(word, count, count_list):
    tfidf_value = tf(word, count) * idf(word, count_list)
    # print 'tfidf_value', tfidf_value
    # print ('tf is :%d, idf is :%d' %(tf(word, count), idf(word, count_list)))
    return tfidf_value


# print n_containing('python',countlist)
# enumerate()是python的内置函数,enumerate在字典上是枚举、列举的意思,
# 对于一个可迭代的（iterable）/可遍历的对象（如列表、字符串），enumerate将其组成一个索引序列，利用它可以同时获得索引和值
# enumerate多用于在for循环中得到计数
# texts = [text1, text2, text3]
#
# countlist = []
# for text in texts:
#     countlist.append(count_term(text))


# print idf('machin', countlist)

# for i, count in enumerate(countlist):
#     print count
#     print("Top words in document {}".format(i + 1))
#     scores = {word: tfidf(word, count, countlist) for word in count}
#     sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#     for word, score in sorted_words[:5]:
#         print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))


# 语料
corpus = [
    "Natural language processing (NLP) is a field of computer science, artificial intelligence and computational linguistics concerned with the interactions between computers and human (natural) languages, and, in particular, concerned with programming computers to fruitfully process large natural language corpora. Challenges in natural language processing frequently involve natural language understanding, natural language generation (frequently from formal, machine-readable logical forms), connecting language and machine perception, managing human-computer dialog systems, or some combination thereof.",
    "The Georgetown experiment in 1954 involved fully automatic translation of more than sixty Russian sentences into English. The authors claimed that within three or five years, machine translation would be a solved problem.[2] However, real progress was much slower, and after the ALPAC report in 1966, which found that ten-year-long research had failed to fulfill the expectations, funding for machine translation was dramatically reduced. Little further research in machine translation was conducted until the late 1980s, when the first statistical machine translation systems were developed.",
    "During the 1970s, many programmers began to write conceptual ontologies, which structured real-world information into computer-understandable data. Examples are MARGIE (Schank, 1975), SAM (Cullingford, 1978), PAM (Wilensky, 1978), TaleSpin (Meehan, 1976), QUALM (Lehnert, 1977), Politics (Carbonell, 1979), and Plot Units (Lehnert 1981). During this time, many chatterbots were written including PARRY, Racter, and Jabberwacky"]


def count_vectorizer(textArray):
    # 将文本中的词语转换为词频矩阵
    vectorizer = CountVectorizer(stop_words='english', decode_error='ignore')
    # 计算个词语出现的次数
    X = vectorizer.fit_transform(textArray)
    # 获取词袋中所有文本关键词
    word = vectorizer.get_feature_names()

    # 查看词频结果
    print X.toarray()
    return X.toarray()


def tfidf_vectorizer(textArray):
    # 计算TF-IDF
    # tf_transformer = TfidfVectorizer(binary=False, decode_error='ignore', stop_words='english')
    tf_transformer = TfidfVectorizer(tokenizer=tokenize, stop_words='english', decode_error='ignore')
    X_train_counts_tf = tf_transformer.fit_transform(textArray)
    tfidfword = tf_transformer.get_feature_names()

    # 查看词频结果
    #    print X_train_counts_tf.toarray()
    return X_train_counts_tf.toarray()

# tfidf_vectorizer(corpus)
