#!/usr/bin/env python
# coding: utf-8

# ## Implementing a neural net for tabular data of breast cancer features with binary classification - Weekend Project

# In[ ]:


import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.python.data import Dataset
from sklearn.model_selection import train_test_split


# ## Step 1: Initial logisitics and loading the csv
# 
# The data is from [UCI dataset](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+%28Diagnostic%29), but with a modification that the target value __diagnosis__ is a numeric (__diagnosis_numeric__) instead of categorical text in the original data

# In[ ]:


# The data needs to be split into a training set and a test set
# To use 80/20, set the training size to .8
training_set_size_portion = .8

# Keep track of the accuracy score
accuracy_score = 0
# The DNN has hidden units, set the spec for them here, you can change these to see if accuracy increases
# But simpler networks are easy to train and converge, so try making units in each layer smaller, there will be
# very little trade-off in accuracy
hidden_units_spec = [10,20,10]
n_classes_spec = 2
steps_spec = 2000
epochs_spec = 15

file_name = "../input/wdbc.csv"
# Define the temp directory for keeping the model and checkpoints
tmp_dir_spec = "tmp/model"

# Taking only 2 features as of now, can see if any feature cross works after analysing data
features = ['radius','texture']

# Here's the label that we want to predict -- it's also a column in the CSV
labels = ['diagnosis_numeric']

data = pd.read_csv(file_name, low_memory=False, delimiter=',')


# ## Step 2: Exploring feature data
# 
# ### Looking at distribution of feature space and see if any have anomalies and outliers (for example max value being too big compared to 75th percentile value)
# TODO: Add correlation matrix, scatterplot of features we are picking, try with other features too

# In[ ]:


data.describe()


# ### Let us shuffle the data before kicking off test-train split of data, we will just use sklearn *train_test_split* for it

# In[ ]:


randomized_data = data.reindex(np.random.permutation(data.index))
training_data, test_data = train_test_split(randomized_data, test_size=0.2, random_state=42)


# ### Make sure that distribution of test and train data are identical, this should be case since we have shuffled it, but never the less, lets be wary!

# In[ ]:


training_data.describe()


# In[ ]:


test_data.describe()


# In[ ]:


training_features = training_data[features].copy()
training_labels = training_data[labels].copy()

test_features = test_data[features].copy()
test_labels = test_data[labels].copy()


# In[ ]:


feature_columns = [tf.feature_column.numeric_column(key) for key in features]


# In[ ]:


classifier = tf.estimator.DNNClassifier(
    feature_columns=feature_columns, 
    hidden_units=hidden_units_spec, 
    n_classes=n_classes_spec, 
    model_dir=tmp_dir_spec)


# In[ ]:


def my_input_fn(features, targets, batch_size=1, shuffle=True, num_epochs=None):
    # Convert pandas data into a dict of np arrays.
    features = {key:np.array(value) for key, value in dict(features).items()}                                           
    
    # Construct a dataset, and configure batching/repeating.
    ds = Dataset.from_tensor_slices((features,targets)) # warning: 2GB limit
    ds = ds.batch(batch_size).repeat(num_epochs)
    
    # Shuffle the data, if specified.
    if shuffle:
      ds = ds.shuffle(buffer_size=10000)
    
    # Return the next batch of data.
    features, labels = ds.make_one_shot_iterator().get_next()
    return features, labels


# In[ ]:


# Train the model using the classifer.
classifier.train(input_fn=lambda: my_input_fn(training_features, training_labels, batch_size=10), steps=steps_spec)


# In[ ]:


accuracy_score = classifier.evaluate(input_fn=lambda: my_input_fn(test_features, test_labels, num_epochs=1, shuffle=False))["accuracy"]
print("Accuracy = {}".format(accuracy_score))


# In[ ]:


prediction_set = pd.DataFrame({'radius':[14, 13], 'texture':[25, 26]})


# In[ ]:


predict_input_fn = tf.estimator.inputs.pandas_input_fn(x=prediction_set, num_epochs=1, shuffle=False)


# In[ ]:


predictions = list(classifier.predict(input_fn=predict_input_fn))


# In[ ]:


predicted_classes = [p["classes"] for p in predictions] 
results=np.concatenate(predicted_classes) 
print(results)

