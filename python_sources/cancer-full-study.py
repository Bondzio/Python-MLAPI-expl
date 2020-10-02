#!/usr/bin/env python
# coding: utf-8

# # Data Cleaning
# 
# ## 1. Import Dataset

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


raw_data = pd.read_csv("../input/cervical-cancer-risk-classification/kag_risk_factors_cervical_cancer.csv")


# In[ ]:


pd.options.display.max_columns = None
pd.options.display.max_rows = None
raw_data.head()


# ## 2. Detect Missing Values
# 
# Find all columns which have null or wrong type values (like '?')

# In[ ]:


raw_data.info()


# In[ ]:


raw_data.isnull().sum()


# In[ ]:


raw_data['STDs'].value_counts()


# Replace the '?' by NaN and update data type

# In[ ]:


data_na = raw_data.replace('?', np.nan)
data_na = data_na.infer_objects()


# In[ ]:


data_na.info()


# Drop missing values (rows).
# 
# Drop non informative columns before (not enought values)

# In[ ]:


data_nona = data_na.drop(['STDs: Time since first diagnosis','STDs: Time since last diagnosis'],axis=1)
data_nona = data_nona.dropna(axis=0)


# In[ ]:


#is there columns not informatives ?
for col in data_nona.columns:
    print(col)
    print(data_nona[col].unique())


# In[ ]:


data_nona = data_nona.drop(['STDs:AIDS','STDs:cervical condylomatosis'],axis=1)


# In[ ]:


data_nona.info()


# ## Duplicated rows

# In[ ]:


data_nona[data_nona.duplicated()]


# Remove duplicated rows

# In[ ]:


data_clean = data_nona.drop_duplicates()


# Check data type

# In[ ]:


data_clean.dtypes


# In[ ]:


# impossible to convert directly from string to int due to the string format
data_clean = data_clean.astype({'Number of sexual partners': 'float64','First sexual intercourse':'float64','Num of pregnancies':'float64', 'Smokes':'float64', 'Smokes (years)':'float64', 'Smokes (packs/year)':'float64',
       'Hormonal Contraceptives':'float64', 'Hormonal Contraceptives (years)':'float64', 'IUD':'float64',
       'IUD (years)':'float64', 'STDs':'float64', 'STDs (number)':'float64', 'STDs:condylomatosis':'float64',
       'STDs:vaginal condylomatosis':'float64', 'STDs:vulvo-perineal condylomatosis':'float64',
       'STDs:syphilis':'float64', 'STDs:pelvic inflammatory disease':'float64',
       'STDs:genital herpes':'float64', 'STDs:molluscum contagiosum':'float64', 'STDs:HIV':'float64',
       'STDs:Hepatitis B':'float64', 'STDs:HPV':'float64', 'STDs: Number of diagnosis':'float64',
       'Dx:Cancer':'float64', 'Dx:CIN':'float64', 'Dx:HPV':'float64', 'Dx':'float64', 'Hinselmann':'float64', 'Schiller':'float64',
       'Citology':'float64', 'Biopsy':'float64'},copy=False)
data_clean = data_clean.astype({'Number of sexual partners': 'int64','First sexual intercourse':'int64','Num of pregnancies':'int64', 'Smokes':'int64',
       'Hormonal Contraceptives':'int64', 'IUD':'int64',
       'STDs':'int64', 'STDs (number)':'int64', 'STDs:condylomatosis':'int64',
       'STDs:vaginal condylomatosis':'int64', 'STDs:vulvo-perineal condylomatosis':'int64',
       'STDs:syphilis':'int64', 'STDs:pelvic inflammatory disease':'int64',
       'STDs:genital herpes':'int64', 'STDs:molluscum contagiosum':'int64', 'STDs:HIV':'int64',
       'STDs:Hepatitis B':'int64', 'STDs:HPV':'int64', 'STDs: Number of diagnosis':'int64',
       'Dx:Cancer':'int64', 'Dx:CIN':'int64', 'Dx:HPV':'int64', 'Dx':'int64', 'Hinselmann':'int64', 'Schiller':'int64',
       'Citology':'int64', 'Biopsy':'int64'},copy=False)
data_clean.info()


# # EDA

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import seaborn as sns
from scipy import stats
from scipy.stats import norm
# install pandas_profiling : pip install pandas_profiling
import pandas_profiling
from sklearn import preprocessing
from sklearn.preprocessing import Normalizer
from scipy import stats as st
#notebook's library
get_ipython().run_line_magic('matplotlib', 'inline')


# The aim is to predict the likelihood of cancer.
# 
# Ideally, we need to ask to the data provider what is the meaning of the "biopsy", "hinselman", "Schiller" and "citology" columns. For the purpose of this study, let's assume that these columns means "the test returnes positive/the patient has cancer".
# 
# So we consider "biopsy", "hinselman", "Schiller" and "citology" as the target, and the other columns as the features.
# 

# In[ ]:


data_clean['Cancer']=np.where(data_clean.apply(lambda row: row.Hinselmann + row.Schiller + row.Citology + row.Biopsy, axis=1)>0,1,0)


# ## Profiling
# 
# Let's take a closer look to the features, checking correlations and properties.

# In[ ]:


pandas_profiling.ProfileReport(data_clean)


# ## Correlation
# 
# Drop correlated columns

# In[ ]:


data_eda1 = data_clean.drop(['STDs (number)', 'STDs:condylomatosis',
       'STDs:vaginal condylomatosis', 'STDs:vulvo-perineal condylomatosis',
       'STDs:syphilis', 'STDs:pelvic inflammatory disease', 'STDs:genital herpes',
       'STDs:molluscum contagiosum', 'STDs:HIV', 'STDs:Hepatitis B', 'STDs:HPV',
       'STDs: Number of diagnosis','Smokes (years)', 'Smokes (packs/year)','Dx:HPV','Citology','Hinselmann','Schiller','Biopsy'],axis=1)


# In[ ]:


#correlation matrix
k = 14 #number of variables for heatmap
corrmat = data_eda1.corr()
cols = corrmat.nlargest(k, 'Cancer')['Cancer'].index
cm = np.corrcoef(data_eda1[cols].values.T)
sns.set(font_scale=1.25)
# increase the default heatmap size
fig, ax = plt.subplots(figsize=(10,10))  
hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 8}, yticklabels=cols.values, xticklabels=cols.values, ax=ax)
plt.show()


# Correlation with target

# In[ ]:


def display_corr_with_col(df,col):
    corr_matrix = df.corr()
    corr_type = corr_matrix[col].copy()
    abs_corr_type = corr_type.apply(lambda x:abs(x))
    desc_corr_values = abs_corr_type.sort_values(ascending=False)
    y_values = list(desc_corr_values.values)[1:]
    x_values = range(0,len(y_values))
    xlabels = list(desc_corr_values.keys())[1:]
    fig,ax = plt.subplots(figsize=(8,8))
    ax.bar(x_values,y_values)
    ax.set_title('the correlation of all features with {}'.format(col),fontsize=20)
    ax.set_ylabel('Pearson correlatie coefficient [abs waarde]', fontsize=16)
    plt.xticks(x_values,xlabels,rotation='vertical')
    plt.show()

display_corr_with_col(data_eda1,'Cancer')


# ### Observations
# 
# - This is a small dataset: 650 observations
# - The dataset is imbalanced: 85/650 positives
# - After the purge, the correlation intra-features seams to be acceptable
# - some feature may be not valuable for the modeling: IUD and IUD year are correlated, Horm. contra. and horm. contra. year, the three Dx's are correlated
# - the correlation between the target and the features is not very encouraging...
# - the best correlated features are DxCancer and Dx, which seams logical
# 
# 

# ## 2. Trends
# 
# We are working on a class prediction, and not a quantitative target, so we don't have to study the distribution of the target.
# 
# ### Univariate visualization
# 
# For the boolean columns, the profile report above is quite informative. Except the "hormonal contraceptives", the boolean features are all imbalanced.
# 
# Let's check the others.

# In[ ]:


quant_cols = ['Age', 'Number of sexual partners', 'First sexual intercourse',
       'Num of pregnancies','Hormonal Contraceptives (years)','IUD (years)']


# In[ ]:


i = 1
plt.figure(i,figsize=(15, 20), dpi=80)
for col in quant_cols:
    plt.subplot(6,2,i)
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,wspace=0.35)
    sns.distplot(data_eda1[col],fit=norm)
    plt.ylabel('Probability')
    i+=1


# ## 3. Standardization/Normalization
# 
# Since some features are far from normal, let's normalize all quantitative features.

# In[ ]:


data_eda1.reset_index()
norm = preprocessing.normalize(data_eda1)
data_norm = pd.DataFrame(norm)
data_norm.columns = data_eda1.columns


# In[ ]:


from scipy.stats import norm
i = 1
plt.figure(i,figsize=(15, 20), dpi=80)
for col in quant_cols:
    plt.subplot(6,2,i)
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,wspace=0.35)
    sns.distplot(data_norm[col],fit=norm)
    plt.ylabel('Probability')
    i+=1


# In[ ]:


data_eda2 = data_eda1.copy()
data_eda2.index = data_norm.index


# In[ ]:


data_eda2[quant_cols] = data_norm[quant_cols]


# ## 4. Balancing
# 
# With such a imbalanced dataset, the accuracy is highly biased: the model quality can't be assessed this way.

# In[ ]:


data_eda2['Cancer'].loc[data_eda2['Cancer']==1].count()


# In[ ]:


data_eda2_bal = data_eda2.copy()


# In[ ]:


i = round(data_eda2['Cancer'].loc[data_eda2['Cancer']==0].count()/data_eda2['Cancer'].loc[data_eda2['Cancer']==1].count())-2
modulo = data_eda2['Cancer'].loc[data_eda2['Cancer']==0].count() % data_eda2['Cancer'].loc[data_eda2['Cancer']==1].count()
j=0
while j < i:
    data_eda2_bal = data_eda2_bal.append(data_eda2.loc[data_eda2['Cancer']==1], ignore_index=True)
    j += 1
data_eda2_bal = data_eda2_bal.append(data_eda2.loc[data_eda2['Cancer']==1].sample(modulo), ignore_index=True)


# In[ ]:


data_eda2_bal['Cancer'].loc[data_eda2_bal['Cancer']==1].count()


# # Model

# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer, accuracy_score


# In[ ]:


data_eda2_bal.info()


# In[ ]:


X = data_eda2_bal.drop('Cancer',axis=1)
y = data_eda2_bal['Cancer']


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state = 29)


# Let's try basics model without any tuning.
# 
# ### 1. Logistic Regression

# In[ ]:


X_train.sample(5)


# In[ ]:


model_lr = LogisticRegression(random_state = 29, solver = 'liblinear').fit(X_train,y_train)
predict_lr = model_lr.predict(X_test)
print(accuracy_score(y_test, predict_lr))


# ### 2. SVM

# In[ ]:


from sklearn import svm


# In[ ]:


model_svm = svm.SVC(kernel='linear').fit(X_train,y_train)


# In[ ]:


predict_svm = model_svm.predict(X_test)


# In[ ]:


print(accuracy_score(y_test, predict_svm))


# ### 3. Decision tree

# In[ ]:


from sklearn import tree


# In[ ]:


model_tree = tree.DecisionTreeClassifier(criterion='gini').fit(X_train,y_train)


# In[ ]:


predict_tree = model_tree.predict(X_test)


# In[ ]:


print(accuracy_score(y_test, predict_tree))


# ### 4. Bayes

# In[ ]:


from sklearn.naive_bayes import GaussianNB


# In[ ]:


model_bayes = GaussianNB().fit(X_train,y_train)


# In[ ]:


predict_bayes = model_bayes.predict(X_test)


# In[ ]:


print(accuracy_score(y_test, predict_bayes))


# ### 5. RandomForest

# In[ ]:


from sklearn.ensemble import RandomForestClassifier


# In[ ]:


model_rf = RandomForestClassifier().fit(X_train,y_train)


# In[ ]:


predict_rf = model_rf.predict(X_test)


# In[ ]:


print(accuracy_score(y_test, predict_rf))

