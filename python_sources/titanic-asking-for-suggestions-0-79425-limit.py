#!/usr/bin/env python
# coding: utf-8

# ### Importing default modules

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ### Importing Data

# In[ ]:


train = pd.read_csv('/kaggle/input/titanic/train.csv')
test = pd.read_csv('/kaggle/input/titanic/test.csv')


# ### Initial Data Check

# In[ ]:


print('\n',train.info())

print('\nNaN values in the training dataset\n\n',train.isna().sum())


# We have 891 rows, 12 columns: 7 int or str and 5 of oblect type.
# Also there are some missing values in 'Age','Cabin' and 'Embarked' columns on which we must work a bit

# ### Filling NaN values
# 
# First of all let`s fill NaN values for both training and testing dataset.

# In[ ]:


train.Age.hist(bins = 20)


# Let us simply fill NaN in age with its median or mean value.
# Note, there is another aproach in internet, you can group passangers by 'Sex' and 'Pclass' and assign median values.

# In[ ]:


train.Embarked.value_counts()


# For 'Embarked' column we fill NaN values with th emost frequent values i.e 'Q'

# In[ ]:


train.Cabin.value_counts()[:10]


# And for carbin we just assign int values 1 where cabin presents and 0 if it is NaN

# In[ ]:


# we repeat the same data cleaning for train and test sets
for data in [train,test]:
    
    #gr = data.groupby(['Sex','Pclass'])
    #data.Age = gr.Age.apply(lambda x: x.fillna(x.median()))
    
    
    # Lets simply fill NaN in Age by median value
    data.Age.fillna(data.Age.mean(),inplace = True)
    # Lets simply fill NaN in Embarked by the most frequent value
    data.Embarked.fillna('S',inplace=True)
    # Lets simply fill NaN in Cabin by 0 and by 1 if there is any value
    data.Cabin.fillna(0,inplace=True)
    # Also there are missing Fare values in test set. Lets fill it with mean value as well as Age
    data.Fare.fillna(data.Fare.mean(),inplace=True)


# ### Additional Features

# Additionaly, we can create new feature as suggested in many notebooks namely Family size (FamSize). That is sum of Siblings and parents on the bord.

# In[ ]:


# We need ids later on for submission
test_id = test['PassengerId']

for data in [train,test]:
    # We need ids later on for submission
    data.drop(['PassengerId','Ticket'],axis=1,inplace=True)    # We won`t use this values as features
    data['Name']     =  data['Name'].apply(lambda x: len(x)) # as suggested in few notebooks
    data['FamSize'] = data['SibSp']+data['Parch']+1 


# ### Values coding

# In[ ]:


for data in [train,test]:
    
    # Lets create new feature Single, which is 0 if FamSize == 1 else 1
    data['Single']   = data['FamSize'].apply(lambda x: 1 if x == 1 else 0)
    # Lets simply fill NaN in Cabin by 0 and by 1 if there is any value
    data['Cabin']    = data['Cabin'].apply(lambda x: 1 if x != 0 else 0)
    
    
    
    #data['Sex']      = data['Sex'].apply(lambda x: 0 if x == 'female' else 1)
    #data['Embarked'] = data['Embarked'].apply(lambda x: 0 if x == 'C' else (1 if x == 'S' else 'Q'))


# ### Bin some numerical features
# 
# Also we can try to add new categorical features and try to bin Age,Fare,FamSize in bins.
# Which later on will be encoded with sklearn tools

# In[ ]:


for data in [train,test]:
    
    data['AgeBin']    = pd.cut(data['Age']     , bins = 5, labels = ['child','teen','adult','old','oldest'])
    data['FareBin']   = pd.cut(data['Fare']    , bins = 5, labels = ['lowest','low','inter','high','highest'])
    data['FamBin']   = pd.cut(data['FamSize'], bins = 3, labels = ['small','inter','big'])


# ### Create training and validation splits based on train.csv
# 
# First of all we divide our initial on X (features) and y(labels-Survived)
# 
# Aproachin training part, lets divide training set on train and validation. Validation we will use for hyperparameters optimisation with the help of GridSearchCV.

# In[ ]:


from sklearn.model_selection import train_test_split,cross_val_score

X = train.drop(['Survived'],axis=1)
y = train['Survived']

X_train,X_val,y_train,y_val = train_test_split(X,y,test_size=0.33, random_state = 42,shuffle=True)


# ### Importing necessary modules from sklearn

# In[ ]:


# Makes life easier later on
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline

# We need this moduls for encoding
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Our Classifiers
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier 
from sklearn.svm import SVC

# This is cool thing. Helps to 'ensemble' many classifiers together and make better predictions
from sklearn.ensemble import VotingClassifier

# For hyperparameters optimisation
from sklearn.model_selection import cross_val_score,GridSearchCV


# We will use two types of column_transformers. One with scalling int/float values and one without scaling.
# It was observed that SVC performs poorly is there is no any scaling. That is why we use MinMaxScaller(StandardScaler)
# in it pipline.
# 
# For both we use OneHotEncoding to encode categorical and object data type 

# In[ ]:


transformer_trees = make_column_transformer(
    #(MinMaxScaler(),['Name','Age','Fare','FamSize','SibSp','Parch']),
    #(OrdinalEncoder(),['Pclass',]),
    (OneHotEncoder(),['Sex','Single','Cabin','Embarked','AgeBin','FareBin','FamBin']),
    remainder = 'passthrough'
)

transformer_svc = make_column_transformer(
    (MinMaxScaler(),['Name','Age','Fare','FamSize','SibSp','Parch']),
    #(OrdinalEncoder(),['Pclass',]),
    (OneHotEncoder(),['Sex','Single','Cabin','Embarked','AgeBin','FareBin','FamBin']),
    remainder = 'passthrough'
)


# ### 1. Random Forest Classifier

# In[ ]:


clf_rfc = RandomForestClassifier(bootstrap=False,random_state=42)

param_grid_rfc = {'randomforestclassifier__n_estimators':[x for x in range(10,100,10)],
                  'randomforestclassifier__max_depth':[2,5,10,15],
                 }


line_rfc = make_pipeline(transformer_trees,
                         clf_rfc)

search_rfc = GridSearchCV(line_rfc,param_grid_rfc,
                      cv=5,
                      scoring='accuracy',
                      verbose=1,
                      n_jobs=-1,)

search_rfc.fit(X_train,y_train)
pipe_rfc = search_rfc.best_estimator_

print("Best parameter (CV score=%0.3f):" % search_rfc.best_score_)
print(search_rfc.best_params_)

pipe_rfc.fit(X_train,y_train)
print('Train score: ', pipe_rfc.score(X_train,y_train))
print('Val score: ', pipe_rfc.score(X_val,y_val))


# ### 2. Gradient Boosting Classifier

# In[ ]:


clf_gbc = GradientBoostingClassifier(random_state=42)

param_grid_gbc = {'gradientboostingclassifier__n_estimators':[x for x in range(10,50,10)],
                  'gradientboostingclassifier__max_depth':[2,5,10],
                  'gradientboostingclassifier__learning_rate':[0.1,0.5,0.7]
                 }


line_gbc = make_pipeline(transformer_trees,
                         clf_gbc)

search_gbc = GridSearchCV(line_gbc,param_grid_gbc,
                      cv=5,
                      scoring='accuracy',
                      verbose=1,
                      n_jobs=-1,)

search_gbc.fit(X_train,y_train)
pipe_gbc = search_gbc.best_estimator_

print("Best parameter (CV score=%0.3f):" % search_gbc.best_score_)
print(search_gbc.best_params_)

pipe_gbc.fit(X_train,y_train)
print('Train score: ', pipe_gbc.score(X_train,y_train))
print('Val score: ', pipe_gbc.score(X_val,y_val))


# ### 3. SVC

# In[ ]:


clf_svc = SVC(random_state = 42,probability = True)

param_grid_svc = {'svc__C':[x for x in np.arange(0.01,0.1,0.01)],
                  'svc__gamma':[x for x in [0.01,0.05,0.7,0.1]],
                  'svc__kernel':['rbf']
                 }

line_svc = make_pipeline(transformer_svc,
                         clf_svc)

search_svc = GridSearchCV(line_svc,param_grid_svc,
                          cv=5,
                          scoring='accuracy',
                          verbose=1,
                          n_jobs=-1,)

search_svc.fit(X_train,y_train)

pipe_svc = search_svc.best_estimator_

print("Best parameter (CV score=%0.3f):" % search_svc.best_score_)
print(search_svc.best_params_)

pipe_svc.fit(X_train,y_train)

print('Train score: ', pipe_svc.score(X_train,y_train))
print('Val score: ', pipe_svc.score(X_val,y_val))


# ### Ensemble

# In[ ]:


pipe_ens = VotingClassifier(estimators=[('rfc',pipe_rfc),
                                        ('svc',pipe_svc),
                                        ('gbc',pipe_gbc)],
                            voting='soft',n_jobs=-1)

pipe_ens.fit(X_train,y_train)

print('Train score: ', pipe_ens.score(X_train,y_train))
print('Val score: ', pipe_ens.score(X_val,y_val))


# ### Submission

# In[ ]:


pred = pipe_ens.predict(test)
sub = pd.DataFrame({'PassengerId': test_id, 'Survived': pred})
sub.to_csv('submission.csv',index=False)


# In[ ]:


# You can also consider outlier detection to be used
#------------------------------------------------------------------------------
# accept a dataframe, remove outliers, return cleaned data in a new dataframe
# see http://www.itl.nist.gov/div898/handbook/prc/section1/prc16.htm
#------------------------------------------------------------------------------
#def remove_outlier(df_in, col_name):
    #q1 = df_in[col_name].quantile(0.25)
    #q3 = df_in[col_name].quantile(0.75)
    #iqr = q3-q1 #Interquartile range
    #fence_low  = q1-1.5*iqr
    #fence_high = q3+1.5*iqr
    #df_out = df_in.loc[(df_in[col_name] > fence_low) & (df_in[col_name] < fence_high)]
    #return df_out


# ### Conclusion

# Even though this model looks heavy, however I couldn`t overcome limit of 0.79425 with test data set.
# I would appreciate if you provide me any suggestions.

# In[ ]:




