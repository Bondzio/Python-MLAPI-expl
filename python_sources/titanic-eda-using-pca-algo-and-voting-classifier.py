#!/usr/bin/env python
# coding: utf-8

# ## Importing required Libraries

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.preprocessing import LabelEncoder,Normalizer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from lightgbm import LGBMClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score,r2_score
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split,GridSearchCV
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from itertools import combinations
# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

os.chdir("/kaggle/working/")
# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# ## Importing and Viewing Datasets

# In[ ]:


titanic_train = pd.read_csv("/kaggle/input/titanic/train.csv")


# In[ ]:


titanic_test = pd.read_csv("/kaggle/input/titanic/test.csv")


# In[ ]:


titanic_train.head()


# In[ ]:


titanic_test.head()


# ## Visualizations and EDA

# ### Will I survive this, mate?

# In[ ]:


plt.rcParams['figure.figsize'] = (10,3)
plot = sns.countplot(x = 'Survived', data=titanic_train)
plt.xlabel('whether passenger survived?')
plt.ylabel('# of passengers')
plt.title('Survivors Count')
for txt in plot.texts:
    txt.set_visible(False)


# The graph is more skewed towards death of passengers amounting to 60%, while only about 40% survived the disaster. 

# ### Women and Children please hurry, get to the life boat!

# In[ ]:


df = titanic_train[['Sex','Survived']]
grouped_df = df.groupby('Sex')
survivor_percent = grouped_df.sum().values.T*100/grouped_df.apply(len).values
survivor_percent = survivor_percent[0]
gender = list(grouped_df.sum().index)
plt.rcParams['figure.figsize'] = (10,3)
plot = plt.barh(gender,survivor_percent,color=['orange','green'])
plt.title('Gender-wise Survival Percentage')
plt.xlabel('Survival %')


# It appears that survival percent among females were more than 50% percent higher than male. Probably because Women and children might have gotten first preference to take up Lifeboats and Lifevests. It will be a useful feature in our model prediction

# ### As you will, Your Majesty!
# We observe that many passengers have title of Mr, Mrs, Col., Mistress etc. Let's observe whether having a respectable title entitles them to life-boat, life-vest privileges. 

# In[ ]:


title_df = titanic_train[['Name','Survived']]
title_df['Title'] = title_df['Name'].apply(lambda x:x.split(',')[1].split('.')[0].strip())
grouped_df = title_df.groupby('Title')
survivor_percent = grouped_df.sum().values.T*100/grouped_df.apply(len).values
survivor_percent = survivor_percent[0]
titles = list(grouped_df.sum().index)
plt.rcParams['figure.figsize'] = (10,3)
plt.barh(titles,survivor_percent,color=['orange','green','blue','red','pink','lime','yellow','brown','grey'])
plt.xlabel('Survival %')
plt.ylabel('Title')
plt.title('Title of Passengers vs Survival %')


# We see that Title of a passenger aboard the ship also played a huge role in their survival of the wreckage. Nobel Titles like Sir, Countess, Lady and other titles like Mme, Mile, Ms ensured definite survival of 100%. While the titles like Jonkheer, Don, Rev are attributed with no survival.

# ### Are you alone, my dear child?
# Let us see whether Passengers traveling alone or those traveling with family members had higher chances of survival.

# In[ ]:


df = titanic_train[['Name','Parch','SibSp','Survived']]
alone_df = df[(df['Parch'] == 0) & (df['SibSp'] == 0)]
not_alone_df = df[(df['Parch'] != 0) | (df['SibSp'] != 0)]
survival_percent = []
passenger_type = ['Without Family Members','With Family Members']
for df_type in [alone_df,not_alone_df]:
    survival_percent.append(df_type['Survived'].sum()*100/len(df))
plt.barh(passenger_type,survival_percent,color=['green','orange'])
plt.xlabel('Survival %')
plt.title('Survival % comparsion of passengers with and without family members aboard the ship')


# So, passengers with Family Members slightly had more survival % compared to passengers without Family Members on the ship, which makes sense as passengers with Family Members include women, children, elderly who could have been given more priority in case of evacuation compared to healthy male adults. 

# ### Does costly and classy ticket comes with the perk of saving life? 
# Let us check fare of tickets, class of tickets vs survival percent. 

# In[ ]:


df = titanic_train[['Fare','Survived','Ticket','Pclass']]
print("The minimum fare of ticket is: ",min(list(df['Fare'])))
print("The maximum fare of ticket is:",max(list(df['Fare'])))


# Let us divide the fare prices into 4 categories: 
# Cheap (0-128.25), Decent (128.25-256.5), Fairly High (256.5-384.75), Costly (384.75-513).

# In[ ]:


price_interval = [(0,128.25),(128.25,256.5),(256.5,384.75),(384.75,513)]
ticket_type = ['Cheap','Decent','Fairly High','Costly']
survivor_percent = []
for interval in price_interval:
    fare_df = df[(df['Fare']>=interval[0]) & (df['Fare']<interval[1])]
    percent = fare_df['Survived'].sum()*100/len(fare_df)
    survivor_percent.append(percent)
plt.subplot(1,2,1)
plt.pie(survivor_percent,autopct='%1.1f%%',explode=(0,0,0,0.1))
plt.legend([tk_type+': Survivor %: '+str(round(pct,2)) 
           for tk_type,pct in zip(ticket_type,survivor_percent)],bbox_to_anchor=(1,0))
plt.title('Survivor % based on price of tickets bought by passengers')
plt.subplot(1,2,2)
ticket_class_df = df[['Pclass','Survived']]
grouped_df = ticket_class_df.groupby('Pclass')
survivor_percent = grouped_df.sum().T.values[0]*100/grouped_df.apply(len).values
class_list = list(grouped_df.sum().index)
plt.barh(class_list,survivor_percent,color=['orange','green','blue'])
plt.title('Survivor % based on ticket class bought by passengers')
plt.xlabel('Survivor %')
plt.ylabel('Ticket Class')


# So, we see that Costly tickets and high class tickets does come out with high survival offer! It does makes sense because these tickets bought by people of high-class and title, who were given preference during evacuation of sinking ship. Although, between passengers who bought tickets at decent price have 12% more survival percent than those bought at Fairly High price. On the basis of class, 3rd class tickets have very low survival rate while 1st class tickets have more than 60%  survival rate.   

# ### Cabin in the Sinking Ship: A survivor's safe haven?

# In[ ]:


df = titanic_train[['Cabin','Survived']]
df['Cabin'] = df.fillna('Unknown')['Cabin']
group_df = df.groupby('Cabin')
cabin_no = list(group_df.sum().index)
survivor_percent = group_df.sum().values.T[0]*100/group_df.apply(len).values
cabin_df = pd.DataFrame({'Cabin no.':cabin_no,'Survivor %':survivor_percent})
unknown = len(df[df['Cabin']=='Unknown'])*100/len(df)
print("Percentage of Unknown Cabins:",unknown)
plt.rcParams['figure.figsize'] = (20,3)
plot = sns.scatterplot(data = cabin_df,x = 'Cabin no.',y = 'Survivor %')
plt.xticks(rotation=90)
for txt in plot.texts:
    txt.set_visible(False)


# So we see that Cabin is a good feature to describe the passenger's survival. There are majority of cabins that have either no survivors or all survivors. Few cabins having 50-60% survivors. But the problem comes with number of Unknown Cabins in the dataset is more than 70%. This analysis holds for only 30% of the dataset. So that's why this feature might have to be dropped during model training.

# ### Captain! Let's embark on the journey to save as many people as we can 
# Let's check whether port of Embarkation has any influence on the survival rate 

# In[ ]:


df = titanic_train[['Embarked','Survived']]
grouped_df = df.groupby('Embarked')
embarked_port = list(grouped_df.sum().index)
fullname_dict = {'S':'Southampton','C':'Cherbourg','Q':'Queenstown'}
survivor_percent = grouped_df.sum().values.T[0]*100/grouped_df.apply(len)
plt.barh([fullname_dict[port] for port in embarked_port],survivor_percent,
        color=['orange','green','red'])
plt.xlabel('Survivor %')
plt.title('Port of Embarkation vs Survival %')


# We see that people who boarded ship from Cherbourg port have the highest survival percent of more than 55% while the people who boarded ship from Southampton have the lowest survival percent of about 35%.

# ## Feature Engineering & Model Training

# ### Adding Title column to train and test dataset

# In[ ]:


titanic_train['Title'] = titanic_train['Name'].apply(lambda x:x.split(',')[1].split('.')[0].strip())
titanic_test['Title'] = titanic_test['Name'].apply(lambda x:x.split(',')[1].split('.')[0].strip())


# ### Percentage of null values in columns

# ### For train data

# In[ ]:


new_train = titanic_train.drop(['PassengerId','Name'],axis=1)


# In[ ]:


print("Percentage of null values in different columns:")
new_train.isnull().sum()*100/len(new_train)


# Dropping Cabin column as discussed earlier since it has more 70% null values

# In[ ]:


new_train = new_train.drop(['Survived','Cabin'],axis=1)


# ### For test data

# In[ ]:


new_test = titanic_test.drop(['PassengerId','Name'],axis=1)
print("Percentage of null values in different columns:")
new_test.isnull().sum()*100/len(new_test)


# Dropping Cabin column here also

# In[ ]:


new_test = new_test.drop('Cabin',axis=1)


# ### Combining train and test data

# Here we are combining the train test data to fill the missing values in the required columns. I have added a data column which signifies whether the record is from train data or test data, so that it becomes easy to split back into train and test data.

# In[ ]:


new_train['data'] = ['train']*len(new_train)
new_test['data'] = ['test']*len(new_test)
train_test_data = pd.concat([new_train,new_test])
train_test_data.index = range(len(train_test_data))
print('Percentage of null columns in the combined data:')
train_test_data.isnull().sum()*100/len(train_test_data)


# ### Treating Null values
# 

# We will be predicting missing age values using Random Forest Regressor model. But before that, let us fill Embarked Column and Fare Column with Mode and Median respectively because Median is the best option for filling data irrespective of presence of outliers or not.
# 
# After filling outliers, we have one-hot encoded categorical features: Ticket, Pclass, Sex, Embarked and Title. It leads to more than 400+ columns which necessitates the use of PCA for dimensionality reduction. I have chosen the threshold of 80% variance to be captured by the required number out of 400+ features, which I felt yielded good train accuracy and thus is sufficient enough. 

# In[ ]:


categorical_features = ['Ticket','Pclass','Sex','Embarked','Title']
encoded_train_test = train_test_data.copy()
encoded_train_test.drop('data',inplace=True,axis=1)

#Filling Missing Embarked Column with its Mode, Fare Column with Median
encoded_train_test['Embarked'] = encoded_train_test.fillna(encoded_train_test['Embarked'].mode()[0])['Embarked']
encoded_train_test['Fare'] = encoded_train_test.fillna(encoded_train_test['Fare'].median())['Fare']
#One-hot Encoding
for i in categorical_features:
    encoded_train_test = pd.concat([encoded_train_test, pd.get_dummies(encoded_train_test[i],prefix=i)],axis=1).drop(i,axis=1)
#Splitting into test data containing null values and train data containing non-null values of Age 
train_before_pca = encoded_train_test.copy()

#Outlier Treatment through transformation: Refer the Outlier treatment section 
#below on why I chose these functions

train_before_pca['Age'] = np.cbrt(train_before_pca['Age']-30)
train_before_pca['Fare'] = np.cbrt(np.log(train_before_pca['Fare']+5))
train = train_before_pca[train_before_pca['Age'].notna()]
X_train = train.drop('Age',axis=1)
Y_train = train['Age']
test = train_before_pca[train_before_pca['Age'].isna()]
X_test = test.drop('Age',axis=1)

#Applying PCA to determine no. of features for the given threshold
pca_train = PCA()
X_train_pca = pca_train.fit_transform(X_train)
variance_percent = pca_train.explained_variance_ratio_*100
threshold = 80
total_percent = 0
feature_count = 0
for percent in variance_percent:
    if(total_percent<threshold):
        total_percent+=percent
        feature_count+=1
print("Required no. of features to achieve "+str(threshold)+"% of total variance:",feature_count)

#For train data having ages values
pca_train = PCA(feature_count)
X_train_pca = pca_train.fit_transform(X_train)
col_list = []
for i in range(1,X_train_pca.shape[1]+1):
    col_list.append('PCA'+str(i))
X_train_pca = pd.DataFrame(data = X_train_pca,columns = col_list)

#For test data not having ages values
pca_test = PCA(feature_count)
X_test_pca = pca_train.fit_transform(X_test)
X_test_pca = pd.DataFrame(data = X_test_pca,columns = col_list)

#Displaying train R2-score
rf = RandomForestRegressor(random_state = 1)
rf.fit(X_train_pca,Y_train)
print("Train R2 score for Random Forest: ", r2_score(Y_train,rf.predict(X_train_pca)))

#Filling missing Age values
predicted_missing_ages = np.power(rf.predict(X_test_pca),3)+30
null_age_indices = list(X_test.index)
encoded_train_test.loc[null_age_indices,'Age'] = predicted_missing_ages
encoded_train_test['data'] = list(train_test_data['data'])   


# ### Outlier Treatment

# ### Before Transformation

# In[ ]:


plt.subplot(1,2,1)
sns.boxplot(encoded_train_test['Age'])
plt.subplot(1,2,2)
sns.boxplot(encoded_train_test['Fare'])


# ### After transformation

# In[ ]:


plt.subplot(1,2,1)
sns.boxplot(np.cbrt(encoded_train_test['Age']-30))
plt.subplot(1,2,2)
sns.boxplot(np.cbrt(np.log(encoded_train_test['Fare']+5)))


# In[ ]:


encoded_train_test['Age'] = np.cbrt(encoded_train_test['Age']-30)
encoded_train_test['Fare'] = np.cbrt(np.log(encoded_train_test['Fare']+5))


# In[ ]:


encoded_train_test.head()


# ### Applying PCA
# The process of applying PCA is same as before followed for filling age values through Random Forest Model prediction. Here, the variance threshold is set to 90%, as it yielded best result for me. 

# In[ ]:


train_test_before_pca = encoded_train_test.iloc[:,:-1]
pca = PCA()
train_test_after_pca = pca.fit_transform(train_test_before_pca)
variance_percent = pca.explained_variance_ratio_*100
threshold = 90
total_percent = 0
feature_count = 0
for percent in variance_percent:
    if(total_percent<threshold):
        total_percent+=percent
        feature_count+=1
print("Required no. of features to achieve "+str(threshold)+"% of total variance:",feature_count)
pca = PCA(feature_count)
train_test_after_pca = pca.fit_transform(train_test_before_pca)
col_list = []
for i in range(1,train_test_after_pca.shape[1]+1):
    col_list.append('PCA'+str(i))
train_test_after_pca = pd.DataFrame(data = train_test_after_pca,columns = col_list)


# Adding Data column from encoded_train_test 

# In[ ]:


train_test_after_pca['data'] = list(encoded_train_test['data'])


# Splitting using data column into original train and test data

# In[ ]:


train_after_pca = train_test_after_pca[train_test_after_pca['data']=='train'].iloc[:,:-1]
test_after_pca = train_test_after_pca[train_test_after_pca['data']=='test'].iloc[:,:-1]
train_label = titanic_train['Survived']


# ### Train-Validation Set Split

# In[ ]:


X_train,X_test,Y_train,Y_test = train_test_split(train_after_pca,train_label,test_size=0.3,random_state=0)


# This function selects the best model parameters among the given set of parameters to maximize the validation test accuracy  

# In[ ]:


def best_model_param(model,params_dict):
    best_param_dict = 0
    best_score = 0
    param_values = list(params_dict.values())
    param_keys = list(params_dict.keys())
    param_values_flatten = []
    [param_values_flatten.extend(val) for val in param_values]
    comb_list = list(combinations(param_values_flatten,len(param_keys)))
    comb_param_values = []
    for comb in comb_list:
        temp = []
        for param in param_values: 
            temp.append(len(set(comb).intersection(set(param))))
        if temp==[1]*len(param_keys):
            comb_param_values.append(comb)
    for comb in comb_param_values:
        model = model.set_params(**dict(zip(param_keys,comb)))
        model.fit(X_train,Y_train)
        score = accuracy_score(Y_test,model.predict(X_test))
        if(score>best_score):
            best_score = score
            best_param_dict = dict(zip(param_keys,comb))
    return best_param_dict


# ### Selecting best model parameters for each model
# Commented during runtime to save execution time

# In[ ]:


#param_dict = {"n_estimators":[50,100,200],
#              "max_features" :list(range(1,len(list(X_train.columns))+1)),
#              "random_state":[10]}
#rf = RandomForestClassifier()
#best_param_dict = best_model_param(rf,param_dict)
#print(best_param_dict)
rf = RandomForestClassifier(n_estimators = 100, max_features = 10, random_state = 10)


# In[ ]:


#param_dict = {"C":np.arange(0.1,1.1,0.1),"max_iter":range(100,1100,100)}
#log_reg = LogisticRegression()
#best_param_dict = best_model_param(log_reg,param_dict)
#print(best_param_dict)
log_reg = LogisticRegression(C=0.9,max_iter=100)


# In[ ]:


#param_dict = {"learning_rate":[0.001,0.01,0.1,1],"n_estimators":[50,100,200],"random_state":[10]}
#lgbm = LGBMClassifier()
#best_param_dict = best_model_param(lgbm,param_dict)
#print(best_param_dict)
lgbm = LGBMClassifier(learning_rate = 0.01,n_estimators = 200,random_state = 10)


# In[ ]:


#param_dict = {"C":[0.01,0.1,1,10],"gamma":[0.01,0.1,1,10]}
#svc = SVC()
#best_param_dict = best_model_param(svc,param_dict)
#print(best_param_dict)
svc = SVC(C=1,gamma=1)


# In[ ]:


#param_dict = {"max_features" :list(range(1,len(list(X_train.columns))+1)),
#              "random_state":[10]}
#dtc = DecisionTreeClassifier()
#best_param_dict = best_model_param(dtc,param_dict)
#print(best_param_dict)
dtc = DecisionTreeClassifier(max_features=10,random_state=10) 


# In[ ]:


#param_dict = {"activation":["logistic","tanh","relu"],
#              "solver":["adam"],
#              "hidden_layer_sizes":[(100,),(1000,),(10000,)]}
#mlp = MLPClassifier()
#best_param_dict = best_model_param(mlp,param_dict)
#print(best_param_dict)
mlp = MLPClassifier(activation='logistic',solver='adam',hidden_layer_sizes = (1000,))


# ### Fitting Models

# In[ ]:


rf.fit(X_train,Y_train)
log_reg.fit(X_train,Y_train)
naive_bayes_model = GaussianNB()
naive_bayes_model.fit(X_train,Y_train)
lgbm.fit(X_train,Y_train)
svc.fit(X_train,Y_train)
dtc.fit(X_train,Y_train)
mlp.fit(X_train,Y_train)


# ### Printing accuracy of each models on train-validation set

# In[ ]:


Y_train_pred = rf.predict(X_train)
Y_test_pred = rf.predict(X_test)
print("For Random Forest:")
print("Train set accuracy score:",accuracy_score(Y_train,Y_train_pred))
print("Test set accuracy score:",accuracy_score(Y_test,Y_test_pred))


# In[ ]:


Y_train_pred = lgbm.predict(X_train)
Y_test_pred = lgbm.predict(X_test)
print("For Light GBM:")
print("Train set accuracy score:",accuracy_score(Y_train,Y_train_pred))
print("Test set accuracy score:",accuracy_score(Y_test,Y_test_pred))


# In[ ]:


Y_train_pred = log_reg.predict(X_train)
Y_test_pred = log_reg.predict(X_test)
print("For Logistic Regression:")
print("Train set accuracy score:",accuracy_score(Y_train,Y_train_pred))
print("Test set accuracy score:",accuracy_score(Y_test,Y_test_pred))


# In[ ]:


Y_train_pred = svc.predict(X_train)
Y_test_pred = svc.predict(X_test)
print("For Support Vector:")
print("Train set accuracy score:",accuracy_score(Y_train,Y_train_pred))
print("Test set accuracy score:",accuracy_score(Y_test,Y_test_pred))


# In[ ]:


Y_train_pred = mlp.predict(X_train)
Y_test_pred = mlp.predict(X_test)
print("For Multi Layer Perceptron:")
print("Train set accuracy score:",accuracy_score(Y_train,Y_train_pred))
print("Test set accuracy score:",accuracy_score(Y_test,Y_test_pred))


# In[ ]:


Y_train_pred = dtc.predict(X_train)
Y_test_pred = dtc.predict(X_test)
print("For Decision Tree Classifier:")
print("Train set accuracy score:",accuracy_score(Y_train,Y_train_pred))
print("Test set accuracy score:",accuracy_score(Y_test,Y_test_pred))


# In[ ]:


Y_train_pred = naive_bayes_model.predict(X_train)
Y_test_pred = naive_bayes_model.predict(X_test)
print("For Naive Bayes:")
print("Train set accuracy score:",accuracy_score(Y_train,Y_train_pred))
print("Test set accuracy score:",accuracy_score(Y_test,Y_test_pred))


# So, Decision Tree and Naive Bayes model won't be taken into Voting Classifier because of three reasons:
# * Decision Tree is prone to overfitting, so it might predict incorrect values on unknown test data, which might further worsen the predictions of this Classifier
# * Naive Bayes requires strict non-collinearity among features which is not always true in real-life dataset so it can impact the predictions
# * I have tried adding the above two models to the Classifier, it reduces the accuracy score.

# ### Train-Validation Set score by the Voting Classifier

# In[ ]:


vc = VotingClassifier(estimators=[('rf',rf),('log_reg',log_reg),
                                  ('svc',svc),('lgbm',lgbm),
                                  ('mlp',mlp)],voting='hard')
vc.fit(X_train,Y_train)
Y_train_pred = vc.predict(X_train)
Y_test_pred = vc.predict(X_test)
print("For Voting Classifier:")
print("Train set accuracy score:",accuracy_score(Y_train,Y_train_pred))
print("Test set accuracy score:",accuracy_score(Y_test,Y_test_pred))


# In[ ]:


vc.fit(train_after_pca,train_label)


# ### Outputting results

# In[ ]:


Y_pred = vc.predict(test_after_pca)
result = pd.DataFrame({'PassengerId':list(titanic_test['PassengerId']),'Survived':list(Y_pred)})
result.to_csv('/kaggle/working/VotingClassifier.csv',index=False)

