#!/usr/bin/env python
# coding: utf-8

# ## Broadband Customers Churned Analysis
# This NoteBook is created for the pridiction that custumer of broadband service provider is churned or not**

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


# this code show more than one output in one cell
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


# In[ ]:


# import libraries
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# reading data in bbs_cust_base dataframe variable
bbs_cust_base = pd.read_csv('/kaggle/input/broadband-customers-base-churn-analysis/bbs_cust_base_scfy_20200210.csv')
bbs_cust_base.head(10)


# # Assumption
# as per the value of ce_expiry column this data set is taking current month, Jan 2020. We also use Jan 2020 as current month

# In[ ]:


print('bbs_cust_base dataframe has {} rows and {} columns'.format(bbs_cust_base.shape[0],bbs_cust_base.shape[1]))


# In[ ]:


# computer memory used by dataframe in bytes
used_pc_memory = bbs_cust_base.memory_usage(deep=True).sum()
used_pc_memory = used_pc_memory/(1000*1000)
print('bbs_cust_base data frame is using {0:.2f} MB computer memory'.format(used_pc_memory))


# In[ ]:


# data set description
bbs_cust_base.describe(include='all')


# 1. column name Unnamed: 19 has only 1 unique value in only 2 rows.
# 2. if we consider column newacct_no as unique id than we can say that company has dealed 510125 times with his 27605 customers.

# In[ ]:


# removing Unnamed: 19 column

# It shows the values of not null unnamed: 19 rows
bbs_cust_base[bbs_cust_base['Unnamed: 19'].notnull()]

# no use of Unnamed: 19 column so drop it
bbs_cust_base.drop('Unnamed: 19',axis=1,inplace=True)


# In[ ]:


# removing duplicate rows
bbs_cust_base.drop_duplicates(inplace=True)
bbs_cust_base.shape


# In[ ]:


# creating column name's list
col = bbs_cust_base.columns.to_list()

# printing number of unique values in each column.
bbs_cust_base.nunique()


# In[ ]:


# creating catagorical columns name list
catcol = [_ for _ in col if bbs_cust_base[_].nunique() < 30]

# printing all the unique values of categorical colum
for _ in catcol:
    print('{} has {} unique value/s - {}\n'.format(_,bbs_cust_base[_].nunique(),bbs_cust_base[_].unique())) 


# In[ ]:


# column name term_reas_code contains name of code that have the discription in column term_reas_desc
# creating a list of unique values of both column

termination_reasion_code = bbs_cust_base.term_reas_code.unique()
termination_reasion_code_description = bbs_cust_base.term_reas_desc.unique()

# creating a dictionary for termination reasion code and description
termination_reasion = dict(zip(termination_reasion_code,termination_reasion_code_description))

termination_reasion


# In[ ]:


# droping of no more usefule columns
# every customer is billed monthly so bill_cycl column is not useful
# serv_type for each customer is BBS only one type of service so it is also not usefull
# both term_reas_desc column and term_reas_code have same meaning
# service_code column is also not useful for us
bbs_cust_base.drop(columns=['bill_cycl','serv_type','term_reas_desc','serv_code'],inplace=True)


# # handling missing values

# In[ ]:


# checking the null or missing values in dataframe
plt.figure(figsize=(10,10))
sns.heatmap(data=bbs_cust_base.isna(),yticklabels=False,cbar=False,cmap='Set3')
plt.show()

# columns information
bbs_cust_base.info()


# <h6/>columns effc_strt_date, effc_end_date, contract_month and ce_expiry have less missing values. On other hand columns term_reas_code and term_reas_desc have too much missing values.<h6/>

# In[ ]:


# rows of data frame have missng values in effc_strt_date column
bbs_cust_base[bbs_cust_base['effc_strt_date'].isnull()].head()

# shape of null value data frame
print('size of null data frame is ',bbs_cust_base[bbs_cust_base['effc_strt_date'].isnull()].shape)

# total number of unique customers in null dataframe
print('total unique newacct_no is ',bbs_cust_base[bbs_cust_base['effc_strt_date'].isnull()].newacct_no.nunique())

# churned customer in this null data set
bbs_cust_base[bbs_cust_base['effc_strt_date'].isnull()].churn.value_counts()


# # conclusion
# 1. we have total 510125 rows in our original data set out of this only 1937 rows have missing values.
# 2. these all missing values belong to only 200 unique id out of 27605 total unique id
# 3. only 19 unique id have been churned at yet from this null data set
# <h4/>On the basis of above three conclusion we can say that all these rows do not have any valuable counts So we can drope them from our data set<h4/>

# In[ ]:


# drop null values of eff_strt_date column
bbs_cust_base.dropna(subset=['effc_strt_date'],inplace=True)

# let's see data after removing all null value other than column name term_reas_code
plt.figure(figsize=(10,10))
sns.heatmap(data=bbs_cust_base.isna(),yticklabels=False,cbar=False,cmap='Set3')
plt.show()


# # changing dtype of columns

# In[ ]:


# complaint_cnt column contains word ' customer/ user pass away'. we replace this word by 0 complaint.
# complaint_cnt has mixed dtype (integer and string)
# first we change integer in string, than replace words we want and than again change dtype to integer
bbs_cust_base['complaint_cnt'] = bbs_cust_base.complaint_cnt.astype('str')
bbs_cust_base['complaint_cnt'] = bbs_cust_base.complaint_cnt.str.replace(' customer/ user pass away','0')
bbs_cust_base['complaint_cnt'] = bbs_cust_base.complaint_cnt.astype('int')


# In[ ]:


# replace Y by 1 and N by 0 in columns - with_phone_service, churn and current_mth_churn
# and converting their dtype to int32
bbs_cust_base['with_phone_service'] = (bbs_cust_base.with_phone_service == 'Y').astype('int32')
bbs_cust_base['churn'] = (bbs_cust_base.churn == 'Y').astype('int32')
bbs_cust_base['current_mth_churn'] = (bbs_cust_base.current_mth_churn == 'Y').astype('int32')


# In[ ]:


# changing the data type from string/int64 to int32

bbs_cust_base[['contract_month','ce_expiry','secured_revenue']] = bbs_cust_base[['contract_month','ce_expiry','secured_revenue']].astype('int')
bbs_cust_base[['image','tenure']] = bbs_cust_base[['image','tenure']].astype('int32')


# In[ ]:


# changing effc_strt_date and effc_end_date column in datetime formate

bbs_cust_base['effc_strt_date'] = pd.to_datetime(bbs_cust_base['effc_strt_date'],dayfirst=True)
bbs_cust_base['effc_end_date'] = bbs_cust_base.effc_end_date.astype('datetime64[ns]')


# # finding the feature columns

# In[ ]:


# counting of service termination reason
plt.figure(figsize=(15,10))
sns.set_style('whitegrid')
plt.title('service termination reasion counting')
sns.countplot(x='term_reas_code',data=bbs_cust_base,hue='churn')
plt.xticks(rotation=45)
plt.show()


# This graph show that if customer has reason to churned than they do so. only some customers with reason cutting cost do not break service contract. 

# In[ ]:


# we devide term_reas in 4 category.
# 1 for reason in not in control of service provider
# 2 user issue of cost 
# 3 service problem
# 0 for NaN

def term_reasencoder(a):
    if a in ('REV','CLB','NU','OT','CUSN2','CUSB0','MGR'):
        return 1
    elif a in ('NET','UFSS','COVL3','COM15','COVL2','UCSH','LOSF','COVL1','COM10','UEMS','NWQU','NCAP'):
        return 3
    elif a in ('CUCO','OT','TRM','EXP','BILP','EXI','PLR'):
        return 2
    else:
        return 0

bbs_cust_base['term_reas_code'] = bbs_cust_base.term_reas_code.map(term_reasencoder)
bbs_cust_base['term_reas_code'] = bbs_cust_base.term_reas_code.astype('int32')


# In[ ]:


def bandwidthencoder(a):
    if a in ('30M', '10M','BELOW 10M', '50M'):
        return 0
    if a in ('100M','100M (FTTO)'):
        return 1
    if a in ('300M (FTTO)', '1000M (FTTO)', '500M (FTTO)'):
        return 2

bbs_cust_base['bandwidth'] = bbs_cust_base.bandwidth.map(bandwidthencoder)
bbs_cust_base['bandwidth'] = bbs_cust_base.bandwidth.astype('int32')


# In[ ]:


# # creating new feature of month and year from effc_strt and effc_end
# bbs_cust_base = bbs_cust_base.assign(start_month = bbs_cust_base.effc_strt_date.dt.month,
#                                     start_year = bbs_cust_base.effc_strt_date.dt.year,
#                                     end_month = bbs_cust_base.effc_end_date.dt.month,
#                                     end_year = bbs_cust_base.effc_end_date.dt.year)


# In[ ]:


# newacct_no is unique id we set it to index of our dataset
bbs_cust_base.set_index(keys='newacct_no',inplace = True)
bbs_cust_base.head()


# In[ ]:


# kdeplot of tenure
plt.figure(figsize=(8,8))
sns.kdeplot(bbs_cust_base[bbs_cust_base.churn == 1].tenure,label='Churn')
sns.kdeplot(bbs_cust_base[bbs_cust_base.churn == 0].tenure,label='Not Churn')


# In[ ]:


# distribution of tenure column
plt.figure(figsize=(8,8))
sns.distplot(bbs_cust_base[bbs_cust_base.churn == 1].tenure,label='Churn',kde=False)
sns.distplot(bbs_cust_base[bbs_cust_base.churn == 0].tenure,label='Not Churn',kde=False)
plt.legend()


# # Selecting features

# In[ ]:


# we creating new dataframe called broadband_ with some of useful features
broadband_ = bbs_cust_base[['contract_month','ce_expiry','secured_revenue','bandwidth','complaint_cnt','with_phone_service']]

# creating new feature of month and year from effc_strt and effc_end
broadband_['start_month'] = bbs_cust_base.effc_strt_date.dt.month
broadband_['start_year'] = bbs_cust_base.effc_strt_date.dt.year
broadband_['end_month'] = bbs_cust_base.effc_end_date.dt.month
broadband_['end_year'] = bbs_cust_base.effc_end_date.dt.year


# In[ ]:


# As we know in this data set there are many rows for same unique customer id. 
# these rows have different tenure period depends on billing month
# we replace this tenure period with the maximum tenure of the customer with company

broadband_['tenure'] = bbs_cust_base.groupby('newacct_no').tenure.max()


# In[ ]:


# encoding for churn column - 0 if customer is not churn, 1 if customer is already churn but not in this month and 2 if customer churm in current mont
# by adding churn and current_mth_churn columns values
broadband_['churn'] = bbs_cust_base.churn + bbs_cust_base.current_mth_churn


# In[ ]:


# view top 5 rows of new dataframe less with feature called broadband_
broadband_.head()

# shape of the broadband_
broadband_.shape


# In[ ]:


# removing duplicate from the dataframe
broadband_ = broadband_.drop_duplicates()

# size of dataframe after removing duplicates
broadband_.shape


# In[ ]:


# pearsion vlaues of broadband_'s columns with one another
plt.figure(figsize=(15,15))
sns.heatmap(broadband_.corr(),annot=True,cbar=False)
plt.show()


# # model building and testing

# In this classification problem we create and test most of the models and than compare with their score to find best sutiable model. we use following models of sklearn
# 1. Logictic Regression
# 2. Decision Tree 
# 3. Random forest
# 4. Naive Byes 
# 5. KNN model 

# In[ ]:


# selecting churn column as traget column and rest features as indepandet variable
y = broadband_['churn']
x = broadband_.drop(['churn'],axis=1)


# In[ ]:


# train test split
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test =  train_test_split(x,y,test_size=0.25,random_state=42)


# In[ ]:


# we define 2 list that one of them save results of models other list save name of model
labelList = []
resultList = []


# In[ ]:


# Logictic Regression with sklearn
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(random_state=1)
lr.fit(x_train,y_train)
lr_prediction = lr.predict(x_test)
print("test accuracy {}".format(lr.score(x_test,y_test)))

# adding result and label to lists
labelList.append("Log_Rec")
resultList.append(lr.score(x_test,y_test))


# In[ ]:


# Decision Tree 
from sklearn.tree import DecisionTreeClassifier
dt = DecisionTreeClassifier(random_state=1)
dt.fit(x_train,y_train)
dt_prediction = dt.predict(x_test)
print("decison tree score : ",dt.score(x_test,y_test))

# adding result and label to lists
labelList.append("Dec_Tree")
resultList.append(dt.score(x_test,y_test))


# In[ ]:


# Random forest
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=100,random_state = 1)
rf.fit(x_train, y_train)
rf_prediction = rf.predict(x_test)
print("Random forest algor. result: ",rf.score(x_test,y_test))

# adding result and label to lists
labelList.append("Rand_For")
resultList.append(rf.score(x_test,y_test))


# In[ ]:


# Naive Byes 
from sklearn.naive_bayes import GaussianNB
nb = GaussianNB()
nb.fit(x_train,y_train)
nb_prediction = nb.predict(x_test)
print("print accuracy of naive bayes algo: ",nb.score(x_test,y_test))

# adding result and label to lists
labelList.append("Naive_Byes")
resultList.append(nb.score(x_test,y_test))


# In[ ]:


# KNN model
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=3) #n_neighbors = k
knn.fit(x_train,y_train)
knn_prediction = knn.predict(x_test)

# score
print(" {} nn score: {} ".format(3,knn.score(x_test,y_test)))


# In[ ]:


# Finding optimum k value between 1 and 15
score_list = []
for each in range(1,15):
    knn2 = KNeighborsClassifier(n_neighbors = each) # create a new knn model
    knn2.fit(x_train,y_train)
    knn2_prediction = knn2.predict(x_test)
    score_list.append(knn2.score(x_test,y_test))

plt.plot(range(1,15),score_list) # x axis is in interval of 1 and 15
plt.xlabel("k values")
plt.ylabel("accuracy")
plt.show()

# finding max value in a list and it's index.
a = max(score_list) # finding max value in list
b = score_list.index(a)+1 # index of max value.

print("k = ",b," and maximum value is ", a)

# adding result and label to lists
labelList.append("KNN")
resultList.append(a)


# In[ ]:


# First of all we combine 2 lists (labelList and resultList) by using zip method
zipped = zip(labelList, resultList)
zipped = list(zipped)

df = pd.DataFrame(zipped, columns=['label','result'])
df

# Viewing this df table in form of graph
new_index = (df['result'].sort_values(ascending=False)).index.values 
sorted_data = df.reindex(new_index)

plt.plot(sorted_data.loc[:,"label"],sorted_data.loc[:,"result"])
plt.show()


# # conclusion
# 
# <h1/>Above Table and Graph shows that RandomForest is best suitable model for this dataset to find the churn customer.<h1/>

# # Question 1
# 
# <h3/> Total customers actually churned in last 6 months<h3/>

# To find the answer we check two conditions
# 1. is customer churned or not by churn > 0
# 2. ce_expiry value is in range of -6 to 0
# 3. NOTE - We count newacct_no which is unique, only one time even it is apper in data set more than one time

# In[ ]:


bbs_cust_base[(bbs_cust_base.ce_expiry >= -6) & (bbs_cust_base.ce_expiry <= 0)  & (bbs_cust_base.churn == 1)].index.nunique()


# Anwer - After removing the duplicate rows from data set we can say that Total 971 customer actually churned in last 6 months (on the basis of newacct_no which is unique for each customer)

# # Question 2
# 
# <h3/>Total customers predicted as churned by model<h3/>

# In[ ]:


# confusion matrix of randomforest model
from sklearn.metrics import confusion_matrix
rf_cf_matrix = confusion_matrix(y_test,rf_prediction,labels=[0,1,2])

# heatmap to see confusion metrix
sns.heatmap(rf_cf_matrix,cbar=False,annot=True,cmap='coolwarm_r',fmt='')
plt.xlabel('Original')
plt.ylabel('Predict')


# Answer - Total customer predicted churn with value 1 is 83 + 1390 + 827 = 2300 and with value 2 is 27 + 707 + 489 = 1223

# # Question 3
# 
# <h3/>Total no. Of  matched customers from actual vs predicted<h3/>

# In[ ]:


# actual vs predicted is the score of confusion matrix
df.loc[2,:]


# Answer - Our best model Random Forest scored 90.0975 %

# # Model Improvement

# Our Random Forest model can be improved if we do not consider the current_mth_churn column by any type.

# In[ ]:


# dataframe creation
broadband_imp = bbs_cust_base[['contract_month','ce_expiry','secured_revenue','bandwidth','complaint_cnt','with_phone_service']]

# creating new feature of month and year from effc_strt and effc_end
broadband_imp['start_month'] = bbs_cust_base.effc_strt_date.dt.month
broadband_imp['start_year'] = bbs_cust_base.effc_strt_date.dt.year
broadband_imp['end_month'] = bbs_cust_base.effc_end_date.dt.month
broadband_imp['end_year'] = bbs_cust_base.effc_end_date.dt.year

broadband_imp['tenure'] = bbs_cust_base.groupby('newacct_no').tenure.max()
broadband_imp['churn'] = bbs_cust_base.churn

# dropping duplicate value
broadband_imp = broadband_imp.drop_duplicates()
print('After removing duplicate shape of broadband_imp is {}'.format(broadband_imp.shape))

# selecting churn as traget column and rest features as indepandet variable
y_imp = broadband_imp['churn']
x_imp = broadband_imp.drop(['churn'],axis=1)

# train test split
x_train_imp, x_test_imp, y_train_imp, y_test_imp =  train_test_split(x_imp,y_imp,test_size=0.25,random_state=42)

# Random forest
rf_imp = RandomForestClassifier(n_estimators=100,random_state = 1)
rf_imp.fit(x_train_imp, y_train_imp)
rf_prediction_imp = rf.predict(x_test_imp)
print("Improved Random forest algor. result: ",rf_imp.score(x_test_imp,y_test_imp))

# confusion matrix
rf_cf_matrix_imp = confusion_matrix(y_test_imp,rf_prediction_imp,labels=[0,1])

# heatmap to see confusion metrix
sns.heatmap(rf_cf_matrix_imp,cbar=False,annot=True,cmap='coolwarm_r',fmt='')
plt.xlabel('Original')
plt.ylabel('Predict')


# This shows major improvement in the score of our RandomForest Model from 90.09% to 99.13%.

# In[ ]:




