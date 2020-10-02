#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
print(os.listdir("../input"))
pd.set_option('max_columns', 1000)
pd.set_option('max_rows', 10)


# **1.Import Data**

# In[ ]:


data= pd.read_csv('../input/quotes.csv',encoding='latin1')
data.describe()
data.shape
data.columns
types=data.dtypes


# **2.Data Cleaning**

# * 1.**Delete Duplication**
# * 2.**impute missing**
# *    2.1 **if mising >90%: delete**
# *    2.2 **if mising <90% and >50%:replace with unknown**
# *    2.3 **if mising <50%: impute misssing with partial imputation or probability imputation**
# * 3.**Delete the index variable: ID_Variable (primary key is not useful for prediction modeling)**
# * 4.**Replace the missing of ownersip and vehicle-value with unknow**
# * 5.**Use partial imputation to impute the missing value of COMMUTE_DISTANCE because commute distance has high relationship with vehicle use**
# * 6.**Use probability imputation to impute the mising of gender**
# * 7.**Upcase the column VEHICLEMAKE and VEHICLEMODEL**
# * 8.**split the quotedate into month, year,day and week**
# * 9.**Create new variable age instead of year of birth and use partial imputation to impute the missing value of YEARS_LICENSED**
# * 10.**Replace 'Separated','Divorced','Widow/Widower' with single**
# * 11.**Create province for postcode variable**
# * 12.**delete Noise Data**
# * 13.**detect outlier data**
# * 14.**Data accuracy and consistency**
# * 15.**Discretization**
# * 16.**create calculation field**
# 

# In[ ]:


data.drop_duplicates(['ID_Variable'], keep='first', inplace=True)
pd.set_option('max_rows', 100)
(data.shape[0]-data.count())/data.shape[0]

data.drop(['ID_Variable'],axis=1,inplace=True)

data.drop(['YEARS_AS_PRINCIPAL_DRIVER','MARKING_SYSTEM','TRACKING_SYSTEM'],axis=1,inplace=True)

data.rename(columns={'VEHICLE_OWNERSHIP':'OWNERSHIP'},inplace=True) 
data['OWNERSHIP'].fillna('Unkown',inplace=True)
data.rename(columns={'VEHICLE_VALUE':'Value'},inplace=True) 
data['Value'].fillna('Unkown',inplace=True)
data['OCCUPATION'].fillna('Unkown',inplace=True)

for i in set(data['VEHICLEUSE'].values):
    data.loc[(data['COMMUTE_DISTANCE'].isnull())&(data['VEHICLEUSE']==i),'COMMUTE_DISTANCE']= data.loc[data['VEHICLEUSE']==i,'COMMUTE_DISTANCE'].mean()
    
a=data['GENDER'].value_counts()
p_male=a['Male']/(a['Female']+a['Male'])
count=len(data.loc[data['GENDER'].isnull(),'GENDER'])
fill = np.random.choice(['Male','Female'],count,p=[p_male,1-p_male])
data.loc[data['GENDER'].isnull(),'GENDER'] = fill

data['VEHICLEMAKE']=data['VEHICLEMAKE'].str.upper()
data['VEHICLEMODEL']=data['VEHICLEMODEL'].str.upper()

data['QUOTEDATE']=pd.to_datetime(data['QUOTEDATE'])
data['YEAR']=[i.year for i in data['QUOTEDATE']]
data['month']=[i.month for i in data['QUOTEDATE']]
data['DAY']=[i.day for i in data['QUOTEDATE']]
data['QUOTER'] = data['month'].astype('int') / 4 + 1
data['WEEK']=[i.weekday() for i in data['QUOTEDATE']]
data.drop('QUOTEDATE',axis=1,inplace=True)

data['age']=2019-data['YEAR_OF_BIRTH']
data.drop('YEAR_OF_BIRTH',axis=1,inplace=True)

for i in set(data['age'].values):
    data.loc[(data['YEARS_LICENSED'].isnull())&(data['age']==i),'YEARS_LICENSED']=  data.loc[data['age']==i,'YEARS_LICENSED'].mean()

data['MARITAL_STATUS'].replace(['Separated','Divorced','Widow/Widower'],'Single', inplace=True)

a=pd.Series(np.array(list(["A", "B", "C", "E","G","H","J","K","L","M","N","P","R","S","T","V","X","Y"])))
b=pd.Series(np.array(list(["NL","NS","PE","NB","QC","QC","QC","ON","ON","ON","ON","ON","MB","SK","AB","BC","NT","YT"])))
data['province'] = data['POSTAL_CODE'].str[0]
data['province'].replace(a.values,b.values,inplace=True)

