#!/usr/bin/env python
# coding: utf-8

# Our world is moving towards cashless economy and so, we need to build efficient models to track fraud transactions.Here is my attempt to build one. The challenge in this dataset is that, the Class is highly imbalanced.
# I followed the following steps:
# 1. EDA
# 2. train test split
# 3. Normal Scaling
# 4. TSNE for visualization
# 5. SMOTE for upsampling the minority
# 6. Trained multiple models
# 7. Chose the ones with low variance compared to others
# 8. Blending of those models with XGBClassifier
# 
# **Please upvote the kernel if you liked it. Your upvotes will motivate me to code more. Thank you  ** 

# **Importing basic modules**

# In[ ]:



import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import os
from sklearn.preprocessing import StandardScaler
from scipy.stats import kurtosis,skew
from sklearn.manifold import TSNE
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split,StratifiedKFold,GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import average_precision_score,make_scorer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier,AdaBoostClassifier,RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from scipy.stats import zscore
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings('ignore')
print(os.listdir("../input"))


# In[ ]:


data=pd.read_csv('../input/creditcard.csv')
data.head()


# **Taking overview of data**

# In[ ]:


data.shape


# In[ ]:


data.info()


# Hushhhh!! No null values :D :D

# In[ ]:


data.isnull().sum()


# In[ ]:


data.describe()


# Let us plot V1,V2,.. upto V28. V16, V18 and V19 seem to be closer to normal distribution than any other columns. We will dive a bit deeper in the next step. 

# In[ ]:


f,ax=plt.subplots(7,4,figsize=(15,15))
for i in range(28):
    sns.distplot(data['V'+str(i+1)],ax=ax[i//4,i%4])
    

plt.tight_layout()
plt.show()


# Let us create a dataframe with columns mean, standard deviation, max, min, skewness and kurtosis of each of the V columns. Let us plot each of these features.  

# In[ ]:


stats=pd.DataFrame()
cols=[col for col in data.columns[1:29]]
mean=data[cols].mean(axis=0)
std=data[cols].std(axis=0)
max_val=data[cols].max(axis=0)
min_val=data[cols].min(axis=0)
skew=data[cols].skew(axis=0)
kurt=data[cols].kurt(axis=0)
stats['mean']=mean
stats['std']=std
stats['max']=max_val
stats['min']=min_val
stats['skew']=skew
stats['kurt']=kurt
stats.index=cols


# In[ ]:


x_ticks=np.arange(1,29,1)
f,ax=plt.subplots(2,3,figsize=(15,8))
for i in range(6):
    ax[i//3,i%3].plot(x_ticks,stats.iloc[:,i].values,'b.')
    ax[i//3,i%3].set_title(stats.columns[i])
    
plt.tight_layout()
plt.show()


# There is atleast one outlier in each of the graphs. In 'mean' graph, mean of V3 is quite different from other columns.'std' graph looks fine and clearly shows decreasing trend in standard deviation with increasing value of column. In 'max' graph, max value of V6 and V7 is quite different. In 'min' graph, minimum value of V5 is quite different. In 'skew' aswell as 'kurtosis' graph, skewness and kurtosis of V29 are quite high. Let us understand what skewness and kurtosis actually mean. Skewness is a measure of how unsymmetric are the tails of the distribution. Normal distribution has 0 skewness because it has perfectly symmetric tails. V8 and V29 are skewed to left and right respectively to large extent. Skewed to left means the tails are longer on the left side rather than right side of mean. Kurtosis is a measure of how much probability mass is concentrated on the shoulders of distribution. Normal distribution has a kurtosis of 3 (excess kurtosis=0). As kurtosis increases, probability mass decreases from shoulder and spreads at the center and tails of the distribution. Minimum kurtosis possible is 0 (excess kurtosis= -3) and maximum possible is infinite. 0 kurtosis implies all the probability mass is concentrated on the shoulders. Many columns have very high excess kurtosis. Both skewness and kurtosis are unitless. Outliers in a sample have more effect on kurtosis than on skewness because kurtosis involves fourth moment while skewness involves third moment of distribution.

# In[ ]:


print(stats.loc[['V16','V18','V19'],:])


# Here we can see that only looking at graphs is deceptive. I had thought that V16,V18 and V19 look close to normal distributions. But kurtosis of V16 says otherwise. V18 is quite close to normal distribution.

# In[ ]:


plt.figure(figsize=(15,10))
sns.heatmap(data.corr())
plt.show()


# None of the columns is significantly correlated with Class. Amount is kind of significantly correlated with V7 and V20.
# 
# Now let us look how the Classes are distributed.

# In[ ]:


sns.countplot(data['Class'])
print((data['Class'].value_counts()/data.shape[0])*100)


# Class 1 corresponds to Fraud Transactions. We see that only 0.172% of transactions are fraud. The data is highly imbalanced. Since just upsampling with replace=True will lead to lot of duplicates. So, I shall use a technique called SMOTE. It is basically oversamplng technique which tweaks just one column a little bit and thus a new sample of minority class is created.I shall use SMOTE only on training data so that fraud transactions remain as minority in case of validation as it would be in real world scenario.

# In[ ]:


X=data.drop(['Class','Time'],axis=1)
Y=data['Class']
train_X,test_X,train_y,test_y=train_test_split(X,Y,random_state=5,test_size=0.2)


# In[ ]:


sc=StandardScaler()
train_X=sc.fit_transform(train_X)
test_X=sc.transform(test_X)
train_X=pd.DataFrame(train_X,columns=X.columns)
test_X=pd.DataFrame(test_X,columns=X.columns)


# In[ ]:


sm=SMOTE(random_state=5)
train_X_res,train_y_res=sm.fit_sample(train_X,train_y)
train_X_res=pd.DataFrame(train_X_res,columns=train_X.columns)
train_y_res=pd.Series(train_y_res,name='Class')


# Let us see how much separable are the two classes. If we consider all the V columns then we shall have 28 dimensional space. We cannot visualise such high dimensional data. I shall use TSNE to project the points from 28 dimensional space to 2 dimensional space. For faster computation, I shall only take 2500 points from each class.
# 

# In[ ]:


train=pd.concat([train_X_res,train_y_res],axis=1)
fraud=train[train['Class']==1].sample(2500)
non_fraud=train[train['Class']==0].sample(2500)
tsne_data=pd.concat([fraud,non_fraud],axis=0)
tsne_data_1=tsne_data.drop(['Class'],axis=1)


# In[ ]:


tsne=TSNE(n_components=2,random_state=5,verbose=1)
tsne_trans=tsne.fit_transform(tsne_data_1)


# In[ ]:


tsne_data['first_tsne']=tsne_trans[:,0]
tsne_data['second_tsne']=tsne_trans[:,1]
plt.figure(figsize=(15,10))
sns.scatterplot(tsne_data['first_tsne'],tsne_data['second_tsne'],hue='Class',data=tsne_data)


# In[ ]:


models=[SVC(probability=True),LogisticRegression(),LinearDiscriminantAnalysis(),DecisionTreeClassifier(),
       ExtraTreesClassifier(n_estimators=100),AdaBoostClassifier(n_estimators=100),RandomForestClassifier(n_estimators=100)]

model_names=['SVC','LR','LDA','DTC','ETC','ABC','RFC']
train_score=[]
score_1=[]
test_score=[]


# Defining function to train models and predict probabilities.

# In[ ]:


skf=StratifiedKFold(n_splits=5,random_state=5)
def get_model(train_X,train_y,test_X,test_y,model):
    for train_index,val_index in skf.split(train_X,train_y):
        train_X_skf,val_X_skf=train_X.iloc[train_index,:],train_X.iloc[val_index,:]
        train_y_skf,val_y_skf=train_y.iloc[train_index],train_y.iloc[val_index]
        clf=model
        clf.fit(train_X_skf,train_y_skf)
        pred=clf.predict_proba(val_X_skf)[:,1]
        score=average_precision_score(val_y_skf,pred)
        score_1.append(score)
        
    train_score.append(np.mean(score_1))
    clf.fit(train_X,train_y)
    pred_prob=clf.predict_proba(test_X)[:,1]
    score_test=average_precision_score(test_y,pred_prob)
    test_score.append(score_test)
           


# To increase computational speed, I sampled only 50000 points from train_X_res and 10000 points from test_X

# In[ ]:


train_X_sam=train_X_res.sample(10000)
train_X_index=train_X_sam.index
train_y_sam=train_y_res[train_X_index]
train_X_sam.reset_index(drop=True,inplace=True)
train_y_sam.reset_index(drop=True,inplace=True)
test_X_sam=test_X.sample(1000)
test_X_index=test_X_sam.index
test_y_sam=test_y[test_X_index]
test_X_sam.reset_index(drop=True,inplace=True)
test_y_sam.reset_index(drop=True,inplace=True)


# In[ ]:


for model in models:
    get_model(train_X_sam,train_y_sam,test_X,test_y,model)


# In[ ]:


result=pd.DataFrame({'models':model_names,'train_score':train_score,
                    'test_score':test_score},index=model_names)


# In[ ]:


plt.figure(figsize=(10,6))
plt.subplot(1,2,1)
result['train_score'].plot.bar()
plt.title('Train Score')
plt.subplot(1,2,2)
result['test_score'].plot.bar()
plt.title('Test Score')
plt.tight_layout()
plt.show()


# All models are overfitting. But Logistic Regression, ETC, ABC and RFC provide decent test scores.

# Let us try Blending the top 4 performers with XGBClassifier

# In[ ]:


clf=LogisticRegression()
clf.fit(train_X_sam,train_y_sam)
lr_pred=clf.predict_proba(test_X)[:,1]

clf_2=AdaBoostClassifier()
clf_2.fit(train_X_sam,train_y_sam)
abc_pred=clf_2.predict_proba(test_X)[:,1]

clf_3=ExtraTreesClassifier()
clf_3.fit(train_X_sam,train_y_sam)
etc_pred=clf_3.predict_proba(test_X)[:,1]

clf_4=RandomForestClassifier()
clf_4.fit(train_X_sam,train_y_sam)
rfc_pred=clf_4.predict_proba(test_X)[:,1]

xgb=XGBClassifier()
xgb.fit(train_X_sam,train_y_sam)
xgb_pred=xgb.predict_proba(test_X)[:,1]


# This blending score is better than each of the models alone. 

# In[ ]:


blending_pred=0.20*(lr_pred+etc_pred+rfc_pred+abc_pred+xgb_pred)
blending_score=average_precision_score(test_y,blending_pred)
print(blending_score)


# **Things which you can further try** :
# 1. Using different scaling of variables
# 2. Using different algorithm for upsampling
# 3. Using different models
# 4. Hyperparamter tuning of mutiple models and then blending
# 5. Ensembling
