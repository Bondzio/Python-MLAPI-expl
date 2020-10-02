#!/usr/bin/env python
# coding: utf-8

# # Convolutional Fast Sliding Window

# Using a "classical" sliding window is not effective, because we have to pass every sub-image to our CNN. With that approach we would compute things over and over again, as it is highly duplicative. Instead we can share the computation and get rid of the redundant calculations. This is called *convolutional sliding window*.
# 
# The idea is used in state of the art *Single Shot Detectors* like *Yolo, SSD*. These are called single shot, because it does the computation in 1 step not like region proposal methods which first proposes locations and only then classify it.
# 
# This is just a toy example of how it works, so take everything with a grain of salt. :)

# (I've hidden a few longer functions which only serve as utils, to keep you focused on the algorithm and not those little util functions)

# In[ ]:


import numpy as np
import pandas as pd
import cv2
from tqdm import tqdm

from keras.layers import Dense, Conv2D, MaxPooling2D, InputLayer, Flatten, Dropout, Activation, Input, UpSampling2D
from keras.models import Sequential
from keras.optimizers import Adam
from keras import backend as K
from keras.activations import softmax
from keras.utils import to_categorical
from keras.losses import categorical_crossentropy
from keras.callbacks import EarlyStopping

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import animation

from IPython.display import HTML


# ## Prepare data

# In[ ]:


train_df = pd.read_csv("../input/fashion-mnist_train.csv", index_col=0, header=0)


# In[ ]:


train_df.head()


# In[ ]:


def aug_top(image, f=False):
    s = image.shape[1] // 2
    new_image = np.zeros_like(image)
    part_of_image = image[int(s*np.random.uniform(1, 1.7)):, :]
    new_image[0:part_of_image.shape[0], 0:part_of_image.shape[1]] = part_of_image
    if f:
        new_image = cv2.flip(new_image, 0)
    return new_image

def aug_left(image, f=False):
    s = image.shape[0] // 2
    new_image = np.zeros_like(image)
    part_of_image = image[:, int(s*np.random.uniform(1, 1.7)):]
    new_image[0:part_of_image.shape[0], 0:part_of_image.shape[1]] = part_of_image
    if f:
        new_image = cv2.flip(new_image, 1)
    return new_image

def aug(image):
    flip = np.random.choice([False, True])
    aug_type = np.random.choice([0, 1, 2])
    if aug_type == 0:
        aug_image = aug_top(image, flip)
    elif aug_type == 1:
        aug_image = aug_left(image, flip)
    elif aug_type == 2:
        aug_image_1 = aug_top(image, False)
        aug_image_2 = aug_top(image, True)
        half_height = image.shape[0] // 2
        aug_image = np.zeros_like(image)
        aug_image[0:half_height, :] = aug_image_1[0:half_height, :]
        aug_image[half_height:, :] = aug_image_2[half_height:, :]
    return aug_image


# In[ ]:


test_image = x_train[12]

fig, axs = plt.subplots(1, 4)
axs[0].imshow(aug(test_image))
axs[1].imshow(aug(test_image))
axs[2].imshow(aug(test_image))
axs[3].imshow(aug(test_image))


# In[ ]:


x_train = train_df.values
x_train = x_train.reshape(x_train.shape[0], 28, 28)
x_train = x_train.astype(np.float32) / 255.0


# In[ ]:


y_train = train_df.index.values


# In[ ]:


nb_of_images_for_aug = 1000

augmentation_image_indexes = np.arange(len(x_train), dtype=int)
np.random.shuffle(augmentation_image_indexes)
augmentation_image_indexes = augmentation_image_indexes[:nb_of_images_for_aug]


# In[ ]:


for i in tqdm(augmentation_image_indexes):
    aug_image = aug(x_train[i])
    x_train = np.vstack((x_train, np.expand_dims(aug_image, 0)))
    y_train = np.hstack((y_train, [10]))


# In[ ]:


nb_of_classes = len(np.unique(y_train))


# In[ ]:


x_train.shape


# In[ ]:


y_train = to_categorical(y_train, nb_of_classes)


# ## Creating the model

# This is just an toy  model I've put together. The only thing I cared about here is that for inputs like `(28x28) grayscale` images  the output should be `(1x1x10)`. This is how I "converted" the last fully connected layers to convolutional.
# 
# Then the real input of the model as you can see is `(None, None, 1)`. This is because that way it accepts any dimensional images (should be greater than 28x28).
# 
# You can learn more about this conversion from [here](https://www.coursera.org/lecture/convolutional-neural-networks/convolutional-implementation-of-sliding-windows-6UnU4)

# In[ ]:


model = Sequential()
# (rows, cols, channels)
model.add(InputLayer((None, None, 1)))

model.add(Conv2D(32, (5, 5), activation="relu"))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(32, (3, 3), activation="relu"))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(800, (5, 5), activation="relu"))
model.add(Conv2D(800, (1, 1), activation="relu"))

model.add(Conv2D(nb_of_classes, (1, 1), activation="softmax"))


# In[ ]:


model.summary()


# In[ ]:


model.compile(loss=categorical_crossentropy, optimizer=Adam(), metrics=['accuracy'])


# In[ ]:


hist = model.fit(np.expand_dims(x_train, 3),
                 np.expand_dims(np.expand_dims(y_train, 1), 1),
                 epochs=32,
                 batch_size=32,
                 validation_split=0.15,
                 callbacks=[EarlyStopping(monitor="val_loss", patience=5)],
                 verbose=1)


# ## Test the model & Playground

# In[ ]:


# Only above this threshold we count somethig as "detected"
CONFIDENCE_LEVEL = 0.95


# ### Test on single images

# At first I try it on single images (first 4 image), so our output should be `(4, 1, 1, 10)` as we have 4 predictions with shape `(1, 1, 10)`

# In[ ]:


pred = model.predict(np.expand_dims(x_train[:4], 3))


# In[ ]:


pred_labels = np.argmax(pred, 3).flatten()
pred_conf = np.max(pred, 3).flatten()


# In[ ]:


fig = plt.figure(figsize=(10, 4))

for i, (label, conf, img) in enumerate(zip(pred_labels, pred_conf, x_train[:4])):
    ax = fig.add_subplot(1, len(pred_labels), i+1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Pred: {0} | Conf: {1:.2f}".format(label, conf))
    ax.imshow(img)


# ### Test on combined multiple images

# Now, I'll make a bigger image by combining a few together and test the network on it

# In[ ]:


black_image = np.zeros_like(x_train[0])


# In[ ]:


tmp_1 = np.concatenate((x_train[1], black_image), axis=1)
tmp_2 = np.concatenate((black_image, x_train[3]), axis=1)
test_image = np.concatenate((tmp_1, tmp_2), axis=0)


# In[ ]:


test_image_display = (test_image*255).astype(np.uint8)
test_image_h, test_image_w = test_image_display.shape[:2]


# In[ ]:


plt.imshow(test_image_display);


# In[ ]:


test_image.shape


# As we have `56x56` image,  and we slide the `28x28` size window with stride `(4, 4)` we should get an output `(8x8x10)`. This means we have a `8x8` grid from the image and for every cell's depth the probabilities for all the classes.

# \begin{equation}
#     \text{pred} = 
#     \begin{bmatrix}
#         p_{1,1} & p_{1,2} & \dots  & p_{1,8} \\
#         p_{2,1} & p_{2,2} & \dots  & p_{2, 8} \\
#         \vdots & \vdots & \ddots & \vdots \\
#         p_{8,1} & p_{8,2} & \dots  & p_{8, 8}
#     \end{bmatrix}
#     , \qquad \text{where} \quad p_{i,j} = \left( prob_{class_1}, prob_{class_2}, \ldots, prob_{class_{10}} \right)
# \end{equation}

# In[ ]:


pred = model.predict(np.expand_dims(np.expand_dims(test_image, 2), 0))[0]


# In[ ]:


pred.shape


# In[ ]:


predictions_per_location = np.argmax(pred, 2)
predictions_confidences_per_location = np.max(pred, 2)


# At the image below we can see all the cell's predictions and the confidences. As I said, every cell here defines a `(x, y, x+28, y+28)` location on the original image.
# 
# First one is `(0, 0, 28, 28)` then the second is `(4, 0, 32, 28)`

# In[ ]:


fig = plt.figure()

ax = fig.add_subplot(1, 1, 1)
ax.set_title("Predictions w/ confidence heatmap for each grid cell location", y=1.1)
ax.set_xticks(np.arange(0, 8))
ax.set_yticks(np.arange(0, 8))
ims_conf = ax.imshow(predictions_confidences_per_location)
for i in range(0, predictions_confidences_per_location.shape[0]):
    for j in range(0, predictions_confidences_per_location.shape[0]):
        text_color = "black"
        ax.text(j, i,
                 predictions_per_location[i, j],
                 horizontalalignment="center",
                 verticalalignment="center",
                 color=text_color)
fig.colorbar(ims_conf, ax=ax);


# In[ ]:


def extract_locations(image, window_shape=(28, 28), step=4):
    w_h, w_w = window_shape
    i_h, i_w = image.shape[:2]
    
    rects = []
    sub_images = []
    
    for i, y in enumerate(range(0, i_h+2-w_h, step)):
        for j, x in enumerate(range(0, i_w+2-w_w, step)):
            rects.append((x, y, x+w_h, y+w_w))
            sub_image = image[y:y+w_h, x:x+w_w]
            sub_images.append(sub_image)
    
    return np.array(rects), np.array(sub_images)


# In[ ]:


location_rects, sub_images = extract_locations(test_image_display, step=4)


# In[ ]:


len(location_rects)


# In[ ]:


fig = plt.figure(figsize=(10, 4))

ax1 = fig.add_subplot(1, 3, 1)
ax1.set_title("Sliding Window")
ims_sliding_window = ax1.imshow(test_image_display)

ax2 = fig.add_subplot(1, 3, 2)
ax2.set_title("Sub Image")
ims_sub_image = ax2.imshow(sub_images[0])

ax3 = fig.add_subplot(1, 3, 3)
ax3.set_title("Prediction w/ confidence")
ax3.imshow(np.zeros((test_image_h, test_image_w), dtype=np.uint8))
text_prediction = ax3.text(test_image_w//2, 20, "0", horizontalalignment='center', verticalalignment='center', size=25, color="white")
test_confidence = ax3.text(test_image_w//2, 40, "0", horizontalalignment='center', verticalalignment='center', size=20, color="white")

plt.close()

def animate(i):
    new_sliding_widndow_image = cv2.rectangle(test_image_display.copy(), tuple(location_rects[i][:2]),
                                              tuple(location_rects[i][2:]), 255, 1)
    ims_sliding_window.set_data(new_sliding_widndow_image)
    
    ims_sub_image.set_data(sub_images[i])
    
    pred_conf = np.round(np.max(pred, 2).flatten()[i], 3)
    text_prediction.set_text(np.argmax(pred, 2).flatten()[i])
    test_confidence.set_text(pred_conf)
    
    if pred_conf < CONFIDENCE_LEVEL:
        text_prediction.set_color("red")
    else:
        text_prediction.set_color("green")
    
    return ims_sliding_window, ims_sub_image, text_prediction, test_confidence


# In[ ]:


anim = animation.FuncAnimation(fig, animate, frames=len(location_rects), interval=300, blit=True)


# In[ ]:


def show_animation_kaggle(animation):
    import tempfile
    import io
    import base64
    import os
    
    with tempfile.NamedTemporaryFile(suffix="_anim.gif") as tmp:
        file_name = tmp.name
    anim.save(file_name, writer='imagemagick')
    video = io.open(file_name, 'r+b').read()
    encoded = base64.b64encode(video)
    data = '''<img src="data:image/gif;base64,{0}" type="gif" />'''.format(encoded.decode('ascii'))
    os.remove(file_name)
    return HTML(data=data)


# In[ ]:


show_animation_kaggle(anim)


# ## Visualize Confident Predictions

# In[ ]:


indexes_to_keep = np.where(predictions_confidences_per_location.flatten() > CONFIDENCE_LEVEL)
# These are the confidences and bounding boxes we want to keep for the detection
confident_confidences = predictions_confidences_per_location.flatten()[indexes_to_keep]
confident_locations = location_rects[indexes_to_keep]
confident_predictions_labels = predictions_per_location.flatten()[indexes_to_keep]


# In[ ]:


def draw_predictions(image, locations, color=(255, 0, 0)):
    tmp_image = image.copy()
    for loc in locations:
        p1 = tuple(loc[:2])
        p2 = tuple(loc[2:])
        tmp_image = cv2.rectangle(tmp_image, p1, p2, color, 1)
    return tmp_image


# In[ ]:


detection_conf_loc_image = cv2.cvtColor(test_image_display.copy(), cv2.COLOR_GRAY2BGR)
detection_conf_loc_image = draw_predictions(detection_conf_loc_image, confident_locations)


# In[ ]:


plt.imshow(detection_conf_loc_image);


# ### Apply NMS

# In[ ]:


def box_area(box):
    x1, y1, x2, y2 = box
    return (x2 - x1) * (y2 - y1)

def box_intersection_area(a, b):
    a_xmin, a_ymin, a_xmax, a_ymax = a
    b_xmin, b_ymin, b_xmax, b_ymax = b
    
    dx = min(a_xmax, b_xmax) - max(a_xmin, b_xmin)
    dy = min(a_ymax, b_ymax) - max(a_ymin, b_ymin)

    if (dx>=0) and (dy>=0):
        return dx*dy
    
    raise ValueError("Boxes have no intersection")

def calulate_iou(box_1, other_boxes):
    ious = []
    for box_2 in other_boxes:
        try:
            intersection_area = box_intersection_area(box_1, box_2)
        except ValueError:
            # No intersection
            ious.append(0)
            continue
        iou = intersection_area / (box_area(box_1) + box_area(box_2) - intersection_area)
        ious.append(iou)
    return np.array(ious)
    
def nms(boxes, confidences, iou_threshold=0.5):
    if len(boxes) < 2:
        return boxes

    sort_index = np.argsort(confidences)[::-1]
    boxes = boxes[sort_index]
    confidences = confidences[sort_index]

    final_boxes = [boxes[0]]
    
    for box in boxes:
        iou_array = calulate_iou(box, final_boxes)
        overlap_idxs = np.where(iou_array > iou_threshold)[0]
        if len(overlap_idxs) == 0:
            final_boxes.append(box)
    return final_boxes

def nms_multiclass(prediction_labels, boxes, confidences, iou_threshold=0.5):
    unique_labels = np.unique(prediction_labels)
    pred_dict_after_nms = {}
    for label in unique_labels:
        class_specific_indexes = np.where(prediction_labels == label)
        class_boxes = boxes[class_specific_indexes]
        class_confidences = confidences[class_specific_indexes]
        
        kept_boxes = nms(class_boxes, class_confidences, iou_threshold)
        
        pred_dict_after_nms[label] = kept_boxes
    return pred_dict_after_nms
        


# In[ ]:


locations_after_nms_dict = nms_multiclass(confident_predictions_labels, confident_locations, confident_confidences, 0.1)


# In[ ]:


detection_after_nms_image = cv2.cvtColor(test_image_display.copy(), cv2.COLOR_GRAY2BGR)
colors = [(255, 0, 0),
          (0, 255, 0),
          (0, 0, 255),
          (255, 255, 0),
          (255, 0, 255),
          (0, 255, 255),
          (127, 0, 0),
          (0, 127, 0),
          (0, 0, 127),
          (127, 0, 127)]
for i, (label, bboxes) in enumerate(locations_after_nms_dict.items()):
    detection_after_nms_image = draw_predictions(detection_after_nms_image, bboxes, colors[i])


# In[ ]:


plt.imshow(detection_after_nms_image);


# As you can see the problem here, is that after the confidence level thresholding and NMS, we still have a lot of detected locations. One way of to get rid of these is, to create a new class like background, and create training data with from the original, like cropped tshirts, etc... They those would be detected too and we could ignore them. Right now, our classifier is too certain about things that does not exists.
