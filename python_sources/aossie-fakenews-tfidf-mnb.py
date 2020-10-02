#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm


# In[ ]:


trainFile=pd.read_csv('../input/train_merged.csv',encoding='latin-1')
testFile=pd.read_csv('../input/test_merged.csv', encoding='latin-1')


# In[ ]:


totaldata= trainFile['articleBody'].tolist() + trainFile['Headline'].tolist()+testFile['articleBody'].tolist()+testFile['Headline'].tolist()


# In[ ]:


tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', max_features=80, stop_words='english')


# In[ ]:


tfidf_vect.fit(totaldata)


# In[ ]:





# In[ ]:


train_head_vec= tfidf_vect.transform(trainFile['Headline'])
train_body_vec= tfidf_vect.transform(trainFile['articleBody'])
test_head_vec= tfidf_vect.transform(testFile['Headline'])
test_body_vec= tfidf_vect.transform(testFile['articleBody'])


# In[ ]:


# run and tested
import os
import re
import nltk
import numpy as np
from sklearn import feature_extraction
from tqdm import tqdm


_wnl = nltk.WordNetLemmatizer()


def normalize_word(w):
    return _wnl.lemmatize(w).lower()


def get_tokenized_lemmas(s):
    return [normalize_word(t) for t in nltk.word_tokenize(s)]


def clean(s):
    # Cleans a string: Lowercasing, trimming, removing non-alphanumeric

    return " ".join(re.findall(r'\w+', s, flags=re.UNICODE)).lower()


def remove_stopwords(l):
    # Removes stopwords from a list of tokens
    return [w for w in l if w not in feature_extraction.text.ENGLISH_STOP_WORDS]


def gen_or_load_feats(feat_fn, headlines, bodies, feature_file):
    if not os.path.isfile(feature_file):
        feats = feat_fn(headlines, bodies)
        np.save(feature_file, feats)

    return np.load(feature_file)




def word_overlap_features(features, headline, body):
    # common word/ total word
    clean_headline = clean(headline)
    clean_body = clean(body)
    clean_headline = get_tokenized_lemmas(clean_headline)
    clean_body = get_tokenized_lemmas(clean_body)
    feature = len(set(clean_headline).intersection(clean_body)) / float(len(set(clean_headline).union(clean_body)))
    features.append(feature)
    return features




def ngrams(input, n):
    input = input.split(' ')
    output = []
    for i in range(len(input) - n + 1):
        output.append(input[i:i + n])
    return output


def chargrams(input, n):
    output = []
    for i in range(len(input) - n + 1):
        output.append(input[i:i + n])
    return output


def append_chargrams(features, text_headline, text_body, size):
    grams = [' '.join(x) for x in chargrams(" ".join(remove_stopwords(text_headline.split())), size)]
    grams_hits = 0
    grams_early_hits = 0
    grams_first_hits = 0
    for gram in grams:
        if gram in text_body:
            grams_hits += 1
        if gram in text_body[:255]:
            grams_early_hits += 1
        if gram in text_body[:100]:
            grams_first_hits += 1
    features.append(grams_hits)
    features.append(grams_early_hits)
    features.append(grams_first_hits)
    return features


def append_ngrams(features, text_headline, text_body, size):
    grams = [' '.join(x) for x in ngrams(text_headline, size)]
    grams_hits = 0
    grams_early_hits = 0
    for gram in grams:
        if gram in text_body:
            grams_hits += 1
        if gram in text_body[:255]:
            grams_early_hits += 1
    features.append(grams_hits)
    features.append(grams_early_hits)
    return features


