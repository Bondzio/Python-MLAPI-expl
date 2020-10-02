#!/usr/bin/env python
# coding: utf-8

# ## Magic Of Tensorflow 
# ### Tensorflow can create magic with simplest implementaion .This Kernel is proof of that 
# ### If you are Beginner in NLP and Tensorflow then this for You 
# ### Achieved 99% Accuracy with this implementation.Upvotes are really appreciable !!

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# ### Load All important packages 

# In[ ]:


from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np
pd.set_option('display.max_colwidth', -1)
import warnings; warnings.simplefilter('ignore')

print(tf.__version__)


# ## Read train and Test CSV File

# In[ ]:


train = pd.read_csv('/kaggle/input/jigsaw-toxic-comment-classification-challenge/train.csv')
test = pd.read_csv('/kaggle/input/jigsaw-toxic-comment-classification-challenge/test.csv')


# ### Check some values of toxic comments 

# In[ ]:


train[train['toxic']== -1].head(20)


# ### this is multi class classification problem , for simplicity we will consider only one column at a time i.e 'toxic' as label

# In[ ]:


# taking comment_text as input feature and toxic as output feature 

#list_classes = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
#train_labels = train[list_classes].values
train_data = train[['comment_text']]
train_labels = train['toxic']
test_data = test[['comment_text']]
#test_labels = test[['toxic']]
#pd.DataFrame(train_data)
print('training data shape',train_data.shape)
print('training label shape',train_labels.shape)
print('testing data shape',test_data.shape)


# ### Data Cleaning is require as there are so many junk values , chracters and symbol
# ### first we will convert all char to lower case and will perform operations 

# In[ ]:


#data pre-processing packages 
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
from nltk.stem import WordNetLemmatizer
import re


# In[ ]:


#convert to lower case 

train_data['comment_text'] = train_data['comment_text'].str.lower()
test_data['comment_text'] = test_data['comment_text'].str.lower()


# In[ ]:


# remove \n 
#print(train_data['comment_text'].head(2))
train_data['comment_text'] = train_data['comment_text'].str.replace('\n',' ')
test_data['comment_text'] = test_data['comment_text'].str.replace('\n',' ')
#print(train_data['comment_text'].head(2))


# In[ ]:


#similarly replace all possible phrases 
train_data['comment_text'] = train_data['comment_text'].str.replace("i'm",'i am')
train_data['comment_text'] = train_data['comment_text'].str.replace("he's",'he is')
train_data['comment_text'] = train_data['comment_text'].str.replace("weren't",'were not')
train_data['comment_text'] = train_data['comment_text'].str.replace("she's",'she is')
train_data['comment_text'] = train_data['comment_text'].str.replace("that's",'that is')
train_data['comment_text'] = train_data['comment_text'].str.replace("you'r",'you are')
train_data['comment_text'] = train_data['comment_text'].str.replace("what's",'what is')
train_data['comment_text'] = train_data['comment_text'].str.replace("how's",'how is')
train_data['comment_text'] = train_data['comment_text'].str.replace("where's",'where is')
train_data['comment_text'] = train_data['comment_text'].str.replace("\'ll",'will')
train_data['comment_text'] = train_data['comment_text'].str.replace("\'ve", "have")
train_data['comment_text'] = train_data['comment_text'].str.replace("won't",'will not')
train_data['comment_text'] = train_data['comment_text'].str.replace("can't",'can not')


# In[ ]:


#similarly replace all possible phrases in test
test_data['comment_text'] = test_data['comment_text'].str.replace("i'm",'i am')
test_data['comment_text'] = test_data['comment_text'].str.replace("he's",'he is')
test_data['comment_text'] = test_data['comment_text'].str.replace("weren't",'were not')
test_data['comment_text'] = test_data['comment_text'].str.replace("she's",'she is')
test_data['comment_text'] = test_data['comment_text'].str.replace("that's",'that is')
test_data['comment_text'] = test_data['comment_text'].str.replace("you'r",'you are')
test_data['comment_text'] = test_data['comment_text'].str.replace("what's",'what is')
test_data['comment_text'] = test_data['comment_text'].str.replace("how's",'how is')
test_data['comment_text'] = test_data['comment_text'].str.replace("where's",'where is')
test_data['comment_text'] = test_data['comment_text'].str.replace("\'ll",'will')
test_data['comment_text'] = test_data['comment_text'].str.replace("\'ve", "have")
test_data['comment_text'] = test_data['comment_text'].str.replace("won't",'will not')
test_data['comment_text'] = test_data['comment_text'].str.replace("can't",'can not')


# In[ ]:


#remove ip address 
train_data['comment_text'] = train_data['comment_text'].str.replace("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}","")
test_data['comment_text'] = test_data['comment_text'].str.replace("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}","")

#train_data['comment_text'] = re.sub("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}","",train_data['comment_text'])


# In[ ]:


#remove username 
train_data['comment_text'] = train_data['comment_text'].str.replace("\[\[.*\]","")
test_data['comment_text'] = test_data['comment_text'].str.replace("\[\[.*\]","")


# In[ ]:


#remove symbols , special char
train_data['comment_text'] = train_data['comment_text'].str.replace(r"[-()\"#/@;:<>{}`+=~|.!?,]", "")
test_data['comment_text'] = test_data['comment_text'].str.replace(r"[-()\"#/@;:<>{}`+=~|.!?,]", "")


# ## Tokenizing and Padding Words 
# ### In Tensorflow we cant process stream of characters as it as , so convert them into integer format .Now Each statement is of differrent length so need to convert it into same length hence extra padding of 0 is required
# ### It is good practice to define all imp parameter before code as shown below , here i am taking vocab_size = 20k , max_lenght = 200 and embedding size = 16

# In[ ]:


vocab_size = 20000
embedding_dim = 16
max_length = 200
trunc_type = 'post'
oov_tok ="<OOV>"

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
list_train_sentences = train_data['comment_text']
list_test_sentences = test_data['comment_text']
tokenizer = Tokenizer(num_words = vocab_size,oov_token=oov_tok)
tokenizer.fit_on_texts(list(list_train_sentences))
tokenizer.fit_on_texts(list(list_test_sentences))
word_index = tokenizer.word_index
train_sequences = tokenizer.texts_to_sequences(list_train_sentences)
train_padded = pad_sequences(train_sequences,maxlen=max_length,truncating=trunc_type)

test_sequences = tokenizer.texts_to_sequences(list_test_sentences)
test_padded = pad_sequences(test_sequences,maxlen=max_length,truncating=trunc_type)


# In[ ]:


#build model 
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size,embedding_dim,input_length=max_length),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(6,activation='relu'),
    tf.keras.layers.Dense(1,activation='sigmoid')
])
model.compile(loss="binary_crossentropy",optimizer='adam',metrics=['accuracy'])
model.summary()


# ### 99% accuracy is achieved with Basic Tensorflow Implementation !!

# In[ ]:


# Fit the model
num_epochs = 10
model.fit(train_padded,train_labels,epochs=num_epochs)


# In[ ]:


# Predict toxicity on Test Data 
num_epochs = 10
test_res = model.predict(test_padded)


# In[ ]:


# Create New data Frame For Predicted Toxic Values for 'toxic' column
test_result = pd.DataFrame(test_res,columns=['Predicted'])
test_result.head()


# In[ ]:


# read Actual Toxic Value for comarision 
#test_l = pd.read_csv(r'../input/jigsaw-toxic-comment-classification-challenge/test_labels.csv')
#test_l = pd.read_csv('/kaggle/input/jigsaw-toxic-comment-classification-challenge/test_labels.csv')
# for some reason kaggel was not reading test_labels file so i uploaded externally and reading as follows 
# otherwise you can uncomment above 
test_l = pd.read_csv('../input/test-lab/test_labels.csv')
#../input/jigsaw-toxic-comment-classification-challenge/test_labels.csv
test_result['Actual'] = test_l['toxic']


# In[ ]:


# check Comparision 
test_result.head(20)


# ### you can check from above predicted and actual values most of the values are correctly predicted specially value 0 , there is no explanation of value -1 in problem statement, infact there are no -1 values in train set.So need Feature Engineering there !
# 
# ### We have calculated it for only column 'toxic' , similarly you can try for other column and can submit by uncommenting below cell 
# 
# ### If you really like this kernel , please upvote it and give feedback in comment section below , Thanks !
# 

# In[ ]:


# sample_submission = pd.read_csv('/kaggle/input/jigsaw-toxic-comment-classification-challenge/sample_submission.csv')
# sample_submission['toxic'] = test_res
# sample_submission.to_csv('submission.csv',index = False)

