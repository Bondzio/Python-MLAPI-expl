#!/usr/bin/env python
# coding: utf-8

# # Importations 

# In[ ]:


import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns


import os
import gc
import joblib



from sklearn import metrics, linear_model
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from sklearn.preprocessing import StandardScaler
from tqdm.notebook import tqdm



import tensorflow as tf
from sklearn.model_selection import StratifiedKFold
from sklearn import metrics, preprocessing
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import callbacks
from tensorflow.keras import backend as K
from tensorflow.keras import utils

from sklearn import model_selection
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import mean_squared_error
from math import sqrt

import warnings
warnings.filterwarnings("ignore")


# # Loading Data : 

# In[ ]:


train = pd.read_csv('../input/datacept-wine-prices-prediction/trainfinal.csv')
test = pd.read_csv('../input/datacept-wine-prices-prediction/test.csv')


# In[ ]:


train.head(2)


# In[ ]:


test['price'] = -1 
all_data = pd.concat([train,test],ignore_index =True)


# In[ ]:


all_data.shape


# In[ ]:


(train[train['price']<250]['price']).hist(bins=50)


# # MISSING Values 

# In[ ]:


def missing_values(data,number=20) : 
  total = data.isnull().sum().sort_values(ascending=False)
  percent = (data.isnull().sum()/data.isnull().count()).sort_values(ascending=False)
  missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])

  print(missing_data.head(number))
missing_values(all_data)


# there is a high ratio of missing values of taster_name  , taster_twitter_handel and region_2 so i will not use this variable in building the model 

# In[ ]:


all_data = all_data.drop(['taster_twitter_handle','taster_name','region_2'],1)


# # Using Word Embbeding to handel text features : 

# Word embedding is one of the most popular representation of document vocabulary. It is capable of capturing context of a word in a document, semantic and syntactic similarity, relation with other words, etc.
# 
# i will use in this section TF-IDF (term frequency-inverse document frequency) which is a pretrained word embedding model .
# 
# some links and courses to learn more about word-embedding and TF-IDF : 
# * one of the best courses in to learn DL  : https://www.coursera.org/learn/nlp-sequence-models/
# 
# * another super course from Michigan Universty : https://www.coursera.org/learn/python-text-mining?
# 
# * https://towardsdatascience.com/introduction-to-word-embedding-and-word2vec-652d0c2060fa

# # Description 

# In[ ]:


#Nlp 
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.naive_bayes import MultinomialNB
from nltk import word_tokenize
from nltk.corpus import stopwords
import nltk


# In[ ]:


nltk.download('stopwords')
stop_words = stopwords.words('english')


# In[ ]:


# Always start with these features. They work (almost) everytime!
tfv = TfidfVectorizer(min_df=3,  max_features=64, 
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3), use_idf=1,smooth_idf=1,sublinear_tf=1,
            stop_words = 'english')

# Fitting TF-IDF to both training and test sets (semi-supervised learning)
tfv.fit(all_data.description)


# In[ ]:


all_data_description = tfv.transform(all_data.description)
all_data_description = pd.DataFrame(data=all_data_description.todense(),columns=tfv.get_feature_names())
all_data_description.head()


# In[ ]:


description_features = all_data_description.columns.tolist()


# In[ ]:


all_data =pd.concat([all_data,all_data_description],axis=1)


# # Title

# In[ ]:


# Always start with these features. They work (almost) everytime!
tfv = TfidfVectorizer(min_df=3,  max_features=32, 
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3), use_idf=1,smooth_idf=1,sublinear_tf=1,
            stop_words = 'english')

# Fitting TF-IDF to both training and test sets (semi-supervised learning)
tfv.fit(all_data.title.fillna('other'))


# In[ ]:


all_data_title= tfv.transform(all_data.title.fillna('other'))
columns_name = [ x+'_title' for x in tfv.get_feature_names()]
all_data_title = pd.DataFrame(data=all_data_title.todense(),columns=columns_name)
all_data_title.head()


# In[ ]:


title_features = all_data_title.columns.tolist()


# In[ ]:


all_data = pd.concat([all_data,all_data_title],axis=1)


# # Designation

# In[ ]:


# Always start with these features. They work (almost) everytime!
tfv = TfidfVectorizer(min_df=3,  max_features=32, 
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3), use_idf=1,smooth_idf=1,sublinear_tf=1,
            stop_words = 'english')

# Fitting TF-IDF to both training and test sets (semi-supervised learning)
tfv.fit(all_data.designation.fillna('and'))


# In[ ]:


all_data_des= tfv.transform(all_data.title.fillna('other'))
columns_name = [ x+'_des' for x in tfv.get_feature_names()]
all_data_des = pd.DataFrame(data=all_data_des.todense(),columns=columns_name)
all_data_des.head()


# In[ ]:


des_features = all_data_des.columns.tolist()


# In[ ]:


all_data = pd.concat([all_data,all_data_des],axis=1)


# # Analyzing categorical variable

# Categorical variable are known to hide and mask lots of intersting information in a data set and in our poroblem they are the most important variables. so handiling them effectively and efficiently can help us to make a good model . so let's start analyzing this variables 

# In[ ]:


# useful function 
def plot_cat(all_data,var,target='price') : 
  data = pd.concat([all_data[target], all_data[var]], axis=1)
  f, ax = plt.subplots(figsize=(30, 8))
  fig = sns.boxplot(x=var, y=target, data=data)
  fig.axis(ymin=0, ymax=100);
def cat_summary(all_data,var) : 
  new = all_data[var].value_counts() 
  print('there are ',len(new.values),'differnet value of ',var)
  res = pd.DataFrame(data=new.values,
                  index=new.index.to_list(),
                  columns=['number'])
  return res  


# In[ ]:


plot_cat(all_data,'country')


# we can see that the price of the wine price highly dependent on country .

# In[ ]:


embed_cols=[i for i in all_data.select_dtypes(include=['object'])]
print('Categorical Features and Cardinality')
for i in embed_cols:
    print(i,all_data[i].nunique())


#  the problem here that we have some categorical features have a higher cardinality .if we do one hot encoding we will create more than 20000 feature and i don't thing that there is a model can  work well with an dataset had more than 20000 columns . so that why i have decided to use Entity Embedding to handle those categorical features . 

# # how does Entity Embeddings work ?
# 
# We map categorical variables in a function approximation problem into Euclidean spaces, which are the entity embeddings of the categorical variables. The mapping is learned by a neural network during the standard supervised training process. Entity embedding not only reduces memory usage and speeds up neural networks compared with one-hot encoding, but more importantly by mapping similar values close to each other in the embedding space it reveals the intrinsic properties of the categorical variables.

# **links to learn more about entity embbeding** : 
# * https://arxiv.org/abs/1604.06737
# * https://medium.com/@george.drakos62/decoded-entity-embeddings-of-categorical-variables-in-neural-networks-1d2468311635
# * https://www.youtube.com/watch?v=EATAM3BOD_E&fbclid=IwAR3elEdSoNavsh0WQ1gqAiVYHuPPcCrgWL98gUDAosjeOYLbnAqU_FsyS0w
# 

# ## Categorical Features To List Form 
# 
# One need to convert data to list format to match the network structure
# 
# The following function takes the list of categorical features, and prepare such lists for the NN input.
# 
# 

# In[ ]:


#converting data to list format to match the network structure
def preproc(X_train, X_val, X_test):

    input_list_train = dict()
    input_list_val = dict()
    input_list_test = dict()
    
    #the cols to be embedded: rescaling to range [0, # values)
    for c in embed_cols:
        cat_emb_name= c.replace(" ", "")+'_Embedding'
        raw_vals = X_train[c].unique()
        val_map = {}
        for i in range(len(raw_vals)):
            val_map[raw_vals[i]] = i       
        input_list_train[cat_emb_name]=X_train[c].map(val_map).values
        input_list_val[cat_emb_name]=X_val[c].map(val_map).fillna(0).values
        input_list_test[cat_emb_name]=X_test[c].map(val_map).fillna(0).values
    
    input_list_train['points']=X_train['points'].values
    input_list_val['points']=X_val['points'].values
    input_list_test['points']=X_test['points'].values

    input_list_train['description']=X_train[description_features].values
    input_list_val['description']=X_val[description_features].values
    input_list_test['description']=X_test[description_features].values

    input_list_train['title']=X_train[title_features].values
    input_list_val['title']=X_val[title_features].values
    input_list_test['title']=X_test[title_features].values

    input_list_train['desgination']=X_train[des_features].values
    input_list_val['desgination']=X_val[des_features].values
    input_list_test['desgination']=X_test[des_features].values
    
    return input_list_train, input_list_val, input_list_test


# In[ ]:



train = all_data[all_data['price']!=-1].reset_index(drop=True) 
test = all_data[all_data['price']==-1].reset_index(drop=True) 
embed_cols=['country','province','region_1','variety','winery']


# ##  Embedding Dimension - Hyperparamter 

# In[ ]:


for categorical_var in embed_cols:
    
    cat_emb_name= categorical_var.replace(" ", "")+'_Embedding'
  
    no_of_unique_cat  = train[categorical_var].nunique()
    embedding_size = int(min(np.ceil((no_of_unique_cat)/2), 64))
  
    print('Categorica Variable:', categorical_var,
        'Unique Categories:', no_of_unique_cat,
        'Embedding Size:', embedding_size)


# # Entity Embeddings Model 
# 
# 

# In[ ]:


# Proper Naming of Categorical Features for Labelling NN Layers
for categorical_var in embed_cols :
    
    input_name= 'Input_' + categorical_var.replace(" ", "")
    print(input_name)


# Here we basically make the embeding layers one at a time and append, and at the end we concatenate it together with the numerical features.

# In[ ]:


cat_features =['country','province','region_1','variety','winery']


# In[ ]:


def create_model(data, cat_cols  ):    
  input_models=[]
  output_embeddings=[]

  for categorical_var in cat_cols :
      
      #Name of the categorical variable that will be used in the Keras Embedding layer
      cat_emb_name= categorical_var.replace(" ", "")+'_Embedding'
    
      # Define the embedding_size
      no_of_unique_cat  = data[categorical_var].nunique() +1
      embedding_size = int(min(np.ceil((no_of_unique_cat)/2), 24 ))
    
      #One Embedding Layer for each categorical variable
      input_model = layers.Input(shape=(1,),name=cat_emb_name)
      output_model = layers.Embedding(no_of_unique_cat, embedding_size, name=cat_emb_name+'emblayer')(input_model)
      output_model = layers.Reshape(target_shape=(embedding_size,))(output_model)    
    
      #Appending all the categorical inputs
      input_models.append(input_model)
    
      #Appending all the embeddings
      output_embeddings.append(output_model)
    
  #Other non-categorical data columns (numerical). 
  #I define single another network for the other columns and add them to our models list.


  input_numeric = layers.Input(shape=(1,),name='points')
  embedding_numeric = layers.Dense(16, kernel_initializer="uniform")(input_numeric) 
  input_models.append(input_numeric)
  output_embeddings.append(embedding_numeric)

  #description NN
  input_numeric = layers.Input(shape=(len(description_features),),name='description')

  embedding_numeric = layers.Dense(512, kernel_initializer="uniform")(input_numeric) 
  embedding_numeric = layers.Activation('relu')(embedding_numeric)
  embedding_numeric= layers.Dropout(0.6)(embedding_numeric)
  embedding_numeric = layers.Dense(256, kernel_initializer="uniform")(embedding_numeric) 
  embedding_numeric = layers.Activation('relu')(embedding_numeric)
  embedding_numeric= layers.Dropout(0.4)(embedding_numeric)

  input_models.append(input_numeric)
  output_embeddings.append(embedding_numeric)

  # Title NN
  input_numeric = layers.Input(shape=(len(title_features),),name='title')
  embedding_numeric = layers.Dense(32, kernel_initializer="uniform")(input_numeric) 
  embedding_numeric = layers.Activation('relu')(embedding_numeric)
  embedding_numeric= layers.Dropout(0.6)(embedding_numeric)
  input_models.append(input_numeric)
  output_embeddings.append(embedding_numeric)

  # desgination NN
  input_numeric = layers.Input(shape=(len(des_features),),name='desgination')
  embedding_numeric = layers.Dense(32, kernel_initializer="uniform")(input_numeric)
  embedding_numeric = layers.Activation('relu')(embedding_numeric)
  embedding_numeric= layers.Dropout(0.4)(embedding_numeric) 
  
  input_models.append(input_numeric)
  output_embeddings.append(embedding_numeric)

  #At the end we concatenate altogther and add other Dense layers
  output = layers.Concatenate()(output_embeddings)


  output = layers.Dense(1024, kernel_initializer="uniform")(output)
  output = layers.Activation('relu')(output)
  output= layers.Dropout(0.6)(output)
  output = layers.Dense(512, kernel_initializer="uniform")(output)
  output = layers.Activation('relu')(output)
  output= layers.Dropout(0.4)(output)
  output = layers.Dense(256, kernel_initializer="uniform")(output)
  output = layers.Activation('relu')(output)
  output= layers.Dropout(0.2)(output)
  output = layers.Dense(1)(output)

  model = Model(inputs=input_models, outputs=output)
  return model 


# ## The Network Architecture

# In[ ]:


model = create_model(train , cat_features )
model.summary()


# # Data preprocessing 

# In[ ]:


from sklearn.preprocessing import StandardScaler
scalar=StandardScaler()
scalar.fit(train['points'].values.reshape(-1, 1))
train['points']=scalar.transform(train['points'].values.reshape(-1, 1)) 
test['points']=scalar.transform(test['points'].values.reshape(-1, 1)) 


# In[ ]:


# try 
def root_mean_squared_error(y_true, y_pred):
        return K.sqrt(K.mean(K.square(y_pred - y_true), axis=-1)) 


# In[ ]:


def rmse(predictions, targets): 
  return sqrt(mean_squared_error(predictions, targets))


# In[ ]:


X_train,X_vaild =model_selection.train_test_split(train)


# In[ ]:


y_train,y_valid = X_train.price,X_vaild.price
X_train,X_vaild,_ = preproc(X_train,X_vaild,train)


# ## hyperparameters fine tuning

# In[ ]:


EPOCHS = 10 
BATCH_SIZE =1024
AUTO = tf.data.experimental.AUTOTUNE


# In[ ]:


train[description_features].shape


# In[ ]:


train_dataset = (
    tf.data.Dataset
    .from_tensor_slices((X_train, y_train))
    .repeat() 
    .shuffle(2048)
    .batch(BATCH_SIZE)
    .prefetch(AUTO)
)

valid_dataset = (
    tf.data.Dataset
    .from_tensor_slices((X_vaild, y_valid))
    .batch(BATCH_SIZE)
    .cache()
    .prefetch(AUTO)
)


# In[ ]:


model = create_model(train, cat_features)
es = callbacks.EarlyStopping(monitor='val_loss', min_delta=0.0001,
                                 verbose=5, baseline=None, restore_best_weights=True)
rlr = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5,
                                      patience=3, min_lr=1e-6, mode='max', verbose=1)
model.compile(optimizer = Adam(lr=5e-5), loss = 'mean_squared_error', metrics =[root_mean_squared_error])
n_steps = sum( [x.shape[0] for x in X_train.values()] ) // BATCH_SIZE
train_history = model.fit(
    train_dataset,
    steps_per_epoch=n_steps,
    validation_data=valid_dataset,
    epochs=EPOCHS
)

              


# In[ ]:



# summarize history for accuracy
plt.plot(train_history.history['loss'])
plt.plot(train_history.history['val_loss'])
plt.title('loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper right')
plt.show()


# In[ ]:


valid_fold_preds = model.predict(X_vaild)
print(rmse(y_valid.values, valid_fold_preds  ))


# In[ ]:


kf = model_selection.KFold(n_splits=10)

test_preds = np.zeros((len(test)))
score = []
counter = 0 
for fold, (train_index, test_index) in enumerate(kf.split(X=train)):
    counter = counter + 1 
    X_train, X_valid = train.iloc[train_index, :], train.iloc[test_index, :]
    y_train, y_valid = X_train['price'].values, X_valid['price'].values
    X_train ,X_vaild,X_test= preproc(X_train,X_valid,test)
   
    train_dataset = (
    tf.data.Dataset
    .from_tensor_slices((X_train, y_train))
    .repeat() 
    .shuffle(2048)
    .batch(BATCH_SIZE)
    .prefetch(AUTO)
    )

    valid_dataset = (
        tf.data.Dataset
        .from_tensor_slices((X_vaild, y_valid))
        .batch(BATCH_SIZE)
        .cache()
        .prefetch(AUTO)
      )
    test_dataset = (
      tf.data.Dataset
    .from_tensor_slices(X_test)
    .batch(BATCH_SIZE)
    )
    model = create_model(train, cat_features)
    es = callbacks.EarlyStopping(monitor='val_loss', min_delta=0.0001,
                                 verbose=5, baseline=None, restore_best_weights=True)
    rlr = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5,
                                          patience=3, min_lr=1e-6, mode='max', verbose=1)
    model.compile(optimizer = Adam(lr=5e-5), loss = 'mean_squared_error', metrics =[root_mean_squared_error])
    n_steps = sum( [x.shape[0] for x in X_train.values()] ) // BATCH_SIZE
    train_history = model.fit(
        train_dataset,
        steps_per_epoch=n_steps,
        validation_data=valid_dataset,
        epochs=10
    )

    valid_fold_preds = model.predict(valid_dataset, verbose=1)
    print(f'fold {fold} loss = ' ,  rmse(y_valid, valid_fold_preds  ))     
    score.append( rmse(y_valid, valid_fold_preds ))
    test_fold_preds = model.predict(test_dataset, verbose=1)
    test_preds += test_fold_preds.ravel()

    K.clear_session()


# In[ ]:


test_preds /= counter
test_ids = test.id.values
print("Saving submission file")
submission = pd.DataFrame.from_dict({
    'id': test_ids,
    'price': test_preds
})
submission.to_csv("submission.csv", index=False)


# In[ ]:


submission['price'].hist()


# # Modeling with PYTORCH 

# in this section i will use pytorch to 
# implement Entity Embbeding then i will use bert to handel the text features . 
# 
# so if you wanna learn how to work with PYTORCH i suggest that you go throw this course : https://www.coursera.org/learn/deep-neural-networks-with-pytorch

# ### Simple Linear Model 

# In[ ]:


import torch 
from torch import nn,optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
torch.manual_seed(0)
from sklearn import preprocessing  
import transformers 
from tqdm.notebook import tqdm
import pandas as pd
import numpy as np
from sklearn import model_selection
from sklearn import metrics
from transformers import AdamW
from transformers import get_linear_schedule_with_warmup


# In[ ]:


train = pd.read_csv('trainfinal.csv')


# In[ ]:


class simple_linear(nn.Module) : 
  def __init__(self) : 
    super(simple_linear,self).__init__()
    self.linear1 = nn.Linear(1,128)
    self.linear = nn.Linear(128,1) 
  def forward(self,data) :
    points = (data['points'].view(-1,1)).to(device,dtype=torch.float)  
    x=F.relu(self.linear1(points))
    out = self.linear(x)
    return out 


# In[ ]:


from sklearn.preprocessing import StandardScaler
scalar=StandardScaler()
scalar.fit(train['points'].values.reshape(-1, 1))
train['points']=scalar.transform(train['points'].values.reshape(-1, 1)) 


# In[ ]:


class data_set : 
  def __init__(self,df) : 
    self.points = df.points 
    self.price = df.price 
  def __len__(self) : 
    return(len(self.price)) 
  def __getitem__(self,index) : 
    return {
        'points' : torch.tensor(self.points[index]) , 
        'price'  : torch.tensor(self.price[index])
    }


# ### Entity Embeddings with Pytorch 

# ### Data preprocessing 

# In[ ]:


categorical_features = ['country','province','region_1','variety','winery']


# In[ ]:


for f in categorical_features : 
  label_encoder = preprocessing.LabelEncoder()
  label_encoder.fit(train[f].astype('str'))
  train[f] = label_encoder.transform(train[f].astype('str').fillna('-1'))


# In[ ]:


class EmbDataSet() : 
  def __init__(self,df,cat_features) : 
    self.df = df
    self.categorical  = cat_features 
  def __len__(self) : 
    return len(self.df)
  def __getitem__(self,item) : 
    out = dict()
    for i in self.categorical : 
      out[i] = torch.tensor( self.df[i].values[item] , dtype=torch.long )
    
    out['points'] = torch.tensor(self.df['points'].values[item], dtype=torch.float )

    out['price'] = torch.tensor(self.df['price'].values[item],dtype=float ) 
    return out 
    


# In[ ]:


def get_emb_dim(df,categorical):
  output=[]
  for categorical_var in categorical:
      
      cat_emb_name= categorical_var.replace(" ", "")+'_Embedding'
    
      no_of_unique_cat  = train[categorical_var].nunique()
      embedding_size = int(min(np.ceil((no_of_unique_cat)/2), 24))
      output.append((no_of_unique_cat,embedding_size))    
      print('Categorica Variable:', categorical_var,
          'Unique Categories:', no_of_unique_cat,
          'Embedding Size:', embedding_size)
  return output


# In[ ]:


emb_size = get_emb_dim(train,categorical_features)


# In[ ]:


class Embedding_model(nn.Module) : 
  def __init__(self,cat,emb_size) :
    super(Embedding_model,self).__init__()
    self.cat =cat 
    self.emb_size = emb_size 
    outputs_cat = nn.ModuleList()
    for inp , emb  in emb_size :
      embedding_layer = nn.Embedding(inp+2,emb)
                                   
      outputs_cat.append(embedding_layer)
    self.outputs_cat = outputs_cat 

    n_emb = sum([e[1] for e in self.emb_size])
    self.num = nn.Sequential( nn.Linear(1,128),
                              nn.Dropout(0.4) 
                              )
    self.embedding = nn.Sequential( nn.Linear(n_emb,384),
                                    nn.Dropout(0.4)
                                    )
    
    self.fc = nn.Sequential(  

                            
                              nn.Linear(512,256),
                              nn.Dropout(0.3),
                              nn.ReLU(),
                              nn.Linear(256,1)
    )

        
  def forward(self,data)  : 
    outputs_emb = [] 
    for i in range(len(self.cat)) : 
      inputs = data[self.cat[i]].to(device,dtype=torch.long) 
      out = self.outputs_cat[i](inputs)
      outputs_emb.append(out) 
    
    x_cat = torch.cat(outputs_emb,dim= 1)
    x_cat = self.embedding(x_cat)

    inputs = (data['points'].view(-1,1)).to(device,dtype=torch.float)
    inputs = self.num(inputs)
    
    x_all = torch.cat([inputs,x_cat],dim=1) 
    x_final = self.fc(x_all)

    return x_final


# ## Bert Model 

# ## What is BERT ? 
# 
# 

# BERT (Bidirectional Encoder Representations from Transformers) is a  paper published by researchers at Google AI Language. It has caused a stir in the Machine Learning community by presenting state-of-the-art results in a wide variety of NLP tasks, including Question Answering (SQuAD v1.1), Natural Language Inference (MNLI), and others.
# 
# i have learned how to use BERT from this video https://www.youtube.com/watch?v=hinZO--TEk4&t=6s , and have understand how does bert work from this playlist of videos https://www.youtube.com/watch?v=FKlPCK1uFrc&list=PLam9sigHPGwOBuH4_4fr-XvDbe5uneaf6

# ## Implementation of bert with PYTORCH

# In[ ]:


class BertBaseUncased(nn.Module) :
    def __init__(self) : 
        super(BertBaseUncased,self).__init__() 
        self.bert = transformers.BertModel.from_pretrained(BERT_PATH) 
        self.bert_drop = nn.Dropout(0.4) 
        self.out = nn.Linear(768,1) 
    def forward(self,d) : 
        ids = d["ids"]
        token_type_ids = d["token_type_ids"]
        mask = d["mask"]

        ids = ids.to(device, dtype=torch.long)
        token_type_ids = token_type_ids.to(device, dtype=torch.long)
        mask = mask.to(device, dtype=torch.long)
        out1,out2 = self.bert( 
            ids , 
            attention_mask = mask , 
            token_type_ids = token_type_ids 
        )
        bo = self.bert_drop(out2) 
        output = self.out(bo) 
        return output 


# # Engine

# In[ ]:


def loss_fn(outputs, targets):
    return nn.MSELoss()(outputs, targets.view(-1, 1))


# In[ ]:


def train_fn(data_loader, model, optimizer, scheduler):
  model.train()
  tr_loss = 0 
  counter = 0 
  for bi, d in tqdm(enumerate(data_loader), total=len(data_loader)):
    targets = d["price"]
    targets = targets.to(device, dtype=torch.float)
    optimizer.zero_grad()
    outputs = model(d)

    loss = loss_fn(outputs, targets)
    tr_loss += loss.item()
    counter +=1 
    loss.backward()
    optimizer.step()
  return tr_loss/counter


# In[ ]:


def eval_fn(data_loader, model):
  model.eval()
  fin_loss = 0
  counter = 0
  with torch.no_grad():
    for bi, d in tqdm(enumerate(data_loader), total=len(data_loader)):
      targets = d["price"]
      targets = targets.to(device, dtype=torch.float)
      outputs = model(d)
      loss = loss_fn(outputs, targets)
      fin_loss +=loss.item()
      counter += 1
    return fin_loss/counter 


# # Training 

# In[ ]:


df_train, df_valid = model_selection.train_test_split(
        train,
        test_size=0.2,
        random_state=42,
    )


# In[ ]:


DEVICE =torch.device("cuda")
device = torch.device("cuda")
def run(model,EPOCHS):
    
    train_data_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=TRAIN_BATCH_SIZE,
        num_workers=4
    )
    
    
    valid_data_loader = torch.utils.data.DataLoader(
        valid_dataset,
        batch_size=VALID_BATCH_SIZE,
        num_workers=1
    )

    device = torch.device("cuda")
    
    
    param_optimizer = list(model.named_parameters())
    no_decay = ["bias", "LayerNorm.bias", "LayerNorm.weight"]
    optimizer_parameters = [
        {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)], 'weight_decay': 0.001},
        {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)], 'weight_decay': 0.0},
    ]

    num_train_steps = int(len(train_data_loader)) * EPOCHS
    optimizer = AdamW(optimizer_parameters, lr=1e-3)
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0,
        num_training_steps=num_train_steps
    )


    model = nn.DataParallel(model)

    train_loss =  []
    val_loss = []
    for epoch in range(EPOCHS):
       
        tr_loss=train_fn(train_data_loader, model, optimizer, scheduler)
        train_loss.append(tr_loss)
        print(f" train_loss  = {np.sqrt(tr_loss)}")

        
        val = eval_fn(valid_data_loader, model)
        val_loss.append(val)
        print(f" val_loss  = {np.sqrt(val)}")

        scheduler.step()
    return val_loss,train_loss


# ## trying Bert 

# ## trying Embedding Categorical + Points  

# In[ ]:


TRAIN_BATCH_SIZE =128
VALID_BATCH_SIZE = 64


# In[ ]:


train_dataset = EmbDataSet(
        df_train,categorical_features
    )

valid_dataset = EmbDataSet(
        df_valid,
        categorical_features

    )


# In[ ]:


model = Embedding_model(categorical_features,emb_size)
model.to(device)
getattr(tqdm, '_instances', {}).clear()
val_loss,tr_loss = run(model,30)


# In[ ]:



# summarize history for accuracy
plt.plot(tr_loss)
plt.plot(val_loss)
plt.title('loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper right')
plt.show()


# In[ ]:


# summarize history for accuracy
plt.plot(np.sqrt(tr_loss))
plt.plot(np.sqrt(val_loss))
plt.title('mean_squared_error')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper right')
plt.show()


# # putting it all together 

# ![image.png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABUQAAAJ5CAYAAABmPzqqAAAgAElEQVR4Aey9+ZMc1ZmwS8T94bt/wf0Hunqt/uYGYheL8YKX2ewxtmewP9sz89maGY+t1sbe1a3WjhZaorUipFarVyGBAIMwCGGJHbEvUhtaG4sAS0AMCvwRzCXivXGyO7OrqrOqsrpOZp48+TgCV6u6KvPk+z7nnDefPpl5XuuuU8J/xAAGYAAGYAAGYAAGYAAGYAAGYAAGYAAGYAAGYCANDJyXhoPkGOnMMAADMAADMAADMAADMAADMAADMAADMAADMAADigGEKCtkWSEMAzAAAzAAAzAAAzAAAzAAAzAAAzAAAzAAA6lhACEK7KmBnb8C8VcgGIABGIABGIABGIABGIABGIABGIABGIABhChCFCEKAzAAAzAAAzAAAzAAAzAAAzAAAzAAAzAAA6lhACEK7KmBnb8A8RcgGIABGIABGIABGIABGIABGIABGIABGIABhChCFCEKAzAAAzAAAzAAAzAAAzAAAzAAAzAAAzAAA6lhACEK7KmBnb8A8RcgGIABGIABGIABGIABGIABGIABGIABGIABhChCFCEKAzAAAzAAAzAAAzAAAzAAAzAAAzAAAzAAA6lhACEK7KmBnb8A8RcgGIABGIABGIABGIABGIABGIABGIABGIABhChCFCEKAzAAAzAAAzAAAzAAAzAAAzAAAzAAAzAAA6lhACEK7KmBnb8A8RcgGIABGIABGIABGIABGIABGIABGIABGIABhChCFCEKAzAAAzAAAzAAAzAAAzAAAzAAAzAAAzAAA6lhACEK7KmBnb8A8RcgGIABGIABGIABGIABGIABGIABGIABGIABhChCFCEKAzAAAzAAAzAAAzAAAzAAAzAAAzAAAzAAA6lhACEK7KmBnb8A8RcgGIABGIABGIABGIABGIABGIABGIABGIABhChCFCEKAzAAAzAAAzAAAzAAAzAAAzAAAzAAAzAAA6lhACEK7KmBnb8A8RcgGIABGIABGIABGIABGIABGIABGIABGIABhChCFCEKAzAAAzAAAzAAAzAAAzAAAzAAAzAAAzAAA6lhACEK7KmBnb8A8RcgGIABGIABGIABGIABGIABGIABGIABGIABhChCFCEKAzAAAzAAAzAAAzAAAzAAAzAAAzAAAzAAA6lhACEK7KmBnb8A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)

# In[ ]:


class Final_Data_set : 
    def __init__(self,df,cat_features) : 
        self.df = df
        self.categorical  = cat_features 
        self.description = df['description'].values
        self.tokenizer = TOKENZIER 
        self.max_len = MAX_Len 
    def __len__(self) : 
        return len(self.description) 
    def __getitem__(self, item):
      out = dict()
        
      # bert input  

      text = str(self.description[item])
      text = " ".join(text.split())

      inputs = self.tokenizer.encode_plus(
              text,
              None,
              add_special_tokens=True,
              max_length=self.max_len
          )

      ids = inputs["input_ids"]
      mask = inputs["attention_mask"]
      token_type_ids = inputs["token_type_ids"]

      padding_length = self.max_len - len(ids)
      ids = ids + ([0] * padding_length)
      mask = mask + ([0] * padding_length)
      token_type_ids = token_type_ids + ([0] * padding_length)

      out['ids']= torch.tensor(ids, dtype=torch.long)
      out['mask']= torch.tensor(mask, dtype=torch.long)
      out['token_type_ids'] = torch.tensor(token_type_ids, dtype=torch.long)
      
      # other inputs 
      for i in self.categorical : 
        out[i] = torch.tensor( self.df[i].values[item] , dtype=torch.long )
    
      out['points'] = torch.tensor(self.df['points'].values[item], dtype=torch.float )
      out['price'] = torch.tensor(self.df['price'].values[item],dtype=float ) 

      return out


# In[ ]:


class Final_Model(nn.Module) : 
  def __init__(self,cat,emb_size) :
    super(Final_Model,self).__init__()


    # Embeddings layers 
    self.cat =cat 
    self.emb_size = emb_size 
    outputs_cat = nn.ModuleList()
    for inp , emb  in emb_size :
      embedding_layer = nn.Embedding(inp+2,emb)
                                   
      outputs_cat.append(embedding_layer)
    
    self.outputs_cat = outputs_cat 
    n_emb = sum([e[1] for e in self.emb_size])
    self.embedding = nn.Sequential( nn.Linear(n_emb,384),
                                    nn.Dropout(0.4)
                                    )
    
    #Numerical layers 
    self.num = nn.Sequential( nn.Linear(1,128),
                              nn.Dropout(0.4) 
                              )
    #BERT input
    self.bert = transformers.BertModel.from_pretrained(BERT_PATH) 
    self.bert_drop = nn.Dropout(0.4) 
    self.bert_out = nn.Linear(768,512) 
    

    #putting it all together
    self.fc = nn.Sequential(  

                              nn.Linear(1024,512),
                              nn.Dropout(0.4),
                              nn.ReLU(),
                              nn.Linear(512,256),
                              nn.Dropout(0.3),
                              nn.ReLU(),
                              nn.Linear(256,1)
    )

        
  def forward(self,data)  : 
    
    # Categorical features 
    outputs_emb = [] 
    for i in range(len(self.cat)) : 
      inputs = data[self.cat[i]].to(device,dtype=torch.long) 
      out = self.outputs_cat[i](inputs)
      outputs_emb.append(out) 
    x_cat = torch.cat(outputs_emb,dim= 1)
    x_cat = self.embedding(x_cat)

    #numrique features
    inputs = (data['points'].view(-1,1)).to(device,dtype=torch.float)
    inputs = self.num(inputs)
    
    #description input
    ids = data["ids"].to(device, dtype=torch.long)
    token_type_ids = data["token_type_ids"].to(device, dtype=torch.long)
    mask = data["mask"].to(device, dtype=torch.long)
    out1,out2 = self.bert( 
                             ids , 
                             attention_mask = mask , 
                             token_type_ids = token_type_ids 
                         )
    bo = self.bert_drop(out2) 
    output = self.bert_out(bo) 

    #putting it all together 
    x_all = torch.cat([output,inputs,x_cat],dim=1) 
    x_final = self.fc(x_all)

    return x_final


# ## training the model 

# In[ ]:


MAX_Len = 128 
TRAIN_BATCH_SIZE =96
VALID_BATCH_SIZE = 32
BERT_PATH = 'bert-base-uncased'
TOKENZIER = transformers.BertTokenizer.from_pretrained(BERT_PATH ,do_lower_case = True )


# In[ ]:


train_dataset = Final_Data_set(
        df_train,categorical_features
    )

valid_dataset = Final_Data_set(
        df_valid,
        categorical_features

    )


# In[ ]:


model = Final_Model(categorical_features,emb_size)
model.to(device)
getattr(tqdm, '_instances', {}).clear()
#val_loss,tr_loss = run(model,30)


# In[ ]:




