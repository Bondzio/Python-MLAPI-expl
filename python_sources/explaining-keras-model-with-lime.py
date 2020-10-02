#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from keras.applications.inception_resnet_v2 import InceptionResNetV2, preprocess_input
from keras.models import load_model
from keras.preprocessing import image

from sklearn.preprocessing import LabelEncoder
import glob


# ## Loading Data (Train only)

# In[ ]:


# Load the labels:
labels = pd.read_csv('../input/geekhub-ds-2019-challenge/{}'.format('train_labels.csv'))

# Encoding:
le = LabelEncoder(); 
labels['Classes'] = le.fit_transform(labels['Category'])

# Show classes:
for i, c in enumerate(le.classes_): 
    print(i, '=', c)
    
# Load the Data:
anomaly_ids = {
    4, 6, 11, 30, 32, 78, 79, 107, 167, 178, 200, 231, 257, 261, 288, 374, 435, 451,
    462, 484, 561, 613, 711, 725, 750,  820, 843, 940, 974, 994, 974, 1037, 1169, 
    1207, 1217, 1269, 1271, 1306, 1337, 1365, 1368, 1378, 1427, 1437, 1468, 1587, 
    1610, 1659, 1685, 1722, 1759, 1830, 1834, 1859, 1871, 1893, 2011,  2119, 2135, 
    2198, 2203, 2308, 2366, 2370, 2453, 2460, 2461, 2520, 2525,  2543, 2461, 2520, 
    2525, 2552, 2606, 2616, 2621, 2635, 2666, 2708, 2733, 2753, 2764, 2829, 2922, 
    2990, 2977, 2937, 2651, 2912, 2720, 2765, 2821, 2947, 2977, 2195}
X = []
for image_path in np.sort(glob.glob('../input/geekhub-ds-2019-challenge/train/train'+"/*.jpg")):
    if int(image_path.split('/')[-1][:-4]) not in anomaly_ids:
        img = image.load_img(image_path, target_size=(299, 299))
        img_data = image.img_to_array(img)
        img_data = preprocess_input(img_data)
        X.append(img_data)

X = np.array(X)
y = labels.drop(anomaly_ids, axis=0).Classes.values

print('\nX_shape =', X.shape, '\ny_shape =', y.shape, 
      '\nShapes comformable =', X.shape[0] == y.shape[0])


# ## Loading Pre-Trained Model (Inception-ResNet V2)
# From https://www.kaggle.com/astrib/flowersnet (output).

# In[ ]:


model = load_model('../input/flowersnet/flowers_full_model.h5')


# Predicting our labes.

# In[ ]:


y_pred_train = model.predict(X)
bad_predictions = (y_pred_train.argmax(axis=1) != y)
print('Bad predictions:', sum(bad_predictions))


# ## LIME (Local Interpretable Model-Agnostic Explanations)

# In[ ]:


import lime
from lime import lime_image
from skimage.segmentation import mark_boundaries
import matplotlib.pyplot as plt
import random


# In[ ]:


explainer = lime_image.LimeImageExplainer(random_state=42)


# Explain 5 random bad predictions.

# In[ ]:


get_ipython().run_cell_magic('time', '', "fig, ax = plt.subplots(5, 6, sharex='col', sharey='row')\nfig.set_figwidth(20)\nfig.set_figheight(16)\nindecies = random.sample(range(sum(bad_predictions)), 5)\nfor j in range(5):\n    explanation = explainer.explain_instance(X[bad_predictions][indecies[j]], \n                                             model.predict, \n                                             top_labels=5, hide_color=0, num_samples=1000, \n                                             random_seed=42)\n    ax[j,0].imshow(X[bad_predictions][indecies[j]])\n    ax[j,0].set_title(le.classes_[y[bad_predictions][indecies[j]]])\n    for i in range(5):\n        temp, mask = explanation.get_image_and_mask(i, positive_only=True, \n                                                    num_features=5, hide_rest=True)\n        ax[j,i+1].imshow(mark_boundaries(temp / 2 + 0.5, mask))\n        ax[j,i+1].set_title('p({}) = {:.4f}'.format(le.classes_[i], y_pred_train[bad_predictions][indecies[j]][i]))")


# Explain 5 random predictions.

# In[ ]:


get_ipython().run_cell_magic('time', '', "fig, ax = plt.subplots(5, 6, sharex='col', sharey='row')\nfig.set_figwidth(20)\nfig.set_figheight(16)\nindecies = random.sample(range(X.shape[0]), 5)\nfor j in range(5):\n    explanation = explainer.explain_instance(X[indecies[j]], model.predict, \n                                             top_labels=5, hide_color=0, num_samples=1000, \n                                             random_seed=42)\n    ax[j,0].imshow(X[indecies[j]])\n    ax[j,0].set_title(le.classes_[y[indecies[j]]])\n    for i in range(5):\n        temp, mask = explanation.get_image_and_mask(i, positive_only=True, \n                                                    num_features=5, hide_rest=True)\n        ax[j,i+1].imshow(mark_boundaries(temp / 2 + 0.5, mask))\n        ax[j,i+1].set_title('p({}) = {:.4f}'.format(le.classes_[i], y_pred_train[indecies[j]][i]))")


# ## References
# 
# * **LIME** on GitHub [ [link](https://github.com/marcotcr/lime) ]
# * "Why Should I Trust You?": Explaining the Predictions of Any Classifier (Marco Tulio Ribeiro, Sameer Singh, Carlos Guestrin) [ [link](https://arxiv.org/abs/1602.04938) ]

# ## Other Kernels
# 
# * Eplaining XGB-Model with LIME **(tabular data)** [ [link](https://www.kaggle.com/yohanb/explaining-xgb-model-with-lime) ]
# * Explaining RF-Model with LIME **(text classifier)** [ [link](https://www.kaggle.com/yohanb/explaining-rf-model-with-lime) ] 
# 
