#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from preprocessing import *


# In[2]:


def get_indexes(vocab,doc_terms):
    indexes = []
    for v in vocab:
        index = []
        all_docs_count = 0 #appearence count in all docs
        occurence = []
        for i in range(len(doc_terms)): #for each doc
            occur = [] #[doc, count, [pos1, pos2...]]
            doc_count = doc_terms[i].count(v) #appearence count in each doc
            if doc_count != 0: #if appears
                all_docs_count = all_docs_count + 1
                occur.append(i+1)
                occur.append(doc_count)
                pos = []
                for j in range(len(doc_terms[i])):
                    if doc_terms[i][j] == v:
                        pos.append(j+1)
                if len(pos)!=0:
                    occur.append(pos)
            if len(occur)!=0:
                occurence.append(occur)
        index.append(all_docs_count)
        index.append(occurence)
        indexes.append(index)
    return indexes


# In[3]:


def index_query_sing(qry,vocab,indexes):
    q = qry.lower().rstrip()
    vocab_index = vocab.index(q)
    index = indexes[vocab_index] #a row of indexes
    pos = index[1] #[doc, count, [pos1, pos2...]] * n
    result = []
    for p in pos:
        a = p[0] #in which doc
        for b in p[2]: #pos in a doc
            result.append([a,b])
    return result


# In[4]:


def index_query(qry):
    q = qry.lower().rstrip().split(" ")
    if len(q) == 1:
        return index_query_sing(q[0], get_vocab(get_doc_terms_sing()), get_indexes(get_vocab(get_doc_terms_sing()), get_doc_terms_sing()))
    else:
        positions =[]
        for i in range(len(q)): #each word in a querey    
            pos = index_query_sing(q[i], get_vocab(get_doc_terms_sing()), get_indexes(get_vocab(get_doc_terms_sing()), get_doc_terms_sing()))
            positions.append(pos)
        candidates = positions[0]
        result = []
        for c in candidates:
            match = True
            p1 = c[0]
            p2 = c[1]
            for i in range(1, len(positions)):
                if [p1, p2+i] not in positions[i]:
                    match = False
            if match:
                result.append(c)
        return result


# In[ ]:




