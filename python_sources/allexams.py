#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import glob
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns 
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    print(dirname)
    for filename in filenames:
        print(os.path.join(dirname, filename))
        

# Any results you write to the current directory are saved as output.


# In[ ]:


filepath1="/kaggle/input/quiz-1/quiz1.xlsx"
df_opinion1=pd.read_excel(filepath1,'py_opinion')
df_science1=pd.read_excel(filepath1,'py_science')
df_mind1=pd.read_excel(filepath1,'py_mind')
df_sense1=pd.read_excel(filepath1,'py_sense')
df_science1['Class'] = "py_science"
df_sense1['Class'] = "py_sense"
df_opinion1['Class'] = "py_opinion"
df_mind1['Class'] = "py_mind"
data_concat = pd.concat([df_opinion1,df_science1,df_mind1,df_sense1],axis=0,sort=False,)
data_concat1=pd.DataFrame(data_concat)
data_concat1.index=range(0,41,1)
#data_concat1.insert(loc=0,column="Exam1",value="Quiz1")

#data_concat1['isim'] = list(map(lambda x: x.split(), data_concat1['isim']))
#data_concat1['isim'] = list(map(lambda x: x[0], data_concat1['isim']))
data_concat1.rename(columns={'Unnamed: 0':'Name',"D":"True1","Y":"False1","B":"Empty1"},inplace=True)

data_concat1 = data_concat1[["Class","Name","True1","False1","Empty1"]]
data_concat1['Name'] = list(map(lambda x: x.lower(), data_concat1['Name']))
data_concat1.loc[data_concat1['True1'] == 'girmedi', ['True1']] = 0
data_concat1.set_index('Name',inplace=True)
print(data_concat1)


# In[ ]:


filepath2="/kaggle/input/quiz-2"
files=glob.glob(filepath2+'/*')
all_data = [pd.read_excel(f, sheet_name=None, ignore_index=True,sort=False,index_col=0) for f in files ]
all_class = pd.DataFrame(columns=("Name", "True2", "False2", "Empty2"), index=None)
for i in range(len(files)):   
    class_names=['py_sense','py_mind','py_science','py_opinion']
    names=list(all_data[i].keys())    
    for j in all_data[i]:    
        true=all_data[i][j]["ogr.C"][20]
        false=all_data[i][j]["ogr.C"][21]
        blank=all_data[i][j]["ogr.C"][22]
        #DYB=list(all_data[i][j]["ogr.C"][:20])        
        student = {'Name': names[names.index(j)],'True2': true, 'False2': false, "Empty2": blank}
        all_class = all_class.append(student, ignore_index=True)
        all_class1=pd.DataFrame(all_class)
    #total_examers+=(names.index(j))+1       
all_class1['Name'] = list(map(lambda x: x.lower(), all_class1['Name']))
#all_class1.insert(loc=0,column="Exam2",value="Quiz2")
all_class1.set_index('Name',inplace=True)
print(all_class1.index)
#print("Total examers:",total_examers)
#'Class': class_names[i], 


# In[ ]:


filepath3="/kaggle/input/quiz-3/quiz-3.xlsx"
dataframe_3=pd.read_excel(filepath3)
dataframe_3=dataframe_3.iloc[1:,1:6]
#dataframe_3.insert(loc=0,column="Exam3",value="Quiz3")
dataframe_3.rename(columns={"name":"Name","true":"True3","false":"False3","empty":"Empty3"},inplace=True)
#dataframe_3.loc[dataframe_3['Class'] == 'sense', ['Class']] = 'py_sense'
#dataframe_3.loc[dataframe_3['Class'] == 'opinion', ['Class']] = 'py_opinion'
#dataframe_3.loc[dataframe_3['Class'] == 'mind', ['Class']] = 'py_mind'
#dataframe_3.loc[dataframe_3['Class'] == 'science', ['Class']] = 'py_science'
dataframe_3['Name'] = list(map(lambda x: x.lower(), dataframe_3['Name']))
dataframe_3.drop('class', axis=1, inplace=True)
dataframe_3.set_index('Name',inplace=True)
print(dataframe_3.index)


# In[ ]:


filepath4="/kaggle/input/quiz-4/quiz4.xlsx"
dataframe_4=pd.read_excel(filepath4)
dataframe_4=dataframe_4.iloc[:,:]
columns = ['1.','2.','3.','4.','5.','6.','7.', ]
dataframe_4.drop(columns, inplace=True, axis=1)
#dataframe_4.insert(loc=3,column='True',value=dataframe_4["total"])
#dataframe_4.insert(loc=0,column="Exam4",value="Quiz4")
dataframe_4.insert(loc=1,column="False4",value="0")
dataframe_4.insert(loc=2,column="Empty4",value="0")
dataframe_4.rename(columns={"isim":"Name","total":"True4"},inplace=True)
dataframe_4 = dataframe_4[["Name","True4","False4","Empty4"]]
dataframe_4['Name'] = list(map(lambda x: x.lower(), dataframe_4['Name']))
dataframe_4.set_index('Name',inplace=True)
print(dataframe_4)


# In[ ]:



result1 = pd.merge(data_concat1, all_class1, how='left', on='Name')
result2 = pd.merge(dataframe_3,dataframe_4, how='left',on='Name')
#result3 = pd.merge(dataframe_4,result2, how='left',on='Name')
#result3 = pd.merge(result1,result2,how='left',on='Name')
print(result1)
print(result2)


# In[ ]:


result1.info()


