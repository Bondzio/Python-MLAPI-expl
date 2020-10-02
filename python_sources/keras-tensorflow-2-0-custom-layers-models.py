#!/usr/bin/env python
# coding: utf-8

# # From Keras to tf.keras and tf to tf 2.0: The Journey
# 
# Keras could be seen as a what we call the `Wrapper` of either `tensorflow`, `theano` or `CNTK` before the release of `tensorflow 2.0` but it's definition has changed since the rlease of `tf 2.0`. Keras was not in active development for quite some time and was not compatible with `python > 3.5` but a week ago or so, they have released a new version which is now compatible with `python >= 3.6`. 
# 
# # The Change:
# 
# `Tensorflow 2.0` is IMO, a complete shift as a lots of things have changed. I'd say that it has been for better specially for those who wanted to be somewhere between high level Keras for faster developments and  tensorflow for research and very high customization as `tf 2.0` provides both. So it won't be completly wrong to say that tf 2.0 and Keras are almost same today. We'll be looking at the aspect of building a custom Model and Layer using the tf 2.0 and Keras.
# 
# Aprt from that tensorflow has allowed the **Eager Execution** where you can see the results right away instad of building a static graph so that was an exclusiveness `PyTorch` **USED** to have. So it has become Build **and** run (how python works) instead of build **then** run (how c/c++ works).

# ## Layers
# Before we start, we need to note some important facts about layers:
# 
# 1. Each layer uses the `tf.keras.layers.Layer` as a parent class.
# 
# 2. There are weights associated with layers. These weights can be trainable or non-trainable according to your requirement.
# 
# 3. Every layer is initialized with initial weights and it can be any of the `tf.keras.initializers` such as `zeros`, `normal`, `ones` and the most widely used `glorot_uniform`.
# 
# 4. Layers can be recursively combined (inside one another). So the outer layer will depend on the weights of the inner layer.
# 
# 5. We need to have the understanding of the shape of Input coming to the layer and number of output neurons it'll give as an output. We usually do no know the shape so we use a method `build` to get the shape while forward pass.
# 
# 6. A layer may or not have the `loss function` or the `Regularization`. If there are any transformations  implemented in the layers, these have to be executed inside the `call`  (for forward pass) method.
# 
# 7. There are few methods that we can choose to apply. `__init__`  and `call` is a must and using the `build` method before initializing the weights is the best practice to follow in dynamic environments. `grt_config` and `from_config` are used if we want to serialize our layers (for saving).

# In[ ]:


import tensorflow as tf
from tensorflow.keras.layers import Layer
from tensorflow.keras import Model
from tensorflow.keras.activations import relu,sigmoid, softmax, tanh
from tensorflow.keras.initializers import glorot_normal



from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


# # Custom Layers

# In[ ]:


class CustomDense(Layer):
    '''
    Build custom layer mimicks the Dense Layer
    '''
    def __init__(self,units=128,initializer='glorot_uniform',activation=None,name=None,**kwargs):
        '''
        Constructor of the class
        args:
            units: {int} number of neurons in the layer
            initializer: {string or callable instance of tf.keras.initializers } initial weights
            activation: {callable instance of tf.keras.activations} activation function to use
            name: name of the layer {string}. There is already a name param in Base Class
            kwargs: keyword arguments of the base Layer Class
        '''
        super(CustomDense,self).__init__(**kwargs) # constructor of Base Layer class
        self.units = units # number of neurons
        self.activation = activation # activation function
        self.initializer = initializer # initializer
        if name: # it works but but you SHOUD NOT USE IT
            self._name = name
        
    def build(self,input_shape):
        '''
        method typically used to create the weights of Layer subclasses. During forward pass or call() model
        will automatically call the build method to get the shape of the input tensor
        args:
            input_shape: a tensor describing shape of input. it'll be passed automatically as input.shape
        '''
        self.w = self.add_weight(shape=(input_shape[-1],self.units),initializer=self.initializer,trainable=True)
        # add_weight is a method of Layer base class. input_shape[-1] gives number of features
        
        self.b = self.add_weight(shape=(self.units,),initializer=self.initializer,trainable=True)
        # add bias and set to trainable. NOTE: never forget to add a , after self.units as
        # (1) == int(1) but (1,) = tuple([1])

        
    def call(self,input_tensor):
        '''
        method to implement the forward pass
        args:
            input: input tensor
        '''
        result = tf.matmul(input_tensor,self.w)+self.b 
        # apply the formula y = wx + b in matric multiplication form
        
        if self.activation:
            result = self.activation(result) # apply activation function
            
        return result


# In[ ]:


layer = CustomDense(8,activation=softmax,name='my_layer')

# below code is to just create random tensor which will work as the input to the Layer
ini = tf.random_uniform_initializer()
tensor = ini((4,3)) # 4 data points with 3 attributes
tensor


# In[ ]:


print(layer(tensor)[0].numpy().sum())  
# to check if our model is outputting correct sigmoid as sum==1 for each row
layer(tensor)


# In[ ]:


layer.weights # weights and biases. we can access layer.b, layer.w individually too


# In[ ]:


layer.name  # layer._name works too. Not a Private variable as there are no private variables in Python


# ## Privilaged argument in the `Call()`
# There is a special argument  `training`  given for the call method. You can use the Boolean {True, False} for this option to use in Custom Layer to tell if the layer is working with Training or inference (results). For example, there are some methods where you can train differently and when you have to predict, a different strategy is used. For example you can dropout in the training.

# In[ ]:


class HypotheticalLayer(Layer):
    '''
    Build a random layer
    '''
    def __init__(self,units=4,initializer='glorot_uniform',drop_rate=0.23,**kwargs):
        super(HypotheticalLayer,self).__init__(**kwargs) # constructor of Base Layer class
        self.units = units # number of neurons
        self.initializer = initializer # initializer
        self.drop_rate = drop_rate
        
        
    def build(self,input_shape):
        
        self.w = self.add_weight(shape=(input_shape[-1],self.units),initializer=self.initializer,trainable=True)
        
        self.b = self.add_weight(shape=(self.units,),initializer=self.initializer,trainable=True)
   
        
    def call(self,input_tensor,training=False):
        '''
        method to implement the forward pass with training parm
        args:
            input: input tensor
            training: {bool} whether the layer is in training phase or not
        '''
        result = tf.matmul(input_tensor,self.w)+self.b 
        
        if training:
            result = tf.nn.dropout(result,rate=self.drop_rate) # apply dropout
            
        return result


# In[ ]:


hypo_layer = HypotheticalLayer(drop_rate=0.33)
hypo_layer(tensor,training=True) # uses the call method. Apply dropout randomly to 33%


# In[ ]:


hypo_layer(tensor) # default training=False


# ## Nested Layers
# We'll try to build a layer composed of multiple `CustomDense` layers with activation associated with each. 
# Just for the demonstration purpose, we'll cover multiple scenario of how can we initialise our `CustomLayer`

# In[ ]:


class NestedDense(Layer):
    '''
    Build nested layer made of multiple CustomDense layer
    '''
    def __init__(self,l1_unit=8,l2_unit=8,l2_units=4,**kwargs):
        '''
        Constructor of the class
        args:
            l1_units, l2_units, l3_units = no of neurons in the 3 sub layers
            kwargs: keyword arguments of the base Layer Class
        '''
        super(NestedDense,self).__init__(**kwargs) # constructor of Base Layer class
        
        self.l1 = CustomDense(l1_unit,initializer=glorot_normal) # no activation, callable initializer
        self.l2 = CustomDense(l2_units,initializer='ones',activation=relu) 
        # relu activation, he_uniform initializer
        self.l3 = CustomDense(l1_unit) # no activation. default initializer

        
    def call(self,input_tensor):
        '''
        method to implement the forward pass
        args:
            input: input tensor
        '''
        x = self.l1(input_tensor) # layer 1 
        x = tanh(x) # as we had no activation function in layer 1
        
        x = self.l2(x) # pass to layer 2. we have a default activation as relu
        
        x = self.l3(x) # for our hypothetical work, we do not need any activation for output
            
        return x


# In[ ]:


nested_dense = NestedDense()
nested_dense(tensor)


# In[ ]:


nested_dense.weights # layer has weights of all the layers


# ## Serialising Layers
# When we want to save the layer and use later, we need to use the `get_config()` from the **Parent** or Super Class. `get_config()` needs some configuration such as number of units or other parameters.

# In[ ]:


class SerializableLayer(Layer):
    '''
    Build custom layer mimicks the Dense Layer which can noe be serialised or saved
    '''
    def __init__(self,units=128,initializer='glorot_uniform',activation=None,**kwargs):
        super(SerializableLayer,self).__init__(**kwargs) 
        self.units = units
        self.activation = activation 
        self.initializer = initializer 
        
    def build(self,input_shape):
        
        self.w = self.add_weight(shape=(input_shape[-1],self.units),initializer=self.initializer,trainable=True)
       
        self.b = self.add_weight(shape=(self.units,),initializer=self.initializer,trainable=True)
        

        
    def call(self,input_tensor):
        '''
        method to implement the forward pass
        args:
            input: input tensor
        '''
        result = tf.matmul(input_tensor,self.w)+self.b 
        
        if self.activation:
            result = self.activation(result)
        
        return result
            
            
    def get_config(self):
        '''
        Get the configuration of the layer so that you can serialise the layer for further use
        '''
        config = super(SerializableLayer,self).get_config() # get the configuration from the Base Layer
        config.update({'units':self.units,'initializer':self.initializer})
        return config


# In[ ]:


layer = SerializableLayer(units=12,**{'name':'s_l_default'}) 
# see the working of name. this 'name' parameter is from the base Layer class.
print(layer.name)
config = layer.get_config()
print(config)


# In[ ]:


new_layer = SerializableLayer.from_config(config) # make an exact copy of the above layer
new_layer.get_config()


# # Custom Models
# In general, we will use the `Layer` class to define inner computation blocks, and will use the `Model` class to define the outer **model -- the object we will train.**
# 
# For instance, in a `ResNet50` model, we have **several ResNet blocks subclassing Layer, and a single Model encompassing the entire ResNet50 network.**
# 
# The Model class has the same API as Layer, with the following differences:
# 
# 1. It exposes built-in training, evaluation, and prediction loops (`model.fit()`, `model.evaluate()`, `model.predict()`).
# 2. It exposes the list of its inner layers, via the `model.layers` property.
# 3. It exposes saving and serialization APIs (`save()`, `save_weights()`...)
# 
# -[from tf documentation](https://www.tensorflow.org/guide/keras/custom_layers_and_models#the_model_class)

# In[ ]:


class ClassificationModel(Model):
    '''
    A model that performs simple classification where each input can belong to Only 1 class
    '''
    def __init__(self,input_shape,num_dense_layers=1,units=8,classes=2,activation='relu',**kwargs):
        '''
        Constructor of the class to get initial arguments
        args:
            input_shape = {tuple} shape of incoming data
            num_dense_layers: {int} number of dense layers to include in the classification
            units: {int} units to use for each layer
            classes: {int} Number of classes either binary or multiclass
            activation = {string/callable} activation function to use
        '''
        super(ClassificationModel,self).__init__(**kwargs)
        
        assert num_dense_layers>=1 , "number of layers must be >=1"
        assert units>=1 , "units must be >=1"
        assert classes>=2, "classes must be >=2"
        
        self.in_shape = input_shape
        self.n_dense = num_dense_layers
        self.units = units
        self.classes = classes
        self.activation = activation
        
        
        self.in_layer = tf.keras.layers.Dense(self.units,input_shape=self.in_shape,
                                          activation=self.activation,kernel_initializer='glorot_uniform',)
        # input layer has Input_shape param
        
        
        self.middle_layers = [] # middle layers do not have Input_shape
        for i in range(1,self.n_dense-1):
            self.middle_layers.append(tf.keras.layers.Dense(self.units,activation=self.activation,
                                                     kernel_initializer='glorot_uniform',))
            
        if self.classes == 2:
            self.out_layer = tf.keras.layers.Dense(1,activation='sigmoid',
                                                   kernel_initializer='glorot_uniform',)
        else:
            self.out_layer = tf.keras.layers.Dense(self.classes,activation='softmax',
                                            kernel_initializer='glorot_uniform')
            
        
    def call(self,tensor):
        '''
        Perform a forward pass operation
        '''
        x = self.in_layer(tensor)

        for layer in self.middle_layers:
            x = layer(x)

        probs = self.out_layer(x)

        return probs


# In[ ]:


model = ClassificationModel(tensor.shape,3,8,2) # 3 layers with 8 units each and binary classification
model.layers


# In[ ]:


# model.summary() won't work without a fit() or build() method. we can pass in a tensor as a workaround
probs = model(tensor)
model.summary()


# # Custom Model with Custom Layers
# Now, We'll build a Custom Model with custom Layers in it. We'll add a few given layers such as Dropout too to get an understanding that we can mix and match the layers.

# In[ ]:


class FullyConnected(Layer):
    '''
    Fully Connected or Dense layer 
    '''
    def __init__(self,units=16,w_init='he_uniform',b_init='zeros',activation=None,**kwargs):
        '''
        Constructor of the class
        args:
            units: {int} number of neurons to use
            w_init = {string/callable} weight initializer
            b_init = {string/callable/None} bias initializer. None if no bias is included
            activation: {string} activation function to use
            **kwargs: {dict} keyword arg for the parent class
        '''
        super(FullyConnected,self).__init__(**kwargs)
        self.units = units
        self.w_init = w_init
        self.b_init = b_init
        self.activation = tf.keras.activations.get(activation) # gives a respective callable. None gives linear
        
        
    def build(self,input_shape):
        '''
        Assign weights to the layer dynamically. Base layer method
        '''
        self.w = self.add_weight(shape=(input_shape[-1],self.units),initializer=self.w_init,trainable=True)
        if self.b_init:
            self.b = self.add_weight(shape=(self.units,),initializer=self.b_init,trainable=True)
        
    
    def call(self,input_tensor):
        '''
        Forward Pass. Part of Base layer
        '''
        result = tf.matmul(input_tensor,self.w)
        if self.b_init:
            result = result + self.b
            
        if self.activation:
            result = self.activation(result)
        return result
    
    
    def compute_output_shape(self,input_shape):
        '''
        Method of base class which computes the shape of output. 
        compute_output_shape is not needed unless the Layer is Dynamic
        args:
            input_shape: (tuple) shape of incoming tensor
        out:
            out_shape: (tuple)  shape of resulting tensor
        '''
        out_shape = list(input_shape) # because we can not append to tuple
        out_shape[-1] = self.units # replace the incoming feature dimension to outgoing
        return tuple(out_shape) # a tuple is needed for shape
    
    
    def get_config(self):
        config = super(FullyConnected,self).get_config() # get config of the base Layer class
        
        config.update({'units':self.units,'activation':tf.keras.activations.serialize(self.activation)})
        # you need to serialise the callable activation function
        
        return config  


# In[ ]:


class ClassificationModel(Model):
    '''
    A model that performs simple classification where each input can belong to Only 1 class
    '''
    def __init__(self,input_shape,layers_units=[8,],classes=2,activation='relu',**kwargs):
        '''
        Constructor of the class to get initial arguments
        args:
            input_shape = {tuple} shape of incoming data
            layer_units: {list} units to use for each layer
            classes: {int} Number of classes either binary or multiclass
            activation = {string/callable} activation function to use
        '''
        super(ClassificationModel,self).__init__(**kwargs)
        
        assert len(layers_units)>=1 , "units must be >=1"
        assert classes>=2, "classes must be >=2"
        
        self.in_shape = input_shape
        self.units = layers_units
        self.classes = classes
        self.activation = activation
        
        
        self.in_layer = FullyConnected(self.units[0],activation=self.activation,
                                       name='input_layer',
                                       input_shape=self.in_shape)
        # input_shape is a parameter of base class
        
        
        self.middle_layers = [] # middle layers do not have Input_shape
        for i in range(1,len(self.units)):
            self.middle_layers.append(FullyConnected(self.units[i],activation=self.activation))
            
            
        if self.classes == 2:
            self.out_layer = FullyConnected(1,activation='sigmoid',name='output_layer')
        else:
            self.out_layer = FullyConnected(self.classes,activation='softmax',name='output_layer')
            
        
    def call(self,tensor):
        '''
        Perform a forward pass operation
        '''
        x = self.in_layer(tensor)

        for layer in self.middle_layers:
            x = layer(x)

        probs = self.out_layer(x)

        return probs


# # Training Model
# You can train the above model with `keras.Dense()` layer or you can add `FullyConnected()` to `keras.Sequential()/keras.Model()` API too to check how is it performing. We'll train our custom model using our custom layer to classify the wine dataset. It is a multi (3) class classification. 

# In[ ]:


wine = load_wine()
X = wine['data']
y = wine['target']

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=13)


# In[ ]:


model = ClassificationModel(input_shape=X_train.shape,layers_units=[64,32,32],classes=3,activation='relu')


model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.0001),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
# you can also pass all the parameters as callable

model.layers


# In[ ]:


history = model.fit(X_train,y_train,epochs=300,validation_data=(X_test,y_test),batch_size=32)


# In[ ]:


model.summary()


# In[ ]:


plt.style.use('seaborn')
f,ax = plt.subplots(1,2,figsize=(15,6))

ax[0].plot(history.history['val_loss'],label='Validation Loss')
ax[0].plot(history.history['loss'],label='Training Loss')
ax[0].set_title('Losses',weight='bold',size='x-large')
ax[0].set_xlabel('Epoch',size='large')
ax[0].set_ylabel('Loss',size='large')
ax[0].legend()

ax[1].plot(history.history['val_accuracy'],label='Validation Accuracy')
ax[1].plot(history.history['accuracy'],label='Training Accuracy')
ax[1].set_title('Accuracies',weight='bold',size='x-large')
ax[1].set_xlabel('Epoch',size='large')
ax[1].set_ylabel('Accuracy',size='large')
ax[1].legend()

plt.show()


# # End Notes
# There is a lot more that the `tf 2.0` offers you while building custom layers and models including **metrics**, **losses** and much more inside the layers. Please refer more at the official documentation. Hope you enjoyed reading. Good Luck with your journey.
