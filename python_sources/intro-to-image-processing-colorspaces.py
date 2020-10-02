#!/usr/bin/env python
# coding: utf-8

# # Previous tutorial
# ___
# - [What is an image?](https://www.kaggle.com/hrmello/intro-to-image-processing-what-is-an-image)
# 
# # Introduction
# ___
# I spent a little while trying to find a good definition of what a color space (or color model) is, and the best I've found is [this one](http://sun.aei.polsl.pl/~mkawulok/stud/graph/instr.pdf): In essence, a color model is a specification of a 3-D coordinate system and a subspace within that system where each color is represented by a single point. 
# 
# There are lots of color spaces out there and each one is used more often in one application or another. Some examples are:
# - RGB (Red Green Blue): used in computer graphics
# - HSV (Hue Saturation Value): used in image editing softwares (because better represents how people relate to colors than does the RGB color model)
# - HSL (Hue Saturation Lightness): very similar to HSV and used in image editing softwares as well
# - YUV : used in video systems
# 
# In this tutorial we will focus on the first two. 
# 
# # RGB and HSV colorspaces
# ___
# It is always possible to convert from one color type to another and sometimes just changing between color spaces give us useful features for computer vision algorithms, like facial recognition. See the [face detection section of this paper](http://sun.aei.polsl.pl/~mkawulok/stud/graph/instr.pdf) for details if you are curious about it.
# 
# In practice, color spaces are three dimensional coordinate spaces. Take a look at the following pictures.
# ![](https://www.researchgate.net/profile/Douglas_Bertol/publication/310474598/figure/fig1/AS:429814134906881@1479487083658/RGB-left-and-HSV-right-color-spaces.png)
# 
# Here we visualize the differences between RGB and HSV. The former, RGB, is a cartesian colorspace where colors are created by adding or subtracting red, green and blue components. For instance, consider the color (0, 12, 255). For those who are a bit more mathematical, this can also be represented in the RGB space as $0 \hat{r} + 12 \hat{g} + 255\hat{b}$ where $\hat{r}, \hat{g}, \hat{b}$ are unitary vectors in red, green and blue coordinates. This color looks like
# ![](https://i.ibb.co/cN2WhqL/be.jpg)
# It has no red component, just a bit of green and is mostly blue. If we add a red component and the vector becomes, say, (200, 12, 255), then it will look like
# ![](https://i.ibb.co/YTSs9d2/be.jpg)
# 
# HSV, on the other hand, is easier and much more intuitive. We select a hue and then we add saturation and value. The lesser the saturation the more grey the image tend to be. The value define how bright the image is. Let's see an example. Here I'm using HSV(120,40,60):
# ![](https://i.ibb.co/NrTDdg1/be.jpg)
# 
# By increasing the saturation and using HSV(120,90,60), the color becomes
# ![](https://i.ibb.co/Qcs7tqV/be.jpg)
# 
# It is farther from the darker tone as it was when S = 40. 
# Lastly, let's increase the value of the image. Now we will see what HSV(120,90,90) looks like.
# ![](https://i.ibb.co/c83Q91d/be.jpg)
# 
# Way brighter than before, as expected. The fact that HSV is much more intuitive makes it the perfect choice for image editing tools, like GIMP. 
# 
# Here is a nice representation of the transformation steps from RGB to three other color formats (including HSV and HSL):
# 
# <img src="https://upload.wikimedia.org/wikipedia/commons/a/ac/Hsl-and-hsv.svg" width="500">
# 
# # Conversion between RGB and HSV colorspaces
# 
# I won't go deep in the math especially because OpenCV have built-in functions to make those conversions. However it seems to me that this is one of those things we need to see at least once in a lifetime.
# ![](https://wikimedia.org/api/rest_v1/media/math/render/svg/7e43ae6f45887c53e43f6deac0861f04144601f2)
# ![](https://wikimedia.org/api/rest_v1/media/math/render/svg/24828aa961317e956ab569f28e68b3de7a9c8ef7)
# ![](https://wikimedia.org/api/rest_v1/media/math/render/svg/559a63c7700b66ea0204f080e89aad896f2b7432)
# 
# Seems simple enough. The other way around is a bit more complicated, though.
# 
# ![](https://i.ibb.co/HX66gHS/ble.jpg)
# 
# Now that we've seen some theory and math, it's time to get our hands dirty and code. OpenCV's `imread` default color space is BGR -- the exact same channels as RGB but in different order. As mentioned just moments ago, OpenCV will handle all the conversions, as many functions are available. Let's see an example. 

# In[ ]:


import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
get_ipython().run_line_magic('matplotlib', 'inline')

sunflowers_path = glob.glob("../input/flowers/flowers/sunflower/*.jpg")
sunflower_bgr = cv2.imread(sunflowers_path[1])
plt.figure(figsize=(10,10))
plt.imshow(sunflower_bgr);


# The image seems in the wrong color  precisely because it is loaded as BGR but `plt.imshow` thinks it is in RGB. To convert this to the proper color space, we can use `the cv2.cvtColor` method.

# In[ ]:


sunflower_rgb = cv2.cvtColor(sunflower_bgr, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(10,10))
plt.imshow(sunflower_rgb);


# Notice how the redish areas were blue before, while blueish areas were red. Since green channel is the same in both colorspaces, green tones are kept about the same (with just small changes depending on how much red and blue there is).
# 
# Just as we did in the [first part of the tutorial](https://www.kaggle.com/hrmello/intro-to-image-processing-what-is-an-image), let's split the image in channels and see what each one looks like.

# In[ ]:


def plot_channels(img):
    '''plot each image channel'''
    f, axes = plt.subplots(1,3, figsize = (15,15))
    i = 0
    for ax in axes:
        ax.imshow(img[:,:,i], cmap = "gray")
        i+=1

plot_channels(sunflower_rgb)


# As expected, the brightest pixels in red channel are the flowers' ones, while there is very little green and almost no blue intensities on them. On the other hand, the brightest pixels in blue are those from the sky.
# 
# The HSV space will show different aspects of the image. Let's convert the image to HSV and then plot it.

# In[ ]:


sunflower_hsv = cv2.cvtColor(sunflower_rgb, cv2.COLOR_RGB2HSV)
plot_channels(sunflower_hsv)


# The first channel is hue. We can see very clearly most leaves and the sky. Since flowers are very colorful and detailed, they end up having several pixels that seem somewhat noisy. The second channel is saturation. Remember that The more saturated a pixel is, the farthest it is from gray, as saturation is just a measure of the amount of gray in an image. The colored image doesn't have much gray tones, so saturation values are high in most pixels except the sky. The last channel is value (also callaed brightness sometimes) and descibres the intensity of the color. The sky is the brighter aspect in this picture, so it makes sense that it is brighter in Value channel. 
# 
# # Try it yourself!
# ___
# There are lots of other color spaces supported by OpenCV, like Lab, YUV and HSL. [Here](https://docs.opencv.org/3.2.0/d7/d1b/group__imgproc__misc.html#ga4e0972be5de079fed4e3a10e24ef5ef0) you can find all the conversions that can be done within OpenCV. Fork this notebook and convert this image (or any other you want) to other formats and see what they look like. Is there any aspect of the image that becomes clear in one channel and isn't present in the other? For e.g. a flower that is present in one channel but not that visible in another. This can be used as a simple technique to identify elements in an image. 
# 
# # Next tutorial
# 
# - [Image enhancement Part 1](https://www.kaggle.com/hrmello/intro-to-image-processing-image-enhancement-pt-1)
