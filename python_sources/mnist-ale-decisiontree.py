#!/usr/bin/env python
# coding: utf-8

# In[ ]:


###############################################################
# NB: shift + tab HOLD FOR 2 SECONDS!
###############################################################



# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import matplotlib.pyplot as plt
import seaborn as sns

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.
print('Getting traing dataset...')
train_data = pd.read_csv('../input/digit-recognizer/train.csv')
print('Traing data set obtained \n')

print('Getting test dataset...')
test_data = pd.read_csv('../input/digit-recognizer/test.csv')
print('Test data set obtained \n')


# Each image is 28 pixels in height and 28 pixels in width, for a total of 784 pixels in total. Each pixel has a single pixel-value associated with it, indicating the lightness or darkness of that pixel, with higher numbers meaning darker. This pixel-value is an integer between 0 and 255, inclusive.
# 
# The training data set, (train.csv), has 785 columns. **The first column, called "label", is the digit that was drawn by the user**. The rest of the columns contain the pixel-values of the associated image.
# 
# Each pixel column in the training set has a name like pixelx, where x is an integer between 0 and 783, inclusive. To locate this pixel on the image, suppose that we have decomposed x as x = i * 28 + j, where i and j are integers between 0 and 27, inclusive. Then pixelx is located on row i and column j of a 28 x 28 matrix, (indexing by zero).
# 
# 

# In[ ]:


train_data.head(5)


# In[ ]:


test_data


# In[ ]:


train_img = train_data.drop('label', axis=1)
train_label = train_data['label'].values
train_img


# **RECOVERING IMAGES**
# 
# Now we try to print a single image. In order to do so, we need to convert the pandas dataframe into a matrix, i.e. an ordered numpy array. 

# In[ ]:


img_try = train_img.iloc[30].values
img_try = np.reshape(img_try, (28, 28))

fig = plt.figure(figsize=(6, 6))
plt.imshow(img_try)
plt.title(train_label[30], fontsize=30)
plt.show()


# We can now define a function that does the same! 
# 
# It will eat the dataframe, the label and an integer number that will be the selected row

# In[ ]:


# The first function return the matrix out from the dataframe
def return_matrix(train, n=0):
    import numpy as np # linear algebra
    import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
    import matplotlib.pyplot as plt
    
    if ((n>=0) & (n<=783)) :
        img_try = train.iloc[n].values
        img_try = np.reshape(img_try, (28, 28))
    else :
        print('Insert a n between 0 and 783')
        pass 
    return img_try

# The second function eats both train and test dataframe plus an integer number between 0 and 783 (28x28 =784)
def print_matrix(train, test, n=0):
    import numpy as np # linear algebra
    import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
    import matplotlib.pyplot as plt
    
    if ((n>=0) & (n<=783)) :
        mat = return_matrix(train, n)
    
        fig = plt.figure(figsize=(5, 5))
        plt.imshow(mat)
        plt.title(train_label[n], fontsize=30)
    else : 
        print('Insert a n between 0 and 783')
        pass
    
    return print('Done')
        


# In[ ]:


print_matrix(train_img, train_label, 80)


# **DECISION TREE CLASSIFIER**
# 
# We may now start with a CLASSICAL Machine Learning algorithm such a **Decision Tree** classifier. 
# 
# Recall that now we have a set of features as a pd.dataframe saved as 
# > train_img
# 
# and a set of associated labels saved as
# > train_label
# 
# We start using the **return_matrix** function we have defined to transform the pd.dataframe into a np.array. NB: it has to be a flat array![](http://)
# 

# In[ ]:


features = []
labels = []

print('Transforming the data... \n')

for i in np.arange(0, train_label.size):
    features.append(train_img.iloc[i].values)
    labels.append(train_label[i])

print('Done')


# In[ ]:


print(np.array(features).shape)
print(np.array(labels).shape)


# We now need to split the Datasat into Train and Test to perform a supervised machine learning algorithm such as DecisionTreeClassifiare or RandomForestClassifier from scikit-learn

# In[ ]:


# split into training and testing sets
from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(np.array(features), np.array(labels), test_size=0.30)

print('Training records:',Y_train.size)
print('Test records:',Y_test.size)


# Now we import sklearn to create a *pipeline* that 
# 1. Scales the image using the **MinMaxScaler**
# 2. Create a **DecisionTreeClassifier**

# In[ ]:


from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier

# Convert the training features to floats so they can be scaled
X_train_float = X_train.astype('float64')

# Our pipeline performs two tasks:
#   1. Normalize the image arrays
#   2. Train a classification model - Decision Tree
img_pipeline = Pipeline([('norm', MinMaxScaler()),
                         ('classify', DecisionTreeClassifier()),
                        ])

# Use the pipeline to fit a model to the training data
print("Training model...")
clf = img_pipeline.fit(X_train_float, Y_train)

print('classifier trained!')


# We now need to evauete the model; we will plot a confusion matrix

# In[ ]:


# Evaluate classifier
from sklearn import metrics
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

classnames = '0 1 2 3 4 5 6 7 8 9'.split()

# Convert the test features for scaling
X_test_float = X_test.astype('float64')

print('Compute predictions: \n')
predictions = clf.predict(X_test)

print('Classifier Metrics:')
print(metrics.classification_report(Y_test, predictions, target_names=classnames))
print('Accuracy: {:.2%}'.format(metrics.accuracy_score(Y_test, predictions)))

print("\n Confusion Matrix:")
cm = confusion_matrix(Y_test, np.round(predictions, 0))

# Plot confusion matrix as heatmap
plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
plt.colorbar()
tick_marks = np.arange(len(classnames))
plt.xticks(tick_marks, classnames, rotation=85)
plt.yticks(tick_marks, classnames)
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.show()


# Now we need to do the same for the **TEST** values
# 
# Those are objects that have to be classified by the ML algorithm. 

# In[ ]:


test_img = test_data
X_value = []

print('Transforming the data... \n')

for i in np.arange(0, test_img.shape[0]):
    X_value.append(test_img.iloc[i].values)

print('Done')

print(np.array(X_value).shape)


# **PREDICTIONS**
# 
# We now **predict** what the images are; we define a simple function that eats the classifier and the image and returns the preiction

# In[ ]:


# Function to predict the class of an image
def predict_image(classifier, image_array):
    import numpy as np
    
    # These are the classes our model can predict
    classnames = '0 1 2 3 4 5 6 7 8 9'.split()
    
    # Predict the class of each input image
    predictions = classifier.predict(image_array)
    
    predicted_classes = []
    for prediction in predictions:
        # And append the corresponding class name to the results
        predicted_classes.append(classnames[int(prediction)])
    # Return the predictions
    return predicted_classes


# In[ ]:


classnames = '0 1 2 3 4 5 6 7 8 9'.split()

print('Compute predictions: \n')
true_predictions = predict_image(clf, np.array(X_value))
print('End.')


# We now define a function that, gives the images, the prediction and an integer number between 0 and 27999 (dimension of the unkwnow images dataset) returns the plot of the image with the predicted label as a title

# In[ ]:


def plot_pred(img, pred, n=0):
    import matplotlib.pyplot as plt
    import numpy as np
    
    if ((n>=0) & (n<np.array(X_value).shape[0])):
        imag = np.reshape(np.array(img[n]), (28, 28))
        fig = plt.figure(figsize=(5, 5))
        plt.imshow(imag)
        plt.title(pred[n], fontsize=30)
    else: 
        print('Wrong n \n')
        pass
    
    return print('Done')


# In[ ]:


plot_pred(X_value, true_predictions, 30)
plot_pred(X_value, true_predictions, 99)
plot_pred(X_value, true_predictions, 1200)


# Now, we would like to define a SINGLE FUNCTION that eats the training dataset and spits out the trained classifier, doing all the manipulation internally. 
# 
# This means that one can run only the function after having received the dataset. 

# In[ ]:


def decision_tree_classifier_MNIST(train_data, testsize=0.30, criterio='gini'):
    import numpy as np # linear algebra
    import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
    import matplotlib.pyplot as plt
    from sklearn import metrics
    from sklearn.metrics import accuracy_score, confusion_matrix
    from sklearn.model_selection import train_test_split
    
    # First, we need to transform the data
    train_img = train_data.drop('label', axis=1)
    train_label = train_data['label'].values
    
    features = []
    labels = []

    print('Transforming the data...')
    for i in np.arange(0, train_label.size):
        features.append(train_img.iloc[i].values)
        labels.append(train_label[i])
    print('Transformation done \n')
    
    
    # Second, we need to split the dataset into training and test subsets
    print('Splitting the dataset... ')
    X_train, X_test, Y_train, Y_test = train_test_split(np.array(features), np.array(labels), test_size=testsize)
    print('Splitting done \n')
    
    # Third, we need to define the classifier
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.tree import DecisionTreeClassifier
    
    if (criterio != 'gini') :
        crit='entropy'
    else :
        crit ='gini'
        
        # Convert the training features to floats so they can be scaled
    X_train_float = X_train.astype('float64')

        # Our pipeline performs two tasks:
        #   1. Normalize the image arrays
        #   2. Train a classification model - Decision Tree
    img_pipeline = Pipeline([('norm', MinMaxScaler()),
                         ('classify', DecisionTreeClassifier(criterion = crit)),
                        ])

    # Fourth, we train the model
    print("Training model...")
    clf = img_pipeline.fit(X_train_float, Y_train)
    print('Training done. \n')
    
    
    # Finally, we evaluate the trained model
    print('Reporting the model...')
    classnames = '0 1 2 3 4 5 6 7 8 9'.split()
    print('Compute predictions: \n')
    predictions = clf.predict(X_test)

    print('Classifier Metrics:')
    print(metrics.classification_report(Y_test, predictions, target_names=classnames))
    print('Accuracy: {:.2%}'.format(metrics.accuracy_score(Y_test, predictions)))

    print("\n Confusion Matrix:")
    cm = confusion_matrix(Y_test, np.round(predictions, 0))

        # Plot confusion matrix as heatmap
    plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.colorbar()
    tick_marks = np.arange(len(classnames))
    plt.xticks(tick_marks, classnames, rotation=85)
    plt.yticks(tick_marks, classnames)
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.show()
    
    
    print('Process ended succesfully!')
    return clf


# In[ ]:


clf = decision_tree_classifier_MNIST(train_data)


# We thus can use our classifier to make prediction:

# In[ ]:


def predict_image(classifier, image_array):
    import numpy as np
    
    # These are the classes our model can predict
    classnames = '0 1 2 3 4 5 6 7 8 9'.split()
    
    # Predict the class of each input image
    predictions = classifier.predict(image_array)
    
    predicted_classes = []
    for prediction in predictions:
        # And append the corresponding class name to the results
        predicted_classes.append(classnames[int(prediction)])
    # Return the predictions
    return predicted_classes

def evaluate_plot_pred(clf, test_data, n=0):
    import numpy as np # linear algebra
    import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
    import matplotlib.pyplot as plt
    
    # First need to transform the data
    test_img = test_data
    X_value = []

    print('Transforming the data... \n')
    for i in np.arange(0, test_img.shape[0]):
        X_value.append(test_img.iloc[i].values)

    print('Done')
    
    
    # Second, we compute the predictions
    classnames = '0 1 2 3 4 5 6 7 8 9'.split()

    print('Compute predictions: \n')
    true_predictions = predict_image(clf, np.array(X_value)) #notice that we call the function we defined before
    print('Predictions done.')
    
    # Finally, we plot
    if ((n>=0) & (n<np.array(X_value).shape[0])):
        imag = np.reshape(np.array(X_value[n]), (28, 28))
        fig = plt.figure(figsize=(5, 5))
        plt.imshow(imag)
        plt.title(true_predictions[n], fontsize=30)
    else: 
        print('Wrong n \n')
        pass
    
    print('Done. ')
    
    return true_predictions
    


# In[ ]:


true_predictions = evaluate_plot_pred(clf, test_data, 1200)


# In[ ]:




