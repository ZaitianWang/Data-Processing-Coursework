#!/usr/bin/env python
# coding: utf-8

# In[1]:


import boolean_model
import vector_model
import inverted_indexes


# In[2]:


bool_query("to")


# In[3]:


bool_query("do")


# In[4]:


bool_query("to do")


# In[5]:


bool_query("I am")


# In[6]:


bool_query("Let it")


# In[7]:


vect_query("to")


# In[8]:


vect_query("do")


# In[9]:


vect_query("to do")


# In[10]:


vect_query("I am")


# In[11]:


vect_query("Let it")


# In[12]:


get_indexes(get_vocab(get_doc_terms_sing()), get_doc_terms_sing())


# In[13]:


index_query("to")


# In[14]:


index_query("do")


# In[15]:


index_query("to do")


# In[16]:


index_query("I am")


# In[17]:


index_query("Let it")

