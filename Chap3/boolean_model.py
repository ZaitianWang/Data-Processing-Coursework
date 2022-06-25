#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from preprocessing import *


# In[2]:


def bool_sim(qry,doc):
    #requires two [1000100...]s
    if qry.count(1) == 0:
        return 0
    sim = 1
    for i in range(len(qry)):
        if (qry[i] == 1) and (doc[i] == 0):
            sim = 0
            break
    return sim 


# In[3]:


def bool_query(qry):
    result = []
    doc = get_doc()
    for i in range(doc.shape[0]):
        if bool_sim(get_c_q_min(get_vocab(get_doc_terms()),qry), get_c_dj(get_doc_terms(),get_vocab(get_doc_terms()))[i]) == 1:
            result.append("d%d"%(i+1))
    return result


# In[ ]:




