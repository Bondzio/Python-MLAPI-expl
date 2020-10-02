#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import cv2
import math
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))
import warnings
warnings.filterwarnings('ignore')
#%matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore')
sns.set(rc={'figure.figsize' : (22, 10)})
sns.set_style("darkgrid", {'axes.grid' : True})

# Any results you write to the current directory are saved as output.


#  ## IAM Database Line Information
# 
#  ### Format:         
#  a01-000u-00 ok 154 19 408 746 1663 91 A|MOVE|to|stop|Mr.|Gaitskell|from
# * **a01-000u-00**  -> line id for form a01-000u
# * **ok**              -> result of word segmentation
#                             ok: line is correctly segmented
#                             err: segmentation of line has one or more errors
#                         notice: if the line could not be properly segmented
#                                 the transcription and extraction of the whole
#                                 line should not be affected negatively
# * **154**             -> graylevel to binarize line
# * **19**              -> number of components for this line
# * **408 746 1663 91** -> bounding box around this line in x,y,w,h format
# * ** A|MOVE|to|stop|Mr.|Gaitskell|from** -> transcription for this line. word tokens are separated by the character |

# In[ ]:


from subprocess import check_output
forms = pd.read_csv('../input/forms_for_parsing.txt', header=None, names=['info'])
forms.head(5)


# In[ ]:


d = {}
with open('../input/forms_for_parsing.txt') as f:
    for line in f:
        key = line.split(' ')[0]
        
        writer = line.split(' ')[1]
        d[key] = writer
print(len(d.keys()))


# In[ ]:


def showImg(img, cmap=None):
    plt.imshow(img, cmap=cmap, interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show()


# In[ ]:


def prepareImg(img, height):
    "convert given image to grayscale image (if needed) and resize to desired height"
    assert img.ndim in (2, 3)
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h = img.shape[0]
    factor = height / h
    return cv2.resize(img, dsize=None, fx=factor, fy=factor)


# In[ ]:


# Load an color image in grayscale
img1 = cv2.imread('../input/data_subset/data_subset/a01-000u-s00-00.png', cv2.IMREAD_GRAYSCALE)
print(img1.ndim)
print(img1.shape)

showImg(img1, cmap='gray')


# In[ ]:


# read image, prepare it by resizing it to fixed height and converting it to grayscale
img2 = prepareImg(cv2.imread('../input/data_subset/data_subset/a01-000u-s00-00.png'), 50)
showImg(img2, cmap='gray')


# In[ ]:


img2.shape


# In[ ]:


50/img1.shape[0]


# In[ ]:


def createKernel(kernelSize, sigma, theta):
    "create anisotropic filter kernel according to given parameters"
    assert kernelSize % 2 # must be odd size
    halfSize = kernelSize // 2

    kernel = np.zeros([kernelSize, kernelSize])
    sigmaX = sigma
    sigmaY = sigma * theta

    for i in range(kernelSize):
        for j in range(kernelSize):
            x = i - halfSize
            y = j - halfSize

            expTerm = np.exp(-x**2 / (2 * sigmaX) - y**2 / (2 * sigmaY))
            xTerm = (x**2 - sigmaX**2) / (2 * math.pi * sigmaX**5 * sigmaY)
            yTerm = (y**2 - sigmaY**2) / (2 * math.pi * sigmaY**5 * sigmaX)

            kernel[i, j] = (xTerm + yTerm) * expTerm

    kernel = kernel / np.sum(kernel)
    return kernel


# In[ ]:


createKernel(3, 0.8, 3.5)


# Scale space technique for word segmentation proposed by R. Manmatha: http://ciir.cs.umass.edu/pubfiles/mm-27.pdf          
# * **Args**:           
# 		img: grayscale uint8 image of the text-line to be segmented.
# 		kernelSize: size of filter kernel, must be an odd integer.
# 		sigma: standard deviation of Gaussian function used for filter kernel.
# 		theta: approximated width/height ratio of words, filter function is distorted by this factor.
# 		minArea: ignore word candidates smaller than specified area.	
# * **Returns**:            
# 		List of tuples. Each tuple contains the bounding box and the image of the segmented word.

# In[ ]:


kernelSize=25
sigma=11
theta=7
minArea=100


# In[ ]:


# apply filter kernel
kernel = createKernel(kernelSize, sigma, theta)
# The function applies an arbitrary linear filter to an image.
# int ddepth (=-1) - desired depth of the destination image
# anchor - indicates the relative position of a filtered point within the kernel; 
# default value (-1,-1) means that the anchor is at the kernel center.
# borderType - pixel extrapolation method:  
# cv2.BORDER_REPLICATE -  The row or column at the very edge of the original is replicated to the extra border.
imgFiltered = cv2.filter2D(img1, -1, kernel, borderType=cv2.BORDER_REPLICATE).astype(np.uint8)


# In[ ]:


blur = cv2.GaussianBlur(img1,(5,5),0)
showImg(blur, cmap='gray')


# In[ ]:


imgFiltered1 = cv2.filter2D(img1, -1, createKernel(kernelSize, sigma, theta), borderType=cv2.BORDER_REPLICATE)
showImg(imgFiltered1, cmap='gray')
#25, 0.8, 3.5


# In[ ]:


# threshold - If pixel value is greater than a threshold value, it is assigned one value, else it is assigned another value 
# img - source image, which should be a grayscale image. 
# Second argument is the threshold value which is used to classify the pixel values. 
# Third argument is the maxVal which represents the value to be given if pixel value is more than the threshold value. 
# Last - different styles of thresholding
# Returns: threshold value computed, destination image
(_, imgThres) = cv2.threshold(imgFiltered1, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

imgThres = 255 - imgThres
showImg(imgThres, cmap='gray')


# In[ ]:


# find connected components. OpenCV: return type differs between OpenCV2 and 3
# findContours - The function retrieves contours from the binary image
# First argument is source image, second is contour retrieval mode, third is contour approximation method.
if cv2.__version__.startswith('3.'):
    (_, components, _) = cv2.findContours(imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
else:
    # cv2.RETR_EXTERNAL or cv2.RETR_LIST - ???
    (components, _) = cv2.findContours(imgThres, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


# In[ ]:


cv2.__version__


# In[ ]:


(components, _) = cv2.findContours(imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# In[ ]:


len(components)


# In[ ]:


showImg(cv2.drawContours(img1, components, -1, (0,0,255), 5))


# In[ ]:


# append components to result
res = []
for c in components:
    # skip small word candidates
    if cv2.contourArea(c) < minArea:
        continue
    # append bounding box and image of word to result list
    currBox = cv2.boundingRect(c) # returns (x, y, w, h)
    (x, y, w, h) = currBox
    currImg = img1[y:y+h, x:x+w]
    res.append((currBox, currImg))


# In[ ]:


len(res)


# In[ ]:


res[5][1]


# In[ ]:


img1.shape


# In[ ]:


sns.set(rc={'figure.figsize' : (6, 3)})
(x1, y1, w1, h1) = res[5][0]
showImg(img1[y1:y1+h1, x1:x1+w1], cmap='gray')


# In[ ]:


showImg(res[5][1], cmap='gray')


# In[ ]:


def display_contours(contours):
    plt.figure(figsize=(30, 30))
    for i, c in enumerate(contours):
        contour = c[1]
        plt.subplot(8, 4, i+1)  # A grid of 8 rows x 8 columns
        plt.axis('off')
        plt.title("Contour #{0}, size: {1}".format(i, c[0]))
        _ = plt.imshow(contour, cmap='gray')
    plt.show()
        


# In[ ]:


display_contours(res)


# In[ ]:


sorted_res = sorted(res, key=lambda entry:entry[0][0])
display_contours(sorted_res)

