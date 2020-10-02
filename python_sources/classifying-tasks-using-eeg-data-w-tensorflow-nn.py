#!/usr/bin/env python
# coding: utf-8

# In this notebook, we'll try to use Tensorflow to classify the state of the subject according to raw EEG data. I use Nick Merril's Kernel to help guide my data cleaning. We try two tasks, here
# 
#  1. Classify task label by EEG power for 1 subject, only.
#  2. Classify task label by EEG power for all subjects. This is harder, as it tries to use EEG Power data (which is unique to each person) to create a general classification rule for everyone.
# 
# https://www.kaggle.com/elsehow/d/berkeley-biosense/synchronized-brainwave-dataset/classifying-relaxation-versus-doing-math
# 
#  1. List item

# ## Step 1: Classify tasks for just one subject. ##

# In[ ]:


import json
import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn.cross_validation import train_test_split

df = pd.read_csv("../input/eeg-data.csv")
# convert to arrays from strings
df['eeg_power'] = df.eeg_power.map(json.loads)


# In[ ]:


df.head()


# In[ ]:


df = df.drop('Unnamed: 0', 1)
df = df.drop('indra_time', 1)
df = df.drop('browser_latency', 1)
df = df.drop('reading_time', 1)
df = df.drop('attention_esense', 1)
df = df.drop('meditation_esense', 1)
df = df.drop('raw_values', 1)
df = df.drop('signal_quality', 1)
df = df.drop('createdAt', 1)
df = df.drop('updatedAt', 1)

print(df.columns.values)


# In[ ]:


df.head()


# In[ ]:


# separate eeg power to multiple columns
to_series = pd.Series(df['eeg_power']) # df to series
eeg_features=pd.DataFrame(to_series.tolist()) #series to list and then back to df
df = pd.concat([df,eeg_features], axis=1) # concatenate the create columns


# In[ ]:


df


# In[ ]:


# just look at first subject
df=df.loc[df['id'] == 1]


# In[ ]:



df = df.drop('eeg_power', 1) # drop comma separated cell
df = df.drop('id', 1) # drop comma separated cell


# In[ ]:


# prepare for training
label=df.pop("label") # pop off labels to new group
print(df.shape)
print(df.head())
# convert to np array. df has our featuers
df=df.values



# convert labels to onehots 
train_labels = pd.get_dummies(label)
# make np array
train_labels = train_labels.values
print(train_labels.shape)

x_train,x_test,y_train,y_test = train_test_split(df,train_labels,test_size=0.2)
# so now we have predictors and y values, separated into test and train

x_train,x_test,y_train,y_test = np.array(x_train,dtype='float32'), np.array(x_test,dtype='float32'),np.array(y_train,dtype='float32'),np.array(y_test,dtype='float32')


# In[ ]:


x_train.shape


# In[ ]:


y_train.shape


# In[ ]:


# place holder for inputs. feed in later
x = tf.placeholder(tf.float32, [None, 8])
# # # take 20 features  to 10 nodes in hidden layer
w1 = tf.Variable(tf.random_normal([8, 1000],stddev=.5,name='w1'))
# # # add biases for each node
b1 = tf.Variable(tf.zeros([1000]))
# # calculate activations 
hidden_output = tf.nn.softmax(tf.matmul(x, w1) + b1)
w2 = tf.Variable(tf.random_normal([1000, 65],stddev=.5,name='w2'))
b2 = tf.Variable(tf.zeros([65]))

# # placeholder for correct values 
y_ = tf.placeholder("float", [None,65])
# # #implement model. these are predicted ys
y = tf.nn.softmax(tf.matmul(hidden_output, w2) + b2)


# In[ ]:


loss = tf.reduce_mean(tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(y, y_, name='xentropy')))
opt = tf.train.AdamOptimizer(learning_rate=.002)
train_step = opt.minimize(loss, var_list=[w1,b1,w2,b2])


# In[ ]:


def get_mini_batch(x,y):
	rows=np.random.choice(x.shape[0], 50)
	return x[rows], y[rows]


# In[ ]:


# start session
sess = tf.Session()
# init all vars
init = tf.initialize_all_variables()
sess.run(init)


# In[ ]:


ntrials = 10000
for i in range(ntrials):
    # get mini batch
    a,b=get_mini_batch(x_train,y_train)
    # run train step, feeding arrays of 100 rows each time
    _, cost =sess.run([train_step,loss], feed_dict={x: a, y_: b})
    if i%500 ==0:
    	print("epoch is {0} and cost is {1}".format(i,cost))

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

print("test accuracy is {}".format(sess.run(accuracy, feed_dict={x: x_test, y_: y_test})))


# In[ ]:


sess.close


# ## Step 2: Classify tasks for all subjects. ##

# In[ ]:


import json
import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn.cross_validation import train_test_split

df = pd.read_csv("../input/eeg-data.csv")
# convert to arrays from strings
df['eeg_power'] = df.eeg_power.map(json.loads)


# In[ ]:


df[["eeg_power", "signal_quality"]]


# Now we clean the dataset, and drop most of the columns that we won't use in this analysis. 

# In[ ]:


df = df.drop('Unnamed: 0', 1)
df = df.drop('id', 1)
df = df.drop('indra_time', 1)
df = df.drop('browser_latency', 1)
df = df.drop('reading_time', 1)
df = df.drop('attention_esense', 1)
df = df.drop('meditation_esense', 1)
df = df.drop('raw_values', 1)
df = df.drop('signal_quality', 1)
df = df.drop('createdAt', 1)
df = df.drop('updatedAt', 1)

print(df.columns.values)


# eeg_power contains data on  8 commonly-recognized types of EEG frequency bands...these are comma separated, but we need to create new columns for each band (delta (0.5 - 2.75Hz), theta (3.5 - 6.75Hz), low-alpha (7.5 - 9.25Hz), high-alpha (10 - 11.75Hz), low-beta (13 - 16.75Hz), high-beta (18 - 29.75Hz), low-gamma (31 - 39.75Hz), and mid-gamma (41 - 49.75Hz)).

# In[ ]:


to_series = pd.Series(df['eeg_power']) # df to series
eeg_cols=pd.DataFrame(to_series.tolist()) #series to list and then back to df
print(eeg_cols.head())


# This works. We have the 8 variables split into 8 distinct columns. Nice. 

# In[ ]:


df = pd.concat([df,eeg_cols], axis=1, join='outer') # concatenate the create columns
df = df.drop('eeg_power', 1) # drop comma separated cell
print(df.head())


# We have a dataframe that we can now split into test and train sets and do train a NN on. 

# In[ ]:


# prepare for training
label=df.pop("label") # pop off labels to new group
print("the df of features now as shape{0} and the label set has shape {1}".format(df.shape,label.shape))


# We convert these two sets to np arrays to TF training.

# In[ ]:


# convert to np array. df has our featuers
df=df.values


# In[ ]:


# convert labels to onehots 
train_labels = pd.get_dummies(label)
print(train_labels.shape)


# There are 69 different tasks classified by the researchers. There is redundancy here (blink 1 is distinct from blink 2...this will complicate our ability to correctly classify the various task labels, but let's just stick with it for now.)

# In[ ]:


# convert train_labels to np array, too
train_labels = train_labels.values


# In[ ]:


# use sklearn to split for training
x_train,x_test,y_train,y_test = train_test_split(df,train_labels,test_size=0.2)
x_train,x_test,y_train,y_test = np.array(x_train,dtype='float32'), np.array(x_test,dtype='float32'),np.array(y_train,dtype='float32'),np.array(y_test,dtype='float32')


# Now, let's do some tensorflow and build a simple model with 1 hidden layer with 1000 nodes in this layer. 

# In[ ]:


x = tf.placeholder(tf.float32, [None, 8])
w1 = tf.Variable(tf.random_normal([8, 1000],stddev=.5,name='w1'))
b1 = tf.Variable(tf.zeros([1000]))
# # calculate hidden output
hidden_output = tf.nn.softmax(tf.matmul(x, w1) + b1)
# bring from 1000 nodes to one of 69 possible labels
w2 = tf.Variable(tf.random_normal([1000, 68],stddev=.5,name='w2'))
b2 = tf.Variable(tf.zeros([68]))
# # placeholder for correct values 
y_ = tf.placeholder("float", [None,68])
# # #implement model. these are predicted ys
y = tf.nn.softmax(tf.matmul(hidden_output, w2) + b2)


# Prepare the training. Use ADAM optimizer to adjust learning rate over time.

# In[ ]:


loss = tf.reduce_mean(tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(y, y_, name='xentropy')))
opt = tf.train.AdamOptimizer(learning_rate=.005)
train_step = opt.minimize(loss, var_list=[w1,b1,w2,b2])


# Create a function to get mini_batch, so that we aren't feeding data in every training epoch.

# In[ ]:


def get_mini_batch(x,y):
	rows=np.random.choice(x.shape[0], 100)
	return x[rows], y[rows]


# In[ ]:


sess = tf.Session()
# init all vars in graph
init = tf.initialize_all_variables()
sess.run(init)


# Train!

# In[ ]:


ntrials = 10000
for i in range(ntrials):
    # get mini batch
    a,b=get_mini_batch(x_train,y_train)
    # run train step, feeding arrays of 100 rows each time
    _, cost =sess.run([train_step,loss], feed_dict={x: a, y_: b})
    if i%500 ==0:
    	print("epoch is {0} and cost is {1}".format(i,cost))

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

print("test accuracy is {}".format(sess.run(accuracy, feed_dict={x: x_test, y_: y_test})))


# In[ ]:


sess.close


# Given that we are trying to predict one of 69 possible labels, and that there are redundant labels, this accuracy is decent. Random guessing would get this right 1/69 = 1.5%.
# 
# Upon further consideration, we see that most of the data is unlabeled. For instance, for subject 1, there are 943 rows...of these 943, the label "everyone paired"  appears 361 times and "unlabeled" appears 189 times. So if we can just get these two right, we get 58% accuracy. So this is actually not nearly as good as we would think -- the non-uniformity of the distribution makes this classification problem easier. 

# ## Step 3: Consolidate labels and run for individual subject. Compare only MATH and RELAX, similar to Nick's kernel.##

# In[ ]:


import pandas as pd 
import json
from sklearn.cross_validation import train_test_split
import tensorflow as tf
import numpy as np
import random

def prepare_individual_data(df,individual):
	# drop unused features. just leave eeg_power and the label
	df = df.drop('Unnamed: 0', 1)
	# df = df.drop('id', 1)
	df = df.drop('indra_time', 1)
	df = df.drop('browser_latency', 1)
	df = df.drop('reading_time', 1)
	df = df.drop('attention_esense', 1)
	df = df.drop('meditation_esense', 1)
	df = df.drop('raw_values', 1)
	df = df.drop('signal_quality', 1)
	df = df.drop('createdAt', 1)
	df = df.drop('updatedAt', 1)
	# separate eeg power to multiple columns
	to_series = pd.Series(df['eeg_power']) # df to series
	eeg_features=pd.DataFrame(to_series.tolist()) #series to list and then back to df
	df = pd.concat([df,eeg_features], axis=1) # concatenate the create columns
	# df = pd.concat([df,eeg_features], axis=1, join='outer') # concatenate the create columns
	# just look at first subject
	df=df.loc[df['id'] == individual]
	df = df.drop('eeg_power', 1) # drop comma separated cell
	# df = df.drop('id', 1) # drop comma separated cell
	return df

df = pd.read_csv("../input/eeg-data.csv")

relax = df[df.label == 'relax']
# df['label'] = df["label"].astype('category')
df['label'].value_counts()
df['eeg_power'] = df.eeg_power.map(json.loads)

individual_data=prepare_individual_data(df,1)

def clean_labels(dd):
	# clean labels
	dd.loc[dd.label == 'math1', 'label'] = "math"
	dd.loc[dd.label == 'math2', 'label'] = "math"
	dd.loc[dd.label == 'math3', 'label'] = "math"
	dd.loc[dd.label == 'math4', 'label'] = "math"
	dd.loc[dd.label == 'math5', 'label'] = "math"
	dd.loc[dd.label == 'math6', 'label'] = "math"
	dd.loc[dd.label == 'math7', 'label'] = "math"
	dd.loc[dd.label == 'math8', 'label'] = "math"
	dd.loc[dd.label == 'math9', 'label'] = "math"
	dd.loc[dd.label == 'math10', 'label'] = "math"
	dd.loc[dd.label == 'math11', 'label'] = "math"
	dd.loc[dd.label == 'math12', 'label'] = "math"
	dd.loc[dd.label == 'colorRound1-1', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound1-2', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound1-3', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound1-4', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound1-5', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound1-6', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound2-1', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound2-2', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound2-3', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound2-4', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound2-5', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound2-6', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound3-1', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound3-2', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound3-3', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound3-4', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound3-5', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound3-6', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound4-1', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound4-2', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound4-3', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound4-4', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound4-5', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound4-6', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound5-1', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound5-2', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound5-3', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound5-4', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound5-5', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound5-6', 'label'] = "colors"
	dd.loc[dd.label == 'readyRound1', 'label'] = "ready"
	dd.loc[dd.label == 'readyRound2', 'label'] = "ready"
	dd.loc[dd.label == 'readyRound3', 'label'] = "ready"
	dd.loc[dd.label == 'readyRound4', 'label'] = "ready"
	dd.loc[dd.label == 'readyRound5', 'label'] = "ready"
	dd.loc[dd.label == 'blink1', 'label'] = "blink"
	dd.loc[dd.label == 'blink2', 'label'] = "blink"
	dd.loc[dd.label == 'blink3', 'label'] = "blink"
	dd.loc[dd.label == 'blink4', 'label'] = "blink"
	dd.loc[dd.label == 'blink5', 'label'] = "blink"
	dd.loc[dd.label == 'thinkOfItemsInstruction-ver1', 'label'] = "instruction"
	dd.loc[dd.label == 'colorInstruction2', 'label'] = "instruction"
	dd.loc[dd.label == 'colorInstruction1', 'label'] = "instruction"
	dd.loc[dd.label == 'colorInstruction2', 'label'] = "instruction"
	dd.loc[dd.label == 'musicInstruction', 'label'] = "instruction"
	dd.loc[dd.label == 'videoInstruction', 'label'] = "instruction"
	dd.loc[dd.label == 'mathInstruction', 'label'] = "instruction"
	dd.loc[dd.label == 'relaxInstruction', 'label'] = "instruction"
	dd.loc[dd.label == 'blinkInstruction', 'label'] = "instruction"
	return dd

cleaned_individual_data = clean_labels(individual_data)

def drop_useless_labels(df):
	# drop unlabeled and everyone paired and others. leave only relax and math. 
	df = df[df.label != 'unlabeled']
	df = df[df.label != 'everyone paired']
	df = df[df.label != 'instruction']
	df = df[df.label != 'blink']
	df = df[df.label != 'ready']
	df = df[df.label != 'colors']
	df = df[df.label != 'thinkOfItems-ver1']
	df = df[df.label != 'music']
	df = df[df.label != 'video-ver1']
	return df

final_individual_full_data= drop_useless_labels(cleaned_individual_data)

print(final_individual_full_data['label'].value_counts())

print(final_individual_full_data.head())

for i in range(9):
	copy = final_individual_full_data
	copy[0]=copy[0]+random.gauss(1,.1) # add noice to mean freq var
	final_individual_full_data=final_individual_full_data.append(copy,ignore_index=True) # make voice df 2x as big
	print("shape of df after {0}th intertion of this loop is {1}".format(i,final_individual_full_data.shape))


def get_traintest_data(individualdata):
	label=individualdata.pop("label") # pop off labels to new group
	train_labels = pd.get_dummies(label)
	train_labels = train_labels.values
	df=individualdata.values
	x_train,x_test,y_train,y_test = train_test_split(df,train_labels,test_size=0.2)
	#so now we have predictors and y values, separated into test and train
	x_train,x_test,y_train,y_test = np.array(x_train,dtype='float32'), np.array(x_test,dtype='float32'),np.array(y_train,dtype='float32'),np.array(y_test,dtype='float32')
	return x_train, x_test, y_train, y_test


x_train, x_test, y_train, y_test = get_traintest_data(final_individual_full_data)






def get_mini_batch(x,y):
	rows=np.random.choice(x.shape[0], 100)
	return x[rows], y[rows]


def trainNN(x_train, y_train,x_test,y_test,number_trials):
	# there are 8 features
	# place holder for inputs. feed in later
	x = tf.placeholder(tf.float32, [None, x_train.shape[1]])
	# # # take 20 features  to 10 nodes in hidden layer
	w1 = tf.Variable(tf.random_normal([x_train.shape[1], 1000],stddev=.5,name='w1'))
	# # # add biases for each node
	b1 = tf.Variable(tf.zeros([1000]))
	# # calculate activations 
	hidden_output = tf.nn.softmax(tf.matmul(x, w1) + b1)
	w2 = tf.Variable(tf.random_normal([1000, y_train.shape[1]],stddev=.5,name='w2'))
	b2 = tf.Variable(tf.zeros([y_train.shape[1]]))
	# # placeholder for correct values 
	y_ = tf.placeholder("float", [None,y_train.shape[1]])
	# # #implement model. these are predicted ys
	y = tf.nn.softmax(tf.matmul(hidden_output, w2) + b2)
	# loss and optimization 
	loss = tf.reduce_mean(tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(y, y_, name='xentropy')))
	opt = tf.train.AdamOptimizer(learning_rate=.0005)
	train_step = opt.minimize(loss, var_list=[w1,b1,w2,b2])
	# start session
	sess = tf.Session()
	# init all vars
	init = tf.initialize_all_variables()
	sess.run(init)
	ntrials = number_trials
	for i in range(ntrials):
	    # get mini batch
	    a,b=get_mini_batch(x_train,y_train)
	    # run train step, feeding arrays of 100 rows each time
	    _, cost =sess.run([train_step,loss], feed_dict={x: a, y_: b})
	    if i%500 ==0:
	    	print("epoch is {0} and cost is {1}".format(i,cost))
	correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
	accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
	print("test accuracy is {}".format(sess.run(accuracy, feed_dict={x: x_test, y_: y_test})))
	ans = sess.run(y, feed_dict={x: x_test})
	print(y_test[0:3])
	print("Correct prediction\n",ans[0:3])

trainNN(x_train,y_train,x_test,y_test,10000)


# In[ ]:


sess.close()


# This works about as well as Nick Merril's classification (a bit better).

# ## Step 4: Consolidate labels and run for individual subject. Try to classify more than 2 activities. ##

# Let's try to classify an individual subject's mode of thinking, with more possible categories. This is harder.  

# In[ ]:


import pandas as pd 
import json
from sklearn.cross_validation import train_test_split
import tensorflow as tf
import numpy as np
import random


def prepare_individual_data(df,individual):
	# drop unused features. just leave eeg_power and the label
	df = df.drop('Unnamed: 0', 1)
	# df = df.drop('id', 1)
	df = df.drop('indra_time', 1)
	df = df.drop('browser_latency', 1)
	df = df.drop('reading_time', 1)
	df = df.drop('attention_esense', 1)
	df = df.drop('meditation_esense', 1)
	df = df.drop('raw_values', 1)
	df = df.drop('signal_quality', 1)
	df = df.drop('createdAt', 1)
	df = df.drop('updatedAt', 1)
	# separate eeg power to multiple columns
	to_series = pd.Series(df['eeg_power']) # df to series
	eeg_features=pd.DataFrame(to_series.tolist()) #series to list and then back to df
	df = pd.concat([df,eeg_features], axis=1) # concatenate the create columns
	# df = pd.concat([df,eeg_features], axis=1, join='outer') # concatenate the create columns
	# just look at first subject
	df=df.loc[df['id'] == individual]
	df = df.drop('eeg_power', 1) # drop comma separated cell
	# df = df.drop('id', 1) # drop comma separated cell
	return df

