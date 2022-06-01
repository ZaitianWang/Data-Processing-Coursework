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


# train

# In[3]:


performance = pd.DataFrame(columns=["k","threshold","TA","FA","TN","FN","precision","recall"])
for k in range(3,10):
    cluster = []
    for i in range(0,k): #partition
        cluster.append(train_norm[((i*train_norm.shape[0])//k):(((i+1)*train_norm.shape[0])//k):])
    round = 0
    while(True):
        change_count = 0
        round = round + 1
        changed = False
        mean = []
        for row in cluster: #update mean each round
            mean.append([row["cpc_norm"].mean(), row["cpm_norm"].mean()])

        for i in range(0,k): #for each cluster
            cluster_preserve = cluster[i]
            for j in range(0,cluster_preserve.shape[0]): #for each point in the cluster
                move = False
                current_point = cluster_preserve.iloc[j] #the point
                dist = math.dist([current_point["cpc_norm"],current_point["cpm_norm"]], mean[i]) #dist to its center
                dist_min = dist
                for kk in range(0,k):
                    if (kk!=i): #if closer to other
                        if(dist_min - math.dist([current_point["cpc_norm"],current_point["cpm_norm"]], mean[kk]) >= 0.00000001):
                            dist_min = math.dist([current_point["cpc_norm"],current_point["cpm_norm"]], mean[kk])
                            kkk = kk
                            changed = True
                            move = True
                if(move == True):
                    change_count = change_count + 1
                    cluster[kkk] = cluster[kkk].append(current_point)
                    cluster[i] = cluster[i].drop(current_point.name)
        if(changed == False):
            print("k=",k,", rounds=",round)
            break;
    cluster_anom = []
    data_count = []
    anom_count = []
    for i in range(0,k):
        c = cluster[i]
        cluster_anom.append(c[c["is_anomaly"]==True])
        data_count.append(c.shape[0])
        anom_count.append(cluster_anom[i].shape[0])
    anom_rate = []
    for i in range(0,k):
        anom_rate.append(anom_count[i]/data_count[i])
    threshold = [0.01,0.03,0.05,0.10]
    for j in range(0,len(threshold)):
        TA = 0
        FA = 0
        TN = 0
        FN = 0
        for i in range(0,k):
            if (anom_rate[i] >= threshold[j]):
                TA = TA + anom_count[i]
                FA = FA + (data_count[i] - anom_count[i])
            else:
                TN = TN + (data_count[i] - anom_count[i])
                FN = FN + anom_count[i]
        precision = (TA)/(TA+FA)
        recall = (TA)/(TA+FN)
        df = pd.DataFrame({"k":k,"threshold":threshold[j],"TA":TA,"FA":FA,"TN":TN,"FN":FN,"precision":precision,"recall":recall}, index=[performance.shape[0]])
        performance = performance.append(df)


# get optimal parameters: k=5, threshold=0.05

# In[4]:


performance


# In[5]:


plt.scatter(performance["precision"], performance["recall"])


# read testing dataset

# In[6]:


test_norm = pd.read_csv("test_norm.csv")
test_norm_anom = test_norm[test_norm["is_anomaly"]==True]


# test

# In[7]:


k = 5 #8
threshold = 0.05


# In[8]:


performance = pd.DataFrame(columns=["k","threshold","TA","FA","TN","FN","precision","recall"])

cluster = []
for i in range(0,k): #partition
    cluster.append(test_norm[((i*test_norm.shape[0])//k):(((i+1)*test_norm.shape[0])//k):])
round = 0
while(True):
    change_count = 0
    round = round + 1
    changed = False
    mean = []
    for row in cluster: #update mean each round
        mean.append([row["cpc_norm"].mean(), row["cpm_norm"].mean()])

    for i in range(0,k): #for each cluster
        cluster_preserve = cluster[i]
        for j in range(0,cluster_preserve.shape[0]): #for each point in the cluster
            move = False
            current_point = cluster_preserve.iloc[j] #the point
            dist = math.dist([current_point["cpc_norm"],current_point["cpm_norm"]], mean[i]) #dist to its center
            dist_min = dist
            for kk in range(0,k):
                if (kk!=i): #if closer to other
                    if(dist_min - math.dist([current_point["cpc_norm"],current_point["cpm_norm"]], mean[kk]) >= 0.00000001):
                        dist_min = math.dist([current_point["cpc_norm"],current_point["cpm_norm"]], mean[kk])
                        kkk = kk
                        changed = True
                        move = True
            if(move == True):
                change_count = change_count + 1
                cluster[kkk] = cluster[kkk].append(current_point)
                cluster[i] = cluster[i].drop(current_point.name)
    print(round, change_count)
    if(changed == False):
        break;
cluster_anom = []
data_count = []
anom_count = []
for i in range(0,k):
    c = cluster[i]
    cluster_anom.append(c[c["is_anomaly"]==True])
    data_count.append(c.shape[0])
    anom_count.append(cluster_anom[i].shape[0])
anom_rate = []
for i in range(0,k):
    anom_rate.append(anom_count[i]/data_count[i])
detect = [False,False,False,False,False]
TA = 0
FA = 0
TN = 0
FN = 0
for i in range(0,k):
    if (anom_rate[i] >= threshold):
        detect[i] = True
        TA = TA + anom_count[i]
        FA = FA + (data_count[i] - anom_count[i])
    else:
        detect[i] = False
        TN = TN + (data_count[i] - anom_count[i])
        FN = FN + anom_count[i]
precision = (TA)/(TA+FA)
recall = (TA)/(TA+FN)
df = pd.DataFrame({"k":k,"threshold":threshold,"TA":TA,"FA":FA,"TN":TN,"FN":FN,"precision":precision,"recall":recall}, index=[performance.shape[0]])
performance = performance.append(df)


# In[9]:


detect


# In[10]:


cluster


# In[11]:


performance


# In[12]:


test_norm_anom = test_norm[test_norm["is_anomaly"]==True]
for i in range(0,k):
    plt.subplot(1,2,1)
    plt.scatter(cluster[i]["cpc_norm"],cluster[i]["cpm_norm"])
    plt.subplot(1,2,2)
    plt.scatter(cluster[i]["cpc_norm"],cluster[i]["cpm_norm"])
plt.subplot(1,2,2)
plt.scatter(test_norm_anom["cpc_norm"],test_norm_anom["cpm_norm"])
plt.savefig("result_kMeans.jpg")


# In[13]:


cluster_detect = []
for i in range(0,k):
    cluster_detect.append(cluster[i])
    cluster_detect[i]["detect_anomaly"] = detect[i]
cluster_detect


# In[14]:


result = pd.DataFrame()
for c in cluster_detect:
    result = result.append(c)
result = result.sort_values(by=["timestamp"])
result


# In[15]:


result.to_csv("result_kMeans.csv")

