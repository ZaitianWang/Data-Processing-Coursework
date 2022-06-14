#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from functools import reduce
import math
from preprocessing import *


# In[2]:


def vect_sim(qry,doc):
    #requires two weights [0, 1, 0] and [0.4, 0.4, 0.2]
    upper = reduce(lambda x, y: x+y, list(map(lambda x, y: x*y, qry, doc)))
    l1 = reduce(lambda x, y: x+y, list(map(lambda x, y: x*y, doc, doc)))
    l2 = reduce(lambda x, y: x+y, list(map(lambda x, y: x*y, qry, qry)))
    lower = math.sqrt(l1)*math.sqrt(l2)
    sim = upper/lower
    return sim 


# In[3]:


def take_second(e):
    return e[1]


# In[4]:


def vect_query(qry):
    result = []
    doc = get_doc()
    for i in range(doc.shape[0]):
        q = get_qry_weight(qry,get_vocab(get_doc_terms_sing()))
        d = get_doc_weight(get_doc_terms_sing(),get_vocab(get_doc_terms_sing()))[i]
        sim = vect_sim(q, d)
        result.append(["d%d"%(i+1), sim])
    result.sort(key=take_second,reverse=True)
    return result


# In[ ]:




