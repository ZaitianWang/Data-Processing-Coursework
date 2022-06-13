#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas


# In[2]:


def get_doc():
    doc = pandas.read_table("document.txt",sep="：",header=None,engine="python")
    return doc


# In[3]:


def get_doc_length():
    doc = get_doc()
    length = []
    for d in doc[1]:
        w = d.lower().replace("."," ").replace(","," ").replace("，"," ").split(" ")
        w = [word for word in w if word!=""]
        length.append(len(w))
    return length


# In[4]:


def get_doc_terms(): #splitted documents, terms of length 1 or 2
    doc = get_doc()

    doc_words_1 = []
    for d in doc[1]:
        w = d.lower().replace("."," ").replace(","," ").replace("，"," ").split(" ")
        w = [word for word in w if word!=""]
        doc_words_1.append(w)

    doc_words_2 = []
    for words_1 in doc_words_1:
        words_2 = []
        for i in (range(len(words_1)-1)):
            word_2 = words_1[i] + " " + words_1[i+1]
            words_2.append(word_2)
        doc_words_2.append(words_2)

    doc_terms = []
    for i in range(len(doc_words_1)):
        d_t = doc_words_1[i] + doc_words_2[i]
        doc_terms.append(d_t)

    return doc_terms


# In[5]:


def get_doc_terms_sing(): #splitted documents, words of length 1
    doc = get_doc()

    doc_words_1 = []
    for d in doc[1]:
        w = d.lower().replace("."," ").replace(","," ").replace("，"," ").split(" ")
        w = [word for word in w if word!=""]
        doc_words_1.append(w)
    return doc_words_1


# In[6]:


def get_vocab(doc_terms):
    vocab = []
    for ts in doc_terms:
        for t in ts:
            if t in vocab:
                pass
            else:
                vocab.append(t)
    return vocab


# In[7]:


def get_c_dj(doc_terms, vocab):
    c_dj = [] # pat of term co-occur / term conjunctive component
    for terms in doc_terms:
        c = []
        for i in range(len(vocab)):
            if vocab[i] in terms:
                c.append(1)
            else:
                c.append(0)
        c_dj.append(c)
    return c_dj


# In[8]:


def default_queries(index):
    qry = pandas.read_table("query.txt",sep="：",header=None,engine="python")
    return qry[1][index]


# In[9]:


def get_c_q_min(vocab,query):
    c_q_min =[]
    #if c_q = (010)or(011)or(110)or(111), then c_q_min = (010), 
    #indicating the must-have terms with 1 and others with 0
    for v in vocab:
        if v == query.lower().rstrip():
            c_q_min.append(1)
        else:
            c_q_min.append(0)
    return c_q_min


# In[10]:


def get_doc_weight(doc_terms, vocab):
    weight = []
    for i in range(len(doc_terms)):
        w = []
        for j in range(len(vocab)):
            w.append(doc_terms[i].count(vocab[j]) / get_doc_length()[i])
        weight.append(w)
    return weight


# In[11]:


def get_qry_weight(qry, vocab):
    weight = []
    qry_terms = qry.lower().rstrip().split(" ")
    for j in range(len(vocab)):
        weight.append(qry_terms.count(vocab[j]) / len(qry_terms))
    return weight


# In[ ]:




