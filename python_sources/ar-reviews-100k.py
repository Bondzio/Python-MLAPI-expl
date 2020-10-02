#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Please see the dataset description for additional info 
# current accuracy (balanced): see last run (this is the AraBERT implementation using ktran)


# In[ ]:


import time 
print(f'Started: {time.ctime()}')


# In[ ]:


get_ipython().system('pip install -U pip')
get_ipython().system('pip install "tensorflow_gpu>=2.0.0"  # cpu: pip3 install "tensorflo')
get_ipython().system('pip install transformers==2.5.1')
get_ipython().system('pip install ktrain ')


# In[ ]:


# restart run time
#import os
#def restart_runtime():
#  os.kill(os.getpid(), 9)
#restart_runtime()


# In[ ]:


# forked versions of eli5 and stellargraph (required by ktrain)
get_ipython().system('pip install git+https://github.com/amaiya/eli5@tfkeras_0_10_1 ')
get_ipython().system('pip install git+https://github.com/amaiya/stellargraph@no_tf_dep_082')


# In[ ]:


import pandas as pd
pd.set_option('display.max_colwidth',200)
pd.set_option('display.max_rows',50)
df = pd.read_csv('/kaggle/input/arabic-100k-reviews/ar_reviews_100k.tsv',sep='\t')
df['label'].value_counts()


# In[ ]:


df = df.sample(frac=1).reset_index(drop=True)
df.head()


# In[ ]:


class_names=['Mixed', 'Negative', 'Positive']
df['label'] = df['label'].apply(lambda x: class_names.index(x))
print(len(df), '\n')
df.head()


# In[ ]:


df_test = df.sample(frac=0.15, random_state=42)
df_train = df.drop(df_test.index)
len(df_train), len(df_test)


# In[ ]:


x_train = df_train['text'].tolist()
y_train = df_train['label'].to_numpy()
x_test = df_test['text'].tolist()
y_test = df_test['label'].to_numpy()


# In[ ]:


import ktrain
from ktrain import text 
MODEL_NAME = 'aubmindlab/bert-base-arabertv01'
t = text.Transformer(MODEL_NAME, maxlen=400, class_names=class_names)

trn = t.preprocess_train(x_train, y_train)
val = t.preprocess_test(x_test, y_test)
model = t.get_classifier()
learner = ktrain.get_learner(model, train_data=trn, val_data=val, batch_size=6)


# In[ ]:


# takes long time
#learner.lr_find(show_plot=True, max_epochs=2)


# In[ ]:


learner.autofit(1e-6, 3)


# In[ ]:


learner.validate(class_names=t.get_classes())


# In[ ]:


print(learner.view_top_losses(n=5, preproc=t))


# In[ ]:


#n = ?? # from above
#print(x_test[n])


# In[ ]:


#test_text = '' # enter a review - ex. for printed above
#predictor = ktrain.get_predictor(learner.model, preproc=t)
#predictor.predict(test_text)


# In[ ]:


#predictor.explain(test_text)


# In[ ]:


print(f'Finished: {time.ctime()}')

