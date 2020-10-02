#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Supress Warnings
import warnings
warnings.filterwarnings('ignore')

# Importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Visualization
from matplotlib.pyplot import xticks
get_ipython().run_line_magic('matplotlib', 'inline')

# Data display coustomization
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)


# In[ ]:


#Reading the dataset
churndf=pd.read_csv("telecom_churn_data.csv")
churndf.head()


# In[ ]:


churndf.shape


# In[ ]:


churndf.describe()


# In[ ]:


churndf.columns


# In[ ]:


churndf.dtypes


# In[ ]:


churndf.index


# In[ ]:


churndf.info()


# In[ ]:


#Checking the percentage of null values column-wise
round(100*(churndf.isnull().sum()/len(churndf.index)), 2)


# In[ ]:


#Checking the percentage of null values row-wise
round(100*(churndf.isnull().sum(axis=1)/len(churndf.index)), 2)


# In[ ]:


nullDF=pd.DataFrame(round(100*(churndf.isnull().sum()/len(churndf.index)),2),columns=['Null%_in_Cols'])
nullDF


# In[ ]:


# Dropping cols which have over 70% null values
dropCol=nullDF.loc[nullDF['Null%_in_Cols']>=70]
dropCol_list=list(dropCol.index)
dropCol


# In[ ]:


#Dropping the columns from the orignal dataframe
churndf = churndf.drop(dropCol_list, axis = 1)
churndf.head()


# In[ ]:


# IMputing the missing values in the other columns of the dataframe with '0'
churnCol = list(churndf.columns)
churndf=churndf[churnCol].fillna(value=0)


# In[ ]:


churndf.drop_duplicates
churndf.shape


# In[ ]:


# Rechecking null percentages
round(100*(churndf.isnull().sum()/len(churndf.index)), 2)


# In[ ]:


#Dropping some columns which seem irrelevant to our analysis
churndf=churndf.drop(['circle_id', 'loc_og_t2o_mou', 'std_og_t2o_mou', 'loc_ic_t2o_mou', 'last_date_of_month_6', 
          'last_date_of_month_7', 'last_date_of_month_8', 'last_date_of_month_9'], axis = 1)
churndf.head()


# ## FILTERING HIGH VALUE CUSTOMERS
# 
# #### In this study, we need to predict the churn of only the high value customers and they are those customers who have recharged with an amount greater than or equal to X, and X here is the 70th percentile of the average recharge amount in the good phase (6th and 7th month)

# In[ ]:


#high value customers
total=[]
for each in churndf.columns:
    if  'total_rech_' in each:
        total.append(each)
print(total)


# In[ ]:


#Average 
churndf['Avg_JuneJuly']=(churndf['total_rech_amt_6']+churndf['total_rech_amt_7'])/2
churndf2 = churndf[churndf['Avg_JuneJuly']>churndf['Avg_JuneJuly'].quantile(0.70)]
churndf2.shape


# In[ ]:


#labelling 
churndf2['usg_total'] = churndf2['total_og_mou_9']+churndf2['total_ic_mou_9']+churndf2['vol_2g_mb_9']+churndf2['vol_3g_mb_9']
churndf2['churn_count'] = np.where(churndf2['usg_total'] == 0,1,0)
churndf2['churn_count'].value_counts()


# In[ ]:


#Rename Columns with names similar to a common format
churndf.rename(columns={'jun_vbc_3g': 'vbc_3g_6', 'jul_vbc_3g': 'vbc_3g_7', 'aug_vbc_3g': 'vbc_3g_8', 'sep_vbc_3g': 'vbc_3g_9'}, inplace=True)


# In[ ]:


# Tagging the churners and droping all the unwanted columns which correspond to the churn phase i.e we remove all those cols which have _9 in the name
churndf2 = churndf2.drop(['Avg_JuneJuly', 'usg_total'], axis = 1)
col_ending9 = [i for i in churndf2.columns if i.endswith('_9')]
col_ending9


# In[ ]:


churndf2.shape


# In[ ]:


## Converting the dtype of date(object) to datetime 
datecols = churndf.select_dtypes(include=['object'])
print(datecols.iloc[0])


# In[ ]:


for col in datecols.columns:
    churndf[col]=pd.to_datetime(churndf[col])


