#!/usr/bin/env python
# coding: utf-8

# In[16]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import matplotlib.pyplot as plt
import numpy as np
import pickle
FP = "../input/tta/TTA/"
print(os.listdir(FP))
FP = FP + "Journals/"
files = os.listdir(FP)


# #### This data is about a boardgame, Through the Ages.
# 
# #### Let us first take a look at what the raw data looks like.

# In[17]:


Journal = pd.read_pickle(FP + files[3])
Journal.tail(10)


# #### Basically, a Journal is a detailed record of what a player did every round. It also includes some "neutral" processes which are the automatic implementation of the game rules. We can see a lot of that at the end of the game.

# In[18]:


Journal.head(10)


# We can see that most of the relevant information are in the "Text" column. 
# 
# I proceeded in 2 separate directions from here.
# 
# ## 1. Manual Parsing:
# Since I actually know how to play this game online, I can understand what the "Text" column really means.
# 
# I can write customized codes to extract (what I consider as) relevant information from there.
# From the 30k+ Journal files I used my customized code to make the following table.

# In[19]:


Techs = pd.read_pickle("../input/TechXYFullAlt")
print(np.shape(Techs))
Techs.head()


# #### Here we get one row per player per Journal (file).
# #### All but the last 5 columns here records whether a player perform a certain action (playing a certain card) during the game.
# #### The "Result" column is the final score as the fraction of the winning score. The rest are some meta-data of the game and participating players. 
# #### The corresponding analysis is not my main point here.  Some of them are presented in my blog and anyone who's interested can just visit there.
# http://spelguy.blogspot.ca/2018/02/a-data-driven-strategy-guide-for_61.html
# (Actually, I might upload another kernel to go through that later..)
# #### Long story short, exploring a few machine learning pipelines, the above data can predict the final outcome of the game up to 70% accuracy, and the skill of the player up to 60% accuracy.  These are validation error, although the in-sample error is almost the same.
# #### Also, after trying a few different ML algorithms, it appears that linear regression already very close to the maximum accuracy.  None of the more nonlinear models and deeper networks I tried can predict the result better, not even in-sample.

# ## 2. Natural Language Processing.
# This is what I want to focus on here.
# 
# The problem of the previous method is that it is tedius. If this were an abstract game like GO, then it would have been straightforward to extract all relevant information from the game.
# 
# Unfortunately, this is a thematic game.  Its rules and mechanisms rely on a lot of human experience to make sense.  Thus, I really need to think harder about the rules, and code harder in order to extract more precise information from the game.  That is a lot of work, and it is not even clear whether such improvement in information will improve the prediction accuracy. (*For example, my previous attempt only includes whether someone plays a card, but it did not distinguish when was that card played.  The required effort to make that happen will be more than what I am going to show next. )*
# 
# On the other hand, for exactly the same reason, the "Text" in the game Journal looks like natural language.  It is not exactly natural language, because it is actually generated by a machine which follows some realization of the game rules.  It won't make too much sense to someone who does not understand the game rules.  However, it does have similar grammer and contextual structure.
# 
# Thus, it is somewhat a fair question to ask a Data Scientist to perform a blind analysis with NLP. 
# 
# Basically, I should try to pretend that I do not know the rules and process these as bunch of words, and see if that's actually easier, or can it give me even better predictions.
# 

# In[20]:


FP = "../input/tta/TTA/NLP/"
summary = pd.read_pickle(FP + "NLP34")
summary.reset_index(drop=True, inplace=True)
d = list(summary.loc[summary["VP"]==0].index) 
# remove all players who resigned since they will have empty "Text" columns later in the game
summary.drop(d, inplace=True)
summary.dropna(inplace=True) # some files were corrupted resuting in empty "Text" columns
print(np.shape(summary))
summary.head()


# #### Here we have a different processed data for the NLP purpose. Every game is divided into 6 phases, and during each phase, everything in the "Text" column from individual game journals are combined into a big string.  I removed all "end game" information, since that directly tells us about the result.
# 
# #### We can try to use NLP on these to see if it can give us better predictions.
# 
# #### In principle, these wall of texts should include the information I manually parsed.  I also deliberately try to make it have a bit more information.  Since now we are dividing the game into 6 phases, it does contain the information of roughly "when" is a particular card played.
# 

# In[21]:


# bringing in some friends :P
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import text
from sklearn.neural_network import MLPClassifier as MLPC
from scipy.sparse import hstack
from sklearn import svm
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.neural_network import BernoulliRBM as RBM
from sklearn.preprocessing import StandardScaler


# In[22]:


def XY(phases):
    X = []
    d = []
    seg =[]
    for phase in phases:
        x = summary[phase].tolist()
        tfidf = text.TfidfVectorizer(input=x, stop_words="english",
                                    max_df=0.5, min_df=0.05)
        x = tfidf.fit_transform(x)
        X += [x]
        d += list(tfidf.vocabulary_.keys())
        seg += [len(list(tfidf.vocabulary_.keys()))]
    X = hstack(X)  # keeping track of the words we kept
    Y = summary["VP"]/summary["Max VP"]
    Y = Y>Y.median()  
    # this is going to be a simple classifier which predicts
    # whether the % of a player score, with respect to the winner,
    # is among top 50% of all data.
    return X, Y, d, seg


# The above function allows me to convert the data into a standard vector for training my classifier. The most important piece here is that **tfidf.**
# 
# There will be a lot of garbages in the full text, since the system uses a lot of words to describe something everyone does.  It is just the formal language of this online interface and the game rules. Everyone "builds" things, everyone "takes" cards. They do not represent any special strategy/action taken by a player. It is "what" they build and play that matters.
# 
# One can of course create a customized list of "stop_words" to exclude those. However, my main purpose here is to avoid using (too much of) my knowledge about the game and the interface. Thus I don't do that.
# 
# Instead, I set a cutoff on "maximum document frequency".  Namely, if some words are present during most of the games for most of the players, they will not be included. 
# 
# There is also a cutoff on "minimum document frequency". Sometimes, a player's get mentioned in the game. There is no reason to take that into account. There is a danger here that we might exclude a very special strategy. That is fine. In such case, it would have been a very rare strategy that we don't have a lot of statistical confidence to judge anyway.

# In[23]:


phases = np.arange(6) # get all 6 phases together.
Xnlp, Ynlp, d, seg = XY(phases)


# In[25]:


trans = StandardScaler()
X = trans.fit_transform(Xnlp.toarray())
# This rescales the data.
# More importantly, it transform a sparse matrix into 
# a normal matrix, so it won't get rejected by something 
# else down the pipeline

# The rest are optional. I commented them out becuase they did not help.
# But feel free to try them. :P

#trans = TruncatedSVD(n_components=500)
#trans = PCA(n_components=30, whiten=True)
#trans = RBM(n_components=100, learning_rate=0.01)
#X = trans.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X, Ynlp, test_size=0.2, random_state=10)

#clf = svm.SVC(kernel='linear', probability=False)
clf = MLPC(hidden_layer_sizes=(1,),  
          # more layers did not help, as far as I could tell.
          activation = "identity",
          alpha = 0.001)
clf.fit(X_train, Y_train)

InScore = clf.score(X_train, Y_train)
OutScore = clf.score(X_test, Y_test)
InScore, OutScore


# In[26]:


coef = clf.coefs_[0]*clf.coefs_[1] # for MLPC
# a MLPC with 1 neuron in 1 hidden layer is basically 
# a linear classicifier. If you use another linear classifier,
# you need to change the above line into the corresponding 
# coefficients, which should have the same shape.
np.shape(coef)


# In[27]:


imp = pd.DataFrame( np.concatenate(( np.swapaxes([d],0,1), 
                                     coef), axis=1), 
                    columns=["word", "weight"] )
phases = sum([ [i]*seg[i] for i in range(6) ], [])
imp["weight"] = imp["weight"].apply(lambda x:float(x))
imp["phase"]=phases


# In[28]:


imp.sort_values(["weight"],ascending=False).head(10)


# Finally, we are looking at the result.  This tells us that the most obvious sign that someone is going to win, is to have the word **culture** appear in his journal frequently during phase 0.
# 
# It is then followed by the word **gain** during phase 4, and **equal** during phase 5.
# 
# Now, we can see that I have **delayed** using my knowledge of the game up to this point, but I cannot keep doing that anymore.  I need to know how the game works, how this interface works, in order to know **what should I do to make "culture" appear in my journal?** 
# 
# #### Comparing this to method 1, where any linear kernel trained can directly tell me what card to play, this is a bit more tortuous. However, it is less work in front, and I do learn a bit more from it. 

# ### One interesting observation is that the NLP does not make significantly better prediction, comparing to my customized parser, despite the fact that it has extra timing information. 
# Since the in-sample and out-sample errors are so close, I suspect that the game does have intrinsic randomness about 30%. Actually, the Journal did not include every detail to reproduce the actual games. So maybe the randomness + hidden infromation is about 30%. Thus, even if we use all information, we should not be able to predict the outcome better than 70%.

# In[ ]:




