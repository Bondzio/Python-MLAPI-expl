#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Ignore  the warnings
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

# data visualisation and manipulation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns
#configure
# sets matplotlib to inline and displays graphs below the corressponding cell.
get_ipython().run_line_magic('matplotlib', 'inline')
style.use('fivethirtyeight')
sns.set(style='whitegrid',color_codes=True)

#nltk
import nltk

#preprocessing
from nltk.corpus import stopwords  #stopwords
from nltk import word_tokenize,sent_tokenize # tokenizing
from nltk.stem import PorterStemmer,LancasterStemmer  # using the Porter Stemmer and Lancaster Stemmer and others
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer  # lammatizer from WordNet

# for part-of-speech tagging
from nltk import pos_tag

# for named entity recognition (NER)
from nltk import ne_chunk

# vectorizers for creating the document-term-matrix (DTM)
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer

# BeautifulSoup libraray
from bs4 import BeautifulSoup 

import re # regex

#model_selection
from sklearn.model_selection import train_test_split,cross_validate
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV

#evaluation
from sklearn.metrics import accuracy_score,roc_auc_score 
from sklearn.metrics import classification_report
from mlxtend.plotting import plot_confusion_matrix

#preprocessing scikit
from sklearn.preprocessing import MinMaxScaler,StandardScaler,Imputer,LabelEncoder

#classifiaction.
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC,SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier,AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB,MultinomialNB
 
#stop-words
stop_words=set(nltk.corpus.stopwords.words('english'))

#keras
import keras
from keras.preprocessing.text import one_hot,Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense , Flatten ,Embedding,Input,CuDNNLSTM,LSTM
from keras.models import Model
from keras.preprocessing.text import text_to_word_sequence
from gensim.models import Word2Vec


# In[2]:


rev_frame=pd.read_csv('../input/all_tickets-1551435513304.csv')


# In[3]:


df=rev_frame.copy()


# In[4]:


df.head()


# In[5]:


df=df[['body','urgency']]


# In[6]:


print(df.shape)
df.head()


# In[7]:


# check for null values
print(df['body'].isnull().sum())
df['body'].isnull().sum()  # no null values.


# In[8]:


# remove duplicates/ for every duplicate we will keep only one row of that type. 
df.drop_duplicates(subset=['body','urgency'],keep='first',inplace=True) 


# In[9]:


# now check the shape. note that shape is reduced which shows that we did has duplicate rows.
print(df.shape)
df.head()


# In[10]:


# printing some reviews to see insights.
for review in df['body'][:5]:
    print(review+'\n'+'\n')


# In[11]:


def mark_sentiment(rating):
    if(rating<=2):
        return 0
    else:
        return 1


# In[12]:


df['urgency']=df['urgency'].apply(mark_sentiment)


# In[13]:


df.head()


# In[14]:


df['urgency'].value_counts()


# In[15]:


# function to clean and pre-process the text.
def clean_bodys(body):  
    
    # 1. Removing html tags
    review_text = BeautifulSoup(review,"lxml").get_text()
    
    # 2. Retaining only alphabets.
    review_text = re.sub("[^a-zA-Z]"," ",review_text)
    
    # 3. Converting to lower case and splitting
    word_tokens= review_text.lower().split()
    
    # 4. Remove stopwords
    le=WordNetLemmatizer()
    stop_words= set(stopwords.words("english"))     
    word_tokens= [le.lemmatize(w) for w in word_tokens if not w in stop_words]
    
    cleaned_body=" ".join(word_tokens)
    return cleaned_body


# In[16]:


pos_df=df.loc[df.urgency==1,:][:50000]
neg_df=df.loc[df.urgency==0,:][:50000]


# In[17]:


pos_df.head()


# In[18]:


neg_df.head()


# In[19]:


#combining
df=pd.concat([pos_df,neg_df],ignore_index=True)


# In[20]:


print(df.shape)
df.head()


# In[21]:


# shuffling rows
df = df.sample(frac=1).reset_index(drop=True)
print(df.shape)  # perfectly fine.
df.head()


# In[22]:


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
sentences=[]
sum=0
for review in df['body']:
    sents=tokenizer.tokenize(review.strip())
    sum+=len(sents)
    for sent in sents:
        cleaned_body=clean_bodys(sent)
        sentences.append(cleaned_body.split()) # can use word_tokenize also.
print(sum)
print(len(sentences))  # total no of sentences


# In[23]:


# trying to print few sentences
for te in sentences[:5]:
    print(te,"\n")


# In[24]:


get_ipython().run_cell_magic('time', '', 'import gensim\nw2v_model=gensim.models.Word2Vec(sentences=sentences,size=300,window=10,min_count=1)')


# In[25]:


w2v_model.train(sentences,epochs=10,total_examples=len(sentences))


# In[26]:


# embedding of a particular word.
w2v_model.wv.get_vector('like')


# In[27]:


# total numberof extracted words.
vocab=w2v_model.wv.vocab
print("The total number of words are : ",len(vocab))


# In[28]:


# words most similar to a given word.
w2v_model.wv.most_similar('able')


# In[29]:


# similaraity b/w two words
w2v_model.wv.similarity('happening','able')


# In[30]:


print("The no of words :",len(vocab))
# print(vocab)


# In[31]:


# print(vocab)
vocab=list(vocab.keys())


# In[32]:


word_vec_dict={}
for word in vocab:
  word_vec_dict[word]=w2v_model.wv.get_vector(word)
print("The no of key-value pairs : ",len(word_vec_dict)) # should come equal to vocab size


# In[33]:


maxi=-1
for i,rev in enumerate(df['body']):
    tokens=rev.split()
    if(len(tokens)>maxi):
        maxi=len(tokens)
print(maxi)


# In[34]:


tok = Tokenizer()
tok.fit_on_texts(df['body'])
vocab_size = len(tok.word_index) + 1
encd_rev = tok.texts_to_sequences(df['body'])


# In[35]:


max_rev_len=1565  # max lenght of a review
vocab_size = len(tok.word_index) + 1  # total no of words
embed_dim=300 # emb


# In[36]:


# now padding to have a amximum length of 1565
pad_rev= pad_sequences(encd_rev, maxlen=max_rev_len, padding='post')
pad_rev.shape   # note that we had 100K reviews and we have padded each review to have  a lenght of 1565 words.


# In[37]:


# now creating the embedding matrix
embed_matrix=np.zeros(shape=(vocab_size,embed_dim))
for word,i in tok.word_index.items():
  embed_vector=word_vec_dict.get(word)
  if embed_vector is not None:  # word is in the vocabulary learned by the w2v model
    embed_matrix[i]=embed_vector
  # if word is not found then embed_vector corresspo


# In[38]:


# checking.
print(embed_matrix[14])


# In[39]:


# prepare train and val sets first
Y=keras.utils.to_categorical(df['urgency'])  # one hot target as required by NN.
x_train,x_test,y_train,y_test=train_test_split(pad_rev,Y,test_size=0.20,random_state=42)


# In[40]:


#### Basic Model


# In[41]:


from keras.initializers import Constant
from keras.layers import ReLU
from keras.layers import Dropout
model=Sequential()
model.add(Embedding(input_dim=vocab_size,output_dim=embed_dim,input_length=max_rev_len,embeddings_initializer=Constant(embed_matrix)))
# model.add(CuDNNLSTM(64,return_sequences=False)) # loss stucks at about 
model.add(Flatten())
model.add(Dense(16,activation='relu'))
model.add(Dropout(0.50))
# model.add(Dense(16,activation='relu'))
# model.add(Dropout(0.20))
model.add(Dense(2,activation='sigmoid'))  


# In[42]:


model.summary()


# In[43]:


# compile the model
model.compile(optimizer=keras.optimizers.RMSprop(lr=1e-3),loss='binary_crossentropy',metrics=['accuracy'])


# In[44]:


# specify batch size and epocj=hs for training.
epochs=5
batch_size=64


# In[45]:


# fitting the model.

history=model.fit(x_train,y_train,epochs=epochs,batch_size=batch_size,validation_data=(x_test,y_test))


# In[46]:


plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.legend(['training', 'validation'], loc = 'upper left')
plt.show()


# In[47]:


results = model.evaluate(x_test, y_test)


# In[48]:


print('Test accuracy: ', results[1])


# In[49]:


# Serialize model to JSON
model_json = model.to_json()
with open("./model.json", "w") as json_file:
    json_file.write(model_json)

# Serialize weights to HDF5
model.save_weights("./model.h5")


# In[ ]:




