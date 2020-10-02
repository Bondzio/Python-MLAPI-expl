import pandas as pd
import numpy as np
import tensorflow as tf

# Carregando
train = pd.read_csv("../input/train.csv").as_matrix()
print("Training set has {0[0]} rows and {0[1]} columns".format(train.shape))

print(pd.get_dummies(train[0:100,0]))

##########################################
# Construindo modelo
x = tf.placeholder(tf.float32, [None, 784])
W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))
y = tf.matmul(x,W)+b

# Sa�da esperada
y_ = tf.placeholder(tf.float32, [None, 10])

# Fun��o de erro
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
# Algoritmo de treinamento
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()
  
# Treinando
for _ in range(1000):
    batch_xs  = train[:,1:]
    batch_ys = pd.get_dummies(train[:,0]).as_matrix()
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

exit()  
  
##########################################
# Testando
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  
batch_xs  = train[:,1:]
batch_ys = pd.get_dummies(train[:,0]).as_matrix()
  
print(sess.run(accuracy, feed_dict={x: batch_xs,
                                      y_: batch_ys}))

