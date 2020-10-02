#!/usr/bin/env python
# coding: utf-8

# # Predict Breast Cancer

# Predict whether the cancer is benign or malignant

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import tensorflow as tf
import pandas as pd
from sklearn.utils import shuffle
import matplotlib.gridspec as gridspec
import seaborn as sns
import matplotlib.pyplot as plt


# Set the csv file name 

# In[ ]:


train_filename = "../input/data.csv"


# Set column keys

# In[ ]:


idKey = "id"
diagnosisKey = "diagnosis"
radiusMeanKey = "radius_mean"
textureMeanKey = "texture_mean"
perimeterMeanKey = "perimeter_mean"
areaMeanKey = "area_mean"
smoothnessMeanKey = "smoothness_mean"
compactnessMeanKey = "compactness_mean"
concavityMeanKey = "concavity_mean"
concavePointsMeanKey = "concave points_mean"
symmetryMeanKey = "symmetry_mean"
fractalDimensionMean = "fractal_dimension_mean"
radiusSeKey = "radius_se"
textureSeKey = "texture_se"
perimeterSeKey = "perimeter_se"
areaSeKey = "area_se"
smoothnessSeKey = "smoothness_se"
compactnessSeKey = "compactness_se"
concavitySeKey = "concavity_se"
concavePointsSeKey = "concave points_se"
symmetrySeKey = "symmetry_se"
fractalDimensionSeKey = "fractal_dimension_se"
radiusWorstKey = "radius_worst"
textureWorstKey = "texture_worst"
perimeterWorstKey = "perimeter_worst"
areaWorstKey = "area_worst"
smoothnessWorstKey = "smoothness_worst"
compactnessWorstKey = "compactness_worst"
concavityWorstKey = "concavity_worst"
concavePointsWorstKey = "concave points_worst"
symmetryWorstKey = "symmetry_worst"
fractalDimensionWorstKey = "fractal_dimension_worst"


# In[ ]:


train_columns = [idKey, diagnosisKey, radiusMeanKey, textureMeanKey, perimeterMeanKey, areaMeanKey, smoothnessMeanKey, compactnessMeanKey, concavityMeanKey, concavePointsMeanKey, symmetryMeanKey, fractalDimensionMean, radiusSeKey, textureSeKey, perimeterSeKey, areaSeKey, smoothnessSeKey, compactnessSeKey, concavitySeKey, concavePointsSeKey, symmetrySeKey, fractalDimensionSeKey, radiusWorstKey, textureWorstKey, perimeterWorstKey, areaWorstKey, smoothnessWorstKey, compactnessWorstKey, concavityWorstKey, concavePointsWorstKey, symmetryWorstKey, fractalDimensionWorstKey]


# In[ ]:


def get_train_data():
    df = pd.read_csv(train_filename, names= train_columns, delimiter=',', skiprows=1)
    return df


# In[ ]:


train_data = get_train_data()


# ### Exploring the data

# In[ ]:


train_data.head()


# In[ ]:


train_data.describe()


# In[ ]:


train_data.isnull().sum()


# No missing values, that makes things a little easier.
# Let's see how area_mean compares across malignant and benign diagnosis.

# In[ ]:


print ("Malignant")
print (train_data.area_mean[train_data.diagnosis == "M"].describe())
print ()
print ("Benign")
print (train_data.area_mean[train_data.diagnosis == "B"].describe())


# In[ ]:


f, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12,4))

bins = 50

ax1.hist(train_data.area_mean[train_data.diagnosis == "M"], bins = bins)
ax1.set_title('Malignant')

ax2.hist(train_data.area_mean[train_data.diagnosis == "B"], bins = bins)
ax2.set_title('Benign')

plt.xlabel('Area Mean')
plt.ylabel('Number of Diagnosis')
plt.show()


# The 'area_mean' feature looks different as it increases its value across both types of diagnosis. You could argue that malignant diagnosis are more are more uniformly distributed, while benign diagnosis have a normal distribution. This could make it easier to detect a malignant diagnosis when the area_mean is above the 750 value.
# Now let's see how the diagnosis area_worst differs between the two types.

# In[ ]:


print ("Malignant")
print (train_data.area_worst[train_data.diagnosis == "M"].describe())
print ()
print ("Benign")
print (train_data.area_worst[train_data.diagnosis == "B"].describe())


# In[ ]:





# In[ ]:


f, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12,4))

bins = 30

ax1.hist(train_data.area_worst[train_data.diagnosis == "M"], bins = bins)
ax1.set_title('Malignant')

ax2.hist(train_data.area_worst[train_data.diagnosis == "B"], bins = bins)
ax2.set_title('Benign')

plt.xlabel('Area Worst')
plt.ylabel('Number of Diagnosis')
plt.yscale('log')
plt.show()


