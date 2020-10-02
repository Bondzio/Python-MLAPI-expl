#!/usr/bin/env python
# coding: utf-8

# Not sure if this has been done before, but I animated the individual images for each patient, displaying them sequentially. I don't expect (nor planned for) this to produce any benefit for the competition, simply tried to build a nice animation to look at.

# The cell bellow contains code to load files and apply transformations. It was copied from the full processing tutorial (https://www.kaggle.com/gzuidhof/data-science-bowl-2017/full-preprocessing-tutorial - Thanks @gzuidhof). Refer to that link if you have any questions on whats going on:

# In[ ]:


import os
import numpy as np
import dicom
INPUT_FOLDER = '../input/sample_images/'
patients = os.listdir(INPUT_FOLDER)
patients.sort()

# Load the scans in given folder path
def load_scan(path):
    slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
    slices.sort(key = lambda x: int(x.ImagePositionPatient[2]))
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
        
    for s in slices:
        s.SliceThickness = slice_thickness
        
    return slices

def get_pixels_hu(slices):
    image = np.stack([s.pixel_array for s in slices])
    # Convert to int16 (from sometimes int16), 
    # should be possible as values should always be low enough (<32k)
    image = image.astype(np.int16)

    # Set outside-of-scan pixels to 0
    # The intercept is usually -1024, so air is approximately 0
    image[image == -2000] = 0
    
    # Convert to Hounsfield units (HU)
    for slice_number in range(len(slices)):
        
        intercept = slices[slice_number].RescaleIntercept
        slope = slices[slice_number].RescaleSlope
        
        if slope != 1:
            image[slice_number] = slope * image[slice_number].astype(np.float64)
            image[slice_number] = image[slice_number].astype(np.int16)
            
        image[slice_number] += np.int16(intercept)
    
    return np.array(image, dtype=np.int16)


# Bellow is the code that produces the animation, its currently getting the first patient, put you can modify the index to see any other patient.
# 
# Click on the output tab to see the result

# In[ ]:


import matplotlib.pyplot as plt
import matplotlib.animation as animation
get_ipython().run_line_magic('matplotlib', 'inline')

first_patient = load_scan(INPUT_FOLDER + patients[0])
first_patient_pixels = get_pixels_hu(first_patient)

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):    
    ax1.clear()
    ax1.imshow(first_patient_pixels[i], cmap=plt.cm.gray)

ani = animation.FuncAnimation(fig,animate,interval=50, frames=len(first_patient_pixels), repeat=False)
ani.save('ani.gif', writer='imagemagick')	
plt.show()


# In[ ]:




