#!/usr/bin/env python
# coding: utf-8

# **Thanks for viewing my Kernel! If you like my work, please leave an upvote! :) **

# In[ ]:


from IPython.display import Image
Image(filename="../input/telco-churn/telco_header.png")


# **Key Insights:**
# 
# * 45% of the users paying via electronic check churn
# * 43% of the users under month-to-month contract churn
# * 42% of the users with fiber optic internet churn
# * 42% of the users no online security churn
# * 42% of the users opting no for TechSupport churn
# * 42% of the senior citizen users churn
# * 40% of the users with no OnlineBackup churn
# * 39% of the users with no DeviceProtection churn
# * More the tenure is, lesser is the churn ratio
# * Higher the monthly charge is, higher the churn
# * Churned data points are concentrated in high monthly charges and low tenure. 
# * Not churned data points are concentrated in (1) low monthly charges & low tenure and (2) high monthly charges & high tenure.

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

import os
print(os.listdir("../input/"))


# In[ ]:


churn = pd.read_csv('../input/telco-customer-churn/WA_Fn-UseC_-Telco-Customer-Churn.csv')

print('Churn data: \nRows: {}\nCols: {}'.format(churn.shape[0],churn.shape[1]))
print(churn.columns)


# In[ ]:


churn.head()


# **11 missing values found in the dataset for TotalCharges attribute**
# 
# Total Charges has to be converted into numeric values before checking for null values. The missing values can be replaced by monthly charges multiplied by tenure. 

# In[ ]:


churn['TotalCharges'] = pd.to_numeric(churn['TotalCharges'], errors = 'coerce')

for x in churn.columns:
    if churn[x].isnull().values.ravel().sum() > 0:
        print('{} - {}'.format(x,churn[x].isnull().values.ravel().sum()))
        
churn['TotalCharges'].fillna(churn['tenure'] *  churn['MonthlyCharges'], inplace = True)


# **Data Visualizations**
# 
# * 45% of the users paying via electronic check churn
# * 43% of the users under month-to-month contract churn
# * 42% of the users with fiber optic internet churn
# * 42% of the users no online security churn
# * 42% of the users opting no for TechSupport churn
# * 42% of the senior citizen users churn
# * 40% of the users with no OnlineBackup churn
# * 39% of the users with no DeviceProtection churn

# In[ ]:


churn['SeniorCitizen'] = churn['SeniorCitizen'].apply(lambda x: "Senior" if x==1 else ("Non-Senior" if x==0 else x))

cols = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService', 
        'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 
        'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 
        'Contract', 'PaperlessBilling', 'PaymentMethod']

fig, ax = plt.subplots(4,4,figsize=(18,8), sharex=True)

j=0
k=0
    
for i in cols:
    temp = churn.pivot_table(churn, index=[i], columns=['Churn'], aggfunc=len).reset_index()[[i,'tenure']]
    temp.columns=[i,'Churn_N','Churn_Y']
    temp['Churn_ratio']=(temp['Churn_Y'])/(temp['Churn_Y']+temp['Churn_N'])
    
    a = sns.barplot(x='Churn_ratio', y=i, data=temp, ax=ax[j][k], color="palegreen")
    a.set_yticklabels(labels=temp[i])
    for p in ax[j][k].patches:
        ax[j][k].text(p.get_width() + .05, p.get_y() + p.get_height()/1.5, '{:,.1%}'.format(p.get_width()),
                   fontsize=8, color='black', ha='center', va='bottom')
    ax[j][k].set_xlabel('', size=8, color="green")
    ax[j][k].set_ylabel('', size=8, color="green", rotation=0, horizontalalignment='right')
    ax[j][k].set_title(i, size=10, color="green")
    #print(j,k)
    if k==3: 
        j=j+1
        k=0
    else:
        k=k+1 
    
fig.suptitle("Churn ratio across attributes", fontsize=14, family='sans-serif', color="green")
plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                    wspace=1, hspace=1)
plt.xlim(0,.5)
plt.show()


# In[ ]:


fig, ax = plt.subplots(figsize=(8,6))

sns.boxenplot(x="MonthlyCharges", y="gender", data=churn, color="palegreen", ax=ax)
        
ax.set_xlabel('Monthly Charges', size=12, color="green")
ax.set_ylabel('Gender', size=14, color="green")
ax.set_title('Tenure distribution', size=18, color="green")
plt.show()


# **More the tenure is, lesser is the churn ratio**

# In[ ]:


fig, ax = plt.subplots(2, 1, figsize=(8,6), sharey=True, sharex=True)

sns.distplot(churn[churn['Churn']=="Yes"]["tenure"] , color="#F5B7B1", ax=ax[0])
sns.distplot(churn[churn['Churn']=="No"]["tenure"] , color="#ABEBC6", ax=ax[1])
        
ax[0].set_xlabel('Churn - Yes', size=12, color="#800000")
ax[1].set_xlabel('Churn - No', size=12, color="green")
#ax.set_ylabel('Churn', size=14, color="green")
#ax[0].set_title('Tenure distribution', size=18, color="green")
fig.suptitle("Tenure distribution", fontsize=14)
plt.show()


# **Higher the monthly charge is, higher the churn**

# In[ ]:


fig, ax = plt.subplots(2, 1, figsize=(8,6), sharey=True, sharex=True)

sns.distplot(churn[churn['Churn']=="Yes"]["MonthlyCharges"] , color="#F5B7B1", ax=ax[0])
sns.distplot(churn[churn['Churn']=="No"]["MonthlyCharges"] , color="#ABEBC6", ax=ax[1])
        
ax[0].set_xlabel('Churn - Yes', size=12, color="#800000")
ax[1].set_xlabel('Churn - No', size=12, color="green")

fig.suptitle("Monthly Charges distribution", fontsize=14)
plt.show()


# **Distribution of total charges**

# In[ ]:


fig, ax = plt.subplots(2, 1, figsize=(8,6), sharey=True, sharex=True)

sns.distplot(churn[churn['Churn']=="Yes"]["TotalCharges"] , color="#F5B7B1", ax=ax[0])
sns.distplot(churn[churn['Churn']=="No"]["TotalCharges"] , color="#ABEBC6", ax=ax[1])
        
ax[0].set_xlabel('Churn - Yes', size=12, color="#800000")
ax[1].set_xlabel('Churn - No', size=12, color="green")

fig.suptitle("Total Charges distribution", fontsize=14)
plt.show()


# * Churned data points are concentrated in high monthly charges and low tenure. 
# * Not churned data points are concentrated in (1) low monthly charges & low tenure and (2) high monthly charges & high tenure.

# In[ ]:


a = sns.jointplot(x="tenure", y="MonthlyCharges", data=churn[churn['Churn']=='Yes'], kind="kde", color="#F5B7B1", height=5)
plt.title('Churn Yes')
b = sns.jointplot(x="tenure", y="MonthlyCharges", data=churn[churn['Churn']=='No'], kind="kde", color="#ABEBC6", height=5)
plt.title('Churn No')


# In[ ]:





# **More to come..**
