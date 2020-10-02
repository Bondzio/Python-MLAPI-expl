#!/usr/bin/env python
# coding: utf-8

# # Acknowledgements

# The model in this notebook is entirely based on the Roberta CNN notebook by [Wei Hao Khoong](https://www.kaggle.com/khoongweihao) : for more information, see his original work [here](https://www.kaggle.com/khoongweihao/tse2020-roberta-cnn-random-seed-distribution). I thank him very much for his ready-to-use, well performing model. My add-on here is the data augmentation part.

# ## You can find the enlarged train database (x6) here : 
# ### https://www.kaggle.com/louise2001/extended-train-for-tweet

# # Please upvote this notebook and the corresponding dataset if they helped you or gave you new ideas !

# # Parametrization

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow.keras.backend as K
from sklearn.model_selection import StratifiedKFold
from transformers import *
import tokenizers
import math
from copy import deepcopy as dc
import gc
print('TF version',tf.__version__)


# In[ ]:


MAX_LEN = 96
PATH = '../input/tf-roberta/'
tokenizer = tokenizers.ByteLevelBPETokenizer(
    vocab_file=PATH+'vocab-roberta-base.json', 
    merges_file=PATH+'merges-roberta-base.txt', 
    lowercase=True,
    add_prefix_space=True
)
EPOCHS = 1 # originally 3
BATCH_SIZE = 32 # originally 32
PAD_ID = 1
SEED = 88888
LABEL_SMOOTHING = 0.1
tf.random.set_seed(SEED)
np.random.seed(SEED)
sentiment_id = {'positive': 1313, 'neutral': 7974, 'negative': 2430}


# # Data augmentation

# I have used two data augmentation methods, the easiest to implement : **synonym replacement** and **words swapping**. 
# 
# The first one consist of replacing words by their synonyms, the second one to take two random consecutive words and swap their place. 
# 
# A lot of other techniques of NLP data augmentation exist, 2 other rather simple ones are random insertion and random deletion of words. The four of them are quite well described in [this article by Mael Fabien](https://maelfabien.github.io/machinelearning/NLP_8/#data-augmentation-techniques), from whom I took inspiration. 
# 
# More advanced techniques, such as text generation, deep contextualized embeddings, or back translation (translating to another language, then translating back to the original language often gives a slightly different sentence) are not considered in my work.

# Below is the code to create the augmented database, where you can change some parameters as you like. I published the result database with the default parameters [here](https://www.kaggle.com/louise2001/extended-train-for-tweet), please upvote it if you find it useful !

# In[ ]:


train = pd.read_csv('../input/tweet-sentiment-extraction/train.csv').fillna('')
# if you directly want the result database, just uncomment the following line :
# train = pd.read_csv('../input/extended-train-for-tweet/extended_train.csv')
train.head()


# In[ ]:


print(train.shape)
n = train.shape[0]


# We cannot do our transformations blinded. We must be careful of two points :
# - if we make a modification to the `selected_text` part, it must remain identical both in the `text` and `selected_text` ;
# - do not mix up uncarefully the selected and unselected parts of `text`.
# 
# Therefore, the token `"_________________________________"` will be used to replace the `selected_text` in the `text` during modifications, so that we don't lose track.

# In[ ]:


from nltk.corpus import wordnet, stopwords
stop = stopwords.words('english')
stop += ["_________________________________", "u"]
import string
punct = list(string.punctuation)
punct.remove("-")
punct.append(" ")


# For each word of a sentence that isn't a stopword, we will randomly choose between itself and all his synonyms, in order to replace it in the modified sentence. The first function is for getting synonyms of a word, and probabilities of selecting each one of them when we will randomly rebuild a modified sentence.

# In[ ]:


def get_synonyms(word):
    """
    Get synonyms of a word
    """
    if word.lower() in stop:
        return [word], [1]
    
    synonyms = set()
    for syn in wordnet.synsets(word): 
        for l in syn.lemmas(): 
            synonym = l.name().replace("_", " ").replace("-", " ").lower()
            synonym = "".join([char for char in synonym if char in ' qwertyuiopasdfghjklzxcvbnm'])
            synonyms.add(synonym) 
    
    if word not in synonyms:
        synonyms.add(word)
        
    n = len(synonyms)
    
    if n == 1: # we didn't find any synonyms for that word, therefore we will try to check if it's not because of some punctuation interfering
        word_ = "".join(list(filter(lambda x: x not in punct, word)))
        if word_.lower() in stop:
            return [word, word_], [0.5, 0.5]
        for syn in wordnet.synsets(word_): 
            for l in syn.lemmas(): 
                synonym = l.name().replace("_", " ").replace("-", " ").lower()
                synonym = "".join([char for char in synonym if char in ' qwertyuiopasdfghjklzxcvbnm'])
                synonyms.add(synonym) 
        if word_ not in synonyms:
            synonyms.add(word_)
            
    n = len(synonyms)
    if n == 1:
        probabilities = [1]
    else:
        probabilities = [0.5 if w==word else 0.5/(n-1) for w in synonyms]
    
    return list(synonyms), probabilities


# In[ ]:


for word in ['sad', 'SAD', 'Sad...', 'saaaaad']:
    print(f'For word {word}, synonyms and corresponding probabilities are :')
    print(get_synonyms(word))
    print('-'*20)


# For swapping words, we just randomly select an index of word before the last, and swap it with it successor in the sentence. We also return a boolean which is False if we couldn't swap any words (only one word, or empty sentence).

# In[ ]:


def swap_words(words):
    words = words.split()
    if len(words) < 2:
        return " ".join(words), False
    random_idx = np.random.randint(0, len(words)-1)
    words[random_idx], words[random_idx+1] = words[random_idx+1], words[random_idx] 
    return " ".join(words), True


# In[ ]:


for _ in range(5):
    print(swap_words('The sun is shining today, this makes me feel so good !')[0])


# Now, we are ready to wrap this in a function which we will apply to all rows of our train data.

# As more and more examples are generated, we will need to generate `textID` values for them. 
# 
# I chose the following combination : `new` + a counter that we increment.
# 
# `n_samples` is the number of sentences to generate via synonym replacement. Once we have all of them (`n_samples + 1`, counting the original), we double each of them by applying a word swapping, either inside the `selected_text` when possible (at least 2 words), or in the rest of the `text`.

# In[ ]:


def new_row(row, n_samples=1): 
    text, selected_text, textID = row['text'], row['selected_text'], row['textID']
    oth_text = text.replace(selected_text, " _________________________________ ")
    new_selected_text = [get_synonyms(word) for word in selected_text.split()]
    new_oth_text = [get_synonyms(word) for word in oth_text.split()]
    new_sentences = [row]
    for i in range(n_samples):
        oth_text_ = " ".join([np.random.choice(l_syn, p=p, replace=True) for l_syn, p in new_oth_text])
        selected_text_ = " ".join([np.random.choice(l_syn, p=p, replace=True) for l_syn, p in new_selected_text])
        text_ = oth_text_.replace("_________________________________", selected_text_)
        if not selected_text_ in text_:
            print(f'Original : {text} with target {selected_text}, oth_text {oth_text}\nTransformed : {text_} with target {selected_text_}, oth_text {oth_text_}')
            continue
        row2 = dc(row)
        row2['text'] = text_
        row2['selected_text'] = selected_text_
        row2['textID'] = f'new_{textID}'
        new_sentences.append(row2)
    for r in dc(new_sentences):
        r_ = dc(r)
        if np.random.choice([True, False]):
            selected_text, boo = swap_words(r_['selected_text'])
            if boo:
                r_['text'] = r_['text'].replace(r_['selected_text'], selected_text)
                r_['selected_text'] = selected_text
            else:
                oth_text, _ = swap_words(r_['text'].replace(r_['selected_text'], " _________________________________ "))
                r_['text'] = oth_text.replace("_________________________________",r_['selected_text'])
        else:
            oth_text, _ = swap_words(r_['text'].replace(r_['selected_text'], " _________________________________ "))
            r_['text'] = oth_text.replace("_________________________________", r_['selected_text'])
        r_['textID'] = f'new_{textID}'
        new_sentences.append(r_)
    new_rows = pd.concat(new_sentences, axis=1).transpose().drop_duplicates(subset=['text'], inplace=False, ignore_index=True)
    new_rows = new_rows.loc[new_rows['text'].apply(len)<150]
    counter = 0
    for i, row in new_rows.iterrows():
        if row['textID'][:4] == 'new_':
            row['textID'] = row['textID']+f'_{counter}'
            counter += 1
    return new_rows


# In[ ]:


new_row(train.loc[np.random.choice(train.shape[0])], n_samples=8)


# Now we just have to apply it to the whole dataframe ! We don't forget to shuffle it afterwards, otherwise the batches will all have nearly identical rows.

# In[ ]:


temp = [new_row(row, n_samples=2) for _, row in train.iterrows()]
augmented_data = pd.concat(temp, axis=0)#.sample(frac=1)
train['number'] = [t.shape[0] for t in temp]
train['number'] = train['number'].cumsum()
del temp
gc.collect()
augmented_data.drop_duplicates(subset=['text'], inplace=False, ignore_index=True)
augmented_data.reset_index(drop=True, inplace=True)
# augmented_data.head(20)
match_index = dc(train['number'])
train.drop(columns='number', inplace=True)
match_index = [0] + match_index.values.tolist()
match_borders = list(zip(match_index[:-1], match_index[1:]))
del match_index
gc.collect()
train['brackets'] = match_borders
# train.head()


# We don't forget to save it :

# In[ ]:


# augmented_data.to_csv('extended_train.csv', index=False)
# train = augmented_data
# del augmented_data


# Here, you can notice that we have a problem : some of the generated data is very long compared to the original data. This is problematic since in tweets, texts have limited length. What's more, that will become a big problem for our model where we don't want to put a gigantic `MAX_LEN` which will cost us a lot in computation time. Let's have a closer look :

# In[ ]:


# train['text_len'] = train['text'].apply(len)
# train.hist(column='text_len')
# train.loc[train.text_len<150].hist(column='text_len')
# train.loc[train.text_len>=150, 'textID'].apply(lambda x: 'new' in x).describe()


# All the tweets more than 150 characters long are generated ! We will drop those, since they will be a later problem.

# In[ ]:


# train = train.loc[train.text_len<150]
# train.drop(columns=["text_len"], inplace=True)
# train.reset_index(drop=True, inplace=True)


# In[ ]:


# train.to_csv('extended_train.csv', index=False)


# In[ ]:


print(f'We now have {round(augmented_data.shape[0]/n, 1)} as much data as initially !')


# # The Model

# Now we just have to train the model with nearly 6 times as much data as initially !

# # Training Data
# We will now convert the training data into arrays that roBERTa understands. Here are example inputs and targets: 
# ![ids.jpg](attachment:ids.jpg)
# The tokenization logic below is inspired by Abhishek's PyTorch notebook [here][1].
# 
# [1]: https://www.kaggle.com/abhishek/roberta-inference-5-folds

# In[ ]:


ct = augmented_data.shape[0]
input_ids = np.ones((ct,MAX_LEN),dtype='int32')
attention_mask = np.zeros((ct,MAX_LEN),dtype='int32')
token_type_ids = np.zeros((ct,MAX_LEN),dtype='int32')
start_tokens = np.zeros((ct,MAX_LEN),dtype='int32')
end_tokens = np.zeros((ct,MAX_LEN),dtype='int32')

