#!/usr/bin/env python
# coding: utf-8

# ## Real or Not? NLP with Disaster Tweets
# 
# Study shows vast majority of people using Twitter like platform during disasters and breaking news events spread false information without ever getting it a second thought. Researchers examined three types of behavior in these users: they could either spread the false news, seek to confirm it, or cast doubt upon it. It becomes evident to predict if the tweet is real or fake to prevent false information reaching out to the mass especially during natural disasters.
# 
# ![](http://)This notebook tries to implement different ML algorithms to predcit real or fake tweets.
# 
# 

# ### Import all necessary libraries.

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
import os
import time


# ### Load the train, test and submission data 

# In[ ]:


for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


tweet_train = pd.read_csv("/kaggle/input/nlp-getting-started/train.csv")
tweet_test = pd.read_csv("/kaggle/input/nlp-getting-started/test.csv")
target = pd.read_csv("/kaggle/input/nlp-getting-started/sample_submission.csv")


# Read the train data

# In[ ]:


tweet_train.head()


# ### Data cleaning
# Lets create a dataframe and find the number of missing values in train and test datasets.

# In[ ]:


null_vals = pd.DataFrame(columns = {"train","test"})
null_vals["train"] = tweet_train.isnull().sum()
null_vals["test"] = tweet_test.isnull().sum()
print(null_vals)


# The output shows location has many null values and keyword with few null values in both datasets.

# In[ ]:


tweet_train.isnull().sum()


# In[ ]:


tweet_train.head()


# convert the tweet_train to csv file 

# In[ ]:


tweet_train.to_csv('tweet_train_data.csv', index=False)


# In[ ]:


tweet_test.isnull().sum()


# ### Exploratory data analysis
# 
# 1. Real v/s Fake tweets: Lets see how many real and fake tweets are present in the train dataset.

# In[ ]:


tweet_train["target"].value_counts()


# In[ ]:


real = len(tweet_train[tweet_train["target"] == 1])
fake = len(tweet_train[tweet_train["target"] == 0])

df_count_pie = pd.DataFrame({'Class' : ['Real', 'Not Real'], 
                             'Counts' : [real, fake]})
df_count_pie.Counts.groupby(df_count_pie.Class).sum().plot(kind='pie',autopct = '%1.1f%%')
plt.axis('equal')
plt.title("Tweeta which are Real or Not")
plt.show()


# ### Text processing using NLP
# 
# Preprocessing the text data in the train and test dataset.
# 

# In[ ]:


tweet_train["text"][:3]


# The above output shows the text column which needs pre-processing like convert the words to lowercase, remove puntuations and stopwords, tokenize the text to words.

# In[ ]:


stopword = stopwords.words('english')


# In[ ]:


def text_processing(text):
    text = re.sub("[^\w\d\s]+",' ',text)
    text = text.lower()
    tok = nltk.word_tokenize(text)
    words = [word for word in tok if word not in stopword]
    return words


# In[ ]:


def join_words(words):
    words = ' '.join(words)
    return words


# In[ ]:


#preprocess the train text data
tweet_train["text_pre"] = tweet_train["text"].apply(lambda x: text_processing(x))
tweet_train["text"] = tweet_train["text_pre"].apply(lambda x: join_words(x))
#preprocess the test text data
tweet_test["text_pre"] = tweet_test["text"].apply(lambda x: text_processing(x))
tweet_test["text"] = tweet_test["text_pre"].apply(lambda x: join_words(x))


# In[ ]:


tweet_train.head(3)


# In[ ]:


tweet_train.drop("text_pre",axis = 1,inplace = True)


# In[ ]:


tweet_test.drop("text_pre",axis = 1,inplace = True)


# In[ ]:


tweet_train.head()


# In[ ]:


tweet_test.head()


# In[ ]:


tweet_train.to_csv('tweet_train_data.csv', index=False)


# In[ ]:


tweet_test.to_csv('tweet_test_data.csv', index=False)


# ### Automl 

# In[ ]:



dataa = pd.read_csv("../input/datasets1/train_data.csv")
dataa[:3]


# Initialize the clients and move your data to GCS

# In[ ]:


#REPLACE THIS WITH YOUR OWN GOOGLE PROJECT ID
PROJECT_ID = 'tweets-real-fake'
#REPLACE THIS WITH A NEW BUCKET NAME. NOTE: BUCKET NAMES MUST BE GLOBALLY UNIQUE
BUCKET_NAME = 'tweets-automl-project1'
#Note: the bucket_region must be us-central1.
BUCKET_REGION = 'us-central1'


# In[ ]:


import os
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../input/google-creden/tweets-real-fake-f2c2c00c9276.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../input/fakenewsgc/tweets-real-fake-f73343fb0388.json"


# In[ ]:


from google.cloud import storage, automl_v1beta1 as automl

storage_client = storage.Client(project=PROJECT_ID)
tables_gcs_client = automl.GcsClient(client=storage_client, bucket_name=BUCKET_NAME)
automl_client = automl.AutoMlClient()
# Note: AutoML Tables currently is only eligible for region us-central1. 
prediction_client = automl.PredictionServiceClient()
# Note: This line runs unsuccessfully without each one of these parameters
tables_client = automl.TablesClient(project=PROJECT_ID, region=BUCKET_REGION, client=automl_client, gcs_client=tables_gcs_client, prediction_client=prediction_client)


# In[ ]:


bucket = storage.Bucket(storage_client, name=BUCKET_NAME)
if not bucket.exists():
    bucket.create(location=BUCKET_REGION)


# In[ ]:


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket. https://cloud.google.com/storage/docs/ """
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))
    
def download_to_kaggle(bucket_name,destination_directory,file_name,prefix=None):
    """Takes the data from your GCS Bucket and puts it into the working directory of your Kaggle notebook"""
    os.makedirs(destination_directory, exist_ok = True)
    full_file_path = os.path.join(destination_directory, file_name)
    blobs = storage_client.list_blobs(bucket_name,prefix=prefix)
    for blob in blobs:
        blob.download_to_filename(full_file_path)


# In[ ]:


#upload_blob(BUCKET_NAME, '/kaggle/working/tweet_train_data.csv', 'train.csv')
#upload_blob(BUCKET_NAME, '/kaggle/working/tweet_test_data.csv', 'test.csv')
upload_blob(BUCKET_NAME, '../input/datasets1/train_data.csv', 'train.csv')
upload_blob(BUCKET_NAME, '../input/datasets1/test.csv', 'test.csv')


# Train an AutoML Model

# In[ ]:


dataset_display_name = 'fake_news'
new_dataset = False
try:
    dataset = tables_client.get_dataset(dataset_display_name=dataset_display_name)
except:
    new_dataset = True
    dataset = tables_client.create_dataset(dataset_display_name)


# In[ ]:


if new_dataset:
    gcs_input_uris = ['gs://' + BUCKET_NAME + '/train.csv']

    import_data_operation = tables_client.import_data(
        dataset=dataset,
        gcs_input_uris=gcs_input_uris
    )
    print('Dataset import operation: {}'.format(import_data_operation))

    # Synchronous check of operation status. Wait until import is done.
    import_data_operation.result()
print(dataset)


# In[ ]:


model_display_name = 'tutorial_model_automl7'
TARGET_COLUMN = 'label'
ID_COLUMN = 'index'

# TODO: File bug: if you run this right after the last step, when data import isn't complete, you get a list index out of range
# There might be a more general issue, if you provide invalid display names, etc.

tables_client.set_target_column(
    dataset=dataset,
    column_spec_display_name=TARGET_COLUMN
)


# In[ ]:


for col in tables_client.list_column_specs(PROJECT_ID,BUCKET_REGION,dataset.name):
    if TARGET_COLUMN in col.display_name or ID_COLUMN in col.display_name:
        continue
    tables_client.update_column_spec(PROJECT_ID,
                                     BUCKET_REGION,
                                     dataset.name,
                                     column_spec_display_name=col.display_name,
                                     type_code=col.data_type.type_code,
                                     nullable=True)


# Run the model for 4hours

# In[ ]:


TRAIN_BUDGET = 4000
print("Training started")
model = None
try:
    model = tables_client.get_model(model_display_name=model_display_name)
except:
    response = tables_client.create_model(
        model_display_name,
        dataset=dataset,
        train_budget_milli_node_hours=TRAIN_BUDGET,
        exclude_column_spec_names=[ID_COLUMN, TARGET_COLUMN]
    )
    print('Create model operation: {}'.format(response.operation))
    # Wait until model training is done.
    model = response.result()
    
print(model)
print("Training completed")


# In[ ]:


gcs_input_uris = 'gs://' + BUCKET_NAME + '/test.csv'
gcs_output_uri_prefix = 'gs://' + BUCKET_NAME + '/predictions-4'

batch_predict_response = tables_client.batch_predict(
    model=model, 
    gcs_input_uris=gcs_input_uris,
    gcs_output_uri_prefix=gcs_output_uri_prefix,
)
print('Batch prediction operation: {}'.format(batch_predict_response.operation))
# Wait until batch prediction is done.
batch_predict_result = batch_predict_response.result()
batch_predict_response.metadata


# In[ ]:


gcs_output_folder = batch_predict_response.metadata.batch_predict_details.output_info.gcs_output_directory.replace('gs://' + BUCKET_NAME + '/','')
download_to_kaggle(BUCKET_NAME,'/kaggle/working','tables_1.csv', prefix=gcs_output_folder)


# In[ ]:


preds_df = pd.read_csv("tables_1.csv")
sub_automl_2 = pd.DataFrame()
sub_automl_2["id"] = preds_df['id']
sub_automl_2['target'] = np.where((preds_df['target_0_score'] >= preds_df['target_1_score']),0,1)
sub_automl_2.to_csv('submission_automl6.csv', index=False)
print(sub_automl_2[:3])


# In[ ]:


wrd_vec = CountVectorizer()
word_vector = wrd_vec.fit_transform(tweet_train["text"])
test_vector = wrd_vec.transform(tweet_test["text"])


# In[ ]:


gnb = GaussianNB()
gnb.fit(word_vector.toarray(),tweet_train["target"])


# In[ ]:


pred = gnb.predict(test_vector.toarray())


# In[ ]:


log_score = cross_val_score(gnb,word_vector.toarray(),tweet_train["target"],cv = 3)
print(log_score)


# In[ ]:




