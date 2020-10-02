#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.utils import resample
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import RidgeClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, KFold, GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
plt.style.use('ggplot')
# %notebook inline


# # Functions:

# In[ ]:


# Function which read csv raw data into pandas dataframe.
def process_raw_data(row_data_dir="../input/", hf=False):
    if hf:
        hf_data = pd.read_csv(row_data_dir+"HF.csv", header=None).T
        hf_ts = pd.read_csv(row_data_dir+"TimeTicksHF.csv", dtype='float64')
        hf_ts['datetime'] = pd.to_datetime(hf_ts.iloc[:, 0], unit='s')
        
        # adding the timestamps to the data.
        hf_data['datetime'] = hf_ts['datetime']
        # drop nans values.
        hf_data = hf_data.dropna()
        # set datetime as index.
        hf_data = hf_data.set_index('datetime')
        # round datetime index to seconds.
        hf_data.index = hf_data.index.floor('s')
        # drop duplicated index.
        hf_data = hf_data[~hf_data.index.duplicated(keep='first')]
#         hf_data = hf_data.drop(columns = ['ts'])
        

    else:
        lf1i_data = pd.read_csv(row_data_dir+"LF1I.csv", header=None )
        lf1v_data = pd.read_csv(row_data_dir+"LF1V.csv", header=None)
        lf2i_data = pd.read_csv(row_data_dir+"LF2I.csv", header=None)
        lf2v_data = pd.read_csv(row_data_dir+"LF2V.csv", header=None)

        lf1_ts = pd.read_csv(row_data_dir+"TimeTicks1.csv", dtype='float64')
        lf1_ts['datetime'] = pd.to_datetime(lf1_ts.iloc[:, 0], unit='s')
        lf2_ts = pd.read_csv(row_data_dir+"TimeTicks2.csv", dtype='float64')
        lf2_ts['datetime'] = pd.to_datetime(lf2_ts.iloc[:, 0], unit='s')
        

        # list of dataframes.
        data_lst = [lf1i_data, lf1v_data, lf2i_data, lf2v_data]
        # converting from str to complex.
        for data in data_lst:
            for i in range(data.shape[1]):
                data.iloc[:,i] = data.iloc[:,i].str.replace('i', 'j').apply(complex)

                
         # adding the timestamps to the data.
        lf1i_data['datetime'] = lf1_ts['datetime']
        lf1v_data['datetime'] = lf1_ts['datetime']
        lf2i_data['datetime'] = lf2_ts['datetime']
        lf2v_data['datetime'] = lf2_ts['datetime']
        
        # drop nans values.
        lf1i_data = lf1i_data.dropna()
        lf1v_data = lf1v_data.dropna() 
        lf2i_data = lf2i_data.dropna()
        lf2v_data = lf2v_data.dropna()
        
        
        # set datetime as index and round the index to seconds.
        lf1i_data.index = lf1i_data.set_index('datetime').index.floor('s')
        lf1v_data.index = lf1v_data.set_index('datetime').index.floor('s')
        lf2i_data.index = lf2i_data.set_index('datetime').index.floor('s')
        lf2v_data.index = lf2v_data.set_index('datetime').index.floor('s')     
        
        
        # remove duplicated index.
        lf1i_data = lf1i_data[~lf1i_data.index.duplicated(keep='first')]
        lf1i_data.index = lf1i_data.set_index('datetime').index.floor('s')
        
        lf1v_data = lf1v_data[~lf1v_data.index.duplicated(keep='first')]
        lf1v_data.index = lf1v_data.set_index('datetime').index.floor('s')
        
        lf2i_data.index = lf2i_data.set_index('datetime').index.floor('s')
        lf2i_data = lf2i_data[~lf2i_data.index.duplicated(keep='first')]
        
        lf2v_data.index = lf2v_data.set_index('datetime').index.floor('s')
        lf2v_data = lf2v_data[~lf2v_data.index.duplicated(keep='first')]
    
    ### tagging_data ###
    tagging_data = pd.read_csv(row_data_dir+"TaggingInfo.csv", header=None, dtype={'1':str})

    # convertion from unix to datetime.        
    tagging_data['dt_on'] = pd.to_datetime(tagging_data.iloc[:,2], unit='s')
    tagging_data['dt_off'] = pd.to_datetime(tagging_data.iloc[:,3], unit='s')
    
    if hf:
        print('hf_data shape: {0}'.format(hf_data.shape))

        return hf_data, tagging_data
        
    else:  
        print('lf1i_data shape: {0}'.format(lf1i_data.shape))
        print('lf1v_data shape: {0}'.format(lf1v_data.shape))
        print('lf2i_data shape: {0}'.format(lf2i_data.shape))
        print('lf2v_data shape: {0}'.format(lf2v_data.shape))
        
                
        return lf1i_data, lf1v_data, lf2i_data, lf2v_data, tagging_data


# In[ ]:


def assign_labels(tagging_data, row):
    for i in range(tagging_data.shape[0]):
        if row['datetime'] in pd.Interval(tagging_data.iloc[i,-2], tagging_data.iloc[i ,-1], closed='both'):
            return tagging_data.iloc[i, 1]
    return 'None'


# In[ ]:


def elec_features(lf1i_data, lf1v_data, lf2i_data, lf2v_data, idx):
    # Compute net complex power 
    # S=Sum_over(In*Vn*cos(PHIn))=Sum(Vn*complex_conjugate(In))=P+jQ
    l1_p = np.multiply(lf1v_data.iloc[:, :6], np.conj(lf1i_data.iloc[:, :6])).loc[idx]
    l2_p = np.multiply(lf2v_data.iloc[:, :6], np.conj(lf2i_data.iloc[:, :6])).loc[idx]
        
    l1_complex_power = np.sum(l1_p, axis=1).loc[idx]
    l2_complex_power = np.sum(l2_p, axis=1).loc[idx]
    
    # Real, Reactive, Apparent powers: P=Real(S), Q=Imag(S), S=Amplitude(S)=P^2+Q^2
    # l1 - stands for phase 1 S - Vector Aparent Power
    # Phase-1
    l1_real = l1_complex_power.apply(np.real).loc[idx]
    l1_imag = l1_complex_power.apply(np.imag).loc[idx]
    l1_app  = l1_complex_power.apply(np.absolute).loc[idx]

    # Real, Reactive, Apparent power currents
    # l2 - stands for phase 2 S - Vector Aparent Power
    # Phase-2
    l2_real = l2_complex_power.apply(np.real).loc[idx]
    l2_imag = l2_complex_power.apply(np.imag).loc[idx]
    l2_app  = l2_complex_power.apply(np.absolute).loc[idx]
    
    # Compute Power Factor, we only consider the first 60Hz component
    # PF=cosine(angle(S))
    l1_pf = l1_p.iloc[:,0].apply(np.angle).apply(np.cos).loc[idx]
    l2_pf = l2_p.iloc[:,0].apply(np.angle).apply(np.cos).loc[idx]
    y = lf2i_data['label'].astype(str).loc[idx] 
    
    
    return l1_real, l1_imag, l1_app, l2_real, l2_imag, l2_app, l1_pf, l2_pf, y 


# ## Electrical features:

# * **I1_real:** is real component of current harmonic (I) of first phase (1) as recorded from one of the apartments it indicates active current component - the current invested at work: entire power is consumed at load - resistive component.
# 
# 
# * **I1_imag:** is imaginary component of current harmonic (I) of first phase (1) as recorded from one of the apartments it indicates reactive current component - the current invested at work: entire power is consumed at load- capacitive/inductive component.
# 
# 
# * **I1_app:** is apparent power - it represents the entire power S^2=P^2+Q^2 where I1_app=SQRT(I1_real^2+I1_imag^2).
# 
# 
# * **I1_pf:** is power factor angle component - PF=P/Q, PF=I1_real/I1_imag.
# 
# 
# * **I2:** is same as I1 except for 2nd phase.
# 
# 
# * **hf_data:** spectrogram of high frequency noise captured in the home.
# 
# 
# * **y:** is target result indicating the device class: stove, dishwasher, lamp.

# In[ ]:


def proper_index(tagging_data, hf_data, lf1i_data):
    
    print('orginal hf_data  shape: {}'.format(hf_data.shape))
    print('orginal lf_data  shape: {}'.format(lf1i_data.shape))
        
    # slice idx to be in the range of first tagging device on datetime idx to last device off datetime idx.
    idx = lf1i_data.loc[tagging_data.dt_on.iloc[0]:tagging_data.dt_off.iloc[-1],:].index
    
    print('idx len (first transformation): {}'.format(len(idx)))
    
    # idx which are common to hf_data and lf1_data/lf2_data.
    idx = hf_data.index.intersection(idx)
    
    print('idx shape (second transformation): {}'.format(len(idx)))
    
    return idx, hf_data.loc[idx]


# ## White noise data

# In[ ]:


hf_data, tagging_data = process_raw_data(hf=True)
hf_data.head()


# ## Phases data

# In[ ]:


lf1i_data, lf1v_data, lf2i_data, lf2v_data, tagging_data = process_raw_data() 
lf1i_data.head()


# In[ ]:


lf1v_data.head()


# In[ ]:


lf2i_data.head()


# In[ ]:


lf2v_data.head()


# In[ ]:


tagging_data.head()


# In[ ]:


tagging_data.shape


# In[ ]:


lf2i_data['label'] = lf2i_data.apply(lambda row: assign_labels(tagging_data, row), axis=1)


# In[ ]:


lf2i_data.shape


# In[ ]:


lf1i_data.shape


# In[ ]:


idx, hf_data = proper_index(tagging_data, hf_data, lf1i_data)


# In[ ]:


l1_real, l1_imag, l1_app, l2_real, l2_imag, l2_app, l1_pf, l2_pf, y = elec_features(lf1i_data, lf1v_data, lf2i_data, lf2v_data, idx)


# In[ ]:


y.shape


# In[ ]:


l1_real.shape


# In[ ]:


lf2i_data.shape


# In[ ]:


lf2i_data.label.unique()


# In[ ]:


y.unique().tolist()


# # Unbalanced data

# In[ ]:


y.value_counts() 


# * **value_counts Return a Series containing counts of unique values - how many records of electric device of any class.**
# 
# * **bar plot of instants count of every electric device within the target vector y.**
# 

# In[ ]:


y.value_counts().plot(kind='bar')
plt.show()


# In[ ]:


X = pd.concat([l1_real, l1_imag, l1_app, l1_pf, l2_real, l2_imag, l2_app, l2_pf, hf_data], axis=1).values


# * **X** - input array is contain electrical features and white noise data.
# * **y** - is target class: electric load - dishwasher, lamp, stove...

# In[ ]:


X.shape


# In[ ]:


y.shape


# # PCA - Data visualization

# In[ ]:


X_PCA = StandardScaler().fit_transform(X)
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(X_PCA)
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])


# In[ ]:


pca.explained_variance_ratio_


# In[ ]:


y_PCA = y.reset_index(drop=True)
y_PCA.head()


# In[ ]:


finalDf = pd.concat([principalDf, y_PCA ], axis = 1)


# In[ ]:


finalDf.head()


# * PCA - Principal Component Analysis. Analysis through linear dimensionality reduction to two dimensions in order to enable a 2D plot.
# 
# * principalDf is constructed dataframe of principal Components, two components as columns of data representing components 1,2.
# 
# * pca.explained_variance_ratio_ is vector of percentile variance contained at each component.
# 
# * finalDf is a dataframe with 2 principal components that are two linear combinations of the physically meaningful components with class identifier of electric component (stove, dishwasher...) such that the two primary components are the most significant information carriers of model.
# 
# * plot a figure of the two components.
# 
# * targets is target y vector unique identifiers turned into a list.
# 
# * each target electric device class is scatter plotted with components 1,2 as coordinates.

# In[ ]:


# %matplotlib notebook
get_ipython().run_line_magic('matplotlib', 'inline')
fig = plt.figure(figsize = (10,7))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
targets = y.unique().tolist()
targets = list(filter(lambda x: x!= 'None', targets))
colors = ['r', 'g', 'b', 'y', 'm', 'k', 'w', 'c', 'darkred', 'lime', 'dodgerblue', 'magenta', 'yellow' ]
for target, color in zip(targets,colors):
    indicesToKeep = finalDf['label'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(targets)
plt.show()


# # Classifaction models 

# # KNN Classifier

# In[ ]:


clf = KNeighborsClassifier() 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
kf = KFold(n_splits=5, shuffle=True, random_state=25)
scores = cross_val_score(clf, X, y, cv=kf)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() ))


# using sklearn function - train_test_split(X, y, test_size=0.3) Split arrays or matrices into random train and test subsets. 
# 
# test dataset size is 30% of X
# 
# KFold is for cross-validation. split the X, y into n_splits=5 segments to avoid overfitting of training
# n segments constructing the test dataset are embedded separately into training dataset
# clf.fit fits with KNN clasifier the X_train vector to the y_train outcome

# ### Classification Report

# In[ ]:


clf.fit(X_train, y_train)
print(classification_report(y,clf.predict(X)))


# ### Confusion Matrix

# In[ ]:


cm = pd.DataFrame(confusion_matrix(y, clf.predict(X)), index=clf.classes_, columns=clf.classes_)
cm


# * High accuracy classification report.
# * **Confusion matrix:** high accuracy, some confusion between None(none of the devices is on) and some devices.
# * Although imbalanced data - accuracy is high for unbalanced devices - small confusion between kitchen counter, Light and kitchen light with dimmer - this is resolved if train on variable percentage of dimmer lights,some confusion between stove and oven.
# * Heatmap plot based on the confusion matrix dataframe. 

# ### Confusion matrix heatmap

# In[ ]:


plt.figure(figsize=(20,12))
sns.heatmap(cm, annot=True)
plt.show()


# # Ridge Classifier

# In[ ]:


clf = RidgeClassifier( )
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
kf = KFold(n_splits=5, shuffle=True, random_state=25)
scores = cross_val_score(clf, X, y, cv=kf)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() ))


# ### Classification Report

# In[ ]:


clf.fit(X_train, y_train)
print(classification_report(y,clf.predict(X)))


# ### Confusion Matrix

# In[ ]:


cm = pd.DataFrame(confusion_matrix(y, clf.predict(X)), index=clf.classes_, columns=clf.classes_)
cm


# ### Confusion matrix heatmap

# In[ ]:


plt.figure(figsize=(20,12))
sns.heatmap(cm, annot=True)
plt.show()


# # Random Forest Classifier

# * Random Forest classifier with cross-validation.
# * Notice: using hyper parameter class_weight to deal with the unbalanced data. 
# * Accuracy modification is small downwards by 0.1%.
# * Confusion non diagonal components rise a little bit.

# In[ ]:


clf = RandomForestClassifier(n_estimators=100, n_jobs=3, class_weight='balanced')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
kf = KFold(n_splits=5, shuffle=True, random_state=25)
scores = cross_val_score(clf, X, y, cv=kf)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() ))


# ### Classification Report

# In[ ]:


clf.fit(X_train, y_train)
print(classification_report(y,clf.predict(X)))


# ### Confusion Matrix

# In[ ]:


cm = pd.DataFrame(confusion_matrix(y, clf.predict(X)), index=clf.classes_, columns=clf.classes_)
cm


# ### Confusion matrix heatmap

# In[ ]:


plt.figure(figsize=(20,12))
sns.heatmap(cm, annot=True)
plt.show()


# ## Logistic Regression Classifier

# In[ ]:


clf = LogisticRegression(solver='lbfgs', n_jobs=-1, multi_class = 'auto', class_weight='balanced')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
kf = KFold(n_splits=5, shuffle=True, random_state=25)
scores = cross_val_score(clf, X, y, cv=kf)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() ))


# ### Classification Report

# In[ ]:


clf.fit(X_train, y_train)
print(classification_report(y,clf.predict(X)))


# ### Confusion Matrix

# In[ ]:


cm = pd.DataFrame(confusion_matrix(y, clf.predict(X)), index=clf.classes_, columns=clf.classes_)
cm


# ### Confusion matrix heatmap

# In[ ]:


plt.figure(figsize=(20,12))
sns.heatmap(cm, annot=True)
plt.show()


# # Decision Tree Classifier

# In[ ]:


clf = DecisionTreeClassifier(class_weight='balanced')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
kf = KFold(n_splits=5, shuffle=True, random_state=25)
scores = cross_val_score(clf, X, y, cv=kf)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() ))


# ### Classification Report

# In[ ]:


clf.fit(X_train, y_train)
print(classification_report(y,clf.predict(X)))


# ### Confusion Matrix

# In[ ]:


cm = pd.DataFrame(confusion_matrix(y, clf.predict(X)), index=clf.classes_, columns=clf.classes_)
cm


# ### Confusion matrix heatmap

# In[ ]:


plt.figure(figsize=(20,12))
sns.heatmap(cm, annot=True)
plt.show()

