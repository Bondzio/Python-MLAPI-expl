#!/usr/bin/env python
# coding: utf-8

# Importing Library

# In[ ]:


import numpy as np
import pandas as pd
import re
import string
import matplotlib.pyplot as plt
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.metrics import f1_score,precision_score,recall_score
from sklearn import svm


# In[ ]:


df = pd.read_csv('../input/all.csv')   #importing csv


# In[ ]:


df.head() #showing the first 5 content


# In[ ]:


df.shape


# In[ ]:


df.info()


# In[ ]:


df.isnull().sum()


# In[ ]:


# removing empty data
df.dropna(inplace=True)


# In[ ]:


df.groupby('type').count()


# In[ ]:


content = df['content'].tolist()[:3]


# In[ ]:


print(content)


# In[ ]:


labels = 'Love', 'Mythology & Folklore', 'Nature'
sizes = [326, 58, 187]


fig1, ax1 = plt.subplots(figsize=(5,5))
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()


# **Convert Data into Feature**

# In[ ]:


df.content.str.lower()


# In[ ]:


# remove list in the document
remove_list=["A",
"An",
"The",
"Aboard",
"About",
"Above",
"Absent",
"Across",
"After",
"Against",
"Along",
"Alongside",
"Amid",
"Among",
"Amongst",
"Anti",
"Around",
"As",
"At",
"Before",
"Behind",
"Below",
"Beneath",
"Beside",
"Besides",
"Between",
"Beyond",
"But",
"By",
"Circa",
"Concerning",
"Considering",
"Despite",
"Down",
"During",
"Except",
"Excepting",
"Excluding",
"Failing",
"Following",
"For",
"From",
"Given",
"In",
"Inside",
"Into",
"Like",
"Minus",
"Near",
"Of",
"Off",
"On",
"Onto",
"Opposite",
"Outside",
"Over",
"Past",
"Per",
"Plus",
"Regarding",
"Round",
"SO",
"Save",
"Since",
"Than",
"Through",
"To",
"Toward",
"Towards",
"Under",
"Underneath",
"Unlike",
"Until",
"Up",
"Upon",
"Versus",
"Via",
"With",
"Within",
"Without"]


# In[ ]:


# replace those words with space
for  value in remove_list:
    df.content=df.content.str.replace(value," ")
df.content


# In[ ]:


#function to remove punctuation
def removePunctuation(x):
    x = x.lower()
    x = re.sub(r'[^\x00-\x7f]',r' ',x)
    x = x.replace('\r','')
    x = x.replace('\n','')
    x = x.replace('  ','')
    x = x.replace('\'','')
    return re.sub("["+string.punctuation+"]", " ", x)

#getting stop words
from nltk.corpus import stopwords

stops = set(stopwords.words("english")) 


#function to remove stopwords
def removeStopwords(x):
    filtered_words = [word for word in x.split() if word not in stops]
    return " ".join(filtered_words)


def processText(x):
    x= removePunctuation(x)
    x= removeStopwords(x)
    return x


from nltk.tokenize import sent_tokenize, word_tokenize
X= pd.Series([word_tokenize(processText(x)) for x in df['content']])
X.head()


# In[ ]:


# regular expression, using stemming: try to replace tail of words like ies to y 
import re

df.content = df.content.str.replace("ing( |$)", " ")
df.content = df.content.str.replace("[^a-zA-Z]", " ")
df.content = df.content.str.replace("ies( |$)", "y ")


# **Convert Sentences into List of words**

# In[ ]:


def sent_to_words(content):
    return [np.array([x.split() for x in poem.split()]) for poem in content]


# In[ ]:


poem = sent_to_words(content)


# **Convert Char to Number Mapping**

# In[ ]:


def build_dict(poem):
    dictionary = {}
    rev_dict = {}
    count = 0
    for content in poem:
        for i in content:
            if i[0] in dictionary:
                pass
            else:
                dictionary[i[0]] = count
                count += 1
    rev_dict = dict(zip(dictionary.values(), dictionary.keys()))
    return dictionary, rev_dict


# In[ ]:


dictionary, rev_dict = build_dict(poem)


# **Tensor Starts**

# In[ ]:


import tensorflow as tf
from tensorflow.contrib import rnn


# In[ ]:


vocab_size = len(dictionary)


# In[ ]:


# Parameters
learning_rate = 0.0001
training_iters = 1600
display_step = 200
n_input = 9


# In[ ]:


# number of units in RNN cell
n_hidden = 512


# In[ ]:


# tf Graph input
tf.device("/device:GPU:0")
x = tf.placeholder("float", [None, n_input, 1])
y = tf.placeholder("float", [None, vocab_size])


# In[ ]:


# RNN output node weights and biases
weights = {
    'out': tf.Variable(tf.random_normal([n_hidden, vocab_size]))
}
biases = {
    'out': tf.Variable(tf.random_normal([vocab_size]))
}


# In[ ]:


def RNN(x, weights, biases):

    # reshape to [1, n_input]
    x = tf.reshape(x, [-1, n_input])

    # Generate a n_input-element sequence of inputs
    # (eg. [had] [a] [general] -> [20] [6] [33])
    x = tf.split(x,n_input,1)

    # 2-layer LSTM, each layer has n_hidden units.
    # Average Accuracy= 95.20% at 50k iter
    rnn_cell = rnn.MultiRNNCell([rnn.BasicLSTMCell(n_hidden),rnn.BasicLSTMCell(n_hidden)])
    # generate prediction
    outputs, states = rnn.static_rnn(rnn_cell, x, dtype=tf.float32)
    # there are n_input outputs but
    # we only want the last output
    return tf.matmul(outputs[-1], weights['out']) + biases['out']


# In[ ]:


pred = RNN(x, weights, biases)


# In[ ]:


# Loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=pred, labels=y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)


# In[ ]:


# Model evaluation
correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))


# In[ ]:


saver = tf.train.Saver()
init = tf.global_variables_initializer()


# In[ ]:


df_train = sent_to_words(content)


# In[ ]:


j = 0
for i in df_train:
    if i.shape[0] <= n_input:
        df_train = np.delete(df_train, (j), axis = 0)
        j -= 1
    j += 1


# In[ ]:


with tf.Session() as session:
    session.run(init)
    step = 0
    end_offset = n_input + 1
    acc_total = 0
    loss_total = 0
    while step < training_iters:
        acc_total = 0
        loss_total = 0
        j = 0
        for training_data in df_train:
            m = training_data.shape[0]
            windows = m - n_input
            acc_win = 0
            for window in range(windows):
                batch_x = training_data[window : window + n_input]
                batch_y = training_data[window + n_input]
                symbols_in_keys = [dictionary[i[0]] for i in batch_x]
                symbols_in_keys = np.reshape(np.array(symbols_in_keys), [-1, n_input, 1])
        
                symbols_out_onehot = np.zeros([vocab_size], dtype=float)
                symbols_out_onehot[dictionary[batch_y[0]]] = 1.0
                symbols_out_onehot = np.reshape(symbols_out_onehot,[1,-1])

                _, acc, loss, onehot_pred = session.run([optimizer, accuracy, cost, pred], feed_dict={x: symbols_in_keys, y: symbols_out_onehot})
                loss_total += loss
                acc_win += acc
            acc_total += float(acc_win) / m
        acc_total /= len(df_train)
        if (step+1) % display_step == 0:
            print("Iter= " + str(step+1) + ", Average Loss= " +                   "{:.6f}".format(loss_total/display_step) + ", Average Accuracy= " +                   "{:.2f}%".format(100*acc_total))
        step += 1
    print("Optimization Finished!")
    save_path = saver.save(session, "../working/model.ckpt")
    print("Model saved in path: %s" % save_path)
    while True:
        prompt = "%s words: " % n_input
        sentence = 'When I Queen Mab within my fancy viewed, My'
        sentence = sentence.strip()
        words = sentence.split(' ')
        if len(words) != n_input:
            continue
        try:
            symbols_in_keys = [dictionary[str(words[i])] for i in range(len(words))]
            for i in range(64):
                keys = np.reshape(np.array(symbols_in_keys), [-1, n_input, 1])
                onehot_pred = session.run(pred, feed_dict={x: keys})
                onehot_pred_index = int(tf.argmax(onehot_pred, 1).eval())
                sentence = "%s %s" % (sentence,rev_dict[onehot_pred_index])
                symbols_in_keys = symbols_in_keys[1:]
                symbols_in_keys.append(onehot_pred_index)
            print(sentence)
            break
        except:
            print("Word not in dictionary")

