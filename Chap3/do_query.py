#!/usr/bin/env python
# coding: utf-8

# In[1]:


from boolean_model import *
from vector_model import *
from inverted_indexes import *


# In[2]:


print(bool_query("to"))


# In[3]:


print(bool_query("do"))


# In[4]:


print(bool_query("to do"))


# In[5]:


print(bool_query("I am"))


# In[6]:


print(bool_query("Let it"))


# In[7]:


print(vect_query("to"))


# In[8]:


print(vect_query("do"))


# In[9]:


print(vect_query("to do"))


# In[10]:


print(vect_query("I am"))


# In[11]:


print(vect_query("Let it"))


# In[12]:


print(get_indexes(get_vocab(get_doc_terms_sing()), get_doc_terms_sing()))


# In[13]:


print(index_query("to"))


# In[14]:


print(index_query("do"))


# In[15]:


print(index_query("to do"))


# In[16]:


print(index_query("I am"))


# In[17]:


print(index_query("Let it"))

