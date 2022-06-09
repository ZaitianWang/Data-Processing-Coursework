#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math


# import training dataset

# In[2]:


train_norm = pd.read_csv("train_norm.csv")
train_norm_anom = train_norm[train_norm["is_anomaly"]==True]


# train

# In[3]:


performance = pd.DataFrame(columns=["r","pi","TA","FA","TN","FN","precision","recall"])
for r in [0.01, 0.03, 0.05, 0.075, 0.1]:
    for pi in [0.001, 0.003, 0.005, 0.01, 0.02]:
        candidate = [i for i in range(train_norm.shape[0])]
        for i in range(train_norm.shape[0]):
            count = 0
            hic = [train_norm.iloc[i]["cpc_norm"],train_norm.iloc[i]["cpm_norm"]]
            for j in range(train_norm.shape[0]):
                if i!=j:
                    ille = [train_norm.iloc[j]["cpc_norm"],train_norm.iloc[j]["cpm_norm"]]
                    if (math.dist(hic,ille) <= r):
                        count = count + 1
                        if (count >= pi*train_norm.shape[0]):
                            candidate.remove(i)
                            break
        outlier = candidate
        TA = 0
        FA = 0
        TN = 0
        FN = 0
        for i in range(train_norm.shape[0]):
            if train_norm.iloc[i]["is_anomaly"]:
                if outlier.count(i) > 0:
                    TA = TA + 1
                else:
                    FN = FN + 1
            else:
                if outlier.count(i) > 0:
                    FA = FA + 1
                else:
                    TN = TN + 1
        prec = (TA)/(TA+FA)
        recall = (TA)/(TA+FN)
        df = pd.DataFrame({"r":r,"pi":pi,"TA":TA,"FA":FA,"TN":TN,"FN":FN,"precision":prec,"recall":recall}, index=[performance.shape[0]])
        performance = performance.append(df)


# In[4]:


performance


# In[5]:


plt.scatter(performance["precision"], performance["recall"])


# import testing dataset

# In[6]:


test_norm = pd.read_csv("test_norm.csv")
test_norm_anom = test_norm[test_norm["is_anomaly"]==True]


# test

# In[7]:


detect = [True for i in range(test_norm.shape[0])]
performance = pd.DataFrame(columns=["r","pi","TA","FA","TN","FN","precision","recall"])
r = 0.075
pi = 0.003
candidate = [i for i in range(test_norm.shape[0])]
for i in range(test_norm.shape[0]):
    count = 0
    hic = [test_norm.iloc[i]["cpc_norm"],test_norm.iloc[i]["cpm_norm"]]
    for j in range(test_norm.shape[0]):
        if i!=j:
            ille = [test_norm.iloc[j]["cpc_norm"],test_norm.iloc[j]["cpm_norm"]]
            if (math.dist(hic,ille) <= r):
                count = count + 1
                if (count >= pi*test_norm.shape[0]):
                    candidate.remove(i)
                    detect[i] = False
                    break
outlier = candidate
TA = 0
FA = 0
TN = 0
FN = 0
for i in range(test_norm.shape[0]):
    if test_norm.iloc[i]["is_anomaly"]:
        if outlier.count(i) > 0:
            TA = TA + 1
        else:
            FN = FN + 1
    else:
        if outlier.count(i) > 0:
            FA = FA + 1
        else:
            TN = TN + 1
prec = (TA)/(TA+FA)
recall = (TA)/(TA+FN)
df = pd.DataFrame({"r":r,"pi":pi,"TA":TA,"FA":FA,"TN":TN,"FN":FN,"precision":prec,"recall":recall}, index=[performance.shape[0]])
performance = performance.append(df)


# In[8]:


performance


# In[9]:


result = test_norm
result["detect_anomaly"] = detect


# In[10]:


result


# In[11]:


result[result["detect_anomaly"]==True]


# In[12]:


plt.subplot(1,2,1)
plt.scatter(result[result["detect_anomaly"]==False]["cpc_norm"],result[result["detect_anomaly"]==False]["cpm_norm"])
plt.scatter(result[result["detect_anomaly"]==True]["cpc_norm"],result[result["detect_anomaly"]==True]["cpm_norm"])
plt.subplot(1,2,2)
plt.scatter(test_norm["cpc_norm"],test_norm["cpm_norm"])
plt.scatter(test_norm_anom["cpc_norm"],test_norm_anom["cpm_norm"])
plt.savefig("result_DistanceBased.jpg")


# In[13]:


result.to_csv("result_DistanceBased.csv")

