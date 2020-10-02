#!/usr/bin/env python
# coding: utf-8

# # Introduction

# I am going to introduce Mobilenet SSD face extractor. **It is better than MTCNN/same with MTCNN in accuracy, but still have a competitive speed** I am aware of dual shot detector is better, but it takes too long.
# 
# It is recommended by @harshit_sheoran. FYI, it is used in our best score kernel(0.34LB).

# In this kernel, it will be a clean version of that extractor extracting faces from frames. I also included the helper function to go over video(with error catch).

# **Here is the comparison to other face extractors[link](https://www.kaggle.com/unkownhihi/mobilenet-face-extractor-helper-code)**

# # Imports

# In[ ]:


import sys
import matplotlib.pyplot as plt
import cv2
import time
import tensorflow as tf
import numpy as np


# # Initialize Mobilenet Face Extractor

# In[ ]:


import tensorflow as tf
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with tf.io.gfile.GFile('../input/mobilenet-face/frozen_inference_graph_face.pb', 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
        config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth = True
    sess=tf.compat.v1.Session(graph=detection_graph, config=config)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    boxes_tensor = detection_graph.get_tensor_by_name('detection_boxes:0')    
    scores_tensor = detection_graph.get_tensor_by_name('detection_scores:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')


# # Helper Fuction

# In[ ]:


def get_mobilenet_face(image):
    global boxes,scores,num_detections
    (im_height,im_width)=image.shape[:-1]
    imgs=np.array([image])
    (boxes, scores) = sess.run(
        [boxes_tensor, scores_tensor],
        feed_dict={image_tensor: imgs})
    max_=np.where(scores==scores.max())[0][0]
    box=boxes[0][max_]
    ymin, xmin, ymax, xmax = box
    (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                ymin * im_height, ymax * im_height)
    left, right, top, bottom = int(left), int(right), int(top), int(bottom)
    return (left, right, top, bottom)
def crop_image(frame,bbox):
    left, right, top, bottom=bbox
    return frame[top:bottom,left:right]
def get_img(frame):
    return cv2.resize(crop_image(frame,get_mobilenet_face(frame)),(160,160))


# In[ ]:


def detect_video(video):
    capture = cv2.VideoCapture(video)
    v_len = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_idxs = np.linspace(0,v_len,frame_count, endpoint=False, dtype=np.int)
    imgs=[]
    i=0
    for frame_idx in range(int(v_len)):
        ret = capture.grab()
        if not ret: 
            pass
        if frame_idx >= frame_idxs[i]:
            ret, frame = capture.retrieve()
            if not ret or frame is None:
                pass
            else:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                try:
                    face=get_img(frame)
                except Exception as err:
                    print(err)
                    continue
                imgs.append(face)
            i += 1
            if i >= len(frame_idxs):
                break
    if len(imgs)<frame_count:
        return None
    return np.hstack(imgs)


# # Detection/Results

# In[ ]:


video='../input/deepfake-detection-challenge/train_sample_videos/bdnaqemxmr.mp4'


# In[ ]:


frame_count=5
plt.imshow(detect_video(video))


# In[ ]:


frame_count=10
plt.imshow(detect_video(video))


# # Conclusion

# Thanks for reading. Hope this notebook helps! Please upvote this notebook and the associated dataset if you find it helpful.
