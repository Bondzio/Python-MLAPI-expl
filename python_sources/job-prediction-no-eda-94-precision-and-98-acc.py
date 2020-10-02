#!/usr/bin/env python
# coding: utf-8

# ## Fake job Predcition

# Please also check the project made on the same dataset but utilizing pipeline concepts in addition. [link for github repo](https://github.com/saketh97/FakeJobPrediction). **Also if you like this please upvote and follow for interesting other notebooks.**

# Here we will try to predict the fake job postings. There are 18 columns like title, department, company profile, job description etc. I will use NLP Techniques to analyse text data and prepare them for prediction model to train. Also in this code i will use **Functions** to define code and call those functions with dataset as parameter(Train or Test). Once the training is complete the model will be saved as a pickle file to load whenever we need to predict. Also as there are categorical columns we will need categorical encoding and scaling so both of them will aslo be trained and saved using pickle.

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import re
import string
import math
import pandas as pd
from nltk.cluster import cosine_distance
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
import category_encoders as ce
import pickle
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# This Data set is Biased towards real job. The dataset contains 17880 entries in which 17014 are real jobs and only 866 are fake jobs. For such biased data just **accuracy** does not matter but also we should consider **Precision,Recall and F1-Score**.

# In[ ]:


data = pd.read_csv('/kaggle/input/real-or-fake-fake-jobposting-prediction/fake_job_postings.csv')
print('Total data')
print(data.shape)
print('Real jobs')
print(data[data['fraudulent']==0].shape)
print('Fake jobs')
print(data[data['fraudulent']==1].shape)


# Before starting the whole coding process I have split the data into two datasets **Train with 97% split** and **Test with 3% split**. So in the training set we will have 17344 entires and in the test set it will contain 536 entries. The model will have enough data to train and test. I have already shuffled and split the data for the [project in github](https://github.com/saketh97/FakeJobPrediction). So i will use the same datsets.

# In[ ]:


train_set = pd.read_csv('/kaggle/input/train-and-test-for-fake-jobs/train.csv')

test_set = pd.read_csv('/kaggle/input/train-and-test-for-fake-jobs/test.csv')


# Now we have the split datset lets contnue with handling data. This data contains lots of missing values and text contain to be handled.

# ### Missing Values

# I have divided missing values into three subsets.
# 1. Location Column
# 2. Salary Range
# 3. Rest of the columns
# 
# Location columns contains values like **(country,state,location)** in which we will focus only on country part so we split with **,** and store only the 1st part(country). For the Salary range column data looks like **(minsal-maxsal)** so we convert it into two new columns minimum saary and maximum salary. For the rest of columns just replace missing values with **no-info** and **0** for ctegorical and numeric columns repectively.
# 
# **Just expand the below code to check how i have written code.**

# In[ ]:


def missing_values(data):
        data['location'].fillna('no info', inplace = True)
        withoutcomma = data[~data['location'].str.contains(",")].index
        withcomma = data[data['location'].str.contains(",")].index

        for i in withcomma:
            data.loc[i, 'country'] = data.loc[i,'location'].split(',')[0].strip()

        for i in withoutcomma:
            data.loc[i, 'country'] = data.loc[i,'location'].strip()

        """2.salary range"""

        data['salary_range'].fillna('0-0', inplace = True)

        for i in range(0, data.shape[0]):
            str = data.loc[i, 'salary_range']
            if re.search(r'[a-z,A-Z]',str):
                data.loc[i, 'salary_range']='0-0'

            if(data.loc[i, 'salary_range'].find("-") != -1):
                data.loc[i, 'minimum_salary'] = data.loc[i,'salary_range'].split('-')[0]
                data.loc[i,'maximum_salary'] = data.loc[i,'salary_range'].split('-')[1]
            else:
                data.loc[i, 'minimum_salary'] = data.loc[i, 'salary_range']
                data.loc[i, 'maximum_salary'] = data.loc[i, 'salary_range']


        """3. All other categorical columns and remaining numeric columns."""

        columns = data.columns
        for i in columns:
            if(data[i].isna().any()):
                if(data[i].dtypes == 'object'):
                    data[i].fillna('no info', inplace = True)
                    data[i] = data[i].str.lower()

                else:
                    data[i].fillna(0, inplace = True)

        data.drop(['salary_range', 'location'], axis = 1, inplace = True)
        return data


# ### Text Handling

# For columns like title, department, company profile, job description etc for all the categorical I have used NLTK functions like **stop words, Stemming and Word net synset** to find out a similarity factor between columns eg: similarity between job title and job description. Using various combinations I have formed various new columns which represent such kind of similarities. Now all these columns are used in the Random Forest algorithm to find the Fake jobs. With all these steps I have reached precision of 94% and f1-score of 0.80(Max f1-score is 1 so its like 80%).  
# 
# **Just expand the below code blocks to check how i have written code.**

# In[ ]:


stop_words = set(stopwords.words('english'))

def texthandling(data):
    for i in range(0, data.shape[0]):

        data.loc[i, 'company_profile'] = removeuncessary(data.loc[i,'company_profile'])
        data.loc[i, 'description'] = removeuncessary(data.loc[i,'description'])
        data.loc[i, 'requirements'] = removeuncessary(data.loc[i,'requirements'])
        data.loc[i, 'benefits'] = removeuncessary(data.loc[i,'benefits'])
        data.loc[i, 'title'] = removeuncessary(data.loc[i, 'title'])
        data.loc[i, 'department'] = removeuncessary(data.loc[i,'department'])
        data.loc[i, 'industry'] = removeuncessary(data.loc[i,'industry'])
        data.loc[i, 'function'] = removeuncessary(data.loc[i,'function'])

        words = str(data.loc[i, 'company_profile'])
        if(words == 'no info'):
            data.loc[i, 'company_profile_word_count'] = 0
        else:
            data.loc[i, 'company_profile_word_count'] = len(words.split())

        words = str(data.loc[i, 'benefits'])
        if(words == 'no info'):
            data.loc[i, 'benefits_word_count'] = 0
        else:
            data.loc[i, 'benefits_word_count'] = len(words.split())

        data.loc[i, 'title_and_job_similarity'] = synonym_relation(data.loc[i, 'title'], data.loc[i,'description'])

        data.loc[i, 'title_and_req_similarity'] = synonym_relation(data.loc[i, 'title'], data.loc[i,'requirements'])

        data.loc[i, 'profile_and_job_similarity'] = synonym_relation(data.loc[i, 'company_profile'], data.loc[i,'description'])

        data.loc[i, 'profiel_and_req_similarity'] = synonym_relation(data.loc[i, 'company_profile'], data.loc[i,'requirements'])

        data.loc[i,'title_and_department_syn_similarity'] = synonym_relation(data.loc[i, 'title'], data.loc[i, 'department'])

        data.loc[i,'title_and_industry_syn_similarity'] = synonym_relation(data.loc[i, 'title'],data.loc[i, 'industry'])

        data.loc[i,'title_and_function_syn_similarity'] = synonym_relation(data.loc[i, 'title'], data.loc[i, 'function'])

        data.loc[i,'industry_and_department_syn_similarity'] = synonym_relation( data.loc[i, 'industry'], data.loc[i, 'department'])

        data.loc[i,'function_and_department_syn_similarity'] = synonym_relation( data.loc[i, 'function'], data.loc[i, 'department'])
              
        data.loc[i,'industry_and_function_syn_similarity'] =synonym_relation(data.loc[i, 'industry'], data.loc[i, 'function'])

    for i in ['title_and_job_similarity', 'title_and_req_similarity', 'profile_and_job_similarity', 'profiel_and_req_similarity',
              'title_and_department_syn_similarity','title_and_industry_syn_similarity','title_and_function_syn_similarity',
              'function_and_department_syn_similarity','industry_and_department_syn_similarity','industry_and_function_syn_similarity']:
        data[i].fillna(0, inplace = True)

    data.drop(['company_profile', 'benefits', 'description','requirements', 'title', 'department', 'industry', 'function', 'job_id'], axis = 1, inplace = True)
    return data


# In[ ]:


def stopwordsremove(text):
    word_token = word_tokenize(text)
    ps = PorterStemmer()
    filtered = [ps.stem(w.lower())for w in word_token if not w in stop_words]
    return filtered
    
def removeuncessary(text):
    text = re.sub('[%s]'%re.escape(string.punctuation), '', str(text))
    text = re.sub('\w*\d\w*', '', str(text))
    text = re.sub('[^a-zA-Z ]+', ' ', str(text))

    return text
   


# In[ ]:


def synonym_relation(text1, text2):
    if(text1 == 'no info' or text2 == 'no info'):
        return 0
    else:
        text1 = stopwordsremove(text1)
        text2 = stopwordsremove(text2)
        syn_set = set()
        count  = 0
        if(len(text1) == 0 or len(text2) == 0):
            return 0
        if(len(text1) < len(text2)):
            for word in text2:
                for syn in wordnet.synsets(word):
                    for l in syn.lemmas():
                        syn_set.add(l.name())

            for word in text1:
                if word in syn_set:
                        count += 1
            return (count / len(text1))
        else:
            for word in text1:
                for syn in wordnet.synsets(word):
                    for l in syn.lemmas():
                        syn_set.add(l.name())

            for word in text2:
                if word in syn_set:
                    count += 1
            return (count / len(text2))


# ### Categorical Encoding

# Here we crete and train an encoder for categorical columns to perform binary encoding. Then we save the encoder for testing purpose using picle.

# In[ ]:


def categorical_cols_train(data):
        encoder = ce.BinaryEncoder(cols = ['employment_type','required_experience', 'required_education', 'country'])
        newdata = encoder.fit_transform(data)
        pickle.dump( encoder, open( "encoder.p", "wb" ) )
        return newdata

def categorical_cols_test(data):
        encoder = pickle.load( open( "encoder.p", "rb" ) )
        newdata = encoder.transform(data)
        return newdata


# ### Model  

# For the model I am using Random Forest Classifier. After handling the data we will apply Scaler and save the scaler. Also after creating the model save the model with pickle.

# In[ ]:


def train_and_save_model(data):
        X_train = data.drop('fraudulent', axis = 1)
        y_train = data['fraudulent']

        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        pickle.dump( sc, open( "scaler.p", "wb" ))

        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators = 100 ,criterion = 'entropy',random_state = 1)

        model.fit(X_train, y_train)

        filename = 'finalized_model.p'
        pickle.dump(model, open(filename, 'wb'))
        

def load_model_predict(data):
        X_test = data.drop('fraudulent',axis = 1)
        y_test = data['fraudulent']

        scaler = pickle.load( open( "scaler.p", "rb" ) )
        X_test = scaler.transform(X_test)

        filename = 'finalized_model.p'
        model = pickle.load(open(filename, 'rb'))

        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        print("\n"+"SCORES")
        print("confusion matrix")
        print(cm)
        print('F1-Score'+' = '+str(round(f1_score(y_test, y_pred),4)))
        print('Precision'+' = '+str(round(precision_score(y_test, y_pred),4)))
        print('Recall'+' = '+str(round(recall_score(y_test, y_pred),4)))
        print('Accuracy'+' = '+str(round(accuracy_score(y_test,y_pred),4)))


# ### Training Part

# First we read the data and then pass it to Data handling process where the missing values, Text data Handling takes place and finally categorical encoding is done for category columns. After Handling the data and scaling then we will utilize Random Forest algorithm to create and train model on the cleaned data. After training the model then we save the model as a pickle file so it can be loaded any time.  

# In[ ]:


train_set = missing_values(train_set)
train_set = texthandling(train_set)
train_set = categorical_cols_train(train_set)
train_and_save_model(train_set)


# ### Test Part

# Similar to training we need to read the data and then handle the data(missing values, Text data Handling, categorical encoding). After Handling the data and scaling them we will make use of the saved model to test the data and save the predicted result as a csv. Here for testing process we use the saved categorical encoder and saved scaler instead of newly creating. Also in the end it will display the metrics used for rating.
# 

# In[ ]:


test_set = missing_values(test_set)
test_set = texthandling(test_set)
test_set = categorical_cols_test(test_set)
load_model_predict(test_set)

