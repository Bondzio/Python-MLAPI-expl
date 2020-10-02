#!/usr/bin/env python
# coding: utf-8

# The ImageNet Large Scale Visual Recognition Challenge (ILSVRC) evaluates algorithms for object detection and image classification at large scale. One high level motivation is to allow researchers to compare progress in detection across a wider variety of objects -- taking advantage of the quite expensive labeling effort. The winner of each year is shown below.
# 
# | Year | Model     | Top 5 Error Rate(%) |
# |------|-----------|---------------------|
# | [2011](http://image-net.org/challenges/LSVRC/2011/results) |  XRCE(SVM based)| 25.8(Classification)   |
# | [2012](http://image-net.org/challenges/LSVRC/2012/results.html) | [AlexNet(SuperVision)](https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf)   | 15.3(	Error (5 guesses))                |
# | [2013](http://www.image-net.org/challenges/LSVRC/2013/results.php) | [ZF Net](https://cs.nyu.edu/~fergus/papers/zeilerECCV2014.pdf)    | 14.8                |
# | [2014](http://image-net.org/challenges/LSVRC/2014/results) | GoogLeNet |  6.67               |
# | [2015](http://image-net.org/challenges/LSVRC/2015/results) | [ResNet(MSRA)](https://arxiv.org/abs/1512.03385)    |  3.57               |
# | [2016](http://image-net.org/challenges/LSVRC/2016/results) | [Ensemble 5(Trimps-Soushen)](https://arxiv.org/abs/1602.07261)    | 	2.99               |
# | [2017](http://image-net.org/challenges/LSVRC/2017/) | [NUS-Qihoo_DPNs (CLS-LOC](https://arxiv.org/abs/1611.05431))    |  2.71               |
# 
# 
# 
# 
# Except 2011 XRCE is SVM based model, CNN-based architecture became dominant from 2012 AlexNet.  We will implement [LeNet](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf) which is earliest CNN architecture proposed by Yann Lecun in 1998.  We will use MNIST for demonstrate digit recognition, and I will make some adjustment to enhance performance.
# 
# By the way,[VGG](https://arxiv.org/abs/1409.1556) scored 7.3% in 2014. VGG-16, VGG-19 are also famous CNN architecture. 
# 
# Another concept "Inception" is a variation of CNN for better way to stacking layers.
# 
# [GoogLeNet Inception v1: Going Deeper with Convolutions
# ](https://arxiv.org/abs/1409.4842)
# 
# [GoogLeNet Inception v2: Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift](https://arxiv.org/abs/1502.03167)
# 
# [GoogLeNet Inception v3:Rethinking the Inception Architecture for Computer Vision
# ](https://arxiv.org/abs/1512.00567)
# 
# [GoogLeNet Inception v4:Inception-v4, Inception-ResNet and the Impact of Residual Connections on Learning
# ](https://arxiv.org/abs/1602.07261)
# 
# 
# 

# In[ ]:


import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# In[ ]:


# time_load_data = datetime.datetime.now()
digits = pd.read_csv('../input/train.csv')
x_sub = pd.read_csv('../input/test.csv').values.reshape(-1,28,28,1)/255.
x = digits.iloc[:,1:].values.reshape(-1,28,28,1)/255.
y = digits.iloc[:,0].values
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2,shuffle=True)


# In[ ]:


# def leaky_relu(z,alpha=0.001):
#     """
#     relu sometimes will return zero gradient and make certain neruon "dead". Therefore I make some adjustment at the zero size.
#     Bing Xu, Naiyan Wang, Tianqi Chen, Mu Li(2015), Empirical Evaluation of Rectified Activations in Convolutional Network, https://arxiv.org/pdf/1505.00853.pdf
#     """
#     return tf.maximum(z,z*alpha,name='leaky_relu')


# ReLU sometimes will return zero gradient and make certain neruon "dead".  Therefore I make some adjustment at the zero side. This is also known as leaky-ReLU
# 
# [Bing Xu, Naiyan Wang, Tianqi Chen, Mu Li(2015), Empirical Evaluation of Rectified Activations in Convolutional Network](https://arxiv.org/pdf/1505.00853.pdf), 
# 
# Initialization matters, it helps model learn faster and decrease the chance of gradient explosion,different activation function have different initialization suited for training. Some common initializations are He initialization for ReLU, Xavier(Glorot) initialization for tanh. I use He initialization.
# 
# [Xavier Glorot, Yoshua Bengio(2010), Understanding the difficulty of training deep feedforward neural networks](http://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf), 
# 
# [ Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun(2015) ,Delving Deep into Rectifiers:Surpassing Human-Level Performance on ImageNet Classification](https://arxiv.org/pdf/1502.01852.pdf)
# 
# ReLU(Left) vs leaky-ReLU(Right)
# ![leaky-relu](https://imgur.com/u2c177w.jpg)

# In[ ]:


# Feel free to tune this argument
LEARNING_RATE = 0.0001
N_KERNEL = [32,16]
N_EPOCHS = 1000
BATCH_SIZE = 1000
EARLY_STOPING = True


# In[ ]:


# time_start_building_graph = datetime.datetime.now()
tf.reset_default_graph()
with tf.device('/device:GPU:0'):
    x = tf.placeholder(tf.float32,[None,28,28,1],name='x')
    y = tf.placeholder(tf.int64,[None],name='y')

    bn = tf.layers.batch_normalization(x)
    c1 = tf.layers.conv2d(bn,N_KERNEL[0],kernel_size=5,strides=1,padding='SAME',name='1_convolution_layer')
    p2 = tf.layers.max_pooling2d(c1,pool_size=2,strides=2,padding='SAME',name='2_max_pooling')
    
    c3 = tf.layers.conv2d(p2,N_KERNEL[1],10,1,padding='SAME',name='3_convolution_layer')
    p4 = tf.layers.max_pooling2d(c3,pool_size=3,strides=2,padding='SAME',name='4_max_pooling')
    
    p4_shape = p4.get_shape().as_list()
    n_nodes_fc = p4_shape[1]*p4_shape[2]*p4_shape[3]#7*7*16
    flatten = tf.reshape(p4,[-1,n_nodes_fc])
    
    f5 = tf.layers.dense(flatten,84,kernel_initializer=tf.keras.initializers.he_normal(),activation=tf.nn.leaky_relu,name='5_fully_connected')
    dropout1 = tf.layers.dropout(f5,name='drop_out_1')
    
    f6 = tf.layers.dense(dropout1,84,kernel_initializer=tf.keras.initializers.he_normal(),activation=tf.nn.leaky_relu,name='6_fully_connected')
    dropout2 = tf.layers.dropout(f6,name='drop_out_2')
    
    logits = tf.layers.dense(dropout2,10,name='logits')
    loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y,logits=logits),name='Entropy')
    training_op = tf.train.AdamOptimizer(LEARNING_RATE,name='AdamOptimizer').minimize(loss)

    y_pred = tf.argmax(logits,1,name='Prediction')
    accuracy = tf.reduce_mean(tf.cast(tf.equal(y,y_pred),tf.float32),name='accuracy')


# In[ ]:


from IPython.display import clear_output, Image, display, HTML

def strip_consts(graph_def, max_const_size=32):
    """Strip large constant values from graph_def."""
    strip_def = tf.GraphDef()
    for n0 in graph_def.node:
        n = strip_def.node.add() 
        n.MergeFrom(n0)
        if n.op == 'Const':
            tensor = n.attr['value'].tensor
            size = len(tensor.tensor_content)
            if size > max_const_size:
                tensor.tensor_content = bytes(b"<stripped %d bytes>" % size)
    return strip_def

def show_graph(graph_def, max_const_size=32):
    """Visualize TensorFlow graph."""
    if hasattr(graph_def, 'as_graph_def'):
        graph_def = graph_def.as_graph_def()
    strip_def = strip_consts(graph_def, max_const_size=max_const_size)
    code = """
        <script>
          function load() {{
            document.getElementById("{id}").pbtxt = {data};
          }}
        </script>
        <link rel="import" href="https://tensorboard.appspot.com/tf-graph-basic.build.html" onload=load()>
        <div style="height:600px">
          <tf-graph-basic id="{id}"></tf-graph-basic>
        </div>
    """.format(data=repr(str(strip_def)), id='graph'+str(np.random.rand()))

    iframe = """
        <iframe seamless style="width:1200px;height:620px;border:0" srcdoc="{}"></iframe>
    """.format(code.replace('"', '&quot;'))
    display(HTML(iframe))
show_graph(tf.get_default_graph())


# In[ ]:


# time_start_training = datetime.datetime.now()

with tf.name_scope('batch_iterator'):
    dataset = tf.data.Dataset.from_tensor_slices((x_train,y_train)).shuffle(buffer_size=1000).repeat(N_EPOCHS).batch(BATCH_SIZE)
    batch_iterator = dataset.make_one_shot_iterator()
    next_batch = batch_iterator.get_next()
    
train_loss = []
train_accuracy = []
test_accuracy = []
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
with tf.Session(config=config) as sess:
    tf.global_variables_initializer().run()
    for iteration in range(N_EPOCHS*len(x_train)//BATCH_SIZE):
        try:
            x_batch,y_batch = sess.run(next_batch)
            sess.run(training_op,feed_dict={x: x_batch, y: y_batch})
            train_loss.append(loss.eval(feed_dict={x: x_batch, y: y_batch}))
            # each epoch will take about (len(x_train)/BATCH_SIZE) to complete
            if iteration % ((len(x_train)//BATCH_SIZE)*10) == 0:
                __train_accuracy =accuracy.eval(feed_dict={x: x_train, y: y_train})
                __test_accuracy = accuracy.eval(feed_dict={x:x_test,y:y_test})
                train_accuracy.append(__train_accuracy)
                test_accuracy.append(__test_accuracy)
                print(f'In epoch {iteration//((len(x_train)//BATCH_SIZE))} Train accuracy: {__train_accuracy},     Test accuracy: {__test_accuracy}')
                if EARLY_STOPING:
                    if __train_accuracy > 0.999995:
                        print('Accuracy on training set {} has greater than 99.9995%. Early stopping to avoid overfitting.'.format(__train_accuracy))
                        break
        except tf.errors.OutOfRangeError:
            pass
#     time_start_predicting = datetime.datetime.now()
    y_test_pred=y_pred.eval(feed_dict={x:x_test})
#     time_finish_predicting = datetime.datetime.now()
    y_sub=y_pred.eval(feed_dict={x:x_sub})


# In[ ]:


# time_of_steps = [time_load_data,time_start_building_graph,time_start_training,time_start_predicting,time_finish_predicting]
# time_consume_of_steps = []
# for i in range(len(time_of_steps)):
#     if i == 0:
#         time_consume_of_steps.append(0)
#     else:
#         time_consume_of_steps.append(time_of_steps[i]-time_of_steps[i-1])
# pd.DataFrame([time_of_steps,time_consume_of_steps])


# In[ ]:


print('Accuracy on testing set:',accuracy_score(y_test,y_test_pred))


# In[ ]:


plt.figure(figsize=(20,5))

plt.subplot(1,2,1)
plt.title('Training loss:Cross Entropy')
plt.plot(train_loss)
plt.xlabel('Iterations')
plt.ylabel('Cross Entropy')
plt.xlim(0,)
plt.ylim(0,1.5)

plt.subplot(1,2,2)
plt.title('Training accuracy')
plt.plot([i*10 for i in range(len(train_accuracy))],train_accuracy,label= 'Training set')
plt.plot([i*10 for i in range(len(train_accuracy))],test_accuracy,label= 'Testing set')
plt.legend(loc='upper left')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.xlim(0,)
_=plt.ylim(0.1,)


# In[ ]:


random_idx = np.random.choice([i for i in range(len(y_sub))],9)
print([y_sub[i] for i in random_idx])
plt.figure(figsize=(10,10))
for i in range(9):
    plt.subplot(3,3,i+1)
    plt.imshow(x_sub.reshape(-1,28,28)[random_idx[i]],cmap='gray')


# In[ ]:


submission = pd.read_csv('../input/sample_submission.csv')
submission['Label'] = y_sub
submission.to_csv(f'../working/submission{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")}.csv',index=False)


# In[ ]:


# To be continued: comparing to SVM
# from sklearn.svm import SVC
# svm = SVC()
# svm.fit(x_train.reshape(-1,784),y_train.reshape(-1))