for k, row in augmented_data.iterrows():
    
    # FIND OVERLAP
    text1 = " "+" ".join(row['text'].split())
    text2 = " ".join(row['selected_text'].split())
    idx = text1.find(text2)
    chars = np.zeros((len(text1)))
    chars[idx:idx+len(text2)]=1
    if text1[idx-1]==' ': 
        chars[idx-1] = 1 
    enc = tokenizer.encode(text1) 
        
    # ID_OFFSETS
    offsets = []
    idx=0
    for t in enc.ids:
        w = tokenizer.decode([t])
        offsets.append((idx,idx+len(w)))
        idx += len(w)
    
    # START END TOKENS
    toks = []
    for i,(a,b) in enumerate(offsets):
        sm = np.sum(chars[a:b])
        if sm>0: 
            toks.append(i) 
        
    s_tok = sentiment_id[row['sentiment']]
    input_ids[k,:len(enc.ids)+3] = [0, s_tok] + enc.ids + [2]
    attention_mask[k,:len(enc.ids)+3] = 1
    if len(toks)>0:
        start_tokens[k,toks[0]+2] = 1
        end_tokens[k,toks[-1]+2] = 1


# In[ ]:


ct_train = train.shape[0]
input_ids_train = np.ones((ct_train,MAX_LEN),dtype='int32')
attention_mask_train = np.zeros((ct_train,MAX_LEN),dtype='int32')
token_type_ids_train = np.zeros((ct_train,MAX_LEN),dtype='int32')
start_tokens_train = np.zeros((ct_train,MAX_LEN),dtype='int32')
end_tokens_train = np.zeros((ct_train,MAX_LEN),dtype='int32')

for k, row in train.iterrows():
    
    # FIND OVERLAP
    text1 = " "+" ".join(row['text'].split())
    text2 = " ".join(row['selected_text'].split())
    idx = text1.find(text2)
    chars = np.zeros((len(text1)))
    chars[idx:idx+len(text2)]=1
    if text1[idx-1]==' ': 
        chars[idx-1] = 1 
    enc = tokenizer.encode(text1) 
        
    # ID_OFFSETS
    offsets = []
    idx=0
    for t in enc.ids:
        w = tokenizer.decode([t])
        offsets.append((idx,idx+len(w)))
        idx += len(w)
    
    # START END TOKENS
    toks = []
    for i,(a,b) in enumerate(offsets):
        sm = np.sum(chars[a:b])
        if sm>0: 
            toks.append(i) 
        
    s_tok = sentiment_id[row['sentiment']]
    input_ids_train[k,:len(enc.ids)+3] = [0, s_tok] + enc.ids + [2]
    attention_mask_train[k,:len(enc.ids)+3] = 1
    if len(toks)>0:
        start_tokens_train[k,toks[0]+2] = 1
        end_tokens_train[k,toks[-1]+2] = 1


# # Test Data
# We must tokenize the test data exactly the same as we tokenized the training data.

# In[ ]:


test = pd.read_csv('../input/tweet-sentiment-extraction/test.csv').fillna('')


# We need to build the augmented test that we will use to cross-validate the test predictions:

# In[ ]:


def test_new_row(row, n_samples=1): 
    text, textID = row['text'], row['textID']
    new_text = [get_synonyms(word) for word in text.split()]
    new_sentences = [row]
    for i in range(n_samples):
        text_ = " ".join([np.random.choice(l_syn, p=p, replace=True) for l_syn, p in new_text])
        row2 = dc(row)
        row2['text'] = text_
        row2['textID'] = f'new_{textID}'
        new_sentences.append(row2)
    for r in dc(new_sentences):
        r_ = dc(r)
        text, boo = swap_words(r_['text'])
        if boo:
            r_['text'] = text
            r_['textID'] = f'new_{textID}'
            new_sentences.append(r_)
    new_rows = pd.concat(new_sentences, axis=1).transpose().drop_duplicates(subset=['text'], inplace=False, ignore_index=True)
    new_rows = new_rows.loc[new_rows['text'].apply(len)<150]
    counter = 0
    for i, row in new_rows.iterrows():
        if row['textID'][:4] == 'new_':
            row['textID'] = row['textID']+f'_{counter}'
            counter += 1
    return new_rows


# In[ ]:


temp = [test_new_row(row, n_samples=2) for _, row in test.iterrows()]
test_augmented_data = pd.concat(temp, axis=0)#.sample(frac=1)
test['number'] = [t.shape[0] for t in temp]
test['number'] = test['number'].cumsum()
del temp
gc.collect()
test_augmented_data.drop_duplicates(subset=['text'], inplace=False, ignore_index=True)
test_augmented_data.reset_index(drop=True, inplace=True)
test_match_index = dc(test['number'])
test.drop(columns='number', inplace=True)
test_match_index = [0] + test_match_index.values.tolist()
test_match_borders = list(zip(test_match_index[:-1], test_match_index[1:]))
del test_match_index
gc.collect()
test['brackets'] = test_match_borders


# In[ ]:


test_augmented_data.head(10)


# In[ ]:


test.head()


# In[ ]:


ct = test.shape[0]
test_input_ids_t = np.ones((ct,MAX_LEN),dtype='int32')

for k, row in test.iterrows():

    # INPUT_IDS
    text1 = " "+" ".join(row['text'].split())
    enc = tokenizer.encode(text1)                
    s_tok = sentiment_id[row['sentiment']]
    test_input_ids_t[k,:len(enc.ids)+3] = [0, s_tok] + enc.ids + [2]
    
ct = test_augmented_data.shape[0]
input_ids_t = np.ones((ct,MAX_LEN),dtype='int32')
attention_mask_t = np.zeros((ct,MAX_LEN),dtype='int32')
token_type_ids_t = np.zeros((ct,MAX_LEN),dtype='int32')

for k, row in test_augmented_data.iterrows():

    # INPUT_IDS
    text1 = " "+" ".join(row['text'].split())
    enc = tokenizer.encode(text1)                
    s_tok = sentiment_id[row['sentiment']]
    input_ids_t[k,:len(enc.ids)+3] = [0, s_tok] + enc.ids + [2]
    attention_mask_t[k,:len(enc.ids)+3] = 1


# # Build roBERTa Model
# We use a pretrained roBERTa base model and add a custom question answer head. First tokens are input into `bert_model` and we use BERT's first output, i.e. `x[0]` below. These are embeddings of all input tokens and have shape `(batch_size, MAX_LEN, 768)`. Next we apply `tf.keras.layers.Conv1D(filters=1, kernel_size=1)` and transform the embeddings into shape `(batch_size, MAX_LEN, 1)`. We then flatten this and apply `softmax`, so our final output from `x1` has shape `(batch_size, MAX_LEN)`. These are one hot encodings of the start tokens indicies (for `selected_text`). And `x2` are the end tokens indicies.
# 
# ![bert.jpg](attachment:bert.jpg)

# In[ ]:


import pickle

def save_weights(model, dst_fn):
    weights = model.get_weights()
    with open(dst_fn, 'wb') as f:
        pickle.dump(weights, f)


def load_weights(model, weight_fn):
    with open(weight_fn, 'rb') as f:
        weights = pickle.load(f)
    model.set_weights(weights)
    return model

def loss_fn(y_true, y_pred):
    # adjust the targets for sequence bucketing
    ll = tf.shape(y_pred)[1]
    y_true = y_true[:, :ll]
    loss = tf.keras.losses.categorical_crossentropy(y_true, y_pred,
        from_logits=False, label_smoothing=LABEL_SMOOTHING)
    loss = tf.reduce_mean(loss)
    return loss


def build_model():
    ids = tf.keras.layers.Input((MAX_LEN,), dtype=tf.int32)
    att = tf.keras.layers.Input((MAX_LEN,), dtype=tf.int32)
    tok = tf.keras.layers.Input((MAX_LEN,), dtype=tf.int32)
    padding = tf.cast(tf.equal(ids, PAD_ID), tf.int32)

    lens = MAX_LEN - tf.reduce_sum(padding, -1)
    max_len = tf.reduce_max(lens)
    ids_ = ids[:, :max_len]
    att_ = att[:, :max_len]
    tok_ = tok[:, :max_len]

    config = RobertaConfig.from_pretrained(PATH+'config-roberta-base.json')
    bert_model = TFRobertaModel.from_pretrained(PATH+'pretrained-roberta-base.h5',config=config)
    x = bert_model(ids_,attention_mask=att_,token_type_ids=tok_)
    
    x1 = tf.keras.layers.Dropout(0.1)(x[0])
    x1 = tf.keras.layers.Conv1D(768, 2,padding='same')(x1)
    x1 = tf.keras.layers.LeakyReLU()(x1)
    x1 = tf.keras.layers.Dense(1)(x1)
    x1 = tf.keras.layers.Flatten()(x1)
    x1 = tf.keras.layers.Activation('softmax')(x1)
    
    x2 = tf.keras.layers.Dropout(0.1)(x[0]) 
    x2 = tf.keras.layers.Conv1D(768, 2,padding='same')(x2)
    x2 = tf.keras.layers.LeakyReLU()(x2)
    x2 = tf.keras.layers.Dense(1)(x2)
    x2 = tf.keras.layers.Flatten()(x2)
    x2 = tf.keras.layers.Activation('softmax')(x2)

    model = tf.keras.models.Model(inputs=[ids, att, tok], outputs=[x1,x2])
    optimizer = tf.keras.optimizers.Adam(learning_rate=3e-5) 
    model.compile(loss=loss_fn, optimizer=optimizer)
    
    # this is required as `model.predict` needs a fixed size!
    x1_padded = tf.pad(x1, [[0, 0], [0, MAX_LEN - max_len]], constant_values=0.)
    x2_padded = tf.pad(x2, [[0, 0], [0, MAX_LEN - max_len]], constant_values=0.)
    
    padded_model = tf.keras.models.Model(inputs=[ids, att, tok], outputs=[x1_padded,x2_padded])
    return model, padded_model


# # Metric

# In[ ]:


def jaccard(str1, str2): 
    a = set(str1.lower().split()) 
    b = set(str2.lower().split())
    if (len(a)==0) & (len(b)==0): 
        return 0.5
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


# # Train roBERTa Model
# We train with 5 Stratified KFolds (based on sentiment stratification). Each fold, the best model weights are saved and then reloaded before oof prediction and test prediction. Therefore you can run this code offline and upload your 5 fold models to a private Kaggle dataset. Then run this notebook and comment out the line `model.fit()`. Instead your notebook will load your model weights from offline training in the line `model.load_weights()`. Update this to have the correct path. Also make sure you change the KFold seed below to match your offline training. Then this notebook will proceed to use your offline models to predict oof and predict test.

# In[ ]:


jac = []; VER='v0'; DISPLAY=1 # USE display=1 FOR INTERACTIVE
oof_start = np.zeros((input_ids.shape[0],MAX_LEN))
oof_end = np.zeros((input_ids.shape[0],MAX_LEN))
preds_start = np.zeros((input_ids_t.shape[0],MAX_LEN))
preds_end = np.zeros((input_ids_t.shape[0],MAX_LEN))

skf = StratifiedKFold(n_splits=2,shuffle=True,random_state=SEED) #originally 5 splits
for fold,(idx_T,idx_V) in enumerate(skf.split(input_ids_train,train.sentiment.values)):
    idxT = np.array([i for (a,b) in train.loc[idx_T, 'brackets'] for i in range(a, b)])
    idxV = np.array([i for (a,b) in train.loc[idx_V, 'brackets'] for i in range(a, b)])
    print('#'*25)
    print('### FOLD %i'%(fold+1))
    print('#'*25)
    
    K.clear_session()
    model, padded_model = build_model()
        
    #sv = tf.keras.callbacks.ModelCheckpoint(
    #    '%s-roberta-%i.h5'%(VER,fold), monitor='val_loss', verbose=1, save_best_only=True,
    #    save_weights_only=True, mode='auto', save_freq='epoch')
    inpT = [input_ids[idxT,], attention_mask[idxT,], token_type_ids[idxT,]]
    targetT = [start_tokens[idxT,], end_tokens[idxT,]]
    inpV = [input_ids[idxV,],attention_mask[idxV,],token_type_ids[idxV,]]
    targetV = [start_tokens[idxV,], end_tokens[idxV,]]
    # sort the validation data
    shuffleV = np.int32(sorted(range(len(inpV[0])), key=lambda k: (inpV[0][k] == PAD_ID).sum(), reverse=True))
    inpV = [arr[shuffleV] for arr in inpV]
    targetV = [arr[shuffleV] for arr in targetV]
    weight_fn = '%s-roberta-%i.h5'%(VER,fold)
    for epoch in range(1, EPOCHS + 1):
        # sort and shuffle: We add random numbers to not have the same order in each epoch
        shuffleT = np.int32(sorted(range(len(inpT[0])), key=lambda k: (inpT[0][k] == PAD_ID).sum() + np.random.randint(-3, 3), reverse=True))
        # shuffle in batches, otherwise short batches will always come in the beginning of each epoch
        num_batches = math.ceil(len(shuffleT) / BATCH_SIZE)
        batch_inds = np.random.permutation(num_batches)
        shuffleT_ = []
        for batch_ind in batch_inds:
            shuffleT_.append(shuffleT[batch_ind * BATCH_SIZE: (batch_ind + 1) * BATCH_SIZE])
        shuffleT = np.concatenate(shuffleT_)
        # reorder the input data
        inpT = [arr[shuffleT] for arr in inpT]
        targetT = [arr[shuffleT] for arr in targetT]
        model.fit(inpT, targetT, 
            epochs=epoch, initial_epoch=epoch - 1, batch_size=BATCH_SIZE, verbose=DISPLAY, callbacks=[],
            validation_data=(inpV, targetV), shuffle=False)  # don't shuffle in `fit`
        save_weights(model, weight_fn)

    print('Loading model...')
    # model.load_weights('%s-roberta-%i.h5'%(VER,fold))
    load_weights(model, weight_fn)

    print('Predicting OOF...')
    oof_start[idxV,],oof_end[idxV,] = padded_model.predict([input_ids[idxV,],attention_mask[idxV,],token_type_ids[idxV,]],verbose=DISPLAY)
    
    print('Predicting Test...')
    preds = padded_model.predict([input_ids_t,attention_mask_t,token_type_ids_t],verbose=DISPLAY)
    preds_start += preds[0]/skf.n_splits
    preds_end += preds[1]/skf.n_splits
    
    # DISPLAY FOLD JACCARD
    alls = []
    for k in idxV:
        a = np.argmax(oof_start[k,])
        b = np.argmax(oof_end[k,])
        if a>b: 
            st = augmented_data.loc[k,'text'] # IMPROVE CV/LB with better choice here
        else:
            text1 = " "+" ".join(augmented_data.loc[k,'text'].split())
            enc = tokenizer.encode(text1)
            st = tokenizer.decode(enc.ids[a-2:b-1])
        alls.append(jaccard(st,augmented_data.loc[k,'selected_text']))
    jac.append(np.mean(alls))
    print('>>>> FOLD %i Jaccard ='%(fold+1),np.mean(alls))
    print()


# In[ ]:


print('>>>> OVERALL 3Fold CV Jaccard =',np.mean(jac))


# In[ ]:


print(jac) # Jaccard CVs


# # Kaggle Submission

# In[ ]:


alls = []
for k in range(input_ids_t.shape[0]):
    a = np.argmax(preds_start[k,])
    b = np.argmax(preds_end[k,])
    if a>b: 
        st = test_augmented_data.loc[k,'text']
    else:
        text1 = " "+" ".join(test_augmented_data.loc[k,'text'].split())
        enc = tokenizer.encode(text1)
        st = tokenizer.decode(enc.ids[a-2:b-1])
    alls.append(st)
test_augmented_data['selected_text'] = alls


# In[ ]:


test_augmented_data.head()


# ## Coherence in predictions : multivoting

# In[ ]:


test_augmented_data = pd.read_csv('../input/tweet-different-thresholds/test_augmented_data.csv')


# In[ ]:


test_ = dc(test)
def get_submission(threshold):
    test1 = dc(test_)
    for ind, (a, b) in enumerate(test1.brackets.values.tolist()[0:5]):
        df = test_augmented_data.loc[np.arange(a,b),['textID', 'text', 'selected_text']]
        try:
            selected_text = " ".join(df.loc[df.textID.str.contains('new_')==False,'selected_text'].values[0].split())
            text = " ".join(df.loc[df.textID.str.contains('new_')==False,'text'].values[0].split())
        except:
            print(test1.loc[ind,:])
            print(df)
            break
        print(f'Selected_text : {selected_text}, from text {text}')
        text = text.lower().split(selected_text.lower())
        print(f'When splitting :{text}')
        text_before, text_after = text[0].split(), text[-1].split()
        rows = df.loc[df.textID.str.contains('new_')]
        words_dic = []
        i = 0
        for word in text_before:
            print(f'In text_before, processing word {i} : {word}')
            words_dic.append(word)
            l, p = get_synonyms(word)
            coeff = 0.5 if (word.lower() in stop or "".join(list(filter(lambda x: x not in punct, word))) in stop) else 1
            rows[f'scoring_word_{i}'] = rows['selected_text'].apply(lambda x: coeff*np.average([w in x for w in l], weights=p))
            i+=1
        for word in selected_text.split():
            print(f'In selected_text, processing word {i} : {word}')
            words_dic.append(word)
            l, p = get_synonyms(word)
            coeff = 0.5 if (word.lower() in stop or "".join(list(filter(lambda x: x not in punct, word))) in stop) else 1
            rows[f'scoring_word_{i}'] = rows['selected_text'].apply(lambda x: 2*coeff*np.average([w in x for w in l], weights=p))
            i+=1
        for word in text_after:
            print(f'In text_after, processing word {i} : {word}')
            words_dic.append(word)
            l, p = get_synonyms(word)
            coeff = 0.5 if (word.lower() in stop or "".join(list(filter(lambda x: x not in punct, word))) in stop) else 1
            rows[f'scoring_word_{i}'] = rows['selected_text'].apply(lambda x: coeff*np.average([w in x for w in l], weights=p))
            i+=1

            
        s = " ".join([words_dic[int(f.split('_')[-1])] for f in (rows[[f'scoring_word_{j}' for j in range(i)]].mean(axis=0)>=threshold).index.tolist()])
        test1.loc[ind, 'selected_text'] = " ".join([words_dic[int(f.split('_')[-1])] for f in (rows[[f'scoring_word_{j}' for j in range(i)]].mean(axis=0)>=threshold).index.tolist()])

    return test1

get_submission(threshold=0.5)


# In[ ]:


test2 = get_submission(threshold=0.3)
test3 = get_submission(threshold = 1)


# try different submissions with different thresholds

# In[ ]:


test1.to_csv('submission_05.csv', index=False)
test2.to_csv('submission_03.csv', index=False)
test3.to_csv('submission_1.csv', index=False)


# In[ ]:


test_augmented_data.to_csv('test_augmented_data.csv', index=False)


# In[ ]:


test[['textID','selected_text']].to_csv('submission.csv', index=False)


# In[ ]:


pd.set_option('max_colwidth', 60)
test.sample(25)


# In[ ]:




