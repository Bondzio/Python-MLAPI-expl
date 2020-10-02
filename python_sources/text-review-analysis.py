#!/usr/bin/env python
# coding: utf-8

# The Amazon text reviews given by the users are considered word by word and text reviews are cleaned by using Stop words and removed unwanted HTML tags. Once time stamp is assigned, then our objective is to determine whether the review is positive or negative.We will classify the reviews by using Bag of Words and TFIDF(Term frequency and inverse document frequency), and classification algorithm called K Nearest Neighbors where the review would be chosen on the nearest distances based on the majority voting. The results are explained with the help of a confusion matrix and classification report for both the cases.
# 

# # Introduction

# In[ ]:


import pandas as pd
sample=pd.read_csv("../input/samplereviews.csv")


# In[ ]:


print(sample.shape)


# In[ ]:


#look of the dataset
sample.head()


#  # Data Cleaning

# In[ ]:





# In[ ]:


def partition(x):
    if x < 3:
        return 'negative'
    return 'positive'

#changing reviews with score less than 3 to be positive
actualScore = sample['Score']
positiveNegative = actualScore.map(partition) 
sample['Score'] = positiveNegative


# In[ ]:


sample.head()


# In[ ]:


# no of positive and negative reviews
sample["Score"].value_counts()


# In[ ]:


#dropping  the duplicates column if any
sorted_data=sample.sort_values('ProductId', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')
final=sorted_data.drop_duplicates(subset={"UserId","ProfileName","Time","Text"}, keep='first', inplace=False)
final.shape


# In[ ]:


# no duplicate columns found
(final['Id'].size*1.0)/(sample['Id'].size*1.0)*100


# In[ ]:


final=final[final.HelpfulnessNumerator<=final.HelpfulnessDenominator]
# Help..Num is always less than Denom.. as Denom is people who upvote and donwvote
#Before starting the next phase of preprocessing lets see the number of entries left
print(final.shape)

#How many positive and negative reviews are present in our dataset?
final['Score'].value_counts()


# # Text Processing

# In[ ]:


# find sentences containing HTML tags
import re
i=0;
for sent in final['Text'].values:
    if (len(re.findall('<.*?>', sent))):
        print(i)
        print(sent)
        break;
    i += 1;


# In[ ]:


import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
sno = nltk.stem.SnowballStemmer('english') #initialising the snowball stemmer
stop=set(stopwords.words('english'))


def cleanhtml(sentence): #function to clean the word of any html-tags
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', sentence)
    return cleantext
def cleanpunc(sentence): #function to clean the word of any punctuation or special characters
    cleaned = re.sub(r'[?|!|\'|"|#]',r'',sentence)
    cleaned = re.sub(r'[.|,|)|(|\|/]',r' ',cleaned)
    return  cleaned
print(stop)
print('************************************')
print(sno.stem('tasty'))


# In[ ]:


i=0
str1=' '
final_string=[]
all_positive_words=[] # store words from +ve reviews here
all_negative_words=[] # store words from -ve reviews here.
s=''
for sent in final['Text'].values:
    filtered_sentence=[]
    #print(sent);
    sent=cleanhtml(sent) # remove HTMl tags
    for w in sent.split():
        for cleaned_words in cleanpunc(w).split():
            if((cleaned_words.isalpha()) & (len(cleaned_words)>2)):    
                if(cleaned_words.lower() not in stop):
                    s=(sno.stem(cleaned_words.lower())).encode('utf8')
                    filtered_sentence.append(s)
                    if (final['Score'].values)[i] == 'positive': 
                        all_positive_words.append(s) #list of all words used to describe positive reviews
                    if(final['Score'].values)[i] == 'negative':
                        all_negative_words.append(s) #list of all words used to describe negative reviews reviews
                else:
                    continue
            else:
                continue 
    #print(filtered_sentence)
    str1 = b" ".join(filtered_sentence) #final string of cleaned words
    #print("***********************************************************************")
    
    final_string.append(str1)
    i+=1


# In[ ]:


final['CleanedText']=final_string #adding a column of CleanedText which displays the data after pre-processing of the review 
final['CleanedText']=final['CleanedText'].str.decode("utf-8")


# In[ ]:


final.shape


# In[ ]:


final.head(3) #below the processed review can be seen in the CleanedText Column 


# We have to convert the positive and negative which is in numerical to categorical variables which we will use for classifying based on the text. For a set of 10,000 rows, we have 8514 reviews are positive, and 1486 are negative reviews.
# After dropping the duplicates from the 10,000 rows, we have 9803 rows left with a percentage of data retrieval of 98.03 %. The final positive and negative reviews are present in our dataset are 8346 and 1457 respectively.
# The data also contains HTML tags in few reviews and remove all the stop words in reviews which we have clean before working on the model. After cleaning all the text review data is processed and placed in the cleaned text column. 
# 

# # Feature Engineering and Classification

# ### Bag Of words

# In[ ]:


data_pos = final[final["Score"] == "positive"]
data_neg = final[final["Score"] == "negative"]
final = pd.concat([data_pos, data_neg])
score =final["Score"]
final.head()


# In[ ]:


final["Time"] = pd.to_datetime(final["Time"], unit = "s")
final= final.sort_values(by = "Time")
final.head()


# In[ ]:


# entire reviews are stored in X
X = final["CleanedText"]
print("shape of X:", X.shape)
X.shape


# In[ ]:


# Corresponding class labels positive and negative are stores in y
y = final["Score"]
print("shape of y:", y.shape)


# In[ ]:


# split data into train and test where 70% data used to train model and 30% for test
# final[:int(len(final) * 0.75)], final[int(len(final) * 0.75):]
from sklearn.model_selection import train_test_split
X_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
print(X_train.shape, y_train.shape, x_test.shape)


# In[ ]:


# Train Vectorizor using BOW
from sklearn.feature_extraction.text import CountVectorizer 

bow = CountVectorizer()
X_train = bow.fit_transform(X_train)
X_train


# In[ ]:


X_train.shape


# In[ ]:


# Test Vectorizor using BOW
x_test = bow.transform(x_test)
x_test


# In[ ]:


x_test.shape


# In[ ]:


# Fuction to compute k value
def k_classifier_brute(X_train, y_train):
    # creating odd list of K for KNN and note even is not selected as we face problems in majority vote
    myList = list(range(0,50))
    neighbors = list(filter(lambda x: x % 2 != 0, myList))

    # empty list that will hold cv scores
    cv_scores = []

    # perform 10-fold cross validation
    for k in neighbors:
        knn = KNeighborsClassifier(n_neighbors=k, algorithm = "brute")
        scores = cross_val_score(knn, X_train, y_train, cv=10, scoring='accuracy')
        cv_scores.append(scores.mean())

    # changing to misclassification error
    MSE = [1 - x for x in cv_scores]
    
     # determining best k
    optimal_k = neighbors[MSE.index(min(MSE))]
    print('\nThe optimal number of neighbors is %d.' % optimal_k)
    
    plt.figure(figsize=(10,6))
    plt.plot(list(filter(lambda x: x % 2 != 0, myList)),MSE,color='red', linestyle='dashed', marker='o',
             markerfacecolor='black', markersize=10)

   
    plt.title("Misclassification Error vs K")
    plt.xlabel('Number of Neighbors K')
    plt.ylabel('Misclassification Error')
    plt.show()

    print("the misclassification error for each k value is : ", np.round(MSE,3))
    return optimal_k


# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
#from sklearn.model_selection import cross_val_score
from sklearn.cross_validation import cross_val_score
from collections import Counter
from sklearn.metrics import accuracy_score
from sklearn import model_selection
from sklearn import cross_validation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
optimal_k_bow = k_classifier_brute(X_train, y_train)
optimal_k_bow


# In[ ]:


# instantiate learning model k = optimal_k
knn_optimal = KNeighborsClassifier(n_neighbors=optimal_k_bow)

# fitting the model
knn_optimal.fit(X_train, y_train)
#knn_optimal.fit(bow_data, y_train)

# predict the response
pred = knn_optimal.predict(x_test)


# In[ ]:


# Accuracy of train data
train_acc_bow = knn_optimal.score(X_train, y_train)
print("Train accuracy is ", train_acc_bow)


# In[ ]:


# Error on train data
train_err_bow = 1-train_acc_bow
print("Train Error %f%%" % (train_err_bow))


# In[ ]:


# evaluate accuracy on test data
acc_bow = accuracy_score(y_test, pred) * 100
print('\nThe accuracy of the knn classifier for k = %d is %f%%' % (optimal_k_bow, acc_bow))


# In[ ]:


# Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, pred)
cm


# In[ ]:


# plot confusion matrix to describe the performance of classifier.
import seaborn as sns
class_label = ["negative", "positive"]
df_cm = pd.DataFrame(cm, index = class_label, columns = class_label)
sns.heatmap(df_cm, annot = True, fmt = "d")
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")
plt.show()


# In[ ]:


# To show main classification report
from sklearn.metrics import classification_report
print(classification_report(y_test, pred))


# Accuracy on the training data is 85.4%, and Accuracy on the test data based on the nine neighbors is 86%.  We should not conclude the performance only based on the accuracy as it does not tell us how much accurately it is predicting individual class labels. In this case, we have used confusion matrix to interpret the performance of the classifier.
# True Positive: 2525 predicted as positive reviews, and they are positive
# True Negative: 7 predicted as negative reviews and they are negative
# False Positive: 402 predicted as positive reviews and they are negative
# False Negative: 7 predicted as negative reviews and they are positive
# True Positive rate: 2525/2532=99.7%
# True Negative rate:7/409=1.7%
# False Positive rate: 402/409=98.3%
# False Negative rate: 7/2532=0.3%
# 

# ### TFIDF

# In[ ]:


# Split data
X_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
print(X_train.shape, x_test.shape, y_train.shape, y_test.shape)


# In[ ]:


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.metrics import roc_curve, auc
#tfidf = TfidfVectorizer()
#tfidf_data = tfidf.fit_transform(final["CleanedText"])
#tfidf_data
tf_idf_vect = TfidfVectorizer(ngram_range=(1,2))
X_train = tf_idf_vect.fit_transform(X_train)
X_train


# In[ ]:


# Convert test text data to its vectorizor
x_test = tf_idf_vect.transform(x_test)
x_test.shape


# In[ ]:


# To choosing optimal_k

optimal_k_tfidf = k_classifier_brute(X_train, y_train)
optimal_k_tfidf


# In[ ]:


# instantiate learning model k = optimal_k
knn_optimal = KNeighborsClassifier(n_neighbors=optimal_k_tfidf)

# fitting the model
knn_optimal.fit(X_train, y_train)
#knn_optimal.fit(bow_data, y_train)
    
# predict the response
pred = knn_optimal.predict(x_test)


# In[ ]:


# Accuracy on train data
train_acc_tfidf = knn_optimal.score(X_train, y_train)
print("Train accuracy", train_acc_tfidf)


# In[ ]:


# Error on train data
train_err_tfidf = 1-train_acc_tfidf
print("Train Error %f%%" % (train_err_tfidf))


# In[ ]:


#evaluate accuracy
acc_tfidf = accuracy_score(y_test, pred) * 100
print('\nThe accuracy of the knn classifier for k = %d is %f%%' % (optimal_k_tfidf, acc_tfidf))


# In[ ]:


#from sklearn.matrics import confusion_matrix
cm = confusion_matrix(y_test, pred)
cm


# In[ ]:


class_label = ["negative", "positive"]
df_cm = pd.DataFrame(cm, index = class_label, columns = class_label)
sns.heatmap(df_cm, annot = True, fmt = "d")
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.show()


# In[ ]:


from sklearn.metrics import classification_report
print(classification_report(y_test, pred))


# the optimal number of k, i.e. 13 neighbors with classification error 0.144 . Accuracy on the training data is 86.1%, and Accuracy on the test data based on the 13 neighbors is 86.9%. We have used confusion matrix (Exhibit 4.5.2) to interpret the performance of the classifier.
# True Positive: 2525 predicted as positive reviews, and actually they are positive
# True Negative: 32 predicted as negative reviews, and actually they are negative
# False Positive: 377 predicted as positive reviews and actually they are negative
# False Negative: 7 predicted as negative reviews and actually they are positive
# True Positive rate: 2525/2532=99.7%
# True Negative rate:32/409=1.7%
# False Positive rate: 377/409=98.3%
# False Negative rate: 7/2532=0.3%
# 
