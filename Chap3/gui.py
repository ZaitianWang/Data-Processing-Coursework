#!/usr/bin/env python
# coding: utf-8

# In[1]:

from boolean_model import *
from vector_model import *
from inverted_indexes import *
from preprocessing import *


# In[2]:


vocab = get_vocab(get_doc_terms_sing())
indexes = get_indexes(get_vocab(get_doc_terms_sing()), get_doc_terms_sing())
vocab_indexes = []
for i in range(len(vocab)):
    vocab_indexes.append(vocab[i] + ": \t" + str(indexes[i]))
vocab_indexes
v_i = ""
for index in vocab_indexes:
    v_i = v_i + str(index) + "\n"


# In[3]:


def format_result(result):
    f = ""
    for row in result:
        f = f + str(row) + "\n"
    return f


# In[4]:


def display_bool():
    query = input_field.get()
    result = format_result(bool_query(query))
    output_content.set(result)


# In[5]:


def display_vect():
    query = input_field.get()
    result = format_result(vect_query(query))
    output_content.set(result)


# In[6]:


def display_index():
    query = input_field.get()
    result = format_result(index_query(query))
    output_content.set(result)


# In[7]:


from tkinter import *
from tkinter import ttk
root = Tk()
root.title("Document Query")

frm = ttk.Frame(root, padding=20)
frm.grid()
ttk.Label(frm, text="Indexes").grid(column=0, row=0)
ttk.Label(frm, text=v_i).grid(column=0,row=1,rowspan=3)

ttk.Label(frm, text="Query").grid(column=1,row=0,columnspan=3)

input_field = ttk.Entry(frm)
input_field.grid(column=1, row=1, columnspan=3)
output_content = StringVar()
output_content.set("Hint: \ninput anything and click a button \nto retrieve the text in the documents")
output_field = ttk.Label(frm, textvariable=output_content)
output_field.grid(column=1, row=3, columnspan=3)

ttk.Button(frm, text="Boolean", command=display_bool).grid(column=1, row=2)
ttk.Button(frm, text="Vector", command=display_vect).grid(column=2, row=2)
ttk.Button(frm, text="Indexes", command=display_index).grid(column=3, row=2)

root.mainloop()


# In[ ]:




