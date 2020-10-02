#!/usr/bin/env python
# coding: utf-8

# # NLP for detect fake news using PySpark

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


get_ipython().system('pip install pyspark')


# In[ ]:


import pandas as pd
from pyspark import SparkContext
from pyspark.sql import SparkSession, SQLContext

sc= SparkContext(master= 'local', appName= 'Fake and real news')
ss= SparkSession(sc)


# ## 1. Read data set  
# Reading data using the SparkSession.read.csv method causes structural errors for the data file. So read the data using pandas.read_csv method and convert to Spark Dataframe.
# 

# In[ ]:


# Funtion for conver Pandas Dataframe to Spark Dataframe
from pyspark.sql.types import StringType, StructField, StructType
def read_data(path):
  schema= StructType(
      [StructField('title',StringType(),True),
      StructField('text',StringType(),True),
      StructField('subject',StringType(),True),
      StructField('date',StringType(),True)])
  pd_df= pd.read_csv(path)
  sp_df= ss.createDataFrame(pd_df, schema= schema)
  return sp_df


# In[ ]:


# Read data set
path_true= '/kaggle/input/fake-and-real-news-dataset/True.csv'
path_fake= '/kaggle/input/fake-and-real-news-dataset/Fake.csv'
true_df= read_data(path_true)
fake_df= read_data(path_fake)


# ## 2. Check the data set

# In[ ]:


# Number of news true
true_df.count()


# In[ ]:


# Number of news fake
fake_df.count()


# In[ ]:


# Concatenate 2 data sets into one and shuffle data set
from pyspark.sql.functions import lit, rand
data= true_df.withColumn('fake', lit(0)).union(fake_df.withColumn('fake', lit(1))).orderBy(rand())


# In[ ]:


# Check again
data.groupBy('fake').count().show()


# In[ ]:


# Check the values of the subject column
data.select('subject').distinct().show()


# In[ ]:


data.show(5)


# ## 3. Create objects for processing data

# In[ ]:


from pyspark.ml.feature import SQLTransformer, RegexTokenizer, StopWordsRemover, CountVectorizer, Imputer, IDF
from pyspark.ml.feature import StringIndexer, VectorAssembler
StopWordsRemover.loadDefaultStopWords('english')

# 0. Extract tokens from title
title_tokenizer= RegexTokenizer(inputCol= 'title', outputCol= 'title_words',
                                pattern= '\\W', toLowercase= True)
# 1. Remove stop words from title
title_sw_remover= StopWordsRemover(inputCol= 'title_words', outputCol= 'title_sw_removed')
# 2. Compute Term frequency from title
title_count_vectorizer= CountVectorizer(inputCol= 'title_sw_removed', outputCol= 'tf_title')
# 3. Compute Term frequency-inverse document frequency from title
title_tfidf= IDF(inputCol= 'tf_title', outputCol= 'tf_idf_title')
# 4. Extract tokens from text
text_tokenizer= RegexTokenizer(inputCol= 'text', outputCol= 'text_words',
                                pattern= '\\W', toLowercase= True)
# 5. Remove stop words from text
text_sw_remover= StopWordsRemover(inputCol= 'text_words', outputCol= 'text_sw_removed')
# 6. Compute Term frequency from text
text_count_vectorizer= CountVectorizer(inputCol= 'text_sw_removed', outputCol= 'tf_text')
# 7. Compute Term frequency-inverse document frequency text
text_tfidf= IDF(inputCol= 'tf_text', outputCol= 'tf_idf_text')
# 8. StringIndexer subject
subject_str_indexer= StringIndexer(inputCol= 'subject', outputCol= 'subject_idx')
# 9. VectorAssembler
vec_assembler= VectorAssembler(inputCols=['tf_idf_title', 'tf_idf_text', 'subject_idx'], outputCol= 'features')


# ## 4. Create object for Random Forest Classifier model

# In[ ]:


from pyspark.ml.classification import RandomForestClassifier
# 10 Random Forest Classifier
rf= RandomForestClassifier(featuresCol= 'features', labelCol= 'fake', predictionCol= 'fake_predict', maxDepth= 7, numTrees= 20)


# ## 5. Create Pipeline for processing and fitting data to model

# In[ ]:


from pyspark.ml import Pipeline
rf_pipe= Pipeline(stages=[title_tokenizer, # 0
                title_sw_remover, # 1
                title_count_vectorizer, # 2
                title_tfidf, # 3
                text_tokenizer, # 4
                text_sw_remover, # 5
                text_count_vectorizer, # 6
                text_tfidf, # 7
                subject_str_indexer, # 8
                vec_assembler, # 9
                rf]) # 10 model


# ## 6. Splitting the dataset into the training set and test set

# In[ ]:


train, test= data.randomSplit([0.8, 0.2])


# ## 7. Fitting model

# In[ ]:


rf_model= rf_pipe.fit(train)


# ## 8. Evaluate classification model

# In[ ]:


# Function for evaluating classification model
from pyspark.ml.evaluation import  MulticlassClassificationEvaluator, BinaryClassificationEvaluator

accuracy= MulticlassClassificationEvaluator(labelCol= 'fake', predictionCol= 'fake_predict', metricName= 'accuracy')
f1= MulticlassClassificationEvaluator(labelCol= 'fake', predictionCol= 'fake_predict', metricName= 'f1')
areaUnderROC= BinaryClassificationEvaluator(labelCol= 'fake', metricName= 'areaUnderROC')

def classification_evaluator(data_result):
    data_result.crosstab(col1= 'fake_predict', col2= 'fake').show()
    print('accuracy:' ,accuracy.evaluate(data_result))
    print('f1:' ,f1.evaluate(data_result))
    print('areaUnderROC:' ,areaUnderROC.evaluate(data_result))


# ### 8.1 Evaluation of final model fit on the training data set

# In[ ]:


# Predict on training data set
rf_train_result= rf_model.transform(train)


# In[ ]:


classification_evaluator(rf_train_result)


# ### 8.2 evaluation of final model fit on the test data set

# In[ ]:


# Predict on test data set
rf_test_result= rf_model.transform(test)


# In[ ]:


classification_evaluator(rf_test_result)