df = pd.read_csv("../input/eeg-data.csv")

relax = df[df.label == 'relax']
# df['label'] = df["label"].astype('category')
df['label'].value_counts()
df['eeg_power'] = df.eeg_power.map(json.loads)

individual_data=prepare_individual_data(df,1)

def clean_labels(dd):
	# clean labels
	dd.loc[dd.label == 'math1', 'label'] = "math"
	dd.loc[dd.label == 'math2', 'label'] = "math"
	dd.loc[dd.label == 'math3', 'label'] = "math"
	dd.loc[dd.label == 'math4', 'label'] = "math"
	dd.loc[dd.label == 'math5', 'label'] = "math"
	dd.loc[dd.label == 'math6', 'label'] = "math"
	dd.loc[dd.label == 'math7', 'label'] = "math"
	dd.loc[dd.label == 'math8', 'label'] = "math"
	dd.loc[dd.label == 'math9', 'label'] = "math"
	dd.loc[dd.label == 'math10', 'label'] = "math"
	dd.loc[dd.label == 'math11', 'label'] = "math"
	dd.loc[dd.label == 'math12', 'label'] = "math"

	dd.loc[dd.label == 'colorRound1-1', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound1-2', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound1-3', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound1-4', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound1-5', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound1-6', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound2-1', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound2-2', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound2-3', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound2-4', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound2-5', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound2-6', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound3-1', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound3-2', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound3-3', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound3-4', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound3-5', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound3-6', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound4-1', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound4-2', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound4-3', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound4-4', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound4-5', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound4-6', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound5-1', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound5-2', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound5-3', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound5-4', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound5-5', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound5-6', 'label'] = "colors"

	dd.loc[dd.label == 'readyRound1', 'label'] = "ready"
	dd.loc[dd.label == 'readyRound2', 'label'] = "ready"
	dd.loc[dd.label == 'readyRound3', 'label'] = "ready"
	dd.loc[dd.label == 'readyRound4', 'label'] = "ready"
	dd.loc[dd.label == 'readyRound5', 'label'] = "ready"

	dd.loc[dd.label == 'blink1', 'label'] = "blink"
	dd.loc[dd.label == 'blink2', 'label'] = "blink"
	dd.loc[dd.label == 'blink3', 'label'] = "blink"
	dd.loc[dd.label == 'blink4', 'label'] = "blink"
	dd.loc[dd.label == 'blink5', 'label'] = "blink"

	dd.loc[dd.label == 'thinkOfItemsInstruction-ver1', 'label'] = "instruction"
	dd.loc[dd.label == 'colorInstruction2', 'label'] = "instruction"
	dd.loc[dd.label == 'colorInstruction1', 'label'] = "instruction"
	dd.loc[dd.label == 'colorInstruction2', 'label'] = "instruction"
	dd.loc[dd.label == 'musicInstruction', 'label'] = "instruction"
	dd.loc[dd.label == 'videoInstruction', 'label'] = "instruction"
	dd.loc[dd.label == 'mathInstruction', 'label'] = "instruction"
	dd.loc[dd.label == 'relaxInstruction', 'label'] = "instruction"
	dd.loc[dd.label == 'blinkInstruction', 'label'] = "instruction"

	return dd

cleaned_individual_data = clean_labels(individual_data)

def drop_useless_labels(df):
	# drop unlabeled and everyone paired.
	df = df[df.label != 'unlabeled']
	df = df[df.label != 'everyone paired']
	return df

final_individual_full_data= drop_useless_labels(cleaned_individual_data)

print(final_individual_full_data['label'].value_counts())

for i in range(9):
	copy = final_individual_full_data
	copy[0]=copy[0]+random.gauss(1,.1) # add noice to mean freq var
	final_individual_full_data=final_individual_full_data.append(copy,ignore_index=True) # make voice df 2x as big
	print("shape of df after {0}th intertion of this loop is {1}".format(i,final_individual_full_data.shape))


def get_traintest_data(individualdata):
	label=individualdata.pop("label") # pop off labels to new group
	train_labels = pd.get_dummies(label)
	train_labels = train_labels.values
	df=individualdata.values
	x_train,x_test,y_train,y_test = train_test_split(df,train_labels,test_size=0.2)
	#so now we have predictors and y values, separated into test and train
	x_train,x_test,y_train,y_test = np.array(x_train,dtype='float32'), np.array(x_test,dtype='float32'),np.array(y_train,dtype='float32'),np.array(y_test,dtype='float32')
	return x_train, x_test, y_train, y_test


x_train, x_test, y_train, y_test = get_traintest_data(final_individual_full_data)


def get_mini_batch(x,y):
	rows=np.random.choice(x.shape[0], 50)
	return x[rows], y[rows]


def trainNN(x_train, y_train,x_test,y_test,number_trials):
	# there are 8 features
	# place holder for inputs. feed in later
	x = tf.placeholder(tf.float32, [None, x_train.shape[1]])
	# # # take 20 features  to 10 nodes in hidden layer
	w1 = tf.Variable(tf.random_normal([x_train.shape[1], 1000],stddev=.5,name='w1'))
	# # # add biases for each node
	b1 = tf.Variable(tf.zeros([1000]))
	# # calculate activations 
	hidden_output = tf.nn.softmax(tf.matmul(x, w1) + b1)
	w2 = tf.Variable(tf.random_normal([1000, y_train.shape[1]],stddev=.5,name='w2'))
	b2 = tf.Variable(tf.zeros([y_train.shape[1]]))
	# # placeholder for correct values 
	y_ = tf.placeholder("float", [None,y_train.shape[1]])
	# # #implement model. these are predicted ys
	y = tf.nn.softmax(tf.matmul(hidden_output, w2) + b2)
	# loss and optimization 
	loss = tf.reduce_mean(tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(y, y_, name='xentropy')))
	opt = tf.train.AdamOptimizer(learning_rate=.002)
	train_step = opt.minimize(loss, var_list=[w1,b1,w2,b2])
	# start session
	sess = tf.Session()
	# init all vars
	init = tf.initialize_all_variables()
	sess.run(init)
	ntrials = number_trials
	for i in range(ntrials):
	    # get mini batch
	    a,b=get_mini_batch(x_train,y_train)
	    # run train step, feeding arrays of 100 rows each time
	    _, cost =sess.run([train_step,loss], feed_dict={x: a, y_: b})
	    if i%500 ==0:
	    	print("epoch is {0} and cost is {1}".format(i,cost))
	correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
	accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
	print("test accuracy is {}".format(sess.run(accuracy, feed_dict={x: x_test, y_: y_test})))



trainNN(x_train,y_train,x_test,y_test,10000)


# In[ ]:


sess.close()


# The results from this are less satisfactory. Even when I created more fake data, the results didn't improve much. Hmmmm.
