#!/usr/bin/env python
# coding: utf-8

# # About 
# 
# ### -- press f to pay respects --
# Forked from the kernel: https://www.kaggle.com/xhlulu/ieee-fraud-xgboost-with-gpu-fit-in-40s
# 
# VAE code is from here: https://jmetzen.github.io/2015-11-27/vae.html
# 

# In[ ]:


import os
import tensorflow as tf
import time
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt


# # Preprocessing
# 
# Additional to xhulu's work, I've added the min-max normalization. It is required for the cost function of the VAE. Also, I am using the train data, with a training-validation split.

# In[ ]:


get_ipython().run_cell_magic('time', '', 'train_transaction = pd.read_csv(\'../input/train_transaction.csv\', index_col=\'TransactionID\')\ntrain_identity = pd.read_csv(\'../input/train_identity.csv\', index_col=\'TransactionID\')\n\ntrain = train_transaction.merge(train_identity, how=\'left\', left_index=True, right_index=True)\n\nprint("train.shape:",train.shape)\n\ny_train = train[\'isFraud\'].copy()\ndel train_transaction, train_identity\n\nX_train = train.copy()\ndel train\n\n#Fill NaNs\nX_train.fillna(-999, inplace=True)\n\n# Label Encoding\nprint(\'label encoding\')\nfor f in X_train.columns:\n    if X_train[f].dtype==\'object\': \n        lbl = preprocessing.LabelEncoder()\n        lbl.fit(list(X_train[f].values))\n        X_train[f] = lbl.transform(list(X_train[f].values))\n        \n# Normalize\ndef apply_norm(df):\n    min_max_scaler = preprocessing.MinMaxScaler()\n    np_scaled = min_max_scaler.fit_transform(df)\n    df_norm = pd.DataFrame(np_scaled, columns=df.columns)\n    return df_norm\n    \nprint(\'normalizing\')\nX_train_norm = apply_norm(X_train)\n# Get a validation set\nX_train_norm, X_val_norm = train_test_split(X_train_norm, test_size=0.1)\ndel X_train\n\n# Drop target\nX_train_norm = X_train_norm.drop(\'isFraud\', axis=1)\n\nprint("last shapes")\nprint("X_train_norm.shape:",X_train_norm.shape)\nprint("X_val_norm.shape:",X_val_norm.shape)')


# In[ ]:


print("isFraud==0 in validation set:",len(X_val_norm[X_val_norm.isFraud == 0]))
print("isFraud==1 in validation set:",len(X_val_norm[X_val_norm.isFraud == 1]))


# In[ ]:


X_val_norm.describe()


# # Variational autoencoder
# - Code below is taken from J.H. Metzen (and modified a little bit)
# 
# 
# 

# In[ ]:


# Xavier initializer
def xavier_init(fan_in, fan_out, constant=1): 
    """ Xavier initialization of network weights"""
    # https://stackoverflow.com/questions/33640581/how-to-do-xavier-initialization-on-tensorflow
    low = -constant*np.sqrt(6.0/(fan_in + fan_out)) 
    high = constant*np.sqrt(6.0/(fan_in + fan_out))
    return tf.random_uniform((fan_in, fan_out), 
                             minval=low, maxval=high, 
                             dtype=tf.float32)

### Definitions and things
class VariationalAutoencoder(object):
    """ Variation Autoencoder (VAE) with an sklearn-like interface implemented using TensorFlow.
    
    This implementation uses probabilistic encoders and decoders using Gaussian 
    distributions and  realized by multi-layer perceptrons. The VAE can be learned
    end-to-end.
    
    See "Auto-Encoding Variational Bayes" by Kingma and Welling for more details.
    """
    def __init__(self, network_architecture, transfer_fct=tf.nn.softplus, 
                 learning_rate=0.001, batch_size=100):
        self.network_architecture = network_architecture
        self.transfer_fct = transfer_fct
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        
        # tf Graph input
        self.x = tf.placeholder(tf.float32, [None, network_architecture["n_input"]])
        
        # Create autoencoder network
        self._create_network()
        # Define loss function based variational upper-bound and 
        # corresponding optimizer
        self._create_loss_optimizer()
        
        # Initializing the tensor flow variables
        init = tf.global_variables_initializer()

        # Launch the session
        self.sess = tf.InteractiveSession(config=tf.ConfigProto(log_device_placement=True))
        self.sess.run(init)
    
    def _create_network(self):
        # Initialize autoencode network weights and biases
        network_weights = self._initialize_weights(**self.network_architecture)

        # Use recognition network to determine mean and 
        # (log) variance of Gaussian distribution in latent
        # space
        self.z_mean, self.z_log_sigma_sq =             self._recognition_network(network_weights["weights_recog"], 
                                      network_weights["biases_recog"])

        # Draw one sample z from Gaussian distribution
        n_z = self.network_architecture["n_z"]
        eps = tf.random_normal((self.batch_size, n_z), 0, 1, 
                               dtype=tf.float32)
        # z = mu + sigma*epsilon
        self.z = tf.add(self.z_mean, 
                        tf.multiply(tf.sqrt(tf.exp(self.z_log_sigma_sq)), eps))

        # Use generator to determine mean of
        # Bernoulli distribution of reconstructed input
        self.x_reconstr_mean =             self._generator_network(network_weights["weights_gener"],
                                    network_weights["biases_gener"])
            
    def _initialize_weights(self, n_hidden_recog_1, n_hidden_recog_2, 
                            n_hidden_gener_1,  n_hidden_gener_2, 
                            n_input, n_z):
        all_weights = dict()
        all_weights['weights_recog'] = {
            'h1': tf.Variable(xavier_init(n_input, n_hidden_recog_1)),
            'h2': tf.Variable(xavier_init(n_hidden_recog_1, n_hidden_recog_2)),
            'out_mean': tf.Variable(xavier_init(n_hidden_recog_2, n_z)),
            'out_log_sigma': tf.Variable(xavier_init(n_hidden_recog_2, n_z))}
        all_weights['biases_recog'] = {
            'b1': tf.Variable(tf.zeros([n_hidden_recog_1], dtype=tf.float32)),
            'b2': tf.Variable(tf.zeros([n_hidden_recog_2], dtype=tf.float32)),
            'out_mean': tf.Variable(tf.zeros([n_z], dtype=tf.float32)),
            'out_log_sigma': tf.Variable(tf.zeros([n_z], dtype=tf.float32))}
        all_weights['weights_gener'] = {
            'h1': tf.Variable(xavier_init(n_z, n_hidden_gener_1)),
            'h2': tf.Variable(xavier_init(n_hidden_gener_1, n_hidden_gener_2)),
            'out_mean': tf.Variable(xavier_init(n_hidden_gener_2, n_input)),
            'out_log_sigma': tf.Variable(xavier_init(n_hidden_gener_2, n_input))}
        all_weights['biases_gener'] = {
            'b1': tf.Variable(tf.zeros([n_hidden_gener_1], dtype=tf.float32)),
            'b2': tf.Variable(tf.zeros([n_hidden_gener_2], dtype=tf.float32)),
            'out_mean': tf.Variable(tf.zeros([n_input], dtype=tf.float32)),
            'out_log_sigma': tf.Variable(tf.zeros([n_input], dtype=tf.float32))}
        return all_weights
            
    def _recognition_network(self, weights, biases):
        # Generate probabilistic encoder (recognition network), which
        # maps inputs onto a normal distribution in latent space.
        # The transformation is parametrized and can be learned.
        layer_1 = self.transfer_fct(tf.add(tf.matmul(self.x, weights['h1']), 
                                           biases['b1'])) 
        layer_2 = self.transfer_fct(tf.add(tf.matmul(layer_1, weights['h2']), 
                                           biases['b2'])) 
        z_mean = tf.add(tf.matmul(layer_2, weights['out_mean']),
                        biases['out_mean'])
        z_log_sigma_sq =             tf.add(tf.matmul(layer_2, weights['out_log_sigma']), 
                   biases['out_log_sigma'])
        return (z_mean, z_log_sigma_sq)

    def _generator_network(self, weights, biases):
        # Generate probabilistic decoder (decoder network), which
        # maps points in latent space onto a Bernoulli distribution in data space.
        # The transformation is parametrized and can be learned.
        layer_1 = self.transfer_fct(tf.add(tf.matmul(self.z, weights['h1']), 
                                           biases['b1'])) 
        layer_2 = self.transfer_fct(tf.add(tf.matmul(layer_1, weights['h2']), 
                                           biases['b2'])) 
        x_reconstr_mean =             tf.nn.sigmoid(tf.add(tf.matmul(layer_2, weights['out_mean']), 
                                 biases['out_mean']))
        return x_reconstr_mean
            
    def _create_loss_optimizer(self):
        # The loss is composed of two terms:
        # 1.) The reconstruction loss (the negative log probability
        #     of the input under the reconstructed Bernoulli distribution 
        #     induced by the decoder in the data space).
        #     This can be interpreted as the number of "nats" required
        #     for reconstructing the input when the activation in latent
        #     is given.
        # Adding 1e-10 to avoid evaluation of log(0.0)
        reconstr_loss =             -tf.reduce_sum(self.x * tf.log(1e-10 + self.x_reconstr_mean)
                           + (1-self.x) * tf.log(1e-10 + 1 - self.x_reconstr_mean),
                           1)
        # 2.) The latent loss, which is defined as the Kullback Leibler divergence 
        ##    between the distribution in latent space induced by the encoder on 
        #     the data and some prior. This acts as a kind of regularizer.
        #     This can be interpreted as the number of "nats" required
        #     for transmitting the the latent space distribution given
        #     the prior.
        latent_loss = -0.5 * tf.reduce_sum(1 + self.z_log_sigma_sq 
                                           - tf.square(self.z_mean) 
                                           - tf.exp(self.z_log_sigma_sq), 1)
        self.cost = tf.reduce_mean(reconstr_loss + latent_loss)   # average over batch
        # Use ADAM optimizer
        self.optimizer =             tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.cost)
        
    def partial_fit(self, X):
        """Train model based on mini-batch of input data.
        
        Return cost of mini-batch.
        """
        opt, cost = self.sess.run((self.optimizer, self.cost), 
                                  feed_dict={self.x: X})
        return cost
    
    def transform(self, X):
        """Transform data by mapping it into the latent space."""
        # Note: This maps to mean of distribution, we could alternatively
        # sample from Gaussian distribution
        return self.sess.run(self.z_mean, feed_dict={self.x: X})
    
    def generate(self, z_mu=None):
        """ Generate data by sampling from latent space.
        
        If z_mu is not None, data for this point in latent space is
        generated. Otherwise, z_mu is drawn from prior in latent 
        space.        
        """
        if z_mu is None:
            z_mu = np.random.normal(size=self.network_architecture["n_z"])
        # Note: This maps to mean of distribution, we could alternatively
        # sample from Gaussian distribution
        return self.sess.run(self.x_reconstr_mean, 
                             feed_dict={self.z: z_mu})
    
    def reconstruct(self, X):
        """ Use VAE to reconstruct given data. """
        return self.sess.run(self.x_reconstr_mean, 
                             feed_dict={self.x: X})
    
### Training function
def train(dataset, network_architecture, learning_rate=0.001,
          batch_size=1000, training_epochs=10, display_step=5):
    vae = VariationalAutoencoder(network_architecture, 
                                 learning_rate=learning_rate, 
                                 batch_size=batch_size)
    n_samples = dataset.train_num_examples() 
    
    # Training cycle
    for epoch in range(training_epochs):
        time_start = time.time()
        
        avg_cost = 0.
        total_batch = int(n_samples / batch_size)
        # Loop over all batches
        for i in range(total_batch):
            batch_xs = dataset.train_next_batch(batch_size) 
            
            # Fit training using batch data
            cost = vae.partial_fit(batch_xs)
            # Compute average loss
            avg_cost += cost / n_samples * batch_size
            
        # Display logs per epoch step
        time_end = time.time()
        
        if epoch % display_step == 0:
            print("Epoch:", '%04d ends -- ' % (epoch+1), 
                  "avg_cost=", "{:.9f}".format(avg_cost), " time:{:.2f} s".format(time_end-time_start))
    return vae


### Dataset wrapper
class Dataset:
    def __init__(self, X_train, X_test, random_state=None):
        self.x_train = X_train
        self.x_test = X_test
        self.random_state = random_state
      
    def train_num_examples(self):
        return len(self.x_train)

    def train_next_batch(self,batch_size):
        batch = self.x_train.sample(n=batch_size, replace=False, random_state = self.random_state)
        return batch
    
    def test_next_batch(self,batch_size):
        batch = self.x_test.sample(n=batch_size, replace=False, random_state = self.random_state)
        return batch


# ### Initialize and run
# 

# In[ ]:


dataset = Dataset(X_train_norm, X_val_norm, random_state=None)

network_architecture =     dict(n_input=432,  # input dimension
         n_hidden_recog_1=216, # 1st layer encoder neurons
         n_hidden_recog_2=108, # 2nd layer encoder neurons
         n_z=54, # dimensionality of latent space
         n_hidden_gener_1=108, # 1st layer decoder neurons
         n_hidden_gener_2=216, # 2nd layer decoder neurons
        )  

vae = train(dataset, network_architecture, 
            training_epochs=70, learning_rate=5*10e-8,
            batch_size=1000,
            display_step=1)


# ### some notes:
# - when avg_cost gets as low as ~80, I get nan loss error

# ### Try to reconstruct data

# In[ ]:


x_val_notFraud = X_val_norm[X_val_norm.isFraud == 0]
x_val_fraud = X_val_norm[X_val_norm.isFraud == 1]

# Drop the label column
x_val_notFraud = x_val_notFraud.drop('isFraud', axis=1)
x_val_fraud = x_val_fraud.drop('isFraud', axis=1)

print(len(x_val_notFraud))
print(len(x_val_fraud))


# In[ ]:


def vis_reconstruct(df):
    np_arr = df.values
    x_reconstruct = vae.reconstruct(np_arr)

    plt.figure(figsize=(8, 12))
    for i in range(5):
        plt.subplot(5, 2, 2*i + 1)
        plt.imshow(np_arr[i].reshape(18, 24), cmap="viridis")
        plt.title("Test input")
        plt.colorbar()
        plt.subplot(5, 2, 2*i + 2)
        plt.imshow(x_reconstruct[i].reshape(18, 24), cmap="viridis")
        plt.title("Reconstruction")
        plt.colorbar()
    plt.tight_layout()


# In[ ]:


## Reconstruct isFraud == 0
vis_reconstruct(x_val_notFraud.head(1000))


# In[ ]:


## Reconstruct isFraud == 1
vis_reconstruct(x_val_fraud.head(1000))


# In[ ]:





# In[ ]:





# In[ ]:




