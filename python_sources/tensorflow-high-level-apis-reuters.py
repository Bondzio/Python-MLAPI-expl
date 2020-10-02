#!/usr/bin/env python
# coding: utf-8

# # Classifying newswires with tf.keras, tf.data and eager execution
# We will be exploring a multiclass text classification problem

# In[ ]:


import json
import numpy as np
import tensorflow as tf

# enable eager execution
tf.enable_eager_execution()


# ## Download and explore the dataset
# The dataset consists of a set of short newswires and their corresponding topics as published by Reuters in 1986. There are around 46 different topics. The set is divided into 8982 training examples and 2246 test examples. Each training example is a list of words represented as integers similar to IMDB datset and the labels are integers up to 46.

# In[ ]:


def load_data(path, num_words=None, skip_top=0, seed=113, test_split=0.2):
    with np.load(path) as f:
        xs, labels = f['x'], f['y']

    np.random.seed(seed)
    indices = np.arange(len(xs))
    np.random.shuffle(indices)
    xs = xs[indices]
    labels = labels[indices]
    
    if not num_words:
        num_words = max([max(x) for x in xs])

    xs = [[w for w in x if skip_top <= w < num_words] for x in xs]
    
    idx = int(len(xs) * (1 - test_split))
    x_train, y_train = np.array(xs[:idx]), np.array(labels[:idx])
    x_test, y_test = np.array(xs[idx:]), np.array(labels[idx:])
    
    return (x_train, y_train), (x_test, y_test)

def get_word_index(path):
    with open(path) as f:
        return json.load(f)


# In[ ]:


(train_data, train_labels), (test_data, test_labels) = load_data('../input/reuters.npz', num_words=10000)


# In[ ]:


print('Training data', train_data[0])
print('Training labels', train_labels[0])
print('Length of training data', len(train_data))
print('Length of test data', len(test_data))


# ## Prepare the data
# We can get the dictionary from `get_word_index` which hashes the words to their corresponding integers. Let's try and convert a newswire from integers back into it's original text by first reversing this dictionary and then iterating over a newswire and converting the integers to string.

# In[ ]:


# dictionary that hashes words to their integer
word_to_integer = get_word_index('../input/reuters_word_index.npz')


# In[ ]:


print(list(word_to_integer.keys())[0:10])

integer_to_word = dict([(value, key) for (key, value) in word_to_integer.items()])

# demostrate how to find the word from an integer
print(integer_to_word[1])
print(integer_to_word[2])

import random
random_index = random.randint(0, 100)

# we need to subtract 3 from the indices because 0 is 'padding', 1 is 'start of sequence', and 2 is 'unknown'
decoded_newswire = ' '.join([integer_to_word.get(i - 3, 'UNK') for i in train_data[random_index]])
print(decoded_newswire)
print(train_labels[random_index])


# ### Format the data
# As before, we are going to multi-hot encode our newswire which is an array of integers into a 10,000 dimensional vector. We will place 1's in the indices of word-integers that occur in the newswire, and 0's for everything else.

# In[ ]:


def vectorize_sequences(sequences, dimension=10000):
    # create an all-zero matrix of shape (len(sequences), dimension)
    results = np.zeros((len(sequences), dimension), dtype=np.float32)
    for i, sequence in enumerate(sequences):
#         print(i, sequence)
        results[i, sequence] = 1. # set specific indices of results[i] to 1s
    return results

train_data = vectorize_sequences(train_data)
test_data = vectorize_sequences(test_data)

print(train_data.shape)
print(train_data[0])


# ### Format the labels
# We will also use `tf.keras.utils.to_categorical` to one hot encode our labels

# In[ ]:


LABEL_DIMENSIONS = 46

print(train_labels[0]) # before
train_labels = tf.keras.utils.to_categorical(train_labels, LABEL_DIMENSIONS)
print(train_labels[0]) # after

test_labels = tf.keras.utils.to_categorical(test_labels, LABEL_DIMENSIONS)

# Needed later
train_labels = train_labels.astype(np.float32)
test_labels = test_labels.astype(np.float32)


# ## Create the model
# Similar to IMDB model and modified to work for a multiclass classification problem

# In[ ]:


# create model
model = tf.keras.Sequential()

model.add(tf.keras.layers.Dense(64, activation=tf.nn.relu, input_shape=(10000, )))
model.add(tf.keras.layers.Dense(64, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(LABEL_DIMENSIONS, activation=tf.nn.softmax))

optimizer = tf.train.RMSPropOptimizer(learning_rate=0.001)

model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

model.summary()


# ### Validation set
# As always, we want to test our model on data it hasn't seen before, but before we get our final test accuracy, we'll create a validation set.

# In[ ]:


VAL_SIZE = 1000

val_data = train_data[:VAL_SIZE]
partial_train_data = train_data[VAL_SIZE:]

val_labels = train_labels[:VAL_SIZE]
partial_train_labels = train_labels[VAL_SIZE:]


# In[ ]:


# create a tf.data Dataset and train the model
BATCH_SIZE = 512
TRAINING_SIZE = partial_train_labels.shape[0]

training_set = tf.data.Dataset.from_tensor_slices((partial_train_data, partial_train_labels))
training_set = training_set.shuffle(TRAINING_SIZE).batch(BATCH_SIZE)


# In[ ]:


EPOCHS = 20

# stores list of metric values for plotting later
training_loss_list = []
training_accuracy_list = []
validation_loss_list = []
validation_accuracy_list = []

for epoch in range(EPOCHS):
    for newswires, labels in training_set:
        # calculating training loss and accuracy
        training_loss, training_accuracy = model.train_on_batch(newswires, labels)
        
    # calculate validation loss and accuracy
    validation_loss, validation_accuracy = model.evaluate(val_data, val_labels)
    
    # add to the lists
    training_loss_list.append(training_loss)
    training_accuracy_list.append(training_accuracy)
    validation_loss_list.append(validation_loss)
    validation_accuracy_list.append(validation_accuracy)
    
    print(('Epoch #%d\t Training Loss: %.2f\t Training Accuracy: %.2f\t Validation Loss: %.2f\t Validation Accuracy: %.2f') % (epoch + 1, training_loss, training_accuracy, validation_loss, validation_accuracy))


# In[ ]:


# plot loss and accuracy
import matplotlib.pyplot as plt

epochs = range(1, EPOCHS + 1)

plt.plot(epochs, training_loss_list, 'bo', label='Training loss')
plt.plot(epochs, validation_loss_list, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()


# In[ ]:


plt.clf() # clear plot

plt.plot(epochs, training_accuracy_list, 'bo', label='Training accuracy')
plt.plot(epochs, validation_accuracy_list, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.show()


# ## Testing the model
# Now that we have successfully trained the mode and our training accuracy has jumped over 90%, we can test it. The test accuracy is a better evaluation metric for how our model will peform in the real world

# In[ ]:


loss, accuracy = model.evaluate(test_data, test_labels)
print('Test accuracy: %.2f'% (accuracy))

