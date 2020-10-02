#!/usr/bin/env python
# coding: utf-8

# # Spam Classifier 
# This tutorial aims at providing basic information on how to perform preprocessing of text data, vectorization, choosing a Machine Learning model and optimizing its hyperparameters.
# The Spam Classifier aims at classifiying SMS as spam(1) or ham(0).

# Lets start by importing the necessary libraries

# In[1]:


import pandas as pd
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
from nltk.stem import WordNetLemmatizer
import re
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import LabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
import seaborn as sn
import matplotlib.pyplot as plt


# ### Load data
# Use read_csv function to load the dataframe

# In[2]:


df= pd.read_csv("../input/spam.csv", encoding='ISO-8859-1')


# In[3]:


cols=['Unnamed: 2','Unnamed: 3','Unnamed: 4']
df.drop(cols,axis=1,inplace=True)


# In[4]:


df.rename(columns={'v1': 'Label', 'v2': 'Message'}, inplace=True)


# In[5]:


df.shape


# ### Transformer
# 
# ##### Custom Transformer for selecting columns from Pandas dataframe and a transformer for encoding labels

# In[6]:


class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_name):
        self.attribute_name=attribute_name
    def fit(self,X,y=None):
        return self
    def transform(self, X):
        return X[self.attribute_name].values
    
class MyLabelBinarizer(TransformerMixin):
    def __init__(self, *args, **kwargs):
        self.encoder = LabelBinarizer(*args, **kwargs)
    def fit(self, x, y=0):
        self.encoder.fit(x)
        return self
    def transform(self, x, y=0):
        return self.encoder.transform(x)


# ##### Create Custom Transformer for cleaning data
# Use WordNetLemmatizer available in NLTK library to lemmatize words. Lemmatization is the process of converting words to it root word. For eg: Words like running, ran will be converted to its root word run.

# In[7]:


class NLTK_Preprocessing_Module(BaseEstimator, TransformerMixin):
    
    def fit(self,X,y=None):
        return self
    
    def transform(self,X):
        return (self.helperFunction(X))
    
    def lemmatize_all(self,sentence):
        
        wnl = WordNetLemmatizer()
        for word, tag in pos_tag(word_tokenize(sentence)):
            if tag.startswith("NN"):
                yield wnl.lemmatize(word, pos='n')
            elif tag.startswith('VB'):
                yield wnl.lemmatize(word, pos='v')
            elif tag.startswith('JJ'):
                yield wnl.lemmatize(word, pos='a')
            elif tag.startswith('R'):
                yield wnl.lemmatize(word, pos='r')
            else:
                yield word
            
    def msgProcessing(self,raw_msg):
        
        meaningful_words=[]
        words2=[]
        raw_msg = str(raw_msg.lower())
        raw_msg=re.sub(r'[^a-z\s]', ' ', raw_msg)
        words=raw_msg.split()
        """Remove words with length lesser than 2"""
        for i in words:
            if len(i)>=2:
                words2.append(i)
        stops=set(stopwords.words('english'))
        meaningful_words=" ".join([w for w in words2 if not w in stops])
        return(" ".join(self.lemmatize_all(meaningful_words)))


    def helperFunction(self,df):
        
        print ("Data Preprocessing!!!")
        cols=['Message']
        df=df[cols]
        df.Message.replace({r'[^\x00-\x7F]+':''},regex=True,inplace=True)
        num_msg=df[cols].size
        clean_msg=[]
        for i in range(0,num_msg):
            clean_msg.append(self.msgProcessing(df['Message'][i]))
        df['Processed_msg']=clean_msg
        X=df['Processed_msg']
        print ("Data Preprocessing Ends!!!")
        return X


# ### Pipeline

# In[8]:


label=["Label"]
pipeline1=Pipeline([("nltk",NLTK_Preprocessing_Module()),])

pipeline2=Pipeline([("dataframe_selector",DataFrameSelector(label)),
                    ("label binarizer",MyLabelBinarizer()),])


# In[9]:


data_prepared=pipeline1.fit_transform(df)


# In[10]:


encoded_label=pipeline2.fit_transform(df)


# In[37]:


encoded_label


# Split data into train and test dataset

# In[11]:


from sklearn.model_selection import train_test_split
xtrain,xval,ytrain,yval= train_test_split(data_prepared,encoded_label,test_size=0.2, random_state=42)


# ### Vectorization 
# Convert text data to vectors using CountVectorizer

# In[12]:


def vectorizer(train,test):
    vectorizer= CountVectorizer(analyzer="word", tokenizer= None, preprocessor= None, stop_words= None, max_features=6000)
    train_data_features= vectorizer.fit_transform(train)
    train_data_features= train_data_features.toarray()
    test_data_features=vectorizer.transform(test)
    test_data_features=test_data_features.toarray()
    return train_data_features,test_data_features


# In[13]:


xtrain_vector,xval_vector=vectorizer(xtrain,xval)


# ### Training various classifiers
# Here I am going to choose four classifiers.
# ##### 1. Naive Bayes
# ##### 2. Decision Tree
# ##### 3. Random Forest
# ##### 4. Support Vector Machine
# 
# Train various classifiers using default hyperparameters and check how well they perform using k-cross validation.

# In[ ]:





# In[14]:


MNB=MultinomialNB()
DT=DecisionTreeClassifier()
RF=RandomForestClassifier()
SVM=svm.SVC()


# In[15]:


MNB_scores=cross_val_predict(MNB, xtrain_vector, ytrain,cv=5,method="predict_proba")
DT_scores=cross_val_predict(DT, xtrain_vector, ytrain,cv=5,method="predict_proba")
RF_scores=cross_val_predict(RF, xtrain_vector, ytrain,cv=5,method="predict_proba")
SVM_scores=cross_val_predict(SVM, xtrain_vector, ytrain,cv=5,method="decision_function")


# In[16]:


MNB_scores1=MNB_scores[:,1]
DT_scores1=DT_scores[:,1]
RF_scores1=RF_scores[:,1]
SVM_scores1=SVM_scores


# ## Plot Receiver Output Characteristic (ROC) Curve
# Calculate FPR (False Positive Rate) and TPR (True Positive Rate) for generating the ROC Curve.

# In[17]:


fpr_MNB,tpr_MNB,threshold_MNB=roc_curve(ytrain, MNB_scores1)
fpr_DT,tpr_DT,threshold_DT=roc_curve(ytrain, DT_scores1)
fpr_RF,tpr_RF,threshold_RF=roc_curve(ytrain, RF_scores1)
fpr_SVM,tpr_SVM,threshold_SVM=roc_curve(ytrain, SVM_scores1)


# In[18]:


def plot_roc_curve(fpr,tpr,label=None):
    plt.plot(fpr,tpr,linewidth=2,label=label)
    plt.plot([0,1],[0,1],'k--')
    plt.axis([0,1,0,1])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Label')
    plt.legend(loc="lower right")    


# In[19]:


plot_roc_curve(fpr_MNB,tpr_MNB,"Multinomial")
plot_roc_curve(fpr_DT,tpr_DT,"DT")
plot_roc_curve(fpr_RF,tpr_RF,"RF")
plot_roc_curve(fpr_SVM,tpr_SVM,"SVM")


# There is a tradeoff between TPR and FPR. Higher the TPR, higher will be the FPR. A good classifier will stay as far away from the dotted lines, ie to the top left corner. To check which classifier performs better, calculate the Area Under Curve score. A good classifier will have ROC AUC score 1. 

# In[20]:


auc_MNB=roc_auc_score(ytrain, MNB_scores1)
auc_DT=roc_auc_score(ytrain, DT_scores1)
auc_RF=roc_auc_score(ytrain, RF_scores1)
auc_SVM=roc_auc_score(ytrain, SVM_scores1)


# In[21]:


print ("ROC-AUC Score of Multinomial NB: ",auc_MNB)
print ("ROC-AUC Score of Decision Tree: ",auc_DT)
print ("ROC-AUC Score of Random Forest: ",auc_RF)
print ("ROC-AUC Score of Support Vector Machine: ",auc_SVM)


# The ROC AUC score of SVM is clearly the largest, hence SVM is the best performing model followed by Decision Tree. We will optimize the hyperparameters of SVM and Multinomial NB using GridSearch. GridSearchCV is a built-in function in sklearn which allows us to find the optimal parameters of a model. 

# ## Hyperparameter Optimization  
# In the above steps, we trained the various ML models using default hyperparameters which may not be the optimal values. The optimal values for the hyperparameters can be found by
# 1. GridSearch
# 2. Randomized Search.
# 
# Here we will use GridSearchCV available in sklearn library.

# In[72]:


#Function to plot confusion matrix as heatmap
def plot_confusion_heatmap(ytrue,ypred):
    array = confusion_matrix(ytrue,ypred)       
    df_cm = pd.DataFrame(array, range(2),range(2))
    sn.set(font_scale=1.4)
    sn.heatmap(df_cm, annot=True,annot_kws={"size": 16})


# In[24]:


svm_params=[{"kernel":['linear','rbf','poly']},{"C":[1,10,100,1000]},{"gamma":[0,10,100]}]
model1=svm.SVC()
gridsearch1=GridSearchCV(model1, svm_params, cv=5, refit=True)


# In[28]:


gridsearch.fit(xtrain_vector, ytrain)


# In[61]:


mnb_params=[{"alpha":[0.0,1.0,2.0,3.0,4.0,5.0]},{"fit_prior":["True","False"]}]
model2= MultinomialNB()
gridsearch2=GridSearchCV(model2, mnb_params, cv=5, refit=True)


# In[62]:


gridsearch2.fit(xtrain_vector, ytrain)


# In[64]:


print("SVM")
print(gridsearch1.best_estimator_)
print(gridsearch1.best_score_)
print("Multinomial NB")
print(gridsearch2.best_estimator_)
print(gridsearch2.best_score_)


# ## Test Model

# In[35]:


pred1=gridsearch1.predict(xval_vector)


# In[59]:


print("Confusion Matrix[SVM]:\n\n",confusion_matrix(yval,pred1))


# ##### Interpretation of Confusion Matrix
# The first row corresponds to ham (0) and second row corresponds to spam (1).
# The first column corresponds to ham and second column corresponds to spam.
# 
# Element at position (0,0) =964, samples that are ham and classified as ham (TN)
# 
# Element at position (0,1) =1, samples that are ham and incorrectly classified as spam (FP)
# 
# Element at position (1,0) =20, samples that are spam and incorrectly classified as ham (FN)
# 
# Element at position (1,1)= 130, samples that are spam and correctly classified as spam (TP)

# In[65]:


pred2=gridsearch2.predict(xval_vector)


# In[75]:


print("Confusion Matrix[Multinomial NB]:\n\n",confusion_matrix(yval,pred2))


# In[74]:


print("Confusion Heatmap of SVM")
plot_confusion_heatmap(yval,pred1)


# In[73]:


print("Confusion Heatmap of Multinomial NB")
plot_confusion_heatmap(yval,pred2)


# In[ ]:




