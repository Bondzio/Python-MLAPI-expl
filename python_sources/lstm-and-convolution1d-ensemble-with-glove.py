#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import os
print(os.listdir("../input"))


# In[ ]:


from keras.models import Sequential
from keras.layers import LSTM,Dense,GlobalMaxPool1D,Dropout,Embedding,Bidirectional,Flatten,CuDNNLSTM,Convolution1D,MaxPool1D
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from tqdm import tqdm
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


df = pd.read_csv('../input/jigsaw-toxic-comment-classification-challenge/train.csv')


# In[ ]:


df.head()


# In[ ]:


list_classes = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
y = df[list_classes].values


# In[ ]:


tqdm.pandas()


# Using word embeddings so that words with similar words have similar representation in vector space. It represents every word as a vector. The words which have similar meaning are place close to each other. Quick understanding can be done from [this](https://towardsdatascience.com/word-embeddings-exploration-explanation-and-exploitation-with-code-in-python-5dac99d5d795) article.

# In[ ]:


f = open('../input/gloveembeddings/glove.6B.50d.txt')
embedding_values = {}
for line in tqdm(f):
    value = line.split(' ')
    word = value[0]
    coef = np.array(value[1:],dtype = 'float32')
    embedding_values[word] = coef


# There are many words in the training data which are not there in the glove embeddings. So we take the mean of the embeddings and replace the absent words in the embeddings with mean.

# In[ ]:


all_embs = np.stack(embedding_values.values())
emb_mean,emb_std = all_embs.mean(), all_embs.std()
emb_mean,emb_std


# In[ ]:


x = df['comment_text']


# These are the steps that needs to be performed so that we can convert each word of our vocabulary into a unique integer. Tokenizer is initalized in first step. Then fitting on the text will help us create a vocabulary so that each word is assigned with a unique integer. Then we convert in the whole sentence of the comment into a sequence of numbers which are assigned by the tokenizer.

# In[ ]:


token = Tokenizer(num_words=20000)


# In[ ]:


token.fit_on_texts(x)


# In[ ]:


seq = token.texts_to_sequences(x)


# Padding the sequence helps in making all the sentence of same length. maxlen is the parameter which decides the length we want to assign to all the sentences. Padding is done by adding 0 on either the end of sentence or prior the sentence if the sentence is having length less than max length. This is also a parameter which user can change, by defaults its prefix. If the length of the sentence is more than 100 then it is pruned which brings down the length to 50 (maxlen)

# In[ ]:


pad_seq = pad_sequences(seq,maxlen=50)


# Now we will be converting each word in our vocabulary into word embeddings. This embedding is vector of 1x50 dimension which represents each word as a vector and placing them into a vector space. Embedding matrix is created in which the number assigned to the word by tokenizer is assigned with the corresponding vector which we get from the glove embeddings

# In[ ]:


vocab_size = len(token.word_index)+1
print(vocab_size)


# In[ ]:


embedding_matrix = np.random.normal(emb_mean, emb_std, (vocab_size, 50))
for word,i in tqdm(token.word_index.items()):
    values = embedding_values.get(word)
    if values is not None:
        embedding_matrix[i] = values


# Want to learn more about LSTM and RNN. Please follow [this link](https://towardsdatascience.com/illustrated-guide-to-lstms-and-gru-s-a-step-by-step-explanation-44e9eb85bf21) for clear explaination

# In[ ]:


model1 = Sequential()


# Here this embedding layer is important as this will help us in training of the sentences with their respective embeddings whihc we have assigned above. The first parameter is the size of our vocabulary. Second parameter is the output embeddings length which is 50 in this case as we used the 50 glove embeddings of each word. The length of each observation which is expected by the network is given by input_length parameter. We have padded all the observations to 50 hence we set input_length = 50. Weights parameter shows that the embeddings which we want to use is embeddings_matrix and it should not be altered hence trainable is kept false. If we want to train our own embeddings we can simply remove the weights and trainable parameter.

# In[ ]:


model1.add(Embedding(vocab_size,50,input_length=50,weights = [embedding_matrix],trainable = False))


# Building a LSTM model. LSTM networks are useful in sequence data as they are capable of remembering the past words which help them in understanding the meaning of the sentence which helps in text classification. Bidirectional Layer is helpful as it helps in understanding thesentence from start to end and also from end to start. It works in both the direction. This is useful as the reverse order LSTM layer is capable of learning patterns which are not possible for the normal LSTM layers which goes from start to end of the sentence in the normal order. Hence Bidirectional layers are useful in text classification problems as different patterns can be captured from 2 directions. CuDNNLSTM is same as LSTM. If you are using GPU then CuDNNLSTM will be faster but if you are using CPU please use LSTM.
# There are serveral pooling techniques used. Average Pooling, Global Average Pooling, Max Pooling and Global Max Pooling. Average Pooling and Max Pooling take in kernel size as argument. If the input of the max pooling layer is 0,1,2,2,5,1,2, global max pooling outputs 5, whereas ordinary max pooling layer with pool size equals to 3 outputs 2,2,5,5,5 (assuming stride=1). Same is the case with Average Pooling only instead of taking the maximum values we do the average of all the values.
# 

# In[ ]:


model1.add(Bidirectional(CuDNNLSTM(50,return_sequences=True)))
model1.add(GlobalMaxPool1D())


# Dense Layers is a fully connencted layer that is each input node in one layer is connected to all the neurons in the next layer. It is basically helping us out in classification of the dependent variable with an activation function which tells the neuron when to be activated. Relu activation function is used here. There are many different activation functions which can be used like sigmoid, tanh, relu etc. Dropout layers is helping us to avoid overfitting. In dropout few neurons are randomly turned off. This is done in order to remove the dependency of neurons on each other. No neuron is particularly responsible for learning a specific feature. The argument 0.2 specifies that 20% of the neurons in this layers are going to the turned off. This values ideally ranges between 0.1 to 0.5.

# In[ ]:


model1.add(Dense(50,activation = 'relu'))
model1.add(Dropout(0.2))


# The last layers is the dense layer with number of neurons equal to number of classes of dependent variable (6 in this case). The activation used here is softmax. We use sigmoid because its a multi label classification problem (one observation can belong to more than one class). This is one of the special cases but when we are working on a multi label classification problem where one observation is assigned to a single class then we use softmax activation function in our final layer. It performs same as a sigmoid function that is it provides us with the probabilities of the observation belonging to a particular class. We pick the maximum probability and assign that observation to the class having maximum probability. Sigmoid is used when we are dealing with a binary classification problem. Probability less than 0.5 is assigned to 0 class and more than 0.5 is assigned to 1 class.

# In[ ]:


model1.add(Dense(6,activation = 'sigmoid'))


# Compiling the model is final step to complete building the model. Optimizer is like the cost function (similar to gradient descent). Adam is one of the best performing function used in deep learning models. We can change and test with different optimizers too. Mathimatical intuation of all the optimizers can be found [here](https://towardsdatascience.com/types-of-optimization-algorithms-used-in-neural-networks-and-ways-to-optimize-gradient-95ae5d39529f). 
# Binary cross entropy is the loss function which checks the loss in predictions made by the model by calulating the distance between the predicted value and the actual value. We use categorical_crossentropy when dealing with multiclass classification problem and binary_crossentropy when dealing with binary classification. This is a special case for multilabel classification problem hence we are looking for probability of observation belonging to each class. Top few classes are taken for classification.

# Accuracy is being used for checking the performance of the model. Accuracy is one the evalution which can be used check if the model is overfitting or underfitting. If the training accuracy is very high as compared to testing accuracy we can see that the model is overfitting as it is not generalizing well on the unseen data (test data). To avoid overfitting we can reduce the complexity of the model, add more data, add more regularization (dropout, batch normalization). If the training accuracy is much less than testing accuracy then the model is underfitting which means model is not able to capture the features so we need to train the model with more number of epochs.

# In[ ]:


model1.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])


# Batch size is the parameter which defines how many oberservations are fed into the model at a time for training. More the batch size more computational resources and memory is required for processing. This is one of the hyperparameter which can be used for tuning the model. Batch Size of 1 will fed one observation at a time which is really useful but the training and convergence speed will be very slow and model might overfit easily.

# In[ ]:


history = model1.fit(pad_seq,y,epochs =3,batch_size=32,validation_split=0.1)


# In[ ]:


model1.summary()


# In[ ]:


test = pd.read_csv('../input/jigsaw-toxic-comment-classification-challenge/test.csv')


# In[ ]:


test.head()


# Preprocessing of the test data so that model can easily make its prediction as it should be in the same format as that of our training data. Note that we are using the same tokenizer in our testing and we are not fitting it again because this might change the numbers assigned to words which are there in the training data.

# In[ ]:


x_test = test['comment_text']
test_seq = token.texts_to_sequences(x_test)
test_pad_seq = pad_sequences(test_seq,maxlen=50)


# In[ ]:


predict1 = model1.predict(test_pad_seq)


# In[ ]:


sample_submission = pd.read_csv('../input/jigsaw-toxic-comment-classification-challenge/sample_submission.csv')
sample_submission[list_classes] = predict1
sample_submission.to_csv('submission1.csv', index=False)


# Here we are training with Simple LSTM without any Bidirectional Layer. If you want to add dropout for the LSTM layer then it should be done within the LSTM. Dropout argument is done for dropping inputs to the LSTM cell and recurrent dropout is done for dropping the long term memory of the LSTM connection. More clear explaination can be found [here](https://stackoverflow.com/questions/44924690/keras-the-difference-between-lstm-dropout-and-lstm-recurrent-dropout)

# In[ ]:


model2 = Sequential()
model2.add(Embedding(vocab_size,50,input_length=50,weights = [embedding_matrix],trainable = False))
model2.add(LSTM(50,dropout=0.1,recurrent_dropout=0.1))
model2.add(Dense(50,activation = 'relu'))
model2.add(Dense(6,activation = 'sigmoid'))
model2.compile(optimizer = 'adam',loss = 'binary_crossentropy',metrics = ['accuracy'])


# In[ ]:


history = model2.fit(pad_seq,y,epochs =3,batch_size=32,validation_split=0.1)


# In[ ]:


predict2 = model2.predict(test_pad_seq)
sample_submission = pd.read_csv('../input/jigsaw-toxic-comment-classification-challenge/sample_submission.csv')
sample_submission[list_classes] = predict2
sample_submission.to_csv('submission2.csv', index=False)


# Here we will be using convolution1D model. This model works with a kernel of size 5 which hovers over the sentence capturing only the important features of the model. This will help in extracting the features that are significant to classify the text into different categories. After which we use a MaxPooling layer which will help in taking the maximum value from the kernel size of 2. This will also help us in reducing the computation and extracting only the important feature present under the kernel at that point of time. We can still change the model by changing the number of neurons and also by changing the number of layers which will change the computational complexity of the model too. Number of features to be extracted and kernel size are the hyperparameters you can tune to explore different models and results. More explaination on Convolution1D can be found [here](https://blog.goodaudience.com/introduction-to-1d-convolutional-neural-networks-in-keras-for-time-sequences-3a7ff801a2cf).

# In[ ]:


model3 = Sequential()
model3.add(Embedding(vocab_size,50,input_length=50,weights = [embedding_matrix],trainable = False))
model3.add(Convolution1D(9,kernel_size=5,activation='relu'))
model3.add(MaxPool1D(2))
model3.add(Flatten())
model3.add(Dense(50,activation = 'relu'))
model3.add(Dense(6,activation = 'sigmoid'))
model3.compile(optimizer = 'adam',loss = 'binary_crossentropy',metrics = ['accuracy'])


# In[ ]:


history = model3.fit(pad_seq,y,epochs =3,batch_size=32,validation_split=0.1)


# In[ ]:


predict3 = model3.predict(test_pad_seq)
sample_submission = pd.read_csv('../input/jigsaw-toxic-comment-classification-challenge/sample_submission.csv')
sample_submission[list_classes] = predict3
sample_submission.to_csv('submission3.csv', index=False)


# Here we again use convolution1D but changing the number of filters and also the kernel size. Also instead of GlobalMaxPooling we are using MaxPooling1D with a Kernel size of 2 which means that a kernel with size 2 will hover the features and considering only the Maximum value under that kernel and discarding the other values.

# In[ ]:


model4 = Sequential()
model4.add(Embedding(vocab_size,50,input_length=50,weights = [embedding_matrix],trainable = False))
model4.add(Convolution1D(18,kernel_size=3,activation='relu'))
model4.add(MaxPool1D(2))
model4.add(Flatten())
model4.add(Dense(50,activation = 'relu'))
model4.add(Dense(6,activation = 'sigmoid'))
model4.compile(optimizer = 'adam',loss = 'binary_crossentropy',metrics = ['accuracy'])


# In[ ]:


history = model4.fit(pad_seq,y,epochs =3,batch_size=32,validation_split=0.1)


# In[ ]:


predict4 = model4.predict(test_pad_seq)
sample_submission = pd.read_csv('../input/jigsaw-toxic-comment-classification-challenge/sample_submission.csv')
sample_submission[list_classes] = predict4
sample_submission.to_csv('submission4.csv', index=False)


# Making prediction with Ensemble model as well where we can combine all the 4 models that we have trained. This helps in reducing the variance of the model and we can also say that more number of combined models are always better than a single model.

# In[ ]:


ensemble_prediction = 0.25*predict1+0.25*predict2+0.25*predict3+0.25*predict4
sample_submission = pd.read_csv('../input/jigsaw-toxic-comment-classification-challenge/sample_submission.csv')
sample_submission[list_classes] = ensemble_prediction
sample_submission.to_csv('submission_ensemble.csv', index=False)