def hand_features(headlines, bodies):
    def binary_co_occurence(headline, body):
        # Count how many times a token in the title
        # appears in the body text.
        bin_count = 0
        bin_count_early = 0
        for headline_token in clean(headline).split(" "):
            if headline_token in clean(body):
                bin_count += 1
            if headline_token in clean(body)[:255]:
                bin_count_early += 1
        return [bin_count, bin_count_early]

    def binary_co_occurence_stops(headline, body):
        # Count how many times a token in the title
        # appears in the body text. Stopwords in the title
        # are ignored.
        bin_count = 0
        bin_count_early = 0
        for headline_token in remove_stopwords(clean(headline).split(" ")):
            if headline_token in clean(body):
                bin_count += 1
                bin_count_early += 1
        return [bin_count, bin_count_early]

    def count_grams(headline, body):
        # Count how many times an n-gram of the title
        # appears in the entire body, and intro paragraph

        clean_body = clean(body)
        clean_headline = clean(headline)
        features = []
        features = append_chargrams(features, clean_headline, clean_body, 2)
        features = append_chargrams(features, clean_headline, clean_body, 8)
        features = append_chargrams(features, clean_headline, clean_body, 4)
        features = append_chargrams(features, clean_headline, clean_body, 16)
        features = append_ngrams(features, clean_headline, clean_body, 2)
        features = append_ngrams(features, clean_headline, clean_body, 3)
        features = append_ngrams(features, clean_headline, clean_body, 4)
        features = append_ngrams(features, clean_headline, clean_body, 5)
        features = append_ngrams(features, clean_headline, clean_body, 6)
        return features

    def other_feature(headline, body):
        features=[]
        features= word_overlap_features(features, headline, body)
        return features
    X = []
    for i, (headline, body) in tqdm(enumerate(zip(headlines, bodies))):
        lst= binary_co_occurence(headline, body) + binary_co_occurence_stops(headline, body) + count_grams(headline, body)+ other_feature(headline, body)
        X.append(lst)


    X =np.array(X)
    return X


# In[ ]:


train_handF= hand_features(trainFile['Headline'].tolist(), trainFile['articleBody'].tolist())
test_handF=hand_features(testFile['Headline'].tolist(), testFile['articleBody'].tolist())


# In[ ]:


from scipy.sparse import  hstack


# In[ ]:


train_final= hstack([train_head_vec,train_body_vec]).toarray()


# In[ ]:


test_final= hstack([test_head_vec,test_body_vec]).toarray()


# In[ ]:


train_final =np.concatenate((train_final,train_handF), axis=1)
test_final =np.concatenate((test_final,test_handF), axis=1)


# In[ ]:


print(type(train_final), train_final.shape, test_final.shape)


# In[ ]:


trainFile.head()


# In[ ]:


train_labels= trainFile['Stance'].copy()
test_labels= testFile['Stance'].copy()


# In[ ]:


from sklearn.metrics import accuracy_score


from sklearn.naive_bayes import MultinomialNB

mnb = MultinomialNB(alpha=0.34)
mnb.fit(train_final, train_labels)


# In[ ]:


#testing naive bayes
prediction = mnb.predict(test_final)
accuracy_score(test_labels,prediction)


# In[ ]:


np.unique(prediction)


# In[ ]:


from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
import matplotlib.pyplot as plt


# In[ ]:


matrix1 = confusion_matrix(test_labels, prediction)


# In[ ]:


matrix1


# In[ ]:


def plot_confusion_matrix(cm,
                          target_names,
                          title='Confusion matrix',
                          cmap=None,
                          normalize=True):
    """
    given a sklearn confusion matrix (cm), make a nice plot

    Arguments
    ---------
    cm:           confusion matrix from sklearn.metrics.confusion_matrix

    target_names: given classification classes such as [0, 1, 2]
                  the class names, for example: ['high', 'medium', 'low']

    title:        the text to display at the top of the matrix

    cmap:         the gradient of the values displayed from matplotlib.pyplot.cm
                  see http://matplotlib.org/examples/color/colormaps_reference.html
                  plt.get_cmap('jet') or plt.cm.Blues

    normalize:    If False, plot the raw numbers
                  If True, plot the proportions

    Usage
    -----
    plot_confusion_matrix(cm           = cm,                  # confusion matrix created by
                                                              # sklearn.metrics.confusion_matrix
                          normalize    = True,                # show proportions
                          target_names = y_labels_vals,       # list of names of the classes
                          title        = best_estimator_name) # title of graph

    Citiation
    ---------
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

    """
    import matplotlib.pyplot as plt
    import numpy as np
    import itertools

    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")


    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.show()


# In[ ]:


plot_confusion_matrix(cm=matrix1,target_names=['agree', 'disagree', 'discuss', 'unrelated'])


# In[ ]:





# In[ ]:





# In[ ]:


trainFile['Stance'].value_counts()


# In[ ]:


testFile['Stance'].value_counts()