# It looks pretty much the same as the last graph.
# Next, let's take a look at the rest of the features features.

# In[ ]:


#Select only the rest of the features.
r_data = train_data.drop([idKey, areaMeanKey, areaWorstKey, diagnosisKey], axis=1)
r_features = r_data.columns


# In[ ]:


plt.figure(figsize=(12,28*4))
gs = gridspec.GridSpec(28, 1)
for i, cn in enumerate(r_data[r_features]):
    ax = plt.subplot(gs[i])
    sns.distplot(train_data[cn][train_data.diagnosis == "M"], bins=50)
    sns.distplot(train_data[cn][train_data.diagnosis == "B"], bins=50)
    ax.set_xlabel('')
    ax.set_title('histogram of feature: ' + str(cn))
plt.show()


# Update the value of diagnosis. 1 for Malignant and 0 for Benign

# In[ ]:


train_data.loc[train_data.diagnosis == "M", 'diagnosis'] = 1
train_data.loc[train_data.diagnosis == "B", 'diagnosis'] = 0


# Create a new feature for benign (non-malignant) diagnosis.

# In[ ]:


train_data.loc[train_data.diagnosis == 0, 'benign'] = 1
train_data.loc[train_data.diagnosis == 1, 'benign'] = 0


# Convert benign column type to integer

# In[ ]:


train_data['benign'] = train_data.benign.astype(int)


# Rename 'Class' to 'Malignant'.

# In[ ]:


train_data = train_data.rename(columns={'diagnosis': 'malignant'})


# 212 malignant diagnosis, 357 benign diagnosis.
# 37.25% of diagnostics were malignant. 

# In[ ]:


print(train_data.benign.value_counts())
print()
print(train_data.malignant.value_counts())


# In[ ]:


pd.set_option("display.max_columns",101)
train_data.head()


# Create dataframes of only Malignant and Benign diagnosis.

# In[ ]:


Malignant = train_data[train_data.malignant == 1]
Benign = train_data[train_data.benign == 1]


# Set train_X equal to 80% of the malignant diagnosis.

# In[ ]:


train_X = Malignant.sample(frac=0.8)
count_Malignants = len(train_X)


# Add 80% of the benign diagnosis to train_X.

# In[ ]:


train_X = pd.concat([train_X, Benign.sample(frac = 0.8)], axis = 0)


# test_X contains all the diagnostics not in train_X.

# In[ ]:


test_X = train_data.loc[~train_data.index.isin(train_X.index)]


# Shuffle the dataframes so that the training is done in a random order.

# In[ ]:


train_X = shuffle(train_X)
test_X = shuffle(test_X)


# Add our target features to train_Y and test_Y

# In[ ]:


train_Y = train_X.malignant
train_Y = pd.concat([train_Y, train_X.benign], axis=1)


# In[ ]:


test_Y = test_X.malignant
test_Y = pd.concat([test_Y, test_X.benign], axis=1)


# Drop target features from train_X and test_X

# In[ ]:


train_X = train_X.drop(['malignant','benign'], axis = 1)
test_X = test_X.drop(['malignant','benign'], axis = 1)


# Check to ensure all of the training/testing dataframes are of the correct length

# In[ ]:


print(len(train_X))
print(len(train_Y))
print(len(test_X))
print(len(test_Y))


# Names of all of the features in train_X.

# In[ ]:


features = train_X.columns.values


# Transform each feature in features so that it has a mean of 0 and standard deviation of 1; 
# This helps with training the softmax algorithm.

# In[ ]:


for feature in features:
    mean, std = train_data[feature].mean(), train_data[feature].std()
    train_X.loc[:, feature] = (train_X[feature] - mean) / std
    test_X.loc[:, feature] = (test_X[feature] - mean) / std


# ## Train the Neural Network

# Parameters

# In[ ]:


learning_rate = 0.005
training_dropout = 0.9
display_step = 1
training_epochs = 5
batch_size = 100
accuracy_history = [] 
cost_history = []
valid_accuracy_history = [] 
valid_cost_history = [] 


# Number of input nodes

# In[ ]:


input_nodes = train_X.shape[1]


# Number of labels (malignant and benign)

# In[ ]:


num_labels = 2


# Split the testing data into validation and testing sets

# In[ ]:


split = int(len(test_Y)/2)

train_size = train_X.shape[0]
n_samples = train_Y.shape[0]

input_X = train_X.as_matrix()
input_Y = train_Y.as_matrix()
input_X_valid = test_X.as_matrix()[:split]
input_Y_valid = test_Y.as_matrix()[:split]
input_X_test = test_X.as_matrix()[split:]
input_Y_test = test_Y.as_matrix()[split:]


# In[ ]:


def calculate_hidden_nodes(nodes):
    return (((2 * nodes)/3) + num_labels)


# Number of nodes in each hidden layer

# In[ ]:


hidden_nodes1 = round(calculate_hidden_nodes(input_nodes))
hidden_nodes2 = round(calculate_hidden_nodes(hidden_nodes1))
hidden_nodes3 = round(calculate_hidden_nodes(hidden_nodes2))
print(input_nodes, hidden_nodes1, hidden_nodes2, hidden_nodes3)


# Percent of nodes to keep during dropout.

# In[ ]:


pkeep = tf.placeholder(tf.float32)


# Input

# In[ ]:


x = tf.placeholder(tf.float32, [None, input_nodes])


# Layer 1

# In[ ]:


W1 = tf.Variable(tf.truncated_normal([input_nodes, hidden_nodes1], stddev = 0.1))
b1 = tf.Variable(tf.zeros([hidden_nodes1]))
y1 = tf.nn.relu(tf.matmul(x, W1) + b1)


# Layer 2

# In[ ]:


W2 = tf.Variable(tf.truncated_normal([hidden_nodes1, hidden_nodes2], stddev = 0.1))
b2 = tf.Variable(tf.zeros([hidden_nodes2]))
y2 = tf.nn.relu(tf.matmul(y1, W2) + b2)


# Layer 3

# In[ ]:


W3 = tf.Variable(tf.truncated_normal([hidden_nodes2, hidden_nodes3], stddev = 0.1)) 
b3 = tf.Variable(tf.zeros([hidden_nodes3]))
y3 = tf.nn.relu(tf.matmul(y2, W3) + b3)
y3 = tf.nn.dropout(y3, pkeep)


# Layer 4

# In[ ]:


W4 = tf.Variable(tf.truncated_normal([hidden_nodes3, 2], stddev = 0.1)) 
b4 = tf.Variable(tf.zeros([2]))
y4 = tf.nn.softmax(tf.matmul(y3, W4) + b4)


# Output

# In[ ]:


y = y4
y_ = tf.placeholder(tf.float32, [None, num_labels]) 


# Minimize error using cross entropy

# In[ ]:


cost = -tf.reduce_sum(y_ * tf.log(y))


# AdamOptimizer

# In[ ]:


optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)


# Test Model

# In[ ]:


correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))


# Calculate accuracy

# In[ ]:


accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


# Initializing the variables

# In[ ]:


init = tf.global_variables_initializer()


# Launch the graph

# In[ ]:


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    
    for epoch in range(training_epochs): 
        for batch in range(int(n_samples/batch_size)):
            batch_x = input_X[batch * batch_size : (1 + batch) * batch_size]
            batch_y = input_Y[batch * batch_size : (1 + batch) * batch_size]

            sess.run([optimizer], feed_dict={x: batch_x, 
                                             y_: batch_y,
                                             pkeep: training_dropout})

        # Display logs after every 10 epochs
        if (epoch) % display_step == 0:
            train_accuracy, newCost = sess.run([accuracy, cost], 
                                               feed_dict={x: input_X, y_: input_Y, 
                                                          pkeep: training_dropout})

            valid_accuracy, valid_newCost = sess.run([accuracy, cost], 
                                                     feed_dict={x: input_X_valid, 
                                                                y_: input_Y_valid, pkeep: 1})

            print ("Epoch:", epoch, "Acc =", "{:.5f}".format(train_accuracy), 
                   "Cost =", "{:.5f}".format(newCost), 
                   "Valid_Acc =", "{:.5f}".format(valid_accuracy), 
                   "Valid_Cost = ", "{:.5f}".format(valid_newCost))
            
            # Record the results of the model
            accuracy_history.append(train_accuracy)
            cost_history.append(newCost)
            valid_accuracy_history.append(valid_accuracy)
            valid_cost_history.append(valid_newCost)
            
            # If the model does not improve after 15 logs, stop the training.
            if valid_accuracy < max(valid_accuracy_history) and epoch > 100:
                stop_early += 1
                if stop_early == 15:
                    break
            else:
                stop_early = 0
            
    print("Optimization Finished!")
    
    # Plot the accuracy and cost summaries 
    f, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10,4))

    ax1.plot(accuracy_history, color='b') # blue
    ax1.plot(valid_accuracy_history, color='g') # green
    ax1.set_title('Accuracy')

    ax2.plot(cost_history, color='b')
    ax2.plot(valid_cost_history, color='g')
    ax2.set_title('Cost')

    plt.xlabel('Epochs (x10)')
    plt.show()


# The prediction accuracy for the test data set using the AdamOptimizer model is 95%!

# ## Conclusion

# After using the AdamOptimizer model with all of the features in our Neural Network, it gives a prediction accuracy of ~96% and a cross-validation score of ~96% for the test data set.
# This models performs reasonably well and I suppose that if we have created new features, we could have built a more useful neural network.