data=data.loc[data['age']>16,]


# In[ ]:


import copy as copy
data2=copy.deepcopy(data)


# **Export cleaned data file into Tableau and from the boxplot, we can identify there are some outliers/noises data exists and should be solved**

# ![image.png](attachment:image.png)

# In[ ]:


data=data.loc[data['ANNUAL_KM']<350000,]
data=data.loc[data['COMMUTE_DISTANCE']<40000,]
data=data.loc[data['age']<100,]
data=data.loc[data['YEARS_LICENSED']<100,]


# ![image.png](attachment:image.png)

# ![image.png](attachment:image.png)

# ![image.png](attachment:image.png)

# **Discretization**

# In[ ]:


gap = (data['age'].max()-data['age'].min())/5
pt = []

for i in range(6):
    pt.append(data2['age'].min() + i*gap)
label = ['young','adult','mid_age','senior','xsenior']
data['age_group']= pd.cut(data['age'], pt, labels=label)
data.drop('age_group',axis=1,inplace=True)

import copy as copy
data2=copy.deepcopy(data)


# **5. identify input variables and target variable and Feature preprocessing(label encoding:change categorical variable into numerical)**

# In[ ]:


y = data.IS_BOUND
x = data.drop('IS_BOUND', axis=1)

from sklearn.preprocessing import LabelEncoder
L = LabelEncoder()
for i in x.columns:
    if x[i].dtypes == 'object':
        x[i] = L.fit_transform(x[i].astype(str))


# **Statistic Analysis**

# * 1.**Describe staistics**
# * 2.**Frequency Table**
# * 3.**Box Plot: 25th percentile, 75 percentile, Interquartile Range(IQR), Max,Min**
# * 4.**Median,Mode, Covariance,standard deviation,Variance,max,min,skewness,kurtosis **
# * 5.**correlation among attributes**
# * 6.**pearson correlation between input variables and target variables**
# * 7.**Factor Analysis**
# * 8.**T-test(one-sample)**
# * 9.**T-test(independent group: Whether the male's mean of annual km has significant difference with that of female)**
# * 10.**Normal distribution testing**
# * 11.**QQ Plot**
# * 12.**Chi-square Test(chi2,p,dof,expected)**
# * 13.**ANOVA(whether there is huge difference in means of different yypes of ownership )**
# * 14.**Pivot table**
# 

# In[ ]:


from scipy import stats
describe=data.describe()

data['VEHICLEYEAR'].value_counts()

IQR=(np.percentile(data['age'],75))-(np.percentile(data['age'],25))
Min=(np.percentile(data['age'],25)-1.5*IQR)
Max=(np.percentile(data['age'],75)+1.5*IQR)   

median=[]
for i in describe.columns:
    median.append(np.median(describe[i]))
from scipy.stats import mode
mode(x)
data.cov()
np.std(x)
np.var(x)
np.max(x)
np.min(x)
skew = stats.skew(x)
kurtosis = stats.kurtosis(x)

data.corr()

from scipy.stats import pearsonr
for I in x.columns:
   print(I,pearsonr(x[i],y))

population=data['age']
stats.ttest_1samp(population,45)

population1=data.loc[data['GENDER']=='Male','ANNUAL_KM']
population2=data.loc[data['GENDER']=='Female','ANNUAL_KM']
stats.ttest_ind(population1,population2)

stats.normaltest(x)

from matplotlib import pyplot as plt
plt.subplot(2, 2,1)
stats.probplot(x['age'], dist="norm", plot=plt)
plt.subplot(2, 2,2)
stats.probplot(x['ANNUAL_KM'], dist="norm", plot=plt)
plt.subplot(2, 2,3)
stats.probplot(x['COMMUTE_DISTANCE'], dist="norm", plot=plt)
plt.subplot(2, 2,4)
stats.probplot(x['Value'], dist="norm", plot=plt)
plt.show()

stats.chi2_contingency(data['age'],data['IS_BOUND'])
stats.chi2_contingency(data['VEHICLEYEAR'],data['IS_BOUND'])
stats.chi2_contingency(x['month'],y)
stats.chi2_contingency(x['DAY'],y)

population1=data.loc[data['OWNERSHIP']=='Owned','ANNUAL_KM']
population2=data.loc[data['OWNERSHIP']=='Leased','ANNUAL_KM']
population3=data.loc[data['OWNERSHIP']=='Non-owned','ANNUAL_KM']
stats.ttest_ind(population1,population2)
stats.f_oneway(population1,population2,population3)

pivot=pd.pivot_table(data,'IS_BOUND',index='VEHICLEUSE',columns='OCCUPATION',aggfunc='count',fill_value=0)

