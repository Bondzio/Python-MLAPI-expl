#Linear regression with L1 and L2 penalties
#Random Forest
#XGBoost tree or something similar (there's a lot of open source packages for this)

#Try a dimensionality reduction method on all, or a subset of your data (https://scikit-learn.org/stable/modules/unsupervised_reduction.html)
#Try a feature selection method.

#Try one regression method that we *have not* covered in class.

#Put these in Kaggle Kernels(can be one big one if you want) but don't make them public until after the competition is over.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model

trainF = pd.read_csv("../input/trainFeatures.csv")
trainL = pd.read_csv("../input/trainLabels.csv")
testF = pd.read_csv("../input/testFeatures.csv")

def printresult(y_test, filename):
	ind = np.arange(1,len(y_test)+1,1)
	dataset = pd.DataFrame({'id':ind,'OverallScore':y_test[:,1]})
	dataset.to_csv(filename, sep=',', index=False)

def cleandata(df):
    for col in df.columns:
        if (df[col].isnull().sum())/len(df) > 0.9:
            df.drop(col,inplace=True,axis=1)
    for column in list(df.columns[df.isnull().sum() > 0]):
        df[column].fillna(df[column].mean(), inplace=True)
    df.drop({'ids'}, inplace = True, axis = 1)
    df['erkey'] = df['erkey'].str.slice_replace(0, 3, '')
    df['erkey'] = pd.to_numeric(df['erkey'])
    return df

trainData = cleandata(pd.merge(trainF, trainL, on='ids'))
X_train=trainData.iloc[:,0:47]
Y_train=trainData.iloc[:,47:49]

X_train = np.array(X_train)
Y_train = np.array(Y_train)
X_test = cleandata(testF)
X_test = np.array(X_test)

reg = linear_model.Lars(normalize=True, precompute='auto',eps=2.220446049250313e-1)
reg.fit(X_train, Y_train)
y_test = reg.predict(X_test)
printresult(y_test, "LeastAngleReg.csv")

