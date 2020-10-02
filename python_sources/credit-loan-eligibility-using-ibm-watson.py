#!/usr/bin/env python
# coding: utf-8

# ## 1.Import data train_split as a pandas dataframe 

# In[ ]:


import pandas as pd
import numpy as np
# insert train_split data as Pandas Dataframe Object and remove the df* variable

train_df = pd.read_csv('../input/train_split.csv')
train_df.head()


# In[ ]:


train_df.shape


# ## 2.Take the necessary pre processing steps

# In[ ]:


from sklearn import preprocessing
import numpy as np

def prep_data(WORKING_DF):
    encoded = pd.DataFrame()
    
    WORKING_DF.drop(columns=['batch_enrolled', 'desc', 'zip_code'], axis=1)
    # Mapping and encoding emp_length values
    scale_mapper = {np.nan:0, '< 1 year':1, '1 year':2, '2 years':3, '3 years':4, '4 years':5, '5 years':6, '6 years':7, '7 years':8, '8 years':9, '9 years':10, '10+ years':11}
    encoded['emp_length_encoded'] = WORKING_DF['emp_length'].replace(scale_mapper)

    # Encoding remaining ordinal variables
    grouped = WORKING_DF[['delinq_2yrs', 'inq_last_6mths', 'mths_since_last_delinq', 'mths_since_last_record', 'pub_rec', 'total_acc', 'open_acc', 'collections_12_mths_ex_med', 'acc_now_delinq', 'last_week_pay']]
    grouped = grouped.apply(preprocessing.LabelEncoder().fit_transform)
    encoded = pd.concat([encoded, grouped], axis=1)


    # One-hot encode nominal variables
    grouped = WORKING_DF[['term', 'grade', 'sub_grade', 'home_ownership', 'verification_status', 'pymnt_plan', 'purpose', 'addr_state', 'initial_list_status', 'application_type', 'verification_status_joint', 'member_id']]
    grouped = pd.get_dummies(grouped)
    encoded = pd.concat([encoded, grouped], axis=1)

    # Append float columns to encoded df
    grouped = WORKING_DF[['annual_inc', 'dti', 'revol_bal', 'revol_util', 'total_acc', 'total_rec_int', 'total_rec_late_fee', 'recoveries',
                          'collection_recovery_fee', 'tot_coll_amt', 'tot_cur_bal', 'total_rev_hi_lim', 'open_acc', 'mths_since_last_major_derog']]

    # Fill NaN values with mean of each column
    fill_NaN = preprocessing.Imputer(missing_values=np.nan, strategy='mean', axis=0)
    imputed_df = pd.DataFrame(fill_NaN.fit_transform(grouped))
    imputed_df.columns = grouped.columns
    imputed_df.index = grouped.index

    encoded = pd.concat([encoded, imputed_df], axis=1)
    return encoded


# In[ ]:


encoded = prep_data(train_df)
encoded_test_df = prep_data(train_df)
encoded = encoded.drop(columns=['home_ownership_ANY'], axis=1)


# In[ ]:


encoded_test_df.head()


# ## 3.Split data into test and train datasets

# In[ ]:


from sklearn.model_selection import train_test_split

X = encoded
y = train_df['loan_status']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)


# ## 4.Create your first ML Model

# In[ ]:


from sklearn.linear_model import LinearRegression

lr_clf = LinearRegression()
lr_clf.fit(X_train, y_train)


# In[ ]:


lr_clf.predict([X_test.iloc[1,:]])


# In[ ]:


lr_clf.predict(X_test)


# In[ ]:


lr_clf.score(X_test, y_test)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier

rf_clf = RandomForestClassifier(n_estimators=1500, max_depth=200, random_state=0)
rf_clf.fit(X_train, y_train) 


# In[ ]:


rf_clf.score(X_test, y_test)


# ## 5.Creating a ML Pipeline

# In[ ]:


from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
pipeline = make_pipeline(StandardScaler(),RandomForestClassifier(n_estimators=1000, max_depth=2, random_state=0) )


# In[ ]:


model = pipeline.fit(X_train, y_train)


# In[ ]:


predicted = model.predict(X_test)


# In[ ]:


print(predicted)


# In[ ]:


from sklearn import svm, metrics
metrics.classification_report(y_test, predicted)


# ## 6.Publishing the model to Watson ML

# In[ ]:


get_ipython().system(' pip install watson_machine_learning_client')


# In[ ]:


from watson_machine_learning_client import WatsonMachineLearningAPIClient


# In[ ]:


#get wml credentials from your service credentials tab under your ML Service
wml_credentials={
  
  "username": "55826a0d-f7c7-4980-a509-5c291ba63134",
  "password": "bdff31f5-063f-44ae-b38d-743fdd8c14b7",
  "instance_id": "5e8dd26f-9800-4ffe-a971-46c6225530e1",
  "url": "https://eu-gb.ml.cloud.ibm.com"
}


# In[ ]:


#get wml credentials from your service credentials tab under your ML Service
# wml_credentials={
  
#   "username": "******",
#   "password": "******",
#   "instance_id": "******",
#   "url": "******"
# }


# In[ ]:


client = WatsonMachineLearningAPIClient(wml_credentials)


# In[ ]:


import json

instance_details = client.service_instance.get_details()
print(json.dumps(instance_details, indent=2))


# In[ ]:


model_props = {client.repository.ModelMetaNames.AUTHOR_NAME: "Shadab", 
               client.repository.ModelMetaNames.AUTHOR_EMAIL: "shadab.cs0058@gmail.com",
               client.repository.ModelMetaNames.NAME: "Loan eligibility model created on notebook"}


# In[ ]:


published_model = client.repository.store_model(model=model, meta_props=model_props,                                                 training_data=X_train, training_target=y_train)


# In[ ]:


published_model_uid = client.repository.get_model_uid(published_model)
model_details = client.repository.get_details(published_model_uid)

print(json.dumps(model_details, indent=2))


# In[ ]:


models_details = client.repository.list_models()


# In[ ]:


loaded_model = client.repository.load(published_model_uid)
print(loaded_model)


# In[ ]:


test_predictions = loaded_model.predict(X_test[:10])


# In[ ]:


print(test_predictions)


# ## 7.Deploying as a webservice

# In[ ]:


created_deployment = client.deployments.create(published_model_uid, "Deployment of locally created scikit model")


# In[ ]:


scoring_endpoint = client.deployments.get_scoring_url(created_deployment)

print(scoring_endpoint)


# In[ ]:




deployments = client.deployments.get_details()

print(json.dumps(deployments, indent=2))


# In[ ]:


deployment_url = client.deployments.get_url(created_deployment)

print(deployment_url)


# In[ ]:


scoring_payload = {"values": [list(X_test.iloc[1,:])]}


# In[ ]:


predictions = client.deployments.score(scoring_endpoint, scoring_payload)


# In[ ]:


print(json.dumps(predictions, indent=2))

