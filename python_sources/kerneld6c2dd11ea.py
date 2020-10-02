#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 22:41:13 2018

@author: muzammil1
"""

## ML Model for classification of Mushrooms
import numpy as np
import pandas as pd

from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.naive_bayes import GaussianNB

# Storing the dataset in a DataFrame
df = pd.read_csv('..//input/mushrooms.csv')

#function handles character data by converting them into numerical data
def handle_non_numerical_data(df):
    columns = df.columns.values#taking all the columns of the dataset into variable 

    for column in columns:
        text_digit_vals = {}#contains all the unique values and the number with which they will be replaced
        def convert_to_int(val):
            return text_digit_vals[val]

        if df[column].dtype != np.int64 and df[column].dtype != np.float64:#if the column datatype is not int or float then conversion will start
            column_contents = df[column].values.tolist()
            unique_elements = set(column_contents)
            x = 0
            for unique in unique_elements:
                if unique not in text_digit_vals:
                    text_digit_vals[unique] = x
                    x+=1

            df[column] = list(map(convert_to_int, df[column]))
    return df
df = handle_non_numerical_data(df)

# Now spliting the data in 70 - 30 % 
test_size = 0.3  # 30% of the data is used for testing 
train_data = df[:-int(test_size*len(df))]  #training data
test_data =  df[-int(test_size*len(df)):]  #testing data

# Separting Target column and feature columns
X_train = train_data.drop('class',1)
y_train = train_data['class']
X_test = test_data.drop('class',1)
y_test = test_data['class']

clf = GaussianNB() # creating object module for KNN classifier
clf.fit(X_train, y_train) # Fitting the data

y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred) 
print('Accuracy:', accuracy)
