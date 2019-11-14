"""STAT and ENTI module"""
import csv
import socket
import threading
import multiprocessing
import os
from pynlp import StanfordCoreNLP

def enti_fun(tmp, conn):
    """If enti command send etities and it types back to client"""
    nlp = StanfordCoreNLP(annotators='entitymentions')
    for row in tmp:
        document = nlp(row)
        for entity in document.entities:
            conn.sendall((str(entity)+','+'('+str(entity.type)+')'+';').encode("ISO8859-1"))
        conn.sendall(('endofthetwit;').encode("ISO8859-1"))
    conn.sendall(('allend').encode("ISO8859-1"))



def search_the_most_popular_word(all_words, res_list):
    """TOP TEN WORDS"""
    max_repeat = max_index = i_index = 0
    while i_index != len(all_words):
        if max_repeat < res_list[i_index]:
            max_repeat = res_list[i_index]
            word = all_words[i_index]
            max_index= i_index
        i_index+=1
    res = all_words[max_index]
    return res

def ten_words(tmp, column):
    buf = full_column(tmp, column)
    repeat_list = []
    top_ten = ['ten most common words']
    for i in range(10):
        counter = 0
        while counter != len(buf):
            repeat_list.append(buf.count(buf[counter]))
            counter += 1
        word = search_the_most_popular_word(buf, repeat_list)
        top_ten.append(word)
        k = buf.index(word)
        try:
            while True:
                buf.pop(k)
                repeat_list.pop(k)
                k = buf.index(word)
        except ValueError:
            continue
    return top_ten

def top_ten_authors(tmp, followers, user_name, nickname):
    """TOP TEN AUTHORS """
    follow_lst = []
    result = ['top ten authors: ']
    for i in tmp:
        follow_lst.append((i[followers]))
    follow_lst = sorted(follow_lst,reverse = True)
    if len(follow_lst)>10:
        count = 10
    else:
        count = len(follow_lst)
    k = 1
    for i in follow_lst:
        if k > count:
            break
        for j in tmp:
            if str(i) == j[followers]:
                nick_name = j[nickname]
                username = j[user_name]
                break
        result.append(str(k)+')'+'User Name: '+username+',Nickname: '+nick_name+',Followers: '
                +str(i))
        k += 1
    return result

def top_ten_tweets(tmp, rts, tweet, author):
    """TOP TEN TWEETS ,AUTHORS AND COUNT RETWEETS"""
    d = {}
    result = ['Ten Tweets and number of ReTweets']
    for i in tmp:
        if i[rts] != '':
            d[i[tweet]] = int(i[rts])
    r = sorted(d.items(), key = lambda x: x[1],reverse = True)
    i = 1
    if len(r) < 10:
        count = len(r)
    else:
        count = 10
    for k in r:
        if i > count:
            break
        a = ''
        for j in tmp:
            if j[rts] == str(k[1]):
                a = j[author]
                break
        result.append(str(i)+')'+str(k[0])+',retweets '':'+str(k[1])+',author:'+str(a))
        i += 1
    return result

def country_and_retweets(tmp, user_name, nick_name, tw_cont, country):
    """CONTRY TWEETS AND RETWEETS """
    res_tws = ['Tweets Country']
    res_rts = ['ReTweets Country']
    for i in tmp:
        if i[tw_cont][0:2] == 'RT':
            res_rts.append(i[country])
        else:
            res_tws.append(i[country])
    return res_tws, res_rts

def make_dict(lst):
    d = {}
    count = 0
    for i in lst:
        d[i] = count
        count += 1
    return d

def full_column(tmp, column):
    full_text = []
    for i in tmp:
        full_text.append(i[column])
    full_text = ''.join(full_text)
    lst = full_text.split()
    return lst

def stat_fun(tmp, conn):
    res = []
    d = make_dict(tmp[0])
    res.append(ten_words(tmp[1:len(tmp)], d['Tweet content']))
    res.append(top_ten_tweets(tmp[1:len(tmp)], d['RTs'], d['Tweet content'], d['User Name']))
    res.append(top_ten_authors(tmp[1:len(tmp)], d['Followers'], d['User Name'], d['Nickname']))
    tw_c, rtw_c = country_and_retweets(tmp[1:len(tmp)], d['User Name'], d['Nickname'], d['Tweet content'], d['Country'])
    res.append(tw_c)
    res.append(rtw_c)
    for i in res:
        for j in i:
            conn.sendall((str(j)+';').encode("ISO8859-1"))
    conn.sendall(('allend').encode("ISO8859-1"))
