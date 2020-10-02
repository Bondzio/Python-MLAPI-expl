#!/usr/bin/env python
# coding: utf-8

# **ABSTRACT**
# 
# Many combination of structures are available for proteins involved in the central processes of life, however it can be a challenge to find the information that we need, since protein data bank archives so many different structures, often with multiple combination of structures for a given molecule, or partial structures, or structures that have been modified from their native form. This paper presents SVM-based algorithm to identify protein structures and compare with a Naive Bayes-based algorithm on a set of protein database from Research Collaboratory for Structural Bioinformatics (RCSB) Protein Data Bank (PDB). Performance was measured for identification scenarios. The classification performance for SVM with one-vs-rest approach is ~94% versus Naive Bayes is ~90%.
# 
# **Keywords**: support vector machine, sequences, pattern recognition, bag of words
# 

# In[ ]:


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Import Datasets
df_seq = pd.read_csv('/kaggle/input/protein-data-set/pdb_data_seq.csv')
df_char = pd.read_csv('/kaggle/input/protein-data-set/pdb_data_no_dups.csv')

print('Datasets have been loaded...')


# In[ ]:


# 2). ----- Filter and Process Dataset ------

# Filter for only proteins
protein_char = df_char[df_char.macromoleculeType == 'Protein']
protein_seq = df_seq[df_seq.macromoleculeType == 'Protein']

# Select only necessary variables to join
protein_char = protein_char[['structureId','classification']]
protein_seq = protein_seq[['structureId','sequence']]
protein_seq.head()


# In[ ]:


protein_char.head()


# In[ ]:


model_f = protein_char.set_index('structureId').join(protein_seq.set_index('structureId'))
model_f.head()


# In[ ]:


print('%d rows in joined dataset' %model_f.shape[0])


# In[ ]:


model_f.isnull().sum()


# In[ ]:


model_f = model_f.dropna()
print('%d rows in updated joined dataset' %model_f.shape[0])


# In[ ]:


counts = model_f.classification.value_counts()
print(counts)


# In[ ]:


types = np.asarray(counts[(counts > 1000)].index)
print(types)


# In[ ]:


#data = model_f[model_f.classification.isin(types)]
data = model_f.loc[(model_f.classification == 'FLUORESCENT PROTEIN') | (model_f.classification == 'BIOSYNTHETIC PROTEIN') | 
                   (model_f.classification == 'CONTRACTILE PROTEIN') | (model_f.classification == 'TRANSLATION') |
                   (model_f.classification == 'METAL TRANSPORT') | (model_f.classification == 'PROTEIN FIBRIL') |
                   (model_f.classification == 'MOTOR PROTEIN') | (model_f.classification == 'MEMBRANE PROTEIN')]
print('%d filtered dataset' %data.shape[0])


# In[ ]:


# Split Data
X_train, X_test,y_train,y_test = train_test_split(data['sequence'], data['classification'], test_size = 0.2, random_state = 1)


# In[ ]:


# Exploring CountTokenizer

# list of text documents
text = ["The quick brown fox jumped over the lazy dog."]
# create the transform
vectorizer = CountVectorizer()
# tokenize and build vocab
vectorizer.fit(text)
# summarize
print(vectorizer.vocabulary_)
# encode document
vector = vectorizer.transform(text)
# summarize encoded vector
print(vector.shape)
print(type(vector))
print(vector.toarray())


# In[ ]:


vect = CountVectorizer(analyzer = 'char_wb', ngram_range = (4,4))


# In[ ]:


# Fit and Transform CountVectorizer
vect.fit(X_train)
X_train_df = vect.transform(X_train)
X_test_df = vect.transform(X_test)


# In[ ]:


print(vect.vocabulary_)
print(X_train_df.shape)
print(type(X_train_df))
print(X_train_df.toarray())


# In[ ]:


print(vect.get_feature_names()[-20:])


# In[ ]:


prediction = dict()

# Naive Bayes Model
from sklearn.naive_bayes import MultinomialNB
model = MultinomialNB()
model.fit(X_train_df, y_train)
NB_pred = model.predict(X_test_df)
prediction["MultinomialNB"] = accuracy_score(NB_pred, y_test)
print( prediction['MultinomialNB'])


# In[ ]:


print(classification_report(y_test,NB_pred))


# In[ ]:


from sklearn import svm
clf_svc = svm.SVC(gamma=0.001, C=100) # experiment with one-vs-one
clf_svc.fit(X_train_df, y_train)
NB_pred = clf_svc.predict(X_test_df)

print(classification_report(y_test,NB_pred))
prediction["SVM_SVC"] = accuracy_score(y_test,NB_pred)
print( prediction['SVM_SVC'])


# In[ ]:


clf = svm.LinearSVC(random_state=1, C=100) # experiment with one-vs-rest
clf.fit(X_train_df, y_train)
NB_pred = clf.predict(X_test_df)

print(classification_report(y_test,NB_pred))
prediction["SVM_LINEARSVC"] = accuracy_score(y_test,NB_pred)
print(prediction['SVM_LINEARSVC'])


# In[ ]:


# test prediction

a = ['MHIPEGYLSPQTCAVMGAAMVPVLTVAAKKVNKSFDKKDVPAMAIGSAFAFTIMMFNVPIPGGTTAHAIGATLLATTLGPWAASISLTLALFIQALLFGDGGILALGANSFNMAFIAPFVGYGIYRLMLSLKLNKVLSSAIGGYVGINAAALATAIELGLQPLLFHTANGTPLYFPYGLNVAIPAMMFAHLTVAGIVEAVITGLVVYYLLEHHHHHH']

print('predicted : ', clf.predict(vect.transform(a)))

print('training data : ', model_f.loc[model_f.sequence=='MHIPEGYLSPQTCAVMGAAMVPVLTVAAKKVNKSFDKKDVPAMAIGSAFAFTIMMFNVPIPGGTTAHAIGATLLATTLGPWAASISLTLALFIQALLFGDGGILALGANSFNMAFIAPFVGYGIYRLMLSLKLNKVLSSAIGGYVGINAAALATAIELGLQPLLFHTANGTPLYFPYGLNVAIPAMMFAHLTVAGIVEAVITGLVVYYLLEHHHHHH'])


# In[ ]:


from sklearn.model_selection import cross_val_score

scores = cross_val_score(clf, X_train_df, y_train, cv=5)


# In[ ]:


print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


# In[ ]:


scores


# In[ ]:


from sklearn.model_selection import cross_val_score

scores = cross_val_score(clf_svc, X_train_df, y_train, cv=5)

print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

print(scores)


# In[ ]:


scores = cross_val_score(model, X_train_df, y_train, cv=5)


# In[ ]:


print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


# In[ ]:


scores


# In[ ]:




