#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math


# fill missing data, merge cpc and cpm, and normalize train set

# In[2]:


cpc_train = pd.read_csv("cpc_train.csv")
cpc_train = cpc_train[0:956:]
cpm_train = pd.read_csv("cpm_train.csv")
cpm_train = cpm_train[0:956:]


# In[3]:


cpc_train = cpc_train.fillna(cpc_train.mean().cpc)
cpm_train = cpm_train.fillna(cpm_train.mean().cpm)


# In[4]:


train = cpc_train.merge(cpm_train)


# In[5]:


train.to_csv("train.csv", index=False)


# In[6]:


train = pd.read_csv("train.csv")


# In[7]:


cpc_max = train.max().cpc
cpc_min = train.min().cpc
cpm_max = train.max().cpm
cpm_min = train.min().cpm


# In[8]:


cpc_norm = (train["cpc"]-cpc_min)/(cpc_max-cpc_min)
cpm_norm = (train["cpm"]-cpm_min)/(cpm_max-cpm_min)


# In[9]:


train_norm = pd.DataFrame({"timestamp":train["timestamp"],"cpc_norm":cpc_norm})
train_norm = train_norm.merge(pd.DataFrame({"timestamp":train["timestamp"],"cpm_norm":cpm_norm}))
train_norm = train_norm.merge(pd.DataFrame({"timestamp":train["timestamp"],"is_anomaly":train["is_anomaly"]}))


# In[10]:


train_norm.to_csv("train_norm.csv", index=False)


# fill missing data, merge cpc and cpm, and normalize test set

# In[11]:


cpc_test = pd.read_csv("cpc_test.csv")
cpm_test = pd.read_csv("cpm_test.csv")
cpc_test = cpc_test.fillna(cpc_test.mean().cpc)
cpm_test = cpm_test.fillna(cpm_test.mean().cpm)
test = cpc_test.merge(cpm_test)
test.to_csv("test.csv", index=False)


# In[12]:


test = pd.read_csv("test.csv")


# In[13]:


cpc_max = test.max().cpc
cpc_min = test.min().cpc
cpm_max = test.max().cpm
cpm_min = test.min().cpm
cpc_norm = (test["cpc"]-cpc_min)/(cpc_max-cpc_min)
cpm_norm = (test["cpm"]-cpm_min)/(cpm_max-cpm_min)
test_norm = pd.DataFrame({"timestamp":test["timestamp"],"cpc_norm":cpc_norm})
test_norm = test_norm.merge(pd.DataFrame({"timestamp":test["timestamp"],"cpm_norm":cpm_norm}))
test_norm = test_norm.merge(pd.DataFrame({"timestamp":test["timestamp"],"is_anomaly":test["is_anomaly"]}))
test_norm.to_csv("test_norm.csv", index=False)


# In[ ]:




