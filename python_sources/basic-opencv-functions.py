#!/usr/bin/env python
# coding: utf-8

# I have used few basic functions of Opencv 

# In[ ]:


import cv2
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

# Function For Plotting Images
def plot(img):
    plt.axis("off")
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) #Since Opencv store image as BGR
    plt.show()


# ## Canny edge detector
# The Canny edge detector is an edge detection operator that uses a multi-stage algorithm to detect a wide range of edges in images. It is a very amazing technique for detecting edges.

# In[ ]:


original=cv2.imread('/kaggle/input/natural-images/data/natural_images/person/person_0097.jpg')
plot(original)
edges=cv2.Canny(original,50,100) # 50 and 100 are min and max thresholds respectively. 
plot(edges)


# ## Hough transform to detect lines.
# Hough transformation are used to detect many shapes in images if they can be represented mathematically.
# Its main advantage is that it can even detect break or distorted shapes.

# In[ ]:


original=cv2.imread('/kaggle/input/four-shapes/shapes/triangle/958.png')
plot(original)
edges = cv2.Canny(original,50,150) # Hough transforms requires binary image as input
lines = cv2.HoughLines(edges,1,np.pi/180,50) # 50 is the threshold value
for line in lines:
    rho,theta=line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(original,(x1,y1),(x2,y2),(0,0,255),2)
plot(original)


# ## Hough transform to detect circles.

# In[ ]:


original=cv2.imread('/kaggle/input/natural-images/data/natural_images/person/person_0505.jpg')
gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY) 
gray_blurred = cv2.blur(gray, (3, 3)) 
plot(original)
detected_circles = cv2.HoughCircles(gray_blurred,  
                   cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
               param2 = 30, minRadius = 1, maxRadius = 40) 
if detected_circles is not None: 
  
    # Convert the circle parameters a, b and r to integers. 
    detected_circles = np.uint16(np.around(detected_circles)) 
  
    for pt in detected_circles[0, :]: 
        a, b, r = pt[0], pt[1], pt[2] 
  
        # Draw the circumference of the circle. 
        cv2.circle(original, (a, b), r, (0, 255, 0), 2) 
  
        # Draw a small circle (of radius 1) to show the center. 
        cv2.circle(original, (a, b), 1, (0, 0, 255), 3) 
plot(original)


# ## Harris and Stephen operator for corner.
# Corners are used as important features of image. Harris Corner Detector is a corner detection operator that is commonly used in computer vision algorithms to extract corners and infer features of an image

# In[ ]:


original = cv2.imread('/kaggle/input/four-shapes/shapes/star/591.png')
gray = cv2.cvtColor(original,cv2.COLOR_BGR2GRAY) #Input should be grayscale image
plot(original) #plot original Image
gray = np.float32(gray)

corners = cv2.cornerHarris(gray,2,3,0.04) #detect corners

corners = cv2.dilate(corners,None)
original[corners>0.2*corners.max()]=[0,0,255]
plot(original) # Plot detected corners


# ## FAST corner detector.
# There are several feature detectors and many of them are really good. But when looking from a real-time application point of view, they are not fast enough.
# Fast corner detector comes to rescue here.

# In[ ]:


img = cv2.imread('/kaggle/input/natural-images/data/natural_images/person/person_0145.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
plot(img) # Plot original image

fast =cv2.FastFeatureDetector_create(threshold=20)

kp = fast.detect(gray,None) 

result = cv2.drawKeypoints(img, kp, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
plot(result) # Plot Detected Corners


# In[ ]:




