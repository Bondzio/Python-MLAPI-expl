#!/usr/bin/env python
# coding: utf-8

# ## At first install pixellib library

# In[ ]:


get_ipython().system(' pip install pixellib')


# ## Download mask rcnn coco weights

# In[ ]:


get_ipython().system('wget --quiet https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5')


# ## Show Input Image

# In[ ]:


import cv2
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (50,10)
image=cv2.imread("/kaggle/input/open-images-instance-segmentation-rvc-2020/test/00000b4dcff7f799.jpg")
plt.imshow(image)


# ## Import Libraries and Use pixellib built in function to create object and load model

# In[ ]:


import pixellib
from pixellib.instance import instance_segmentation
segment_image = instance_segmentation()
segment_image.load_model("/kaggle/working/mask_rcnn_coco.h5") 


# ## Image Segementation and Object Detection

# Use segmentImage function for image segmentation, pass input image and output image name, and make show_bboxes parameter True for bounding box object detection

# In[ ]:


segment_image.segmentImage("/kaggle/input/open-images-instance-segmentation-rvc-2020/test/00000b4dcff7f799.jpg", output_image_name = "/kaggle/working/output_1.jpg",show_bboxes = True)
image=cv2.imread("/kaggle/working/output_1.jpg")
plt.rcParams["figure.figsize"] = (50,10)
plt.imshow(image)


# ## Image Segementation and Object Detection

# In[ ]:


segment_image.segmentImage("/kaggle/input/open-images-instance-segmentation-rvc-2020/test/0005339c44e6071b.jpg", output_image_name = "output_2.jpg",show_bboxes = True)
image=cv2.imread("output_2.jpg")
plt.imshow(image)


# In[ ]:


segment_image.segmentImage("/kaggle/input/open-images-instance-segmentation-rvc-2020/test/00246c2940caa984.jpg", output_image_name = "output_3.jpg",show_bboxes = True)
image=cv2.imread("output_3.jpg")
plt.imshow(image)


# In[ ]:


segment_image.segmentImage("/kaggle/input/open-images-instance-segmentation-rvc-2020/test/006a3b0fc42143a4.jpg", output_image_name = "output_4.jpg",show_bboxes = True)
image=cv2.imread("output_4.jpg")
plt.imshow(image)


# In[ ]:


segment_image.segmentImage("/kaggle/input/open-images-instance-segmentation-rvc-2020/test/00841769515cc799.jpg", output_image_name = "output_5.jpg",show_bboxes = True)
image=cv2.imread("output_5.jpg")
plt.imshow(image)


# In[ ]:


segment_image.segmentImage("/kaggle/input/open-images-instance-segmentation-rvc-2020/test/004e5f92f9ebedad.jpg", output_image_name = "output_6.jpg",show_bboxes = True)
image=cv2.imread("output_6.jpg")
plt.imshow(image)


# In[ ]:


segment_image.segmentImage("/kaggle/input/open-images-instance-segmentation-rvc-2020/test/01150a01bfc01532.jpg", output_image_name = "output_7.jpg",show_bboxes = True)
image=cv2.imread("output_7.jpg")
plt.imshow(image)


# In[ ]:


segment_image.segmentImage("/kaggle/input/open-images-instance-segmentation-rvc-2020/test/013f7c87a409c900.jpg", output_image_name = "output_8.jpg",show_bboxes = True)
image=cv2.imread("output_8.jpg")
plt.imshow(image)


# ## If you like this notebook, please upvote.
