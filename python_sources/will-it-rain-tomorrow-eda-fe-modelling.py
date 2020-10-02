#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install plot_metric')
get_ipython().system('pip install catboost')
from catboost import CatBoostClassifier
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import lightgbm as lgb
from sklearn.model_selection import GridSearchCV

import seaborn as sns
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly as py
import plotly.graph_objs as go
import xgboost as xgb
from plot_metric.functions import BinaryClassification
get_ipython().system('pip install category_encoders')
import missingno as msno
from sklearn.model_selection import train_test_split
from sklearn import base
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,roc_auc_score,classification_report,confusion_matrix
from IPython.display import Image
from category_encoders import TargetEncoder
import warnings
warnings.filterwarnings("ignore")


# # Will it rain tomorrow?
# 

# <img src="https://media.giphy.com/media/IuVFGSQZTd6TK/giphy.gif">

# ### In this project, we tried to predict whether it will rain tomorrow. It is a classification project. There is a Yes or No class (a binary classification problem).  Yes, it will rain tomorrow. If No, it will not rain tomorrow. In this project,Rain in Tomorrow dataset was used.

# ### Since our target variable is categorical, we will use these models. These can be listed as follows:
# 
# 
# 1.   XGboost Classifier
# 2.   Light-GBM Classifier
# 1.   CatBoost Classifier
# 2.   GradientBoosting Classifier
# 1.   Logistic Regression
# 
# 
# 
# 
# 
# 
# 
# 

# ## Content
# ### This dataset contains daily weather observations from numerous Australian weather stations such as Rainfall, Wind and Humidity.
# ### The following steps were followed in this project:
# 
# 1.   Exploratory data analysis
# 2.   Visualization
# 2.   Split data into training and test set
# 2.   Feature Engineering
# 1.   Modelling
# 1.   Feature Importance
# 1.   Predict results
# 
# 
# 

# # 1. Exploratory data analysis

# ## Import Data

# In[ ]:


path = "../input/weather-dataset-rattle-package/weatherAUS.csv"

data = pd.read_csv(path)


# ## Data Analysis
# 

# In[ ]:


data.head()


# In[ ]:


data.info()


# In[ ]:


data.describe()


# ### It is given in the dataset description, that we should drop the RISK_MM feature variable from the dataset description. So, we should drop it as follows-

# In[ ]:


data.drop('RISK_MM', axis=1 ,inplace=True)


# ### Target content changed to 1-0.

# In[ ]:


data.RainTomorrow = [0 if each=='No' else 1 for each in data.RainTomorrow]


# ### The date was divided into days, months, years.

# In[ ]:


data['Date'] = pd.to_datetime(data['Date'])
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month
data['Day'] = data['Date'].dt.day
data.drop('Date', axis=1 ,inplace=True)
data


# ### Number and rate of Target Variables

# In[ ]:


# The Class Distribution
fig, ax =plt.subplots(nrows=1,ncols=2, figsize=(10,4))
labels=['No', 'Yes']
sns.countplot(x=data.RainTomorrow, data=data, palette="pastel",ax=ax[0])
data['RainTomorrow'].value_counts().plot.pie(autopct="%1.2f%%", ax=ax[1], colors=['#66b3ff','#ffcc99'], 
                                             labels=labels, explode = (0, 0.1), startangle=90)
plt.show()


# In[ ]:


rain_no = data[data['RainTomorrow']== 0]
rain_yes = data[data['RainTomorrow']== 1]

fig = go.Figure([go.Bar(x=['Rain-Yes', 'Rain-No'], y=[len(rain_yes),len(rain_no)], marker_color='lightsalmon')])
fig.update_layout(title_text='Is Rain Tomorrow')
fig.show()


# ![](https://cdn.discordapp.com/attachments/703002285994672192/715889102012022835/rain_yes_no.png)

# ### We see an unbalanced distribution in the dataset

# ## Information about Missing values.

# ### Showing missing values

# In[ ]:


msno.matrix(data)
plt.show()


# In[ ]:


msno.bar(data,sort='descending',color='#008599')
plt.show()


# ## Representation of missing values, unique values, etc.

# In[ ]:


def Missing_Values(data):
    variable_name=[]
    total_value=[]
    total_missing_value=[]
    missing_value_rate=[]
    unique_value_list=[]
    total_unique_value=[]
    data_type=[]
    for col in data.columns:
        variable_name.append(col)
        data_type.append(data[col].dtype)
        total_value.append(data[col].shape[0])
        total_missing_value.append(data[col].isnull().sum())
        missing_value_rate.append(round(data[col].isnull().sum()/data[col].shape[0],3))
        unique_value_list.append(data[col].unique())
        total_unique_value.append(len(data[col].unique()))
    missing_data=pd.DataFrame({"Variable":variable_name,"Total_Value":total_value,                             "Total_Missing_Value":total_missing_value,"Missing_Value_Rate":missing_value_rate,
                             "Data_Type":data_type,"Unique_Value":unique_value_list,\
                               "Total_Unique_Value":total_unique_value})
    return missing_data.sort_values("Missing_Value_Rate",ascending=False)


# In[ ]:


data_info=Missing_Values(data)
data_info


# ## Types of data measurement scales

# In[ ]:


data_info["Scales_of_measurement"]=["Continuous","Continuous","Ordinal","Ordinal","Continuous","Continuous","Nominal","Nominal","Continuous","Nominal","Continuous","Continuous","Continuous","Continuous","Continuous","Nominal","Continuous","Continuous","Continuous","Continuous","Nominal","Nominal","Nominal","Nominal","Nominal"]

data_info = data_info.set_index("Variable")
data_info


# ## Determination of numerical columns.

# In[ ]:


numerical_columns = list(data_info.loc[(data_info.loc[:,"Scales_of_measurement"]=="Continuous")].index)
len(numerical_columns), numerical_columns


# ## Determination of categorical columns.

# In[ ]:


categorical_columns = list(data_info.loc[(data_info.loc[:,"Scales_of_measurement"]=="Nominal") |
                                       (data_info.loc[:,"Scales_of_measurement"]=="Ordinal")].index)
len(categorical_columns), categorical_columns


# # 2. Visualization

# In[ ]:


f,ax = plt.subplots(figsize=(10, 10))
sns.heatmap(data.corr(), annot=True, linewidths=0.5,linecolor="black", fmt= '.1f',ax=ax,cmap="coolwarm")
plt.show()


# In[ ]:


labels = data_info.Scales_of_measurement.value_counts().index
sizes = data_info.Scales_of_measurement.value_counts().values
plt.figure(figsize = (6,6))
plt.pie(sizes,  labels=labels, colors=sns.color_palette('bright'), autopct='%1.1f%%')
plt.title('Variable Types',fontsize = 17,color = 'brown')
plt.show()


# In[ ]:


fig, ax =plt.subplots(nrows=1,ncols=2, figsize=(20,7))
sns.barplot(x=data.Month,y=data.MinTemp,hue="RainTomorrow",data=data,ax=ax[0],palette="pastel")
sns.barplot(x=data.Month,y=data.MaxTemp,hue="RainTomorrow",data=data,ax=ax[1],palette="pastel")
plt.show()


# In[ ]:


def pairplot(data,lst):
    sns.set(style="ticks")
    sns.pairplot(data[lst],hue="RainTomorrow")
lst=["MinTemp","MaxTemp","Temp9am","Temp3pm","RainTomorrow"]
data_2016=data[data.Year==2016]
pairplot(data_2016,lst)


# In[ ]:


from plotly.offline import iplot
fig, ax =plt.subplots(nrows=1,ncols=1, figsize=(18,8))
sns.pointplot(x="Year",y="Cloud3pm",data=data,hue="RainToday")
sns.pointplot(x="Year",y="Cloud3pm",data=data,hue="RainTomorrow",color="red")
plt.show()


# Note: The blue line is Today-No, The black line is Tomorrow-No,The red line is Today-Yes, The brown line is Tomorrow-Yes

# # 3. Split data into training and test set

# In[ ]:


x1=data.iloc[:,0:21]
x2=data.iloc[:,22:]
X=pd.concat((x1,x2),axis=1)
Y=data["RainTomorrow"]


# In[ ]:


x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.2,random_state=42)


# In[ ]:


x_train.shape,y_train.shape


# # 4. Feature Engineering

# ## Outlier cleaning

# ### Visualization before outlier

# In[ ]:


def boxplot_for_outlier(df,columns):
    count = 0
    fig, ax =plt.subplots(nrows=2,ncols=7, figsize=(20,8))
    for i in range(2):
        for j in range(7):
            sns.boxplot(x = df[columns[count]], palette="Set2",ax=ax[i][j])
            count = count+1
boxplot_for_outlier(x_train,numerical_columns)


# ### Outlier cleaning for Train

# In[ ]:


lower_and_upper={}
x_train_outlier=x_train.copy()

for col in numerical_columns:
    if(col=="Rainfall"): 
        sparse_value = x_train[col].mode()[0]
        nonsparse_data = pd.DataFrame(x_train[x_train[col] != sparse_value][col])
        q1=nonsparse_data[col].describe()[4]
        q3=nonsparse_data[col].describe()[6]
        iqr=q3-q1
        lowerbound = q1 - (1.5*iqr)
        upperbound = q3 + (1.5*iqr)
        lower_and_upper[col]=(lowerbound,upperbound)
        nonsparse_data.loc[(nonsparse_data.loc[:,col]<lowerbound),col] =  lowerbound*0.75
        nonsparse_data.loc[(nonsparse_data.loc[:,col]>upperbound),col] =  upperbound*1.25
        x_train_outlier[col][nonsparse_data.index]=nonsparse_data[col]
        
    else:
        q1=x_train_outlier[col].describe()[4]
        q3=x_train_outlier[col].describe()[6]
        iqr=q3-q1
        lowerbound = q1 - (1.5 * iqr)
        upperbound = q3 + (1.5 * iqr)
        lower_and_upper[col]=(lowerbound,upperbound)
        number_of_outlier = x_train_outlier.loc[(x_train_outlier.loc[:,col]<lowerbound)                                                           | (x_train_outlier.loc[:,col]>upperbound)].shape[0]
        if(number_of_outlier>0):
            print(number_of_outlier," outlier values cleared in" ,col)
            x_train_outlier.loc[(x_train_outlier.loc[:,col]<lowerbound),col] =  lowerbound*0.75
            x_train_outlier.loc[(x_train_outlier.loc[:,col]>upperbound),col] =  upperbound*1.25


# ### Outlier cleaning for Test

# In[ ]:


x_test_outlier=x_test.copy()

for col in numerical_columns:
    if(col =="Rainfall"):
        sparse_value = x_test[col].mode()[0]
        nonsparse_data = pd.DataFrame(x_test[x_test[col] != sparse_value][col])
        nonsparse_data.loc[(nonsparse_data.loc[:,col]<lower_and_upper[col][0]),col] =  lower_and_upper[col][0]*0.75
        nonsparse_data.loc[(nonsparse_data.loc[:,col]>lower_and_upper[col][1]),col] =  lower_and_upper[col][1]*1.25
        x_test_outlier[col][nonsparse_data.index]=nonsparse_data[col]
        
    else:
        
        number_of_outlier_test = x_test_outlier.loc[(x_test_outlier.loc[:,col]<lower_and_upper[col][0]) |                                                    (x_test_outlier.loc[:,col]>lower_and_upper[col][1])].shape[0]
        if(number_of_outlier_test>0):
            print(number_of_outlier_test," outlier values cleared in" ,col)
            x_test_outlier.loc[(x_test_outlier.loc[:,col]<lower_and_upper[col][0]),col] =  lower_and_upper[col][0]*0.75
            x_test_outlier.loc[(x_test_outlier.loc[:,col]>lower_and_upper[col][1]),col] =  lower_and_upper[col][1]*1.25


# ### Visualization after outlier

# In[ ]:


boxplot_for_outlier(x_train_outlier,numerical_columns)


# In[ ]:


x_test[numerical_columns]=x_test_outlier[numerical_columns]
x_train[numerical_columns]=x_train_outlier[numerical_columns]


# ## Missing Value Imputation

# ### Missing Value Heatmap

# In[ ]:


msno.heatmap(data, figsize=(18,8))
plt.show()


# ### List for low missing values

# In[ ]:


zero_missing_rate=list(data_info[data_info["Missing_Value_Rate"]==0].index)
low_missing_rate=list(data_info[(data_info['Missing_Value_Rate']>0)&(data_info['Missing_Value_Rate']<=0.05)].index)
low_missing_rate.remove("RainToday")
low_missing_rate,zero_missing_rate


# ### Simple Imputer for Low Missing Values

# In[ ]:


def simple_imputer(data,columns):
    
    for col in columns:
        total_nan=int(data[col].isnull().sum())
        
        if(col in categorical_columns):
            
            most_frequent_value=data[col].value_counts().index[0]
            data[col]=data[col].fillna(most_frequent_value)
            
            print("A total of {} Categorical variable {} have been imputed.".format(total_nan,col))
            
        else:
            mean=data[col].mean()
            std=data[col].std()
            
            random_normal=np.random.normal(loc=mean,scale=std,size=total_nan) 
            data[col][data[col].isnull()]=random_normal
            
            print("A total of {} Numerical variable {} have been imputed.".format(total_nan,col))


# In[ ]:


simple_imputer(x_train,low_missing_rate)


# In[ ]:


simple_imputer(x_test,low_missing_rate)


# In[ ]:


Missing_Values(x_train[low_missing_rate])


# ###### Correlation of Rainfall and RainToday column missing values is 1. Column RainToday was Yes when the values in column Rainfall were greater than 1, and No when it was less than 1. Accordingly, a filling process will be made.

# In[ ]:


list1=pd.Series(x_train[x_train["RainToday"].isnull()]["Rainfall"])
list2=pd.Series(x_test[x_test["RainToday"].isnull()]["Rainfall"])


# In[ ]:


x_train["RainToday"].fillna(pd.Series(["Yes" if x>1 else "No" for x in list1],index=list1.index),inplace=True)


# In[ ]:


x_test["RainToday"].fillna(pd.Series(["Yes" if x>1 else "No" for x in list2],index=list2.index),inplace=True)


# In[ ]:


Missing_Values(x_train)


# ### TargetEncoder was made for columns with empty and categorical values, considering 'NaN' as a variable.

# In[ ]:


def target_encoder(train,test,columns):
    for col in columns:
        encoder = TargetEncoder()
        train[col]=encoder.fit_transform(train[col],y_train)
        test[col]=encoder.transform(test[col])
        print(test.loc[:,[col]].isnull().sum())
        print(train.loc[:,[col]].isnull().sum())


# In[ ]:


target_encoder_cols = ["WindDir9am","WindGustDir"]
x_train_encoder=x_train.copy()
x_test_encoder=x_test.copy()
target_encoder(x_train_encoder,x_test_encoder,target_encoder_cols)


# ### We made Model based filling for other empty columns. These models were XGBoost and KNN. Continued with KNN, which provides the best performance.

# In[ ]:


data_info_2=Missing_Values(x_train_encoder)
model_based_list=list(data_info_2["Variable"][data_info_2["Missing_Value_Rate"]>0.06])
model_based_list


# In[ ]:


from sklearn.impute import KNNImputer


# In[ ]:


knn_imputer=KNNImputer(n_neighbors=3)
x_test_mbi=x_test_encoder.copy()
x_train_mbi=x_train_encoder.copy()
for col in model_based_list:
    x_train_mbi[col] = knn_imputer.fit_transform(np.array(x_train_mbi[col]).reshape(-1,1),y_train)
    x_test_mbi[col] = knn_imputer.transform(np.array(x_test_mbi[col]).reshape(-1,1))
    print(x_test_mbi.loc[:,[col]].isnull().sum())
    print(x_train_mbi.loc[:,[col]].isnull().sum())


# In[ ]:


Missing_Values(x_train_mbi)


# ### Since our models could not train categorical variables, they were converted to numerical value with LabelEncoder.
# 

# In[ ]:


def Label_Encoder(df,columns,train_or_test):
    for col in columns:
        le = LabelEncoder()
        if(train_or_test == "test"):

            le.fit(x_train_mbi[col].copy().astype(str))
            df[col] = le.transform(df[col].copy().astype(str))

        else:
            df[col] = le.fit_transform(df[col].copy().astype(str))
    return df


# In[ ]:


x_test_mbi = Label_Encoder(x_test_mbi,["Location","RainToday","WindDir3pm"],"test")  


# In[ ]:


x_train_mbi = Label_Encoder(x_train_mbi,["Location","RainToday","WindDir3pm"],"train")


# # 5. Modelling

# In[ ]:


before_importance_scores=pd.DataFrame(columns=["scores"])


# ## XGBoost Classifier

# In[ ]:


from sklearn import metrics
import time
start_time = time.process_time()
xgb_model = xgb.XGBClassifier(n_estimators=150,random_state=0,learning_rate=0.1,eta=0.4,booster="gbtree",base_score=0.8,colsample_bylevel=0.9009229642844634,gamma=0.49967765132613584,
                        max_depth=6,min_child_weight=7,reg_lambda=0.27611902459972926,subsample=0.9300916052594785)

xgb_model.fit(x_train_mbi, y_train)
print(time.process_time()-start_time)
y_pred = xgb_model.predict_proba(x_test_mbi)
y_pred = y_pred[:, 1]

fpr, tpr, threshold = metrics.roc_curve(y_test, y_pred)
roc_auc = metrics.auc(fpr, tpr)
before_importance_scores.loc["XGboost Classifier"]=roc_auc

bc = BinaryClassification(y_test, y_pred, labels=["0", "1"])

# Figures
plt.figure(figsize=(5,5))
bc.plot_roc_curve()
plt.show()


# ## Lightm-GBM Classifier

# In[ ]:


start_time = time.process_time()
lgbm_model = lgb.LGBMClassifier(min_child_samples=25,n_estimators=150,subsample=0.11,
                                boosting_type="dart",learning_rate=0.25)

lgbm_model.fit(x_train_mbi, y_train)
print(time.process_time()-start_time)
y_pred = lgbm_model.predict_proba(x_test_mbi)
y_pred = y_pred[:, 1]

fpr, tpr, threshold = metrics.roc_curve(y_test, y_pred)
roc_auc = metrics.auc(fpr, tpr)
before_importance_scores.loc["LGBM Classifier"]=roc_auc


bc = BinaryClassification(y_test, y_pred, labels=["0", "1"])

# Figures
plt.figure(figsize=(5,5))
bc.plot_roc_curve()
plt.show()


# ## CatBoost Classifier

# In[ ]:


start_time = time.process_time()
cat_model = CatBoostClassifier(depth=10,max_bin=60,bagging_temperature= 0.2,random_strength=5)

cat_model.fit(x_train_mbi, y_train,verbose=False)
print(time.process_time()-start_time)
y_pred = cat_model.predict_proba(x_test_mbi)
y_pred = y_pred[:, 1]

fpr, tpr, threshold = metrics.roc_curve(y_test, y_pred)
roc_auc = metrics.auc(fpr, tpr)
before_importance_scores.loc["CatBoost Classifier"]=roc_auc

bc = BinaryClassification(y_test, y_pred, labels=["0", "1"])

# Figures
plt.figure(figsize=(5,5))
bc.plot_roc_curve()
plt.show()


# ## GradientBoosting Classifier

# In[ ]:


from sklearn.ensemble import GradientBoostingClassifier
start_time = time.process_time()
gradient_model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1,
                                                   max_depth=7, random_state=0)

gradient_model.fit(x_train_mbi, y_train)
print(time.process_time()-start_time)
y_pred = gradient_model.predict_proba(x_test_mbi)
y_pred = y_pred[:, 1]

fpr, tpr, threshold = metrics.roc_curve(y_test, y_pred)
roc_auc = metrics.auc(fpr, tpr)
before_importance_scores.loc["GradientBoosting Classifier"]=roc_auc

bc = BinaryClassification(y_test, y_pred, labels=["0", "1"])

# Figures
plt.figure(figsize=(5,5))
bc.plot_roc_curve()
plt.show()


# ## Logistic Regression

# In[ ]:


from sklearn.linear_model import LogisticRegression
start_time = time.process_time()
log_reg_model = LogisticRegression(C= 0.1, solver= 'liblinear',class_weight={1: 0.5, 0: 0.5},penalty="l1")

log_reg_model.fit(x_train_mbi, y_train)
print(time.process_time()-start_time)
y_pred = log_reg_model.predict_proba(x_test_mbi)
y_pred = y_pred[:, 1]


fpr, tpr, threshold = metrics.roc_curve(y_test, y_pred)
roc_auc = metrics.auc(fpr, tpr)
before_importance_scores.loc["Logistic Regression"]=roc_auc

bc = BinaryClassification(y_test, y_pred, labels=["0", "1"])

# Figures
plt.figure(figsize=(5,5))
bc.plot_roc_curve()
plt.show()


# ### Visualization before feature importance

# In[ ]:


import plotly.express as px
fig = px.bar(before_importance_scores, x=before_importance_scores.index, y='scores',height=400,width=900,text=round(before_importance_scores.scores,3),title="Visualization before feature importance")
fig.update_traces(marker_color='rgb(158,20,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
fig.show()


# ![](https://cdn.discordapp.com/attachments/703002285994672192/716668021233680394/before.png)

# # 6. Feature Importance

# In[ ]:


import operator
xgb_params = {"objective": "reg:linear", "eta": 0.01, "max_depth": 8, "seed": 42, "silent": 1}
num_rounds = 1000

dtrain = xgb.DMatrix(x_train_mbi, label=y_train)
gbdt = xgb.train(xgb_params, dtrain, num_rounds)

importance = gbdt.get_fscore()
importance = sorted(importance.items(), key=operator.itemgetter(1))

df = pd.DataFrame(importance, columns=['feature', 'fscore'])
df['fscore'] = df['fscore'] / df['fscore'].sum()

plt.figure()
df.plot()
df.plot(kind='barh', x='feature', y='fscore', legend=False, figsize=(6, 10))
plt.title('XGBoost Feature Importance')
plt.xlabel('relative importance')
plt.show()


# In[ ]:


lst=list(df["feature"][df["fscore"]<0.03])
lst


# In[ ]:


x_train_importance=x_train_mbi.drop(lst,axis=1)
x_test_importance=x_test_mbi.drop(lst,axis=1)


# ## Modelling after feature importance

# In[ ]:


after_importance_scores=pd.DataFrame(columns=["scores"])


# ## XGBoost Classifier

# In[ ]:


start_time = time.process_time()
xgb_model = xgb.XGBClassifier(n_estimators=150,random_state=0,learning_rate=0.1,eta=0.4,booster="gbtree",
                              base_score=0.8,colsample_bylevel=0.9009229642844634,gamma=0.49967765132613584,
                              max_depth=6,min_child_weight=7,reg_lambda=0.27611902459972926,
                              subsample=0.9300916052594785)

xgb_model.fit(x_train_importance, y_train)
print(time.process_time()-start_time)
y_pred = xgb_model.predict_proba(x_test_importance)
y_pred = y_pred[:, 1]

fpr, tpr, threshold = metrics.roc_curve(y_test, y_pred)
roc_auc = metrics.auc(fpr, tpr)
after_importance_scores.loc["XGboost Classifier"]=roc_auc


bc = BinaryClassification(y_test, y_pred, labels=["0", "1"])

# Figures
plt.figure(figsize=(5,5))
bc.plot_roc_curve()
plt.show()


# ## Light-GBM Classifier

# In[ ]:


start_time = time.process_time()
lgbm_model = lgb.LGBMClassifier(min_child_samples=25,n_estimators=150,subsample=0.11,
                                boosting_type="dart",learning_rate=0.25)

lgbm_model.fit(x_train_mbi, y_train)
print(time.process_time()-start_time)
y_pred = lgbm_model.predict_proba(x_test_mbi)
y_pred = y_pred[:, 1]

fpr, tpr, threshold = metrics.roc_curve(y_test, y_pred)
roc_auc = metrics.auc(fpr, tpr)
after_importance_scores.loc["LGBM Classifier"]=roc_auc

bc = BinaryClassification(y_test, y_pred, labels=["0", "1"])

# Figures
plt.figure(figsize=(5,5))
bc.plot_roc_curve()
plt.show()


# ## CatBoost Classifier

# In[ ]:


start_time = time.process_time()
cat_model = CatBoostClassifier(depth=10,max_bin=60,bagging_temperature= 0.2,random_strength=5)


cat_model.fit(x_train_mbi, y_train,verbose=False)
print(time.process_time()-start_time)
y_pred = cat_model.predict_proba(x_test_mbi)
y_pred = y_pred[:, 1]

fpr, tpr, threshold = metrics.roc_curve(y_test, y_pred)
roc_auc = metrics.auc(fpr, tpr)
after_importance_scores.loc["CatBoost Classifier"]=roc_auc

bc = BinaryClassification(y_test, y_pred, labels=["0", "1"])

# Figures
plt.figure(figsize=(5,5))
bc.plot_roc_curve()
plt.show()


# ## GradientBoosting Classifier

# In[ ]:


start_time = time.process_time()
gradient_model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1,
                                                   max_depth=7, random_state=0)

gradient_model.fit(x_train_mbi, y_train)
print(time.process_time()-start_time)
y_pred = gradient_model.predict_proba(x_test_mbi)
y_pred = y_pred[:, 1]

fpr, tpr, threshold = metrics.roc_curve(y_test, y_pred)
roc_auc = metrics.auc(fpr, tpr)
after_importance_scores.loc["GradientBoosting Classifier"]=roc_auc

bc = BinaryClassification(y_test, y_pred, labels=["0", "1"])

# Figures
plt.figure(figsize=(5,5))
bc.plot_roc_curve()
plt.show()


# ## Logistic Regression

# In[ ]:


from sklearn.linear_model import LogisticRegression
start_time = time.process_time()
log_reg_model = LogisticRegression(C= 0.1, solver= 'liblinear',class_weight={1: 0.5, 0: 0.5},penalty="l1")

log_reg_model.fit(x_train_importance, y_train)
print(time.process_time()-start_time)
y_pred = log_reg_model.predict_proba(x_test_importance)
y_pred = y_pred[:, 1]

fpr, tpr, threshold = metrics.roc_curve(y_test, y_pred)
roc_auc = metrics.auc(fpr, tpr)
after_importance_scores.loc["Logistic Regression"]=roc_auc

bc = BinaryClassification(y_test, y_pred, labels=["0", "1"])

# Figures
plt.figure(figsize=(5,5))
bc.plot_roc_curve()
plt.show()


# ### Visualization after feature importance
# 

# In[ ]:


import plotly.express as px
fig = px.bar(after_importance_scores, x=before_importance_scores.index, y='scores',height=400,width=900,text=round(after_importance_scores.scores,3),title="Visualization after feature importance")
fig.update_traces(marker_color='rgb(180,60,50)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.7)
fig.show()


# ![](https://cdn.discordapp.com/attachments/703002285994672192/716668019140460584/after.png)

# # 7.Predict results

# ## Visualization for After Feature Importance and Before Feature Importance
# 

# In[ ]:


import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Bar(
    x=before_importance_scores.index,
    y=before_importance_scores.scores,
    name='Before Importance',text=round(before_importance_scores.scores,3),textposition='auto',
    marker_color='purple'
))
fig.add_trace(go.Bar(
    x=after_importance_scores.index,
    y=after_importance_scores.scores,
    name="After Importance",text=round(after_importance_scores.scores,3),textposition='auto',
    marker_color='pink'
))

fig.update_layout(barmode='group', xaxis_tickangle=-30,title="Visualization for After Feature Importance and Before Feature Importance")
fig.show()


# ![](https://cdn.discordapp.com/attachments/703002285994672192/716668024374951977/vs.png)

# ## Conclusion 
# 
# ### In this project, 5 machine learning algorithms were used. The CatBoost Algorithm has a higher accuracy rate  than other algorithms by a little difference. We saw that There is no big difference in accuracy rate after feature importance is done. The training time of LightGBM algorithm is faster than others.
# 
# ### <p style='color:#561225'><i>I hope you find this kernel useful. If you like it please do an upvote.</i><p>