# In[ ]:


result1[['True1']] = result1[['True1']].astype('float')
result1[['True2']] = result1[['True2']].astype('float')
result1[['False2']] = result1[['False2']].astype('float')
result1[['Empty2']] = result1[['Empty2']].astype('float')


# In[ ]:


result2.info()


# In[ ]:


print(result1.corr())
print(result2.corr())


# In[ ]:


f,ax = plt.subplots(figsize=(8, 8))
sns.heatmap(result1.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)
plt.show()
f,ax = plt.subplots(figsize=(8, 8))
sns.heatmap(result2.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)
plt.show()


# In[ ]:


result1.True1.plot(kind = 'line', color = 'g',label = 'True1',linewidth=1,alpha = 0.5,grid = True,linestyle = ':')
result2.True3.plot(color = 'r',label = 'True3',linewidth=1, alpha = 0.5,grid = True,linestyle = '-.')
plt.legend(loc='upper right')     # legend = puts label into plot
plt.xlabel('x axis')              # label = name of label
plt.ylabel('y axis')
plt.title('Line Plot')            # title = title of plot
plt.show()


# In[ ]:


result2.plot(kind='scatter', x='True3', y='True4',alpha = 0.5,color = 'red')
plt.xlabel('True3')              # label = name of label
plt.ylabel('True4')
plt.title('True3 True4 Scatter Plot')            # title = title of plot
plt.show()


# In[ ]:


result2.True4.plot(kind = 'hist',bins = 5,range = (0,20), figsize = (7,7))
plt.show()


# In[ ]:


dataframe1_2 = pd.DataFrame(columns=("Exam","Class", "Name", "True", "False", "Empty"))

#dataframe1_2=dataframe1_2.append(all_class1,ignore_index=True)
dataframe1_2=dataframe1_2.append(data_concat1,ignore_index=True)
dataframe1_2=dataframe1_2.append(all_class1,ignore_index=True)
dataframe1_2=dataframe1_2.append(dataframe_3,ignore_index=True)
dataframe1_2=dataframe1_2.append(dataframe_4,ignore_index=True)
#dataframe1_2.loc[dataframe1_2['True'] == 'NaN', ['True']] = 0
dataframe1_2.replace(np.nan, 0, inplace=True)

print(dataframe1_2)


# In[ ]:





# In[ ]:


exam1 = dataframe1_2[dataframe1_2["Exam"]=="Quiz1"]
exam2 = dataframe1_2[dataframe1_2["Exam"]=="Quiz2"]
exam3 = dataframe1_2[dataframe1_2["Exam"]=="Quiz3"]
exam4 = dataframe1_2[dataframe1_2["Exam"]=="Quiz4"]
exam1_1st = exam3.sort_values(by="True", ascending=False).tail(3)
exam1_1st


# In[ ]:


exam3_mind= exam3[exam3["Class"] == "py_mind"]
exam3_mind["True"].mean()


# In[ ]:


dataframe1_2["True"].mean()


# In[ ]:





# In[ ]:





# In[ ]:


for i in all_class1['Name']:
        for j in data_concat1['Name'] :
            if i == j :
                q1true = all_class1[all_class1['Name'].str.contains(i)]
                print(q1true)
               


# In[ ]:


all_true = all_class1["True"]
all_false = all_class1["False"]
all_empty = all_class1["Empty"]
#print("dogru sayilari =", sum(all_true), "Yanlis sayilari =", sum(all_false), "Bos sayilari = ", sum(all_empty))
#soru = 3 tum siniflarin Dogru yanlis bos ortalamalari
print("All Classes:\nD Average =",all_true.mean(),"\nY Average = ", all_false.mean(), "\nB Average =", all_empty.mean())
#%%


# In[ ]:


#%%
c_mind = all_class1['True2'][:10]
c_mind_ort=sum(c_mind)/10
print("\npy_mind average:",c_mind_ort)
c_opinion = all_class1['True2'][10:20]
c_opinion_ort=sum(c_opinion)/10
print("py_opinion average:",c_opinion_ort)
c_science = all_class1['True2'][20:28]
c_science_ort=sum(c_science)/10
print("py_science average:",c_science_ort)
c_sense = all_class1['True2'][28:38]
c_sense_ort=sum(c_sense)/10
print("py_sense average:",c_sense_ort)


# In[ ]:


#%%
all_1st3= all_class1.sort_values(by='True2', ascending=False).head(3)
print("Most succesfull 3 students:\n",all_1st3)


# In[ ]:


#%%
c_mind = all_class1[all_class["Class"]=="py_mind"]
print("py_mind most succesfull:",c_mind.sort_values(by='True', ascending=False).head(1))
c_opinion = all_class1[all_class["Class"]=="py_opinion"]
print("py_opinion most succesfull:",c_opinion.sort_values(by='True', ascending=False).head(1))
c_science = all_class1[all_class["Class"]=="py_science"]
print("py_science most succesfull:",c_science.sort_values(by='True', ascending=False).head(1))
c_sense = all_class1[all_class["Class"]=="py_sense"]
print("py_sense most succesfull:",c_sense.sort_values(by='True', ascending=False).head(1))


# In[ ]:


all_class1['Name'] = list(map(lambda x: x.split(), all_class1['Name']))
all_class1['Name'] = list(map(lambda x: x[0], all_class1['Name']))
print(all_class1)

name=all_class1['Name'][0]
for i in all_class1.iloc[:,1]:
        if name == i:
            print(name)


# In[ ]:




