#!/usr/bin/env python
# coding: utf-8

# # Pre-trained computer vision model transfer learning with tensorFlow Hub
# 
# 

# [TensorFlow Hub](http://tensorflow.org/hub) is a way to share pretrained model components. See the [TensorFlow Module Hub](https://tfhub.dev/) for a searchable listing of pre-trained models. This tutorial demonstrates:
# 
# 1. How to use TensorFlow Hub with `tf.keras`.
# 1. How to do image classification using TensorFlow Hub.
# 1. How to do simple transfer learning.

# ## Setup

# In[ ]:


from __future__ import absolute_import, division, print_function, unicode_literals
import matplotlib.pylab as plt


# In[ ]:


#!pip install tf-nightly-gpu
get_ipython().system('pip install tensorflow-gpu')
get_ipython().system('pip install tensorflow-hub')
from tensorflow.keras import layers
import tensorflow as tf
import tensorflow_hub as hub


# ### Download the classifier
# 
# Use `hub.module` to load a mobilenet, and `tf.keras.layers.Lambda` to wrap it up as a keras layer. Any [TensorFlow 2 compatible image classifier URL](https://tfhub.dev/s?q=tf2&module-type=image-classification) from tfhub.dev will work here.

# In[ ]:


classifier_url ="https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/2" #@param {type:"string"}


# In[ ]:


IMAGE_SHAPE = (224, 224)

classifier = tf.keras.Sequential([
    hub.KerasLayer(classifier_url, input_shape=IMAGE_SHAPE+(3,))
])


# ### Run it on a single image

# Download a single image to try the model on.

# In[ ]:


import numpy as np
import PIL.Image as Image

grace_hopper = tf.keras.utils.get_file('image.jpg','https://storage.googleapis.com/download.tensorflow.org/example_images/grace_hopper.jpg')
grace_hopper = Image.open(grace_hopper).resize(IMAGE_SHAPE)
grace_hopper


# In[ ]:


grace_hopper = np.array(grace_hopper)/255.0
grace_hopper.shape


# Add a batch dimension, and pass the image to the model.

# In[ ]:


result = classifier.predict(grace_hopper[np.newaxis, ...])
result.shape


# The result is a 1001 element vector of logits, rating the probability of each class for the image.
# 
# So the top class ID can be found with argmax:

# In[ ]:


predicted_class = np.argmax(result[0], axis=-1)
predicted_class


# ### Decode the predictions
# 
# We have the predicted class ID,
# Fetch the `ImageNet` labels, and decode the predictions

# In[ ]:


labels_path = tf.keras.utils.get_file('ImageNetLabels.txt','https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
imagenet_labels = np.array(open(labels_path).read().splitlines())


# In[ ]:


plt.imshow(grace_hopper)
plt.axis('off')
predicted_class_name = imagenet_labels[predicted_class]
_ = plt.title("Prediction: " + predicted_class_name.title())


# ## Simple transfer learning

# Using TF Hub it is simple to retrain the top layer of the model to recognize the classes in our dataset.

# ### Dataset
# 
#  For this example you will use the TensorFlow flowers dataset:

# In[ ]:


data_root = tf.keras.utils.get_file(
  'flower_photos','https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',
   untar=True)


# The simplest way to load this data into our model is using `tf.keras.preprocessing.image.ImageDataGenerator`,
# 
# All of TensorFlow Hub's image modules expect float inputs in the `[0, 1]` range. Use the `ImageDataGenerator`'s `rescale` parameter to achieve this.
# 
# The image size will be handled later.

# In[ ]:


image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)
image_data = image_generator.flow_from_directory(str(data_root), target_size=IMAGE_SHAPE)


# The resulting object is an iterator that returns `image_batch, label_batch` pairs.

# In[ ]:


for image_batch, label_batch in image_data:
  print("Image batch shape: ", image_batch.shape)
  print("Label batch shape: ", label_batch.shape)
  break


# ### Run the classifier on a batch of images

# Now run the classifier on the image batch.

# In[ ]:


result_batch = classifier.predict(image_batch)
result_batch.shape


# In[ ]:


predicted_class_names = imagenet_labels[np.argmax(result_batch, axis=-1)]
predicted_class_names


# Now check how these predictions line up with the images:

# In[ ]:


plt.figure(figsize=(10,9))
plt.subplots_adjust(hspace=0.5)
for n in range(30):
  plt.subplot(6,5,n+1)
  plt.imshow(image_batch[n])
  plt.title(predicted_class_names[n])
  plt.axis('off')
_ = plt.suptitle("ImageNet predictions")


# The results are far from perfect, but reasonable considering that these are not the classes the model was trained for (except "daisy").

# ### Download the headless model
# 
# TensorFlow Hub also distributes models without the top classification layer. These can be used to easily do transfer learning.
# 
# Any [Tensorflow 2 compatible image feature vector URL](https://tfhub.dev/s?module-type=image-feature-vector&q=tf2) from tfhub.dev will work here.

# In[ ]:


feature_extractor_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/2" #@param {type:"string"}


# Create the feature extractor.

# In[ ]:


feature_extractor_layer = hub.KerasLayer(feature_extractor_url,
                                         input_shape=(224,224,3))


# It returns a 1280-length vector for each image:

# In[ ]:


feature_batch = feature_extractor_layer(image_batch)
print(feature_batch.shape)


# Freeze the variables in the feature extractor layer, so that the training only modifies the new classifier layer.

# In[ ]:


feature_extractor_layer.trainable = False


# ### Attach a classification head
# 
# Now wrap the hub layer in a `tf.keras.Sequential` model, and add a new classification layer.

# In[ ]:


model = tf.keras.Sequential([
  feature_extractor_layer,
  layers.Dense(image_data.num_classes, activation='softmax')
])

model.summary()


# In[ ]:


predictions = model(image_batch)


# In[ ]:


predictions.shape


# ### Train the model
# 
# Use compile to configure the training process:

# In[ ]:


model.compile(
  optimizer=tf.keras.optimizers.Adam(),
  loss='categorical_crossentropy',
  metrics=['acc'])


# Now use the `.fit` method to train the model.
# 
# To keep this example short train just 2 epochs. To visualize the training progress, use a custom callback to log the loss and accuracy of each batch individually, instead of the epoch average.

# In[ ]:


class CollectBatchStats(tf.keras.callbacks.Callback):
  def __init__(self):
    self.batch_losses = []
    self.batch_acc = []

  def on_train_batch_end(self, batch, logs=None):
    self.batch_losses.append(logs['loss'])
    self.batch_acc.append(logs['acc'])
    self.model.reset_metrics()


# In[ ]:


steps_per_epoch = np.ceil(image_data.samples/image_data.batch_size)
    
batch_stats_callback = CollectBatchStats()
    
history = model.fit_generator(image_data, epochs=2,
                              steps_per_epoch=steps_per_epoch,
                              callbacks = [batch_stats_callback])


# Now after, even just a few training iterations, it can already see that the model is making progress on the task.

# In[ ]:


plt.figure()
plt.ylabel("Loss")
plt.xlabel("Training Steps")
plt.ylim([0,2])
plt.plot(batch_stats_callback.batch_losses)


# In[ ]:


plt.figure()
plt.ylabel("Accuracy")
plt.xlabel("Training Steps")
plt.ylim([0,1])
plt.plot(batch_stats_callback.batch_acc)


# ### Check the predictions
# 
# To redo the plot from before, first get the ordered list of class names:

# In[ ]:


class_names = sorted(image_data.class_indices.items(), key=lambda pair:pair[1])
class_names = np.array([key.title() for key, value in class_names])
class_names


# Run the image batch through the model and convert the indices to class names.

# In[ ]:


predicted_batch = model.predict(image_batch)
predicted_id = np.argmax(predicted_batch, axis=-1)
predicted_label_batch = class_names[predicted_id]


# Plot the result

# In[ ]:


label_id = np.argmax(label_batch, axis=-1)


# In[ ]:


plt.figure(figsize=(10,9))
plt.subplots_adjust(hspace=0.5)
for n in range(30):
  plt.subplot(6,5,n+1)
  plt.imshow(image_batch[n])
  color = "green" if predicted_id[n] == label_id[n] else "red"
  plt.title(predicted_label_batch[n].title(), color=color)
  plt.axis('off')
_ = plt.suptitle("Model predictions (green: correct, red: incorrect)")


# ## Export your model
# 
# Now that model is trained, export it as a saved model:

# In[ ]:


import time
t = time.time()

export_path = "/tmp/saved_models/{}".format(int(t))
model.save(export_path)

export_path


# Now confirm that it can be reloaded it, and it still gives the same results:

# In[ ]:


reloaded = tf.keras.models.load_model(export_path, custom_objects={'KerasLayer':hub.KerasLayer})


# In[ ]:


result_batch = model.predict(image_batch)
reloaded_result_batch = reloaded.predict(image_batch)


# In[ ]:


abs(reloaded_result_batch - result_batch).max()


# This saved model can be loaded for inference later, or converted to [TFLite](https://www.tensorflow.org/lite/convert/) or [TFjs](https://github.com/tensorflow/tfjs-converter).
# 
# 
