#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np
import matplotlib.pyplot as plt


# read picture

# In[2]:


lena = cv2.imread("Lena.bmp")
plt.imshow(lena[:,:,::-1])
plt.show()


# Histogram Equalization

# In[3]:


#split raw picture into RGB channels
(b,g,r) = cv2.split(lena)
#do equaization by channl
bH = cv2.equalizeHist(b)
gH = cv2.equalizeHist(g)
rH = cv2.equalizeHist(r)
#merge equalized channels
lenaH = cv2.merge((bH,gH,rH))
#compare performance with raw
plt.subplot(1,2,1).set_title("raw")
plt.imshow(lena[:,:,::-1])
plt.subplot(1,2,2).set_title("with histogram equalized")
plt.imshow(lenaH[:,:,::-1])
plt.show()


# In[4]:


hist,bins = np.histogram(lena.flatten(),256,[0,256])
plt.hist(lena.flatten(),256,[0,256], color = 'b')
hist,bins = np.histogram(lenaH.flatten(),256,[0,256])
plt.hist(lenaH.flatten(),256,[0,256], color = 'r')
plt.xlim([0,256])
plt.legend(('raw','equalized'), loc = 'upper right')
plt.show()


# In[5]:


cv2.imwrite("lenaH.bmp", lenaH)


# Binarization

# In[6]:


#tranform raw to gray scale
lenaG = cv2.cvtColor(lena, cv2.COLOR_BGR2GRAY)
#impose binarization with three customized theresholds, 50, 100, and 150
retval, lenaB_050 = cv2.threshold(lenaG, 50, 255, cv2.THRESH_BINARY)
retval, lenaB_100 = cv2.threshold(lenaG, 100, 255, cv2.THRESH_BINARY)
retval, lenaB_150 = cv2.threshold(lenaG, 150, 255, cv2.THRESH_BINARY)
#compare performance with raw and gray
plt.subplot(2,4,1).set_title("raw")
plt.imshow(lena[:,:,::-1])
plt.subplot(2,4,2).set_title("gray")
plt.imshow(lenaG,cmap="gray")
plt.subplot(2,4,5).set_title("thresh=50")
plt.imshow(lenaB_050,cmap="gray")
plt.subplot(2,4,6).set_title("thresh=100")
plt.imshow(lenaB_100,cmap="gray")
plt.subplot(2,4,7).set_title("thresh=150")
plt.imshow(lenaB_150,cmap="gray")
plt.show()


# In[7]:


#the optimal threshold
plt.imshow(lenaB_100,cmap="gray")
plt.show()


# In[8]:


cv2.imwrite("lenaB.bmp", lenaB_100)


# Noise Addition and Reduction

# In[9]:


#creat an array of gauss white noise
mean = 0
var = 0.01
noise = np.random.normal(mean, var ** 0.5, lena.shape)
#preprocess the raw picture
noiseless = np.array(lena/255, dtype=float)
#impose noise
noisy = noiseless + noise
#postprocess the noisy picture
noisy = np.clip(noisy, 0, 1)
lenaNA = np.uint8(noisy*255)
#reduce noise
lenaNR = cv2.fastNlMeansDenoisingColored(lenaNA, h=13, hColor=15)
#compare pictures
plt.subplot(1,3,1).set_title("raw")
plt.imshow(lena[:,:,::-1])
plt.subplot(1,3,2).set_title("with noise added")
plt.imshow(lenaNA[:,:,::-1])
plt.subplot(1,3,3).set_title("with noise reduced")
plt.imshow(lenaNR[:,:,::-1])
plt.show()
#show the noise-reduced one
plt.imshow(lenaNR[:,:,::-1])
plt.show()


# In[10]:


cv2.imwrite("lenaNA.bmp", lenaNA)
cv2.imwrite("lenaNR.bmp", lenaNR)


# Edge Detection

# In[11]:


plt.figure(figsize=(8,8))
for i in range(5):
    for j in range(5):
        #derive edge from raw picture
        lenaE = cv2.Canny(lena, threshold1=100+100*i, threshold2=100+100*j)
        #compare different thresholds
        plt.subplot(5,5,5*i+j+1)
        plt.imshow(lenaE, cmap="gray")
plt.show()


# In[12]:


#show the edge with optimal thresholds
lenaE = cv2.Canny(lena, threshold1=300, threshold2=200)
plt.imshow(lenaE, cmap="gray")
plt.show()


# In[13]:


cv2.imwrite("lenaE.bmp", lenaE)


# In[ ]:




