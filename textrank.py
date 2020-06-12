from gensim.models import KeyedVectors
import os
import subprocess
import jieba

def wv():
    file = '100000-small.txt'
    wv_from_text = KeyedVectors.load_word2vec_format(file,binary=False)
    wv_from_text.init_sims(replace=True)
    return wv_from_text



def article_jieba_cut(filename):
    txt_list = []
    with open('./pdf/{}.txt'.format(filename),'r',encoding='utf-8') as f:
        for line in f:
            txt_list.append(line)
    article = ''
    for i in range(len(txt_list)):
            article += txt_list[i].replace('\n','').replace('\x0c','')
    stop_words = []
    with open('stopwords.txt','r',encoding='utf-8') as f:
        for i in f:
            stop_words.append(i.replace('\n',''))
    article_cut = jieba.lcut(article)
    return article_cut, stop_words

def cut_dict(first_news,stop_words):
    first_news_1 = []
    for i in first_news:
        if i not in stop_words:
            first_news_1.append(i)
    w_dict = {}
    for i,word in enumerate(first_news_1):
        window_list = []
        for j in range(3):
            if (i+(j+1)) < len(first_news_1):
                window_list.append(first_news_1[i+(j+1)])
            if (i-(j+1)) > -1:
                window_list.append(first_news_1[i-(j+1)])
        if word in w_dict:
            w_dict[word] += window_list
        else:
            w_dict[word] = window_list
    for word in w_dict:
        w_dict[word] = [i for i in set(w_dict[word])]
    w_dict_weight = {}
    for i in w_dict:
        w_dict_weight[i] = 1
    return w_dict,w_dict_weight


def sum_V_jk(V_j,wv_from_text,w_dict):
    sum_v_jk = 0
    if V_j in wv_from_text:
        for V_k in w_dict[V_j]:
            if V_k in wv_from_text:
                sum_v_jk += wv_from_text.similarity(V_j,V_k)
            else:
                sum_v_jk += 0.45
    else:
        sum_v_jk = 0.45*len(w_dict[V_j])
    return sum_v_jk

def sum_V_ij(V_i,wv_from_text,w_dict,w_dict_weight):
    sum_v_ij = 0
    if V_i in wv_from_text:
        for V_j in w_dict[V_i]:
            sum_v_jk = sum_V_jk(V_j,wv_from_text,w_dict)
            if V_j in wv_from_text:
                sum_v_ij = (wv_from_text.similarity(V_i,V_j) * w_dict_weight[V_j] / sum_v_jk) + sum_v_ij
            else:
                sum_v_ij = (0.45 / sum_v_jk) + sum_v_ij
    else:
        for V_j in w_dict[V_i]:
            sum_v_jk = sum_V_jk(V_j,wv_from_text,w_dict)
            sum_v_ij = (0.45/sum_v_jk) + sum_v_ij
    return sum_v_ij

def WS(V_i,wv_from_text,w_dict,w_dict_weight):
    d = 0.85
    ws_weight = (1-d) + (d * sum_V_ij(V_i,wv_from_text,w_dict,w_dict_weight))
    w_dict_weight[V_i] = ws_weight

def num_it(w_dict,w_dict_weight,wv_from_text):
    for i in range(5):
        for word in w_dict:
            WS(word,wv_from_text,w_dict,w_dict_weight)

def words(filename):
    wv_from_text = wv()
    article_cut, stop_words = article_jieba_cut(filename)
    w_dict, w_dict_weight = cut_dict(article_cut,stop_words)
    num_it(w_dict,w_dict_weight,wv_from_text)
    words_list = [i[0] for i in sorted(w_dict_weight.items(),key=lambda x:x[1],reverse=True)][:30]
    return words_list
