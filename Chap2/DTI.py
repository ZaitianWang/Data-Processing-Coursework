#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math


# read training dataset

# In[2]:


train_norm = pd.read_csv("train_norm.csv")
train_norm_anom = train_norm[train_norm["is_anomaly"]==True]


# init training parameters

# In[3]:


samples = [] #a partitions of dataset
for i in range(0,train_norm.shape[0]):
    samples.append(i) #[0-955]
attributes = ["cpc_norm", "cpm_norm"]
attr = 0 #index of attributes
bran = [-1,-1] #branches of each decision, valid locally


# In[4]:


DT_leaves = [[False for col in range(3)] for row in range(3)] #[[fff][fff][fff]]


# training function

# In[5]:


def DTI(samp, attr, bran):
    #if all samples in a same class
    if(list(train_norm.loc[samp]["is_anomaly"]).count(True) == train_norm.loc[samp].shape[0]):
        #leaf = true
        if(attr==1):
            DT_leaves[bran[attr-1]] = [True,True,True]
        elif(attr==2):
            DT_leaves[bran[attr-2]][bran[attr-1]] = True
    elif(list(train_norm.loc[samp]["is_anomaly"]).count(False) == train_norm.loc[samp].shape[0]):
        #leaf = false
        if(attr==1):
            DT_leaves[bran[attr-1]] = [False,False,False]
        elif(attr==2):
            DT_leaves[bran[attr-2]][bran[attr-1]] = False
    #else if no more atttibutees
    elif(attr==len(attributes)):
        #leaf = mode(class)
        mode = train_norm.loc[samp]["is_anomaly"].mode()[0]
        if(attr==1):
            DT_leaves[bran[attr-1]] = [mode,mode,mode]
        elif(attr==2):
            DT_leaves[bran[attr-2]][bran[attr-1]] = mode
    #else if sample = 0
    elif(len(samp)==0):
        #pass
        pass;
    #else (not stop)
    else:
        #split sample
        sub_samp_0 = []
        sub_samp_1 = []
        sub_samp_2 = []
        for s in samp:
            val = train_norm.iloc[s][attributes[attr]] #cpc_norm/cpm_norm
            if val<(1/3):
                sub_samp_0.append(s)
            elif val>=(1/3) and val<(2/3):
                sub_samp_1.append(s)
            else:
                sub_samp_2.append(s)
    #recursive
    if attr<len(bran):
        bran[attr] = 0 #[0,-1],[0,0],[1,0],[2,0]
        DTI(sub_samp_0,attr+1,bran)
        bran[attr] = 1 #[1,-1],[0,1],[1,1]...
        DTI(sub_samp_1,attr+1,bran)
        bran[attr] = 2 #[2,-1],[0,2]...
        DTI(sub_samp_2,attr+1,bran)


# train

# In[6]:


DT_leaves


# In[7]:


DTI(samples,attr,bran)


# In[8]:


DT_leaves


# In[9]:


def trim(tree):
    if type(tree) == list:
        if(tree.count(tree[0]) == len(tree)):
            return tree[0]
        else:
            for i in range(len(tree)):
                tree[i] = trim(tree[i])
            return tree
    else:
        return tree


# In[10]:


DT_leaves = trim(DT_leaves)


# In[11]:


DT_leaves


# read testing dataset

# In[12]:


test_norm = pd.read_csv("test_norm.csv")
test_norm_anom = test_norm[test_norm["is_anomaly"]==True]


# test

# In[13]:


detect = []
for i in range(test_norm.shape[0]):
    branch = [-1,-1]
    val = test_norm.iloc[i]["cpc_norm"]
    if val<(1/3):
        branch[0] = 0
    elif val>=(1/3) and val<(2/3):
        branch[0] = 1
    else:
        branch[0] = 2
    if type(DT_leaves[branch[0]]) == list:
        val = test_norm.iloc[i]["cpm_norm"]
        if val<(1/3):
            branch[1] = 0
        elif val>=(1/3) and val<(2/3):
            branch[1] = 1
        else:
            branch[1] = 2
        detect.append(DT_leaves[branch[0]][branch[1]])
    else: #if after branching is leaf
        detect.append(DT_leaves[branch[0]])


# In[14]:


result = test_norm
result["detect_anomaly"] = detect


# In[15]:


result


# In[16]:


result[result["detect_anomaly"]==True]


# In[17]:


TA = result[(result["detect_anomaly"]==True) & (result["is_anomaly"]==True)].shape[0]
FA = result[(result["detect_anomaly"]==True) & (result["is_anomaly"]==False)].shape[0]
TN = result[(result["detect_anomaly"]==False) & (result["is_anomaly"]==False)].shape[0]
FN = result[(result["detect_anomaly"]==False) & (result["is_anomaly"]==True)].shape[0]
precision = (TA)/(TA+FA)
recall = (TA)/(TA+FN)
performance = pd.DataFrame({"precision":[precision],"recall":[recall]})
performance


# In[18]:


plt.subplot(1,2,1)
plt.scatter(result[result["detect_anomaly"]==False]["cpc_norm"],result[result["detect_anomaly"]==False]["cpm_norm"])
plt.scatter(result[result["detect_anomaly"]==True]["cpc_norm"],result[result["detect_anomaly"]==True]["cpm_norm"])
plt.subplot(1,2,2)
plt.scatter(test_norm["cpc_norm"],test_norm["cpm_norm"])
plt.scatter(test_norm_anom["cpc_norm"],test_norm_anom["cpm_norm"])
plt.savefig("result_DTI.jpg")


# In[19]:


result.to_csv("result_DTI.csv")

