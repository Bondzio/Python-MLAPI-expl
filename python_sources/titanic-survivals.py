#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
get_ipython().run_line_magic('matplotlib', 'inline')


from sklearn.preprocessing import LabelEncoder,StandardScaler


# In[ ]:


data=pd.read_csv('/kaggle/input/titanic/train.csv')


# In[ ]:


data.head()


# In[ ]:


data.info()


# In[ ]:


mode=data['Age'].mode()[0]
data['Age']=data['Age'].fillna(mode)
any(data['Age'].isnull())


# In[ ]:


mode=data['Embarked'].mode()[0]
data['Embarked']=data['Embarked'].fillna(mode)
any(data['Embarked'].isnull())


# In[ ]:


label=LabelEncoder()
data['Embarked']=label.fit_transform(data['Embarked']) # 0:C 1: 2:S
data['Sex']=label.fit_transform(data['Sex']) # 1: male 0: female


# In[ ]:


data.head(10)


# In[ ]:


corr_matrix=data.corr()

f, ax = plt.subplots(figsize=(11, 15))

heatmap = sb.heatmap(corr_matrix,
                      mask = np.triu(corr_matrix),
                      square = True,
                      linewidths = .5,
                      cmap ='coolwarm', 
                      cbar_kws = {'shrink': .4,'ticks' : [-1, -.5, 0, 0.5, 1]},
                      vmin = -1,
                      vmax = 1,
                      annot = True,
                      annot_kws = {"size": 12})

#add the column names as labels
ax.set_yticklabels(corr_matrix.columns, rotation = 0)
ax.set_xticklabels(corr_matrix.columns)

sb.set_style({'xtick.bottom': True}, {'ytick.left': True})


# In[ ]:


plt.figure(figsize=(15,15))
sb.scatterplot(data=data, x='Fare', y='Pclass', hue='Sex',style='Survived',size='Age',style_order=[1,0])


# In[ ]:


data.columns


# In[ ]:


from sklearn.linear_model import LogisticRegression


# In[ ]:


model=LogisticRegression()
model.fit(data[['Pclass','Age','Sex','Fare','Parch','Embarked']],data[['Survived']])


# In[ ]:


test_data=pd.read_csv('/kaggle/input/titanic/test.csv')


# In[ ]:


mode=test_data['Age'].mode()[0]
test_data['Age']=test_data['Age'].fillna(mode)
mode=test_data['Embarked'].mode()[0]
test_data['Embarked']=test_data['Embarked'].fillna(mode)
label=LabelEncoder()
test_data['Embarked']=label.fit_transform(test_data['Embarked']) # 0:C 1: 2:S
test_data['Sex']=label.fit_transform(test_data['Sex']) # 1: male 0: female
test_data['Fare']=test_data['Fare'].fillna(test_data['Fare'].mean())


# In[ ]:


test_data[['Fare','Sex']].tail()


# In[ ]:


any(test_data['Fare'].isnull())


# In[ ]:


prediction=pd.DataFrame(model.predict(test_data[['Pclass','Age','Sex','Fare','Parch','Embarked']]))
prediction.columns=['Survived']
prediction.head()


# In[ ]:


res=pd.read_csv('/kaggle/input/titanic/gender_submission.csv')


# In[ ]:


res.head()


# In[ ]:


test_data.head()


# In[ ]:


final=pd.concat([test_data[['PassengerId']],prediction],axis=1)


# In[ ]:


final.head()


# In[ ]:


compression_opts = dict(method='zip',
                        archive_name='Submisson.csv')  
final.to_csv('Submisson.zip', index=False,
          compression=compression_opts)  