# In[ ]:


# Check for missing vals
Missingpercentage = churndf.isnull().sum() * 100 / len(churndf.index)
df_miss_val = pd.DataFrame({'column_name': churndf.columns,
                                 'Missingpercentage': Missingpercentage })
df_miss_val.loc[df_miss_val.Missingpercentage > 1]


# In[ ]:


churndf2.shape


# In[ ]:


churn_column = churndf2['churn_count']
churn_percentage = (sum(churn_column)/len(churn_column.index))*100
print(churn_percentage)
print(churndf2.shape)


# **** The Churn percentage is 8.636% ****

# ## OUTLIER ANALYSIS

# In[ ]:


churndf2.describe(percentiles=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.96,0.97,0.98,0.99,1])


# In[ ]:


churndf2['Avg_Total_Outgoing_Mins_JuneJuly']=(churndf2['total_og_mou_6']+churndf2['total_og_mou_7'])/2
churndf2['Avg_Total_Incoming_Mins_JuneJuly']=(churndf2['total_ic_mou_6']+churndf2['total_ic_mou_7'])/2
churndf2['Avg_Total_Recharge_JuneJuly']=(churndf2['total_rech_num_6']+churndf2['total_rech_num_7'])/2
churndf2['Avg_TotalRechargeAmount_JuneJuly']=(churndf2['total_rech_amt_6']+churndf2['total_rech_amt_7'])/2
churndf2['Avg_Monthly2gRecharge_JuneJuly']=(churndf2['monthly_2g_6']+churndf2['monthly_2g_7'])/2
churndf2['Avg_Monthly3gRecharge_JuneJuly']=(churndf2['monthly_3g_6']+churndf2['monthly_3g_7'])/2
churndf2['Avg_Sachet2gRecharge_JuneJuly']=(churndf2['sachet_2g_6']+churndf2['sachet_2g_7'])/2
churndf2['Avg_Sachet3gRecharge_JuneJuly']=(churndf2['sachet_3g_6']+churndf2['sachet_3g_7'])/2


# In[ ]:


churndf2['OGCalls_Diff']=churndf2['Avg_Total_Outgoing_Mins_JuneJuly']-churndf2['total_og_mou_8']
churndf2['ICCalls_Diff']=churndf2['Avg_Total_Incoming_Mins_JuneJuly']-churndf2['total_ic_mou_8']
churndf2['Recharge_Diff']=churndf2['Avg_Total_Recharge_JuneJuly']-churndf2['total_rech_num_8']
churndf2['RechargeAmt_Diff']=churndf2['Avg_TotalRechargeAmount_JuneJuly']-churndf2['total_rech_amt_8']
churndf2['2GRecharge_Diff']=churndf2['Avg_Monthly2gRecharge_JuneJuly']-churndf2['monthly_2g_8']
churndf2['3GRecharge_Diff']=churndf2['Avg_Monthly3gRecharge_JuneJuly']-churndf2['monthly_3g_8']
churndf2['2GSachetRecharged_Diff']=churndf2['Avg_Sachet2gRecharge_JuneJuly']-churndf2['sachet_2g_8']
churndf2['3GSachetRecharged_Diff']=churndf2['Avg_Sachet3gRecharge_JuneJuly']-churndf2['sachet_3g_8']


# In[ ]:


churndf2=churndf2.drop(['Avg_Total_Outgoing_Mins_JuneJuly','Avg_Total_Incoming_Mins_JuneJuly','Avg_Total_Recharge_JuneJuly','Avg_TotalRechargeAmount_JuneJuly',
             'Avg_Monthly2gRecharge_JuneJuly','Avg_Monthly3gRecharge_JuneJuly','Avg_Sachet2gRecharge_JuneJuly','Avg_Sachet3gRecharge_JuneJuly'],axis=1)


# In[ ]:


mouTotal=pd.DataFrame(churndf2[['total_og_mou_6','total_og_mou_7','total_og_mou_8','total_ic_mou_6','total_ic_mou_7','total_ic_mou_8']])


# In[ ]:


churndf2=churndf2.drop(["total_og_mou_6","total_og_mou_7","total_og_mou_8","total_ic_mou_6","total_ic_mou_7","total_ic_mou_8"],axis=1)


# In[ ]:


list1=list(churndf2.columns)
imp_att = [col for col in list1 if '_mou' in col]
imp_num_att = churndf2.drop(imp_att, axis = 1)
imp_num_att_col=list(imp_num_att.columns)


# In[ ]:


imp_att_1 = [col for col in imp_num_att_col if 'date' in col]
imp_num_att_1 = imp_num_att.drop(imp_att_1, axis = 1)
imp_num_att_1_col=list(imp_num_att_1.columns)


# In[ ]:


main_att=pd.concat([imp_num_att_1,mouTotal],axis=1)


# In[ ]:


imp_num_att_1=imp_num_att_1.drop(['mobile_number','churn_count'],axis=1)


# In[ ]:


num_final=imp_num_att_1.columns
print(num_final)
print(len(num_final))


# In[ ]:


#BoxPLot to check for outliers in the dataset
plt.figure(figsize=(30,30))
for i in range(1,56):
    plt.subplot(7,8,i)
    sns.boxplot(y=imp_num_att_1[num_final[i-1]])


# In[ ]:


imp_num_att_1=imp_num_att_1[imp_num_att_1.apply(lambda x: np.abs(x - x.mean()) / x.std() < 3).all(axis=1)]  


# In[ ]:


descr=imp_num_att_1.describe(percentiles=[0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.96,0.97,0.98,0.99,1])
descr


# In[ ]:


plt.figure(figsize=(30,30))
for i in range(1,51):
    plt.subplot(7,8,i)
    sns.boxplot(y=imp_num_att_1[num_final[i-1]])


# In[ ]:


# Heatmap to understand the correlations 
plt.figure(figsize = (30,25))
sns.heatmap(imp_num_att_1.corr(), annot = True, cmap="YlGnBu")
plt.show()


# In[ ]:


# Printing the correlation matrix to better understand the correlations
imp_num_att_1.corr()


# ## MODEL BUILDING 

# In[ ]:


churndf2_cols=list(churndf2.columns)
numericAtt = [col for col in churndf2_cols if 'date' in col]
numeric_att_churndf2 = churndf2.drop(numericAtt, axis = 1)
numeric_att_churndf2_col=list(numeric_att_churndf2.columns)
numeric_att_churndf2.head(10)


# In[ ]:


# Feature derivation
churndf2['aonMonth']=churndf2['aon']/30
churndf2=churndf2.drop(['aon'],axis=1)
custByTenure = sns.distplot(churndf2['aonMonth'], hist=True,bins=50,kde=False,hist_kws={'edgecolor':'black'})
custByTenure.set_ylabel('No of Customers')
custByTenure.set_xlabel('Tenure (months)')
custByTenure.set_title('Customers by their tenure')


# In[ ]:


churndf2=churndf2.drop(['mobile_number'],axis=1)
churndf2.shape


# ## SCALING

# In[ ]:


# Importing test_train_split from sklearn library
from sklearn.model_selection import train_test_split


# In[ ]:


#Feature variables is assigned to X
X = numeric_att_churndf2.drop('churn_count',axis=1)
# Response variable is assigned to y
y = numeric_att_churndf2['churn_count']

# Splitting the data into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=101)


# In[ ]:


# From the below plot we observe that there is data imbalance
pd.Series(y_train).value_counts().plot.bar()


# We use SMOTE To handle class imabalance and in our case the churn rate is low with 8.6% resulting in class imbalance

# In[ ]:


from imblearn.over_sampling import SMOTE
sm = SMOTE(random_state = 33)


# In[ ]:


X_train, y_train = sm.fit_sample(X_train, y_train.ravel())


# In[ ]:


# We now observe from the below plot that the data has been balanced
pd.Series(y_train).value_counts().plot.bar()


# In[ ]:


# SCALING
from sklearn.preprocessing import StandardScaler
standard_scaler = StandardScaler()
churndf3_train = standard_scaler.fit_transform(X_train)


# ## PRODUCT COMPONENT ANALYSIS

# In[ ]:


#Step1 : Import the PCA module
from sklearn.decomposition import PCA
pca = PCA(svd_solver='randomized', random_state=50)


# In[ ]:


pca.fit(churndf3_train)


# In[ ]:


#Step2: List all the PCA components
pca.components_


# In[ ]:


pcaComp=pd.DataFrame(pca.components_)
pcaComp.head() 


# In[ ]:


evrDF=pd.DataFrame(pca.explained_variance_ratio_)
evrDF.shape


# In[ ]:


#Step 3: Scree plot to identify how many components are truly required
fig = plt.figure(figsize = (12,8))
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('number of components')
plt.ylabel('cumulative explained variance')
plt.show()


# ** From the Scree Plot above , we observe that around 95% variance in the data is explained by around 65 principal components **

# In[ ]:


np.random.seed(0)

#total PCs count
NoOfPCs= pca.components_.shape[0]

imp = [np.abs(pca.components_[i]).argmax() for i in range(NoOfPCs)]

initName = list(X.columns)

impName = [initName[imp[i]] for i in range(NoOfPCs)]


res = {'PC{}'.format(i): impName[i] for i in range(NoOfPCs)}


# In[ ]:


#Create a new DF to map all the key-value pairs
KeyValMap=pd.DataFrame()
KeyValMap['PCA']=res.keys()


# In[ ]:


KeyValMap['ImpFeatures']=res.values()
KeyValMap


# In[ ]:


#Observe the variance
dataVar=pd.DataFrame(np.transpose(pca.explained_variance_ratio_),columns=['Variance'])
dataVar['Variance']=round(dataVar['Variance'],2)
dataVar.head(10)


# In[ ]:


PCARes=pd.concat([KeyValMap,dataVar],axis=1)
PCARes.head(10)


# In[ ]:


# Extract the top 60 features from the above DF and analyse it separately
PCARes_top60=pd.DataFrame(PCARes.head(60))
PCARes_top60FeaturesList=list(PCARes_top60['ImpFeatures'])


# In[ ]:


#Dimensionality Reduction Using PCA
from sklearn.decomposition import IncrementalPCA
PCARes1 = IncrementalPCA(n_components = 60)


# In[ ]:


PCARes2 = PCARes1.fit_transform(churndf3_train)
PCARes2.shape

#PCARes2=pd.DataFrame(PCARes2,columns=PCARes_top60)
#PCARes2.head()


# In[ ]:


PCA_test = PCARes1.transform(X_test)
PCA_test.shape


# ### Logistic Regression

# In[ ]:


from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn import metrics
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


# In[ ]:


lr_pca = LogisticRegression(random_state = 1)
model_lr_pca = lr_pca.fit(PCARes2,y_train)


# In[ ]:


y_pred = model_lr_pca.predict(PCA_test)


# In[ ]:


#confusion matrix
print(confusion_matrix(y_test,y_pred))
print("Accuracy is",accuracy_score(y_test,y_pred))


# ### Random Forest

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
#default parameters
model_rf = RandomForestClassifier()


# In[ ]:


model_rf.fit(X_train,y_train)
pred_rf = model_rf.predict(X_test)


# In[ ]:


print(confusion_matrix(y_test,pred_rf))
print("Accuracy is",accuracy_score(y_test,pred_rf))


# In[ ]:


#finding the best hyperparameters
from sklearn.model_selection import GridSearchCV
param_grid = {
    'max_depth': [6,7,8],
    'min_samples_leaf': range(100, 150, 250),
    'min_samples_split': range(200, 300, 400),
    'n_estimators': [500,800, 900], 
    'max_features': [14,25]
}
rf = RandomForestClassifier()
grid_search = GridSearchCV(estimator = rf, param_grid = param_grid, 
                          cv = 3, n_jobs = -1,verbose = 1)


# In[ ]:


grid_search.fit(X_train,y_train)
print("Accuracy is",grid_search.best_score_)
print("Best parameters are",grid_search.best_params_)


# In[ ]:


#model with best parameters
rf_best = RandomForestClassifier(bootstrap=True,
                             max_depth=8,
                             min_samples_leaf=150, 
                             min_samples_split=200,
                             max_features=10,
                             n_estimators=100)


# In[ ]:


rf_best.fit(X_train,y_train)


# In[ ]:


pred_best = rf_best.predict(X_test)


# In[ ]:


print(confusion_matrix(y_test,pred_best))
print("Accuracy is",accuracy_score(y_test,pred_best))

