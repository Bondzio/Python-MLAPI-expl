#!/usr/bin/env python
# coding: utf-8

# ## Reference: https://www.kaggle.com/amansrivastava/exploration-bi-lstm-model

# ## Import libraries

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import tensorflow as tf
import seaborn as sns
from IPython.display import YouTubeVideo
import matplotlib.pyplot as plt
import plotly.plotly as py
import networkx as nx
import PIL

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


# video level feature file
print(os.listdir("../input/video-sample/video/"))
# frame level features file
print(os.listdir("../input/frame-sample/frame/"))


# ## Exploratory data analysis 

# ### label_names_2018.csv contains the mapping between the label ids and the label names

# In[ ]:


labels_df = pd.read_csv('../input/label_names_2018.csv', error_bad_lines= False)


# In[ ]:


labels_df.shape


# In[ ]:


labels_df.head()


# In[ ]:


print("Total nubers of labels in sample dataset: %s" %(len(labels_df['label_name'].unique())))


# ## Check the vocabulary file. It has the description of the video indices and the descriptions for the videos.

# In[ ]:


vocab = pd.read_csv('../input/vocabulary.csv')


# In[ ]:


vocab.head()


# In[ ]:


vocab.shape


# ### Exploring the video data

# In[ ]:


video_files = ["../input/video-sample/video/{}".format(i) for i in os.listdir("../input/video-sample/video/")]
print(video_files)


# In[ ]:


vid_ids = []
labels = []
mean_rgb = []
mean_audio = []


# ### Extract the values from the tfrecords

# In[ ]:


for file in video_files:
    for example in tf.python_io.tf_record_iterator(file):
        tf_example = tf.train.Example.FromString(example)
        
        vid_ids.append(tf_example.features.feature['id'].bytes_list.value[0].decode(encoding='UTF-8'))
        labels.append(tf_example.features.feature['labels'].int64_list.value)
        mean_rgb.append(tf_example.features.feature['mean_rgb'].float_list.value)
        mean_audio.append(tf_example.features.feature['mean_audio'].float_list.value)
        
print('Number of videos in Sample data set: %s' % str(len(vid_ids)))
print('Picking a youtube video id: %s' % vid_ids[13])
print('List of label ids for youtube video id %s, are - %s' % (vid_ids[13], str(labels[13])))
print('First 20 rgb feature of a youtube video (',vid_ids[13],'): are - %s' % str(mean_rgb[13][:20]))


# In[ ]:


len(vid_ids)


# In[ ]:


vid_ids


# In[ ]:


labels


# In[ ]:


len(labels)


# In[ ]:


mean_audio


# In[ ]:


len(mean_audio)


# In[ ]:


len(mean_audio[0])


# In[ ]:


len(mean_rgb)


# In[ ]:


len(mean_rgb[0])


# ### Exploring the most common labels.

# ### Mapping the label ids with the label names

# In[ ]:


labels_name = []
for row in labels:
    n_labels = []
    for label_id in row:
        # some labels ids are missing so have put try/except
        try:
            n_labels.append(str(labels_df[labels_df['label_id']==label_id]['label_name'].values[0]))
        except:
            continue
    labels_name.append(n_labels)

print('List of label names for youtube video id %s, are - %s' % (vid_ids[13], str(labels_name[13])))


# In[ ]:


labels_name[143]


# ### Labels count dictionary

# In[ ]:


from collections import Counter
import operator

all_labels = []
for each in labels_name:
    all_labels.extend(each)
    
labels_count_dict = dict(Counter(all_labels))


# In[ ]:


labels_count_dict


# ### Looking at the distribution of top 25 labels

# In[ ]:


labels_count_df = pd.DataFrame.from_dict(labels_count_dict, orient= 'index').reset_index()


# In[ ]:


labels_count_df.shape


# In[ ]:


labels_count_df.columns = ['label', 'count']
sorted_labels_count_df = labels_count_df.sort_values('count', ascending= False)


# In[ ]:


sorted_labels_count_df.head()


# #### Game label has the most number of examples while Recipe has the least

# In[ ]:


TOP = 25
TOP_labels = list(sorted_labels_count_df['label'])[:TOP]
fig, ax = plt.subplots(figsize=(10, 7))
sns.barplot(y='label', x='count', data=sorted_labels_count_df.iloc[0:TOP, :])
plt.title('Top {} labels with sample count'.format(TOP))


# ### Within these top 25 labels, explore the most common ones

# In[ ]:


common_occur_top_label_dict = {}
for row in labels_name:
    for label in row:
        if label in TOP_labels:
            c_labels = [label + "|" + x for x in row if x != label]
            for c_label in c_labels:
                common_occur_top_label_dict[c_label] = common_occur_top_label_dict.get(c_label, 0) + 1
                
# Putting these into a dataframe
common_occur_top_label_df = pd.DataFrame.from_dict(common_occur_top_label_dict, orient= 'index').reset_index()
common_occur_top_label_df.columns = ['common_label', 'count']
sorted_common_occur_top_label_df = common_occur_top_label_df.sort_values('count', ascending=False)


# plotting 25 common occurs labels from top labels
TOP = 25
fig, ax = plt.subplots(figsize=(10,7))
sns.barplot(y='common_label', x='count', data=sorted_common_occur_top_label_df.iloc[0:TOP, :])
plt.title('Top {} common occur labels with sample count'.format(TOP))


# In[ ]:


sorted_common_occur_top_label_df.head


# ### The Video Game | Game is the highest occuring label in the data

# ## Creating a Network Graph to explore the relations amongst the TOP labels

# In[ ]:


top_coocurance_label_dict = {}
for row in labels_name:
    for label in row:
        if label in TOP_labels:
            top_label_siblings = [x for x in row if x != label]
            for sibling in top_label_siblings:
                if label not in top_coocurance_label_dict:
                    top_coocurance_label_dict[label] = {}
                top_coocurance_label_dict[label][sibling] = top_coocurance_label_dict.get(label, {}).get(sibling, 0) + 11


# In[ ]:


from_label = []
to_label = []
value = []
for key, val in top_coocurance_label_dict.items():
    for key2, val2 in val.items():
        from_label.append(key)
        to_label.append(key2)
        value.append(val2)


# In[ ]:


df = pd.DataFrame({ 'from': from_label, 'to': to_label, 'value': value})
sorted_df = df.sort_values('value', ascending=False)
sorted_df = sorted_df.iloc[:50, ]


# In[ ]:


df


# In[ ]:


node_colors = ['turquoise', 'turquoise', 'green', 'crimson', 'grey', 'turquoise', 'turquoise', 
'grey', 'skyblue', 'crimson', 'yellow', 'green', 'turquoise', 
'skyblue', 'skyblue', 'green', 'green', 'lightcoral', 'grey', 'yellow', 
'turquoise', 'skyblue', 'orange', 'green', 'skyblue', 'green', 'turquoise']


# In[ ]:


len(node_colors)


# ### Create a graph using the columns of the dataframe df

# In[ ]:


df = sorted_df
G= nx.from_pandas_edgelist(df, 'from', 'to', 'value', create_using=nx.Graph())


# In[ ]:


plt.figure(figsize = (10,10))
nx.draw(G, pos=nx.circular_layout(G), node_size=1000, with_labels=True, node_color=node_colors)


# ### Position the nodes on a circle

# In[ ]:


nx.draw_networkx_edge_labels(G, pos=nx.circular_layout(G), edge_labels=nx.get_edge_attributes(G, 'value'))


# In[ ]:


plt.title('Network graph representing the co-occurance between the categories', size=20)
plt.show()


# In[ ]:


df = sorted_df
G= nx.from_pandas_edgelist(df, 'from', 'to', 'value', create_using=nx.Graph())
plt.figure(figsize = (10,10))
nx.draw(G, pos=nx.circular_layout(G), node_size=1000, with_labels=True, node_color=node_colors)
nx.draw_networkx_edge_labels(G, pos=nx.circular_layout(G), edge_labels=nx.get_edge_attributes(G, 'value'))
plt.title('Network graph representing the co-occurance between the categories', size=20)
plt.show()


# ## Exploring the frame level of the video.

# In[ ]:


frame_files = ["../input/frame-sample/frame/{}".format(i) for i in os.listdir("../input/frame-sample/frame/")]
feat_rgb = []
feat_audio = []


# In[ ]:


frame_files


# In[ ]:


for file in frame_files:
    for example in tf.python_io.tf_record_iterator(file):        
        tf_seq_example = tf.train.SequenceExample.FromString(example)
        n_frames = len(tf_seq_example.feature_lists.feature_list['audio'].feature)
        sess = tf.InteractiveSession()
        rgb_frame = []
        audio_frame = []
        # iterate through frames
        for i in range(n_frames):
            rgb_frame.append(tf.cast(tf.decode_raw(
                    tf_seq_example.feature_lists.feature_list['rgb'].feature[i].bytes_list.value[0],tf.uint8)
                           ,tf.float32).eval())
            audio_frame.append(tf.cast(tf.decode_raw(
                    tf_seq_example.feature_lists.feature_list['audio'].feature[i].bytes_list.value[0],tf.uint8)
                           ,tf.float32).eval())


        sess.close()
        feat_rgb.append(rgb_frame)
        feat_audio.append(audio_frame)
        break


# In[ ]:


feat_audio


# In[ ]:


feat_rgb


# In[ ]:


print("No. of videos %d" % len(feat_rgb))
print('The first video has %d frames' %len(feat_rgb[0]))
print("Max frame length is: %d" % max([len(x) for x in feat_rgb]))


# ## Bi-LSTM Multilabel classification

# #### Since the frames are sequential in nature, we use a LSTM to extract this type of information and merge this with the video data. These will be passed through the sigmoid layer with units equal to the number of features.

# In[ ]:


from keras.layers import Dense, Input, LSTM, Dropout, Bidirectional
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers.normalization import BatchNormalization
from keras.layers.embeddings import Embedding
from keras.layers.merge import concatenate
from keras.callbacks import TensorBoard
from keras.models import load_model
from keras.models import Model
from keras.utils.vis_utils import plot_model
import operator
import time 
import gc
import os


# ## Creating a train, dev test by combining video_rgb, video_audio, frame_rgb, frame_audio and labels

# In[ ]:


train_video_rgb = []
train_video_audio = []
train_frame_rgb = []
train_frame_audio = []
train_labels = []

val_video_rgb = []
val_video_audio = []
val_frame_rgb = []
val_frame_audio = []
val_labels = []


# In[ ]:


def create_train_dev_dataset(video_rgb, video_audio, frame_rgb, frame_audio, labels):
    shuffle_indices = np.random.permutation(np.arange(len(labels)))
    video_rgb_shuffled = video_rgb[shuffle_indices]
    video_audio_shuffled = video_audio[shuffle_indices]
    frame_rgb_shuffled = frame_rgb[shuffle_indices]
    frame_audio_shuffled = frame_audio[shuffle_indices]
    labels_shuffled = labels[shuffle_indices]
    
    dev_idx = max(1, int(len(labels_shuffled) * validation_split_ratio))
    
#     del video_rgb
#     del video_audio
#     del frame_rgb
#     del frame_audio
#     gc.collect()
    
    train_video_rgb, val_video_rgb = video_rgb_shuffled[:-dev_idx], video_rgb_shuffled[-dev_idx:]
    train_video_audio, val_video_audio = video_audio_shuffled[:-dev_idx], video_audio_shuffled[-dev_idx:]
    
    train_frame_rgb, val_frame_rgb = frame_rgb_shuffled[:-dev_idx], frame_rgb_shuffled[-dev_idx:]
    train_frame_audio, val_frame_audio = frame_audio_shuffled[:-dev_idx], frame_audio_shuffled[-dev_idx:]
    
    train_labels, val_labels = labels_shuffled[:-dev_idx], labels_shuffled[-dev_idx:]
    
    del video_rgb_shuffled, video_audio_shuffled, frame_rgb_shuffled, frame_audio_shuffled, labels_shuffled
    gc.collect()
    
    return (train_video_rgb, train_video_audio, train_frame_rgb, train_frame_audio, train_labels, val_video_rgb, 
            val_video_audio, val_frame_rgb, val_frame_audio, val_labels)


# ## Defining the Model architecture

# In[ ]:


max_frame_rgb_sequence_length = 10
frame_rgb_embedding_size = 1024

max_frame_audio_sequence_length = 10
frame_audio_embedding_size = 128

number_dense_units = 1000
number_lstm_units = 100
rate_drop_lstm = 0.2
rate_drop_dense = 0.2
activation_function='relu'
validation_split_ratio = 0.2
label_feature_size = 10


# ## Creating a dataset of random values having the same size and dimension as the training data set to test the data

# In[ ]:


sample_length = 1000

video_rgb = np.random.rand(sample_length, 1024)
video_audio = np.random.rand(sample_length, 128)

frame_rgb = np.random.rand(sample_length, 10, 1024)
frame_audio = np.random.rand(sample_length, 10, 128)

# Here I have considered i have only 10 labels
labels = np.zeros([sample_length,10])
for i in range(len(labels)):
    j = random.randint(0,9)
    labels[i][j] = 1 


# ### Using checkpoint to store the best model and use it for future

# In[ ]:


def create_model(video_rgb, video_audio, frame_rgb, frame_audio, labels):
    """Create and store best model at `checkpoint` path ustilising bi-lstm layer for frame level data of videos"""
    train_video_rgb, train_video_audio, train_frame_rgb, train_frame_audio, train_labels, val_video_rgb, val_video_audio, val_frame_rgb, val_frame_audio, val_labels = create_train_dev_dataset(video_rgb, video_audio, frame_rgb, frame_audio, labels) 
    
    # Creating 2 bi-lstm layer, one for rgb and other for audio level data
    lstm_layer_1 = Bidirectional(LSTM(number_lstm_units, dropout=rate_drop_lstm, recurrent_dropout=rate_drop_lstm))
    lstm_layer_2 = Bidirectional(LSTM(number_lstm_units, dropout=rate_drop_lstm, recurrent_dropout=rate_drop_lstm))
    
    # creating input layer for frame-level data
    frame_rgb_sequence_input = Input(shape=(max_frame_rgb_sequence_length, frame_rgb_embedding_size), dtype='float32')
    frame_audio_sequence_input = Input(shape=(max_frame_audio_sequence_length, frame_audio_embedding_size), dtype='float32')
    
    frame_x1 = lstm_layer_1(frame_rgb_sequence_input)
    frame_x2 = lstm_layer_2(frame_audio_sequence_input)
    
    # creating input layer for video-level data
    video_rgb_input = Input(shape=(video_rgb.shape[1],))
    video_rgb_dense = Dense(int(number_dense_units/2), activation=activation_function)(video_rgb_input)
    
    video_audio_input = Input(shape=(video_audio.shape[1],))
    video_audio_dense = Dense(int(number_dense_units/2), activation=activation_function)(video_audio_input)
    
    # merging frame-level bi-lstm output and later passed to dense layer by applying batch-normalisation and dropout
    merged_frame = concatenate([frame_x1, frame_x2])
    merged_frame = BatchNormalization()(merged_frame)
    merged_frame = Dropout(rate_drop_dense)(merged_frame)
    merged_frame_dense = Dense(int(number_dense_units/2), activation=activation_function)(merged_frame)
    
    # merging video-level dense layer output
    merged_video = concatenate([video_rgb_dense, video_audio_dense])
    merged_video = BatchNormalization()(merged_video)
    merged_video = Dropout(rate_drop_dense)(merged_video)
    merged_video_dense = Dense(int(number_dense_units/2), activation=activation_function)(merged_video)
    
    # merging frame-level and video-level dense layer output
    merged = concatenate([merged_frame_dense, merged_video_dense])
    merged = BatchNormalization()(merged)
    merged = Dropout(rate_drop_dense)(merged)
     
    merged = Dense(number_dense_units, activation=activation_function)(merged)
    merged = BatchNormalization()(merged)
    merged = Dropout(rate_drop_dense)(merged)
    preds = Dense(label_feature_size, activation='sigmoid')(merged)
    
    model = Model(inputs=[frame_rgb_sequence_input, frame_audio_sequence_input, video_rgb_input, video_audio_input], outputs=preds)
    print(model.summary())
    model.compile(loss='binary_crossentropy', optimizer='nadam', metrics=['acc'])
    early_stopping = EarlyStopping(monitor='val_loss', patience=3)
    
    STAMP = 'lstm_%d_%d_%.2f_%.2f' % (number_lstm_units, number_dense_units, rate_drop_lstm, rate_drop_dense)

    checkpoint_dir = 'checkpoints/' + str(int(time.time())) + '/'

    if not os.path.exists(checkpoint_dir):
        os.makedirs(checkpoint_dir)

    bst_model_path = checkpoint_dir + STAMP + '.h5'
    model_checkpoint = ModelCheckpoint(bst_model_path, save_best_only=True, save_weights_only=False)
    tensorboard = TensorBoard(log_dir=checkpoint_dir + "logs/{}".format(time.time()))
    
    model.fit([train_frame_rgb, train_frame_audio, train_video_rgb, train_video_audio], train_labels,
              validation_data=([val_frame_rgb, val_frame_audio, val_video_rgb, val_video_audio], val_labels),
              epochs=200, batch_size=64, shuffle=True, callbacks=[early_stopping, model_checkpoint, tensorboard])    
    return model


# ## Training model

# In[ ]:


len(video_audio)


# In[ ]:


labels


# In[ ]:


model = create_model(video_audio=video_audio, video_rgb=video_rgb, frame_audio=frame_audio, frame_rgb=frame_rgb, 
                     labels = labels)


# In[ ]:


plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)


# In[ ]:


model_img = plt.imread('model_plot.png')


# In[ ]:




