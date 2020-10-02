#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[2]:


resources = pd.read_csv('../input/resources.csv')
resources.columns


# In[3]:


resources.head()


# In[4]:


train = pd.read_csv('../input/train.csv')
train.columns


# In[5]:


train.head()


# In[6]:


#train.project_essay_1[0]
train.project_resource_summary[0]


# In[7]:


## Dealing with all categorical data
import numpy as np
#array(train.teacher_prefix)
print("Teacher_Prefix : ", np.unique(train["teacher_prefix"].tolist()))
print("project_grade_category : ", np.unique(train["project_grade_category"].tolist()))
#print("project_subject_categories : ", np.unique(train["project_subject_categories"].tolist()))
print("project_subject_subcategories : ", np.unique(train["project_subject_subcategories"].tolist()))
#print("teacher_number_of_previously_posted_projects : ", np.unique(train["teacher_number_of_previously_posted_projects"].tolist()))
#print("Resoures quantity : ", np.unique(resources["quantity"].tolist()))
#print("Resoures price : ", np.unique(resources["price"].tolist()))


# In[8]:


train["teacher_number_of_previously_posted_projects"].hist(bins=1000)
tppp_mean = train['teacher_number_of_previously_posted_projects'].mean()
tppp_min = train['teacher_number_of_previously_posted_projects'].min()
tppp_max = train['teacher_number_of_previously_posted_projects'].max()
tppp_mean, tppp_min, tppp_max


# In[9]:


resources["quantity"].hist(bins=1000)
q_mean = resources["quantity"].mean()
q_min = resources["quantity"].min()
q_max = resources["quantity"].max()
q_mean, q_min, q_max


# In[10]:


resources["price"].hist(bins=1000)
p_mean = resources["price"].mean()
p_min = resources["price"].min()
p_max = resources["price"].max()
p_mean, p_min, p_max


# In[11]:


"""
Note to self
The process that could be applied in this case is as followed:
First
1) Apply LDA topic modelling on title and essay part 
(Note that the essay part will need to be distinguish befpre and after the time when question was changed)
2) Categorize the topic into ten group and use them as features
3) Apply Random Forest or Gradient Boost to the all features

Second
1) Limit essay text to 300 words
2) Apply CNN for essays part
3-1) Taie the result as a feature for Random Forest model or XG boost
3-2) Use the result from CNN as a predictor itself

Third
Combine result from Random Forest and LSTM Neuro Net to get the concensus

Features to be used
'teacher_prefix' - categorical
'school_state' - categorical
'project_grade_category' - categorical
'project_subject_categories' - categorical
'project_subject_subcategories' - categorical (break down into left or right brain or else)
'teacher_number_of_previously_posted_projects' - Numerical
'price' - numerical
'quantity' - numerical

Apply LDA topic modeling or LSTM NN later ('project_title', 'project_essay_1', 'project_essay_2','project_essay_3', 'project_essay_4', 'project_resource_summary')

"""


# In[ ]:


# second run without states
# test_df_final.iloc[np.where(result==0)]


# In[ ]:


# second run without states
# test_df_final.iloc[np.where(result==1)]


# In[26]:


# Feature Engineering
# teacher_prefix
train_df = pd.DataFrame()
train_df['id'] = train['id']
train_df['project_is_approved'] = train['project_is_approved']
train_df['is_teacher_prefix_Dr'] = train['teacher_prefix'].apply(lambda x: 1 if 'Dr.' == x else 0)
train_df['is_teacher_prefix_Normal'] = train['teacher_prefix'].apply(lambda x: 1 if x in ('Mrs.','Ms.','Mr.') else 0)
train_df['is_teacher_prefix_Other'] = train['teacher_prefix'].apply(lambda x: 0 if x in ('Dr.','Mrs.','Ms.','Mr.') else 1)
#for state in np.unique(train["school_state"].tolist()):
#    train_df['school_state_{0}'.format(state)] = train['school_state'].apply(lambda x: 1 if state == x else 0)
for grade in np.unique(train["project_grade_category"].tolist()):
    train_df['project_grade_category_{0}'.format(grade)] = train['project_grade_category'].apply(lambda x: 1 if grade == x else 0)
categories = ['Applied Learning', 'Math & Science', 'Music & The Arts', 'History & Civics', 'Warmth, Care & Hunger', 'Literacy & Language','Special Needs']
for category in categories:
    train_df['project_subject_categories_{0}'.format(category)] = train['project_subject_categories'].apply(lambda x: 1 if category in x else 0)
train_df['teacher_number_of_previously_posted_projects'] = train['teacher_number_of_previously_posted_projects']
train_df.columns


# In[37]:


train_resources = train_df.set_index('id').join(resources.set_index('id'))
price_quantity = train_resources.groupby(['id'])[["price", "quantity"]].sum()
price_quantity['total'] = price_quantity["price"] * price_quantity["quantity"]
X = train_df.set_index('id').join(price_quantity)
y = X['project_is_approved']
# remove unneccesary columns
X.drop(['project_is_approved','price','quantity'], axis=1, inplace=True)
X.columns


# In[28]:


# Feature Engineering
# teacher_prefix
test_df = pd.DataFrame()
test_df['id'] = test['id']
test_df['is_teacher_prefix_Dr'] = test['teacher_prefix'].apply(lambda x: 1 if 'Dr.' == x else 0)
test_df['is_teacher_prefix_Normal'] = test['teacher_prefix'].apply(lambda x: 1 if x in ('Mrs.','Ms.','Mr.') else 0)
test_df['is_teacher_prefix_Other'] = test['teacher_prefix'].apply(lambda x: 0 if x in ('Dr.','Mrs.','Ms.','Mr.') else 1)
#for state in np.unique(test["school_state"].tolist()):
#    test_df['school_state_{0}'.format(state)] = test['school_state'].apply(lambda x: 1 if state == x else 0)
for grade in np.unique(test["project_grade_category"].tolist()):
    test_df['project_grade_category_{0}'.format(grade)] = test['project_grade_category'].apply(lambda x: 1 if grade == x else 0)
categories = ['Applied Learning', 'Math & Science', 'Music & The Arts', 'History & Civics', 'Warmth, Care & Hunger', 'Literacy & Language','Special Needs']
for category in categories:
    test_df['project_subject_categories_{0}'.format(category)] = test['project_subject_categories'].apply(lambda x: 1 if category in x else 0)
test_df['teacher_number_of_previously_posted_projects'] = test['teacher_number_of_previously_posted_projects']
test_df.columns


# In[38]:


test_resources = test_df.set_index('id').join(resources.set_index('id'))
price_quantity_test = test_resources.groupby(['id'])[["price", "quantity"]].sum()
price_quantity_test['total'] = price_quantity_test["price"] * price_quantity_test["quantity"]

test_df_final = test_df.set_index('id').join(price_quantity_test)
test_df_final.drop(['price','quantity'], axis=1, inplace=True)


# In[80]:


from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier()
clf.fit(X, y)


# In[81]:


result = clf.predict(test_df_final)
y.mean(), result.mean()


# In[82]:


result_prob2 = clf.predict_proba(test_df_final)


# In[83]:


with open('result.csv','w') as f:
    for i in range(0,len(result_prob2)):
        f.write(str(test_df_final.index[i])+","+str(result_prob2[i][1])+'\n')
        


# In[84]:


with open('result.csv','r') as f:
    test=f.readlines()
    print(test[1])


# In[85]:


test_df_final.iloc[np.where(result2==1)]


# In[86]:


test_df_final.iloc[np.where(result2==0)]


# In[ ]:




