#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import gensim
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression

import warnings
warnings.filterwarnings('ignore')

print(os.listdir("../input"))
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


data = pd.read_json('../input/train.json')
test = pd.read_json('../input/test.json')


# In[ ]:


print('Training data shape: {}'.format(data.shape))
print('Test data shape: {}'.format(test.shape))


# In[ ]:


# Target variable 
target = data.cuisine


# In[ ]:


data['ingredient_count'] = data.ingredients.apply(lambda x: len(x))


# In[ ]:


def flatten_lists(lst):
    """Remove nested lists."""
    return [item for sublist in lst for item in sublist]


# In[ ]:


f = plt.figure(figsize=(14,8))
gs = gridspec.GridSpec(2, 2)

ax1 = plt.subplot(gs[0, :])
data.ingredient_count.value_counts().hist(ax=ax1)
ax1.set_title('Recipe richness', fontsize=12)

ax2 = plt.subplot(gs[1, 0])
pd.Series(flatten_lists(list(data['ingredients']))).value_counts()[:20].plot(kind='barh', ax=ax2)
ax2.set_title('Most popular ingredients', fontsize=12)

ax3 = plt.subplot(gs[1, 1])
data.groupby('cuisine').mean()['ingredient_count'].sort_values(ascending=False).plot(kind='barh', ax=ax3)
ax3.set_title('Average number of ingredients in cuisines', fontsize=12)

plt.show()


# In[ ]:


# Feed a word2vec with the ingredients
w2v = gensim.models.Word2Vec(list(data.ingredients), size=350, window=10, min_count=2, iter=20)


# Let's try some examples

# In[ ]:


w2v.most_similar(['meat'])


# In[ ]:


w2v.most_similar(['chicken'])


# In[ ]:


def document_vector(doc):
    """Create document vectors by averaging word vectors. Remove out-of-vocabulary words."""
    doc = [word for word in doc if word in w2v.wv.vocab]
    return np.mean(w2v[doc], axis=0)


# In[ ]:


data['doc_vector'] = data.ingredients.apply(document_vector)
test['doc_vector'] = test.ingredients.apply(document_vector)


# In[ ]:


lb = LabelEncoder()
y = lb.fit_transform(target)


# In[ ]:


X = list(data['doc_vector'])
X_test = list(test['doc_vector'])


# In[ ]:


clf = LogisticRegression(C=100)


# In[ ]:


clf.fit(X, y)


# In[ ]:


y_test = clf.predict(X_test)
y_pred = lb.inverse_transform(y_test)


# In[ ]:


test_id = [id_ for id_ in test.id]
sub = pd.DataFrame({'id': test_id, 'cuisine': y_pred}, columns=['id', 'cuisine'])
sub.to_csv('clf_output.csv', index=False)


# In[ ]:




