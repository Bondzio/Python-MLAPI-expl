#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# # Importing some essential libraries

# In[ ]:


# Encoding 
from sklearn.preprocessing import LabelEncoder , OneHotEncoder
from sklearn.compose import ColumnTransformer

# Grid Search (Hyperparameter tuning)
from sklearn.model_selection import GridSearchCV

# ML Models
from sklearn.svm import SVC
from sklearn import svm, tree, linear_model, neighbors, naive_bayes, ensemble, discriminant_analysis, gaussian_process
from xgboost import XGBClassifier
from sklearn import model_selection
import warnings
warnings.filterwarnings("ignore")


# This Titanic Dataset has 2 files train.csv and test.csv . However,test.csv does not have the 'Survived' column to cross verify our accuracy. So we will just use split train.csv to training and test sets and get the accuracy.

# In[ ]:


dataset_raw = pd.read_csv('/kaggle/input/titanic/train.csv')
dataset_traincsv = dataset_raw.copy(deep = True)

dataset_testcsv = pd.read_csv('/kaggle/input/titanic/test.csv')
dataset_testcsv_copy = pd.read_csv('/kaggle/input/titanic/test.csv')

dataset_train_test = [dataset_traincsv , dataset_testcsv]


# In[ ]:


dataset_traincsv.head()


# In[ ]:


dataset_testcsv.head() # Note no 'Survived' column


# # Just exploring different dataframe functions 

# In[ ]:


dataset_traincsv.shape


# In[ ]:


dataset_testcsv.shape


# In[ ]:


dataset_traincsv.columns


# In[ ]:


dataset_testcsv.columns


# In[ ]:


dataset_traincsv.sample(10)


# In[ ]:


dataset_testcsv.sample(10)


# In[ ]:


dataset_traincsv.info()


# In[ ]:


dataset_testcsv.info()


# In[ ]:


dataset_traincsv.describe()


# In[ ]:


dataset_testcsv.describe()


# # Finding out how many categories are there for each categorical variable

# In[ ]:


dataset_traincsv["Sex"].value_counts(dropna = False) #Nan values will also be counted


# In[ ]:


dataset_traincsv['Pclass'].value_counts(dropna = False)


# In[ ]:


dataset_traincsv['Survived'].value_counts(dropna = False)


# In[ ]:


dataset_traincsv['Embarked'].value_counts(dropna = False)


# # Corelation matrix

# You can get a premature idea of what affect each variable has to Survived column.
# Since it only has numerical values and not words we cannot get the full picture. Here for eg we will see that 'Sex' had the biggest role to play but since it is a word variable it can't be seen yet. Once we use Label Encoding to convert to numerical values we can see the corelation. 
# 
# Here we can see 'Pclass' and 'Fare' had a big role to play.

# In[ ]:


dataset_traincsv.corr()


# # Cleaning - Correcting , Completing , Creating and Converting

# #                  1. Correcting

# In[ ]:


print('Train.csv columns with null values:\n', dataset_traincsv.isnull().sum())


# In[ ]:


print('Test.csv columns with null values:\n', dataset_testcsv.isnull().sum())


# No correction required

# # 2. Cleaning

# Here we are treating the null values of our columns.

# In[ ]:


for dataset in dataset_train_test:
    dataset['Age'].fillna(dataset['Age'].median(), inplace = True)
    dataset['Embarked'].fillna(dataset['Embarked'].mode()[0], inplace = True)
    dataset['Fare'].fillna(dataset['Fare'].median(), inplace = True)


# In[ ]:


dataset_traincsv.info()


# In[ ]:


dataset_testcsv.info()


# In[ ]:


# Dropping the 'PassengerId','Cabin' and 'Ticket' columns as they don't have any impact on result.

drop_column = ['PassengerId','Cabin', 'Ticket']
for dataset in dataset_train_test :
    dataset.drop(drop_column, axis=1, inplace = True)


# In[ ]:


dataset_traincsv.isnull().sum() #No Nan values in dataframe now


# In[ ]:


dataset_testcsv.isnull().sum()


# # 3. Creating (Feature Engineering)

# Please refer  https://www.kaggle.com/ldfreeman3/a-data-science-framework-to-achieve-99-accuracy/notebook#Table-of-Contents for more info on this section.
# 
# Here i am creating new features :
# 
# 1. Title - This feature will be extracted from the 'Name' feature. The Name feature in itself is not much of use but the title of people (Master , Mrs ,Miss etc) was detremental in their survival.
# 
# 2. FamilySize - This feature is added to remove the SibSp and Parch features. We are basically trying to reduce the redundant features.
# 
# 3. IsAlone - This feature is for us to determine if a person who came alone (FamilySize = 1) had a lower or more chance of survival. Spoiler Alert : Person had a lower chance of survival as we will see in the coorelation matrix. 

# In[ ]:



for dataset in dataset_train_test:
    dataset['FamilySize'] = dataset['SibSp'] + dataset['Parch'] + 1 

    dataset['IsAlone'] = 1
    dataset['IsAlone'].loc[dataset['FamilySize'] > 1] = 0

    dataset['Title'] = dataset['Name'].str.split(", ", expand=True)[1].str.split(".", expand=True)[0]
    title_names = (dataset['Title'].value_counts() < 10)
    dataset['Title'] = dataset['Title'].apply(lambda x: 'Misc' if title_names.loc[x] == True else x)


# In[ ]:


dataset_traincsv.sample(10)


# In[ ]:


dataset_testcsv.sample(10)


# In[ ]:


dataset_traincsv['Title'].value_counts()


# In[ ]:


dataset_testcsv['Title'].value_counts()


# In[ ]:


dataset_traincsv.info()


# In[ ]:


dataset_testcsv.info()


# # Encoding 'Sex' using Label Encoder

# In[ ]:


dataset_traincsv['Sex'].value_counts()


# In[ ]:


dataset_traincsv['Embarked'].value_counts()


# In[ ]:


dataset_traincsv['Title'].value_counts()


# In[ ]:


# So we will need Label Encoder for 'Sex' (As only 2 values) and OneHotEncoder for 'Embarked' and 'Title'.
# We could actually use Label encoder for 'Title' too as there is a hierarchy i.e Masters,Mrs,Miss are more likely to survive .
# Please let me know if you get the same accuracy. I will be sticking ot OneHotEncoder for 'Title'.

labelencoder = LabelEncoder()
for dataset in dataset_train_test:
    dataset['Sex'] = labelencoder.fit_transform(dataset['Sex'])


# In[ ]:


# Dropping the 'Name' column as it does not have any impact on result

for dataset in dataset_train_test:
    dataset.drop('Name' , axis =1 , inplace = True)


# In[ ]:


dataset_traincsv.head()


# In[ ]:


dataset_testcsv.head()


# We will be doing OneHotEncoding after the splitting is done as OneHotEncoder returns a nparray and it would have been difficult read if i had applied it right now.

# In[ ]:


# Now that 'Sex' is encoded check the co-relation matrix again :

dataset_traincsv.corr()


# As seen above the 'Sex' has the most affect in survivng rate followed by 'Pclass' and 'Fare'

# # Splitting dataframe to independent and dependent variable

# In[ ]:


# Re-ordering the Survived column to the last location just to increase the redability
Survived = dataset_traincsv['Survived']
dataset_traincsv.drop(labels = ['Survived'] , axis = 1 , inplace = True )
dataset_traincsv.insert(10 , 'Survived' , Survived)
dataset_traincsv.sample(10)


# In[ ]:


# for train.csv
x = dataset_traincsv.iloc[: , [0,1,2,5,6,7,8,9]].values
y = dataset_traincsv.iloc[: , 10].values

# for test.csv
x_2 = dataset_testcsv.iloc[: , [0,1,2,5,6,7,8,9]].values


# In[ ]:


x[0:9]


# In[ ]:


y[0:9]


# In[ ]:


x_2[0:9]


# # Now doing the OneHotEncoder on 'Embarked' and 'Title' columns

# In[ ]:


ct_x = ColumnTransformer([('encoder' , OneHotEncoder() , [4,7])] , remainder= 'passthrough')
x = np.array(ct_x.fit_transform(x),dtype = float )
x_2 = np.array(ct_x.fit_transform(x_2) , dtype = float)


# In[ ]:


# Avoiding the Dummy variable trap (This is automatically cared for in ML models. However in some algos like backprop it is not taken care of.)
# x = x[: , 1:]
# x_2 = x_2[: , 1:]


# In[ ]:


x.shape # It is a matrix


# In[ ]:


y.shape # It is a vector


# In[ ]:


x[0] # Just checking if OneHotEncoding was done on not , by checking first row of the array


# In[ ]:


x_2[0]


# # Splitting the data to Test and Training set

# No need to split for x_2 as the whole dataset is x_test.

# In[ ]:


from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x , y , test_size = 0.25)


# In[ ]:


x_train.shape


# In[ ]:


x_test.shape


# In[ ]:


y_train.shape


# In[ ]:


y_test.shape


# # Feature Scaling

# In[ ]:


from sklearn.preprocessing import StandardScaler
sc_x = StandardScaler()
x_train = sc_x.fit_transform(x_train)
x_test = sc_x.transform(x_test) # Only transform as we have applied fit in training set already in above line

# Feature Scaling of x_2
x_2 = sc_x.transform(x_2)


# In[ ]:


x_train[0]


# In[ ]:


x_2[0]


# # SVC model

# In[ ]:


classifier_base = SVC(kernel='linear' ,random_state= 0 )
classifier_base.fit(x_train , y_train)


# In[ ]:


# Applying 10 fold cross validation to check the accuracy
accuracies_base = model_selection.cross_validate(estimator=classifier_base , X=x_train , y= y_train , cv = 10 ) 


# In[ ]:


accuracies_base


# In[ ]:


accuracies_base['test_score'].mean()*100


# Hyperparameter tuning SVC

# In[ ]:


parameters_hyper = [
    
    {'C' : [ i for i in range(1,10,1)] , 
     'gamma' : [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09 , 0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1], 
     'probability' : [False , True],
     'kernel' : ['linear']
    } ,
    
    {'C' : [ i for i in range(1,10,1)] , 
     'gamma' : [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09 , 0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1], 
     'probability' : [False , True],
     'kernel' : ['rbf']
    }
]

grid_search_hyper = GridSearchCV(estimator=classifier_base, param_grid= parameters_hyper , scoring= 'accuracy' , cv= 10 , n_jobs= -1)
grid_search_hyper = grid_search_hyper.fit(x_train , y_train)
best_accuracy_hyper = grid_search_hyper.best_score_
best_parameters_hyper = grid_search_hyper.best_params_ 


# In[ ]:


best_accuracy_hyper


# In[ ]:


best_parameters_hyper


# In[ ]:


C_hyper = best_parameters_hyper.get('C')
gamma_hyper = best_parameters_hyper.get('gamma')
kernel_hyper = best_parameters_hyper.get('kernel')


# Trying out these parameters

# In[ ]:


classifier_hyper = SVC(kernel=kernel_hyper ,C= C_hyper , gamma = gamma_hyper, random_state= 0 ) 
classifier_hyper.fit(x_train , y_train)


# In[ ]:


# Checking the results with 10 Fold cross validation

accuracies_hyper = model_selection.cross_validate(estimator=classifier_hyper , X=x_train , y= y_train , cv = 10 ) 


# In[ ]:


accuracies_hyper


# In[ ]:


accuracies_hyper['test_score'].mean()*100


# # Applying XGBoost

# In[ ]:


classifier_xgb = XGBClassifier()
classifier_xgb.fit(x_train , y_train)

#  10 Fold Cross Validate
accuracies_xgb = model_selection.cross_validate(estimator=classifier_xgb , X=x_train , y= y_train , cv = 10 )


# In[ ]:


accuracies_xgb


# In[ ]:


accuracies_xgb['test_score'].mean()*100


# # Applying Random Forest
# 

# In[ ]:


classifier_rf = ensemble.RandomForestClassifier(n_estimators= 500, criterion='entropy' , random_state= 0)
classifier_rf.fit(x_train , y_train)

# 10 fold Cross Validate
accuracies_rf = model_selection.cross_validate(estimator=classifier_rf , X=x_train , y= y_train , cv = 10 )


# In[ ]:


accuracies_rf


# In[ ]:


accuracies_rf['test_score'].mean()*100


# # Applying ANN

# Using TensorFlow.Keras as keras now comes integrated to TensorFlow. Previous versions of my code used standalone Keras.

# In[ ]:


import tensorflow as tf 


# In[ ]:


# TensorFlow version check
tf.__version__


# In[ ]:


# Initializing the ANN
classifier_ann = tf.keras.models.Sequential() #We will add layers afterwards

# Adding the input layer and first hidden layer
"""nodes = number of output nodes (input nodes are taken care automatically) , activation - activation funct used  """
classifier_ann.add(tf.keras.layers.Dense(units = 7 , activation='relu')) 

# Adding second hidden layer
classifier_ann.add(tf.keras.layers.Dense(units = 7 , activation='relu')) 

# Adding the output layer (We want to have probabilities as output)
"""If no of categories is 3 or more then output_dim = 3 (or more) , activation = softmax""" 
classifier_ann.add(tf.keras.layers.Dense(units = 1 , activation='sigmoid')) 

# Compile ANN (Applying SGD) - The backpropagation step
"""For more than 3 classifiers use loss = categorical_crossentropy"""
classifier_ann.compile(optimizer='adam', loss='binary_crossentropy' , metrics= ['accuracy'] )

# Fitting the ANN to the training set
classifier_ann.fit(x_train , y_train, batch_size= 10 , epochs= 400) 


# In[ ]:


# Predict
y_pred_ann = classifier_ann.predict(x_test)
y_pred_ann = (y_pred_ann > 0.5)

# Making the confusion matrix
from sklearn.metrics import confusion_matrix

cm_ann = confusion_matrix(y_test , y_pred_ann)


# In[ ]:


cm_ann


# In[ ]:


from sklearn.metrics import accuracy_score

accuracy_score(y_test , y_pred_ann)*100


# # Voting Classifiers

# Hard Vote

# In[ ]:


vote_est = [
    #Ensemble Methods: http://scikit-learn.org/stable/modules/ensemble.html
    ('ada', ensemble.AdaBoostClassifier()),
    ('bc', ensemble.BaggingClassifier()),
    ('etc',ensemble.ExtraTreesClassifier()),
    ('gbc', ensemble.GradientBoostingClassifier()),
    ('rfc', ensemble.RandomForestClassifier()),

    #Gaussian Processes: http://scikit-learn.org/stable/modules/gaussian_process.html#gaussian-process-classification-gpc
    ('gpc', gaussian_process.GaussianProcessClassifier()),
    
    #GLM: http://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
    ('lr', linear_model.LogisticRegressionCV()),
    
    #Navies Bayes: http://scikit-learn.org/stable/modules/naive_bayes.html
    ('bnb', naive_bayes.BernoulliNB()),
    ('gnb', naive_bayes.GaussianNB()),
    
    #Nearest Neighbor: http://scikit-learn.org/stable/modules/neighbors.html
    ('knn', neighbors.KNeighborsClassifier()),
    
    #SVM: http://scikit-learn.org/stable/modules/svm.html
    ('svc', svm.SVC(probability=True)),
    
    #xgboost: http://xgboost.readthedocs.io/en/latest/model.html
   ('xgb', XGBClassifier())

]

#Hard Vote or majority rules
vote_hard = ensemble.VotingClassifier(estimators = vote_est , voting = 'hard')

# Cross Validate
vote_hard_cv = model_selection.cross_validate(vote_hard, x_train, y_train , cv = 10)


# In[ ]:


vote_hard_cv


# In[ ]:


vote_hard.fit(x_train , y_train)


# In[ ]:


vote_hard_cv['test_score'].mean()*100


# Soft vote

# In[ ]:


#Soft Vote or weighted probabilities
vote_soft = ensemble.VotingClassifier(estimators = vote_est , voting = 'soft')

# Cross validate
vote_soft_cv = model_selection.cross_validate(vote_soft, x_train , y_train , cv  = 10)


# In[ ]:


vote_soft.fit(x_train, y_train)


# In[ ]:


vote_soft_cv


# In[ ]:


vote_soft_cv['test_score'].mean()*100


# # Predicting values using ANN model and Tuned SVC (As it has the highest accuracy) on test.csv

# For ANN

# In[ ]:


# Predicting the values and setting the threshold for 1 as greater than 0.5
y_pred_testcsv_ann = classifier_ann.predict(x_2)
y_pred_testcsv_ann = (y_pred_testcsv_ann > 0.5) #returns values in True / False in a list of lists format

# Converting True and False values to int
y_pred_testcsv_ann = y_pred_testcsv_ann.astype(int)

# Coverting list of list to 1 flat list
y_predtestcsv_ann = [item for sublist in y_pred_testcsv_ann for item in sublist]

# Converting the flat list to np array
y_predtestcsv_ann = np.asarray(y_predtestcsv_ann , dtype = int)


# In[ ]:


y_predtestcsv_ann


# For Hyperparameter tuned SVC model

# In[ ]:


y_pred_testcsv = vote_soft.predict(x_2)


# In[ ]:


y_pred_testcsv


# In[ ]:


dataset_testcsv_copy['Survived'] = y_predtestcsv_ann


# # Submit file

# In[ ]:


dataset_testcsv_copy.info()


# In[ ]:


submit = dataset_testcsv_copy[['PassengerId','Survived']]
submit.to_csv("../working/submit.csv", index=False)

print('Validation Data Distribution: \n', dataset_testcsv_copy['Survived'].value_counts(normalize = True))
submit.sample(10)


# # Optimizations

# We can further optimize this model by applying all the models and find the optimal hyperparameters of all of them .
# This will take a considerable amount of time.
