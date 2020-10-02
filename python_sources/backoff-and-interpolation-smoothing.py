#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
import pandas as pd
import numpy
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.tokenize import RegexpTokenizer
import re
import gc
from  collections import Counter
import math
import random


# In[2]:


file_0=open("../input/xab",mode='r',encoding='latin-1')
file_content=file_0.read()
file_0.close()
del(file_0)
gc.collect()


# In[3]:


temp = re.sub(r'[^a-zA-Z0-9\-\s\.]*', r'', file_content)
temp = re.sub(r'(\-|\s+)', ' ', temp)
del(file_content)


# In[4]:


sent_token=nltk.sent_tokenize(temp[0:4500])
del(temp)


# In[5]:


print(len(sent_token))


# In[6]:


random.shuffle(sent_token)
train=sent_token[0:28]
test=sent_token[28:32]


# In[ ]:





# In[7]:


def create_token(input):
    res=[]
    for x1 in input:
        l=x1.split(" ")
        res.extend(l)
    return res    
def find_trigrams(input_list):
    trigram_list = []
    for i in range(len(input_list)-2):
        trigram_list.append((input_list[i], input_list[i+1],input_list[i+2]))
    return trigram_list

def compper(d,test,tokenl):
    per=1
    smoothing=1/tokenl
    #value=d.keys()
    length=len(test)
    for t in test:
        if t in d.keys():
            
            per=per*d[t]
            #print("y")
        else:
            per=per*smoothing
    #print(per,length)        
    perl=pow(1/per,1/length)
    #print(per)
    return perl


# In[8]:


random.shuffle(train)
dev_set1=train[25:28]
train_set1=train[0:25]
dev_set2=train[2:5]
train_set2=train[0:2]+train[5:28]
dev_set3=train[19:21]
train_set3=train[0:19]+train[21:28]
dev_set4=train[16:19]
train_set4=train[0:16]+train[19:28]
dev_set5=train[13:16]
train_set5=train[0:13]+train[16:28]


# In[9]:


#train_set2


# In[10]:


train_set=[train_set1,train_set2,train_set3,train_set4,train_set5]
dev_set=[dev_set1,dev_set2,dev_set3,dev_set4,dev_set5]


# In[11]:


d1=dict()
d2=dict()
d3=dict()
d4=dict()
d5=dict()
d=[d1,d2,d3,d4,d5]


# In[ ]:


ra=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]
for i in range(5):
    train=create_token(train_set[i])
    dev=create_token(dev_set[i])
    
    dev1=find_trigrams(dev)
    word_count = Counter(train)
    bi=Counter(nltk.ngrams(train,2))
    tri=Counter(nltk.ngrams(train,3))
    utoken=set(train)
    tokenl=len(utoken)
    length=len(train)
    vocab=len(utoken)
    tint=dict()
    for a1 in ra:
        for a2 in ra:
            for a3 in ra:
                if a1+a2+a3==1:
                    tint=dict()
                    for x in utoken:
                        for y in utoken:
                            if x!=y:
                                for z in utoken:
                                    if x!=z and y!=z:
                                        if tri.get((x,y,z))==None:
                                            tc=0
                                        else :
                                            tc=tri.get((x,y,z))/bi.get((x,y))
                                        if bi.get((y,z))==None:
                                            bc=0
                                        else :
                                            bc=bi.get((y,z))/word_count.get(y)
                                        if word_count.get(z)==None:
                                            uc=0
                                        else :
                                            uc=word_count.get(z)/length

                                        tint[x,y,z]=a1*tc+a2*bc+a3*uc
                d[i][(a1,a2,a3)]=compper(tint,dev1,tokenl)       


# In[ ]:


df=pd.DataFrame()
df["lambda"]=d1.keys()
df["1st"]=d1.values()
df["2st"]=d2.values()
df["3st"]=d3.values()
df["4st"]=d4.values()
df["5st"]=d5.values()


# In[ ]:


df.head()


# In[ ]:


df.tail()


# In[ ]:


res=[]
for i in range(5):
    res.append(df.loc[df[df.columns[i+1]].argmin()]["lambda"])


# In[ ]:


res


# In[ ]:


l1=[]
l2=[]
l3=[]
for jj in res:
    l1.append(jj[0])
    l2.append(jj[1])
    l3.append(jj[2])
    


# In[ ]:


df2=pd.DataFrame()
df2["lambda1"]=l1
df2["lambda2"]=l2
df2["lambda3"]=l3


# In[ ]:


df2


# In[ ]:


df2.to_csv("c.csv")


# In[ ]:


df.to_csv("a.csv")


# In[ ]:




