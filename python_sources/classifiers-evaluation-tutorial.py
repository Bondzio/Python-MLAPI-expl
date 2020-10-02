#!/usr/bin/env python
# coding: utf-8

# # Iris Test Classifiers Evaluation Tutorial

# **Overview**
# 
# I created this classifiers evaluation tutorial specifically to help those who are still trying to grasp the basic concept of data science workflow on supervised learning.
# Mainly as a submission requirement for the class Data Mining MIT504
# 
# The data set is based on Iris Flowers. This is the most basic data set heavily used for beginner tutorials as it is very succinct and can easily be used to teach fundamentals. 
# In our data set, we have 150 samples of iris flowers, and we have 3 classes to predict into: Iris-Versicolor, Iris-Setosa, and Iris-Virginica.
# 
# Given their various features such as Sepal and Petal width and lengths, we can classify them to their respective classes.
# ![Iris Flowers](https://i.imgur.com/MQjZEae.jpg)

# In[ ]:


# Import required libraries
import numpy as np
import pandas as pd
import seaborn as sns

# This is so we can check the files we have in the current system. Most Kaggle Notebook files are found under kaggle/input
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


# Load csv file that we found
# Take note that this data set is just 15kb, so we are confident in putting everything in memory. 
# Fortunately Kaggle gives a provision of 16gb of running memory for Free! 
# So if your data set gets to more than that, I suggest you either breakdown the data or you use a database instead
# as it will be more manageable for larger sets of data
df = pd.read_csv('/kaggle/input/iris/Iris.csv') # df usually is used to abbreviate "Data Frame" from pandas library


# Remember we are using Python 3 in this Notebook, so the last statement will be evaluated as string for output if any.
# If you want to explicitly print, you can use the "print()" function

# Shape shows you the # of samples and the number of features / cols you have in your data set.
print(f'Data Frame Shape (rows, columns): {df.shape}') 

# This method is one of your basic tool to quickly view data. It shows first 5 rows of a frame
df.head() 


# Data Analysis and Exploration
# =============================

# In[ ]:


# I really like this method. Quick way to visualize everything.
# Take note that this is just a quick visualizations of what we have so far
# And from this we can explore further. If you want to know more about the different visualization
# functions; search for Seaborn. There are various libraries but this is my personal liking.
# https://seaborn.pydata.org/examples/index.html

# The "hue" refers to how you would want to differentiate the data in a visualization
# In this case I selected the species as these are the classes we have in our data set
sns.pairplot(df, hue="Species") 


# In[ ]:


# Visualize outcome of classes
sns.countplot(data=df, x="Species").set_title("Species Outcome")


# In here we plotted out the classes and how many instances / outcome of each of them are there on our data set. This is very important as this is where we can see if our dataset needs balancing to clean up or correct biases or possibility of overfitting. Since we see that they are all equal, therefore we have a perfectly balance data set.

# In[ ]:


sns.relplot(data=df, x="SepalWidthCm", y="SepalLengthCm", hue="Species", palette="bright", height=6)


# **In corelation to their Sepal features:**
# 
# In here we just plotted the iris flowers by their Sepal features (length and width). This is just to visualize the dataset we have in corelation to their sepal features. In here we can observe that Setosa can have a shorter length while having biggest width among the 3 classes. 
# 
# Versicolor as we see here has smallest width and on medium sepal length.
# 
# Virginica is the tallest among the 3 classes mostly. With one rare case of having a short sepal length and width.
# 

# In[ ]:


sns.relplot(data=df, x="PetalWidthCm", y="PetalLengthCm", hue="Species", palette="bright", height=6)


# **In corelation to their Petal features:**
# 
# In here we plotted the iris flowers by their petal features, and the result was quite obvious to classify.
# Setosa has the smallest petal features, virginica has the largest petal features and versicolor is mostly in the median range.

# Data Preparation, Balancing and Cleanup
# ===========================================

# In[ ]:


# Check if there are any null values
df.isnull().values.any()


# In[ ]:


# Remove null values
df = df.dropna()


# In[ ]:


# Check if there are any null values
df.isnull().values.any()


# In[ ]:


#Drop not needed columns / features
df.drop('Id', axis=1, inplace=True)
df.head()


# Classifier Setups and Build Model
# =================================

# **Import Necessary Libraries for Scoring and Evaluation**

# In[ ]:


# Import required libraries for performance metrics
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix 
from sklearn.model_selection import train_test_split


# Now this is my custom function on doing matrix caculation to the Confusion Matrix to get the TP, FP, TN and FN respectively.
# This function returns an ordered list of the performance measures.
# 
# TP is True Positives
# FP is False Positives
# TN is True Negative
# FN is False Negative

# In[ ]:


def get_performance_measures(actual, prediction):
    matrix = confusion_matrix(actual, prediction)
    FP = matrix.sum(axis=0) - np.diag(matrix)  
    FN = matrix.sum(axis=1) - np.diag(matrix)
    TP = np.diag(matrix)
    TN = matrix.sum() - (FP + FN + TP)

    return(TP, FP, TN, FN)


# Below we create our custom scorers. A scorer is basically a benchmark of how well your model performs given an actual result and a predicted result.
# 
# There are actually already a comprehensive list of scorers built in Python but for the purpose of learning, we will be creating 2 custom scorers in this notebook: sensitivity and specificity. The rest we just rely on the library to do its work to save up space in this notebook.

# In[ ]:


#Custom Scorers

# # Sensitivity, hit rate, recall, or true positive rate
# TPR = TP/(TP+FN)
# # Specificity or true negative rate
# TNR = TN/(TN+FP) 
# # Precision or positive predictive value
# PPV = TP/(TP+FP)
# # Negative predictive value
# NPV = TN/(TN+FN)
# # Fall out or false positive rate
# FPR = FP/(FP+TN)
# # False negative rate
# FNR = FN/(TP+FN)
# # False discovery rate
# FDR = FP/(TP+FP)

# # Overall accuracy
# ACC = (TP+TN)/(TP+FP+FN+TN)

# Also remember:
# specificity = true negative rate
# sensitivity = true positive rate

def sensitivity_score(y_true, y_pred, mode="multiclass"):
    if mode == "multiclass":
        TP, FP, TN, FN = get_performance_measures(y_true, y_pred)
        TPR = (TP/(TP+FN)).mean()
    elif mode == "binary":
        TP, FP, TN, FN = get_performance_measures(y_true, y_pred)
        TPR = (TP/(TP+FN))[1] # Since the [0] part is the index
    else:
        raise Exception("Mode not recognized!")
    
    return TPR

def specificity_score(y_true, y_pred, mode="multiclass"):
    if mode == "multiclass":
        TP, FP, TN, FN = get_performance_measures(y_true, y_pred)
        TNR = (TN/(TN+FP)).mean()
    elif mode == "binary":
        TP, FP, TN, FN = get_performance_measures(y_true, y_pred)
        TNR = (TN/(TN+FP))[1]
    else:
        raise Exception("Mode not recognized!")
    
    return TNR


# # **Setup Our Scorers**

# In[ ]:


# Define dictionary with performance metrics
# To know what everaging to use: https://stats.stackexchange.com/questions/156923/should-i-make-decisions-based-on-micro-averaged-or-macro-averaged-evaluation-mea#:~:text=So%2C%20micro%2Daveraged%20measures%20add,is%20more%20like%20an%20average.


scoring = {
            'accuracy':make_scorer(accuracy_score), 
            'precision':make_scorer(precision_score, average='weighted'),
            'f1_score':make_scorer(f1_score, average='weighted'),
            'recall':make_scorer(recall_score, average='weighted'), 
            'sensitvity':make_scorer(sensitivity_score, mode="multiclass"), 
            'specificity':make_scorer(specificity_score, mode="multiclass"), 
           }


# # **Setting up our Classifiers**

# In[ ]:


# Import required libraries for machine learning classifiers
from sklearn.tree import DecisionTreeClassifier #Decision Tree
from sklearn.naive_bayes import GaussianNB #Naive Bayes
from sklearn.linear_model import LogisticRegression #Logistic Regression
from sklearn.svm import LinearSVC # Support Vector Machine
from sklearn.neighbors import KNeighborsClassifier #K-nearest Neighbors
from sklearn.cluster import KMeans #K-means

# Instantiate the machine learning classifiers
decisionTreeClassifier_model = DecisionTreeClassifier()
gaussianNB_model = GaussianNB()
logisticRegression_model = LogisticRegression(max_iter=10000)
linearSVC_model = LinearSVC(dual=False)
kNeighbors_model = KNeighborsClassifier()


# Let's make a custom evaluation function to easily aggregate our score results. You can actually do this manually, but by making a function; we can easily reuse it easily for future use.
# 
# The beauty of this function is that it is very versatile and can be use not only for this data set but also to other data sets as well as long as you format them properly.

# In[ ]:


# features = data frame set that contain your features that will be used as input to see if prediction is equal to actual result
# target = data frame set (1 column usually) that will contain your target or actual results.
# folds = this is added so we can easily change the number of folds we want to do with our data set.
# folding is a technique to minimise overfitting and therefore make our model more accurate.
def models_evaluation(features, target, folds):    
    # Perform cross-validation to each machine learning classifier
    decisionTreeClassifier_result = cross_validate(decisionTreeClassifier_model, features, target, cv=folds, scoring=scoring)
    gaussianNB_result = cross_validate(gaussianNB_model, features, target, cv=folds, scoring=scoring)
    logisticRegression_result = cross_validate(logisticRegression_model, features, target, cv=folds, scoring=scoring)
    linearSVC_result = cross_validate(linearSVC_model, features, target, cv=folds, scoring=scoring)
    kNeighbors_result = cross_validate(kNeighbors_model, features, target, cv=folds, scoring=scoring)
    # kMeans_result = cross_validate(kMeans_model, features, target, cv=folds, scoring=scoring)

    # Create a data frame with the models perfoamnce metrics scores
    models_scores_table = pd.DataFrame({
      'Decision Tree':[
                        decisionTreeClassifier_result['test_accuracy'].mean(),
                        decisionTreeClassifier_result['test_precision'].mean(),
                        decisionTreeClassifier_result['test_recall'].mean(),
                        decisionTreeClassifier_result['test_sensitvity'].mean(),
                        decisionTreeClassifier_result['test_specificity'].mean(),
                        decisionTreeClassifier_result['test_f1_score'].mean()
                       ],

      'Gaussian Naive Bayes':[
                                gaussianNB_result['test_accuracy'].mean(),
                                gaussianNB_result['test_precision'].mean(),
                                gaussianNB_result['test_recall'].mean(),
                                gaussianNB_result['test_sensitvity'].mean(),
                                gaussianNB_result['test_specificity'].mean(),
                                gaussianNB_result['test_f1_score'].mean()
                              ],

      'Logistic Regression':[
                                logisticRegression_result['test_accuracy'].mean(),
                                logisticRegression_result['test_precision'].mean(),
                                logisticRegression_result['test_recall'].mean(),
                                logisticRegression_result['test_sensitvity'].mean(),
                                logisticRegression_result['test_specificity'].mean(),
                                logisticRegression_result['test_f1_score'].mean()
                            ],

      'Support Vector Classifier':[
                                    linearSVC_result['test_accuracy'].mean(),
                                    linearSVC_result['test_precision'].mean(),
                                    linearSVC_result['test_recall'].mean(),
                                    linearSVC_result['test_sensitvity'].mean(),
                                    linearSVC_result['test_specificity'].mean(),
                                    linearSVC_result['test_f1_score'].mean()
                                   ],

       'K-nearest Neighbors':[
                        kNeighbors_result['test_accuracy'].mean(),
                        kNeighbors_result['test_precision'].mean(),
                        kNeighbors_result['test_recall'].mean(),
                        kNeighbors_result['test_sensitvity'].mean(),
                        kNeighbors_result['test_specificity'].mean(),
                        kNeighbors_result['test_f1_score'].mean()
                       ],

      },

      index=['Accuracy', 'Precision', 'Recall', 'Sensitivity', 'Specificity', 'F1 Score', ])
    
    # Return models performance metrics scores data frame
    return(models_scores_table)


# In[ ]:


# Let's try to look at our data frame again one last time
df.head()


# # **Preparing Features and Targets**

# In[ ]:


# Specify features columns
# Actually what we are doing here is that we are just dropping the Species column since that is our class
# and the remaining columns will then be our features (eg. inputs to come up to a class)
# axis 0 basically means to drop all of that column
features = df.drop(columns="Species", axis=0)

# Now let's see what features looks like
features

# Don't mind the left hand side, those are just index mainly used for viewing


# In[ ]:


# Specify target column
# Now we try to get the frame of only our target. Which is the "Species" column
target = df["Species"]

# Do note that csv files are also zero-index, that means a row starts from zero.
target


# # **Running our Evaluation**

# In[ ]:


evaluationResult = models_evaluation(features, target, 5)
view = evaluationResult
view = view.rename_axis('Test Type').reset_index() #Add the index names to the column. This will be used for our presentation

# https://pandas.pydata.org/docs/reference/api/pandas.melt.html
# Re-Organizing our dataframe to fit our view need
view = view.melt(var_name='Classifier', value_name='Value', id_vars='Test Type')
# result
sns.catplot(data=view, x="Test Type", y="Value", hue="Classifier", kind='bar', palette="bright", alpha=0.8, legend=True, height=5, margin_titles=True, aspect=2)


# In[ ]:


# In here we just add a new column to our raw data frame, that gets the result for the highest
# scoring classifier in every score test.
evaluationResult['Best Score'] = evaluationResult.idxmax(axis=1)
evaluationResult


# # Conclusion
# 
# So in our findings, for this particular data set and classifiers used,** logistic regression** is by far the most performing and accurate classifier. 
# 
# Although note that their margin of difference are actually quite small and that we only tested it for a small data set (150 samples)
# 
# This is the really basic flow of creating a model up to identifying the classifiers to use based on your model.
# Getting more advanced means that you have to optimized your data set further, your fitting, and even optimize your classifiers further as each of them also have internal parameters that can be used to tweak depending on your data set to get better accuracy.

# In[ ]:




