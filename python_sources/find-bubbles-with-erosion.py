#!/usr/bin/env python
# coding: utf-8

# # Simple Approach Using Erosion

# In[ ]:


from skimage.io import imread, imsave
from glob import glob
import numpy as np
import matplotlib.pyplot as plt


# In[ ]:


stack_image = imread('../input/plateau_border.tif')
print(stack_image.shape, stack_image.dtype)


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize = (12, 4))
for i, (cax, clabel) in enumerate(zip([ax1, ax2, ax3], ['xy', 'zy', 'zx'])):
    cax.imshow(np.sum(stack_image,i).squeeze(), interpolation='none', cmap = 'bone_r')
    cax.set_title('%s Projection' % clabel)
    cax.set_xlabel(clabel[0])
    cax.set_ylabel(clabel[1])


# # Create Bubble Image
# The bubble image is the reverse of the plateau border image (where there is water there can't be air) with a convex hull used to find the mask of the image
# $$ \text{Bubbles} = \text{ConvexHull}(\text{PlateauBorder}) - \text{PlateauBorder} $$

# In[ ]:


from skimage.morphology import binary_opening, convex_hull_image as chull
bubble_image = np.stack([chull(csl>0) & (csl==0) for csl in stack_image])
plt.imshow(bubble_image[5]>0, cmap = 'bone')


# # Find Bubble Centers
# The bubble centers can be found by eroding the bubbles using a 3D ball shaped structuring element of radius 5 (11x11x11) on a downsampled image (so it runs faster)

# In[ ]:


from skimage.morphology import ball as skm_ball, binary_erosion
bubble_centers = binary_erosion(bubble_image[:,::3, ::3], selem = skm_ball(5))


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize = (12, 4))
for i, (cax, clabel) in enumerate(zip([ax1, ax2, ax3], ['xy', 'zy', 'zx'])):
    cax.imshow(np.sum(bubble_centers,i).squeeze(), interpolation='none', cmap = 'bone_r')
    cax.set_title('%s Projection' % clabel)
    cax.set_xlabel(clabel[0])
    cax.set_ylabel(clabel[1])


# # Label Bubbles
# The bubbles are labeled using a connected component analysis on the centers which makes neighboring pixels part of the same label

# In[ ]:


from skimage.morphology import label
bubble_center_label_image = label(bubble_centers)


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize = (12, 4))
for i, (cax, clabel) in enumerate(zip([ax1, ax2, ax3], ['xy', 'zy', 'zx'])):
    cax.imshow(np.max(bubble_center_label_image,i).squeeze(), interpolation='none', cmap = 'jet')
    cax.set_title('%s Projection' % clabel)
    cax.set_xlabel(clabel[0])
    cax.set_ylabel(clabel[1])


# # Regrow the Bubbles
# Regrow the bubbles back to their original size

# In[ ]:


from skimage.morphology import dilation
from scipy import ndimage
bubble_label_image = dilation(bubble_center_label_image, skm_ball(5))
bubble_label_image = ndimage.zoom(bubble_label_image, (1, 3, 3), order = 0) # nearest neighbor


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize = (12, 4))
for i, (cax, clabel) in enumerate(zip([ax1, ax2, ax3], ['xy', 'zy', 'zx'])):
    cax.imshow(np.max(bubble_label_image,i).squeeze(), interpolation='none', cmap = 'jet')
    cax.set_title('%s Projection' % clabel)
    cax.set_xlabel(clabel[0])
    cax.set_ylabel(clabel[1])


# # Show 3D Rendering

# In[ ]:


from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure
from tqdm import tqdm
def show_3d_mesh(image, thresholds):
    p = image[::-1].swapaxes(1,2)
    cmap = plt.cm.get_cmap('nipy_spectral_r')
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    for i, c_threshold in tqdm(list(enumerate(thresholds))):
        verts, faces = measure.marching_cubes(p==c_threshold, 0)
        mesh = Poly3DCollection(verts[faces], alpha=0.25, edgecolor='none', linewidth = 0.1)
        mesh.set_facecolor(cmap(i / len(thresholds))[:3])
        mesh.set_edgecolor([1, 0, 0])
        ax.add_collection3d(mesh)

    ax.set_xlim(0, p.shape[0])
    ax.set_ylim(0, p.shape[1])
    ax.set_zlim(0, p.shape[2])
    
    ax.view_init(45, 45)
    return fig


# In[ ]:


_ = show_3d_mesh(bubble_label_image, range(1,np.max(bubble_label_image), 10))


# # Calculate Bubble Centers

# In[ ]:


def meshgrid3d_like(in_img):
    return np.meshgrid(range(in_img.shape[1]),range(in_img.shape[0]), range(in_img.shape[2]))
zz, xx, yy = meshgrid3d_like(bubble_label_image)


# In[ ]:


out_results = []
for c_label in np.unique(bubble_label_image): # one bubble at a time
    if c_label>0: # ignore background
        cur_roi = bubble_label_image==c_label
        out_results += [{'x': xx[cur_roi].mean(), 'y': yy[cur_roi].mean(), 'z': zz[cur_roi].mean(), 
                         'volume': np.sum(cur_roi)}]


# In[ ]:


import pandas as pd
out_table = pd.DataFrame(out_results)
out_table.to_csv('bubble_volume.csv')
out_table.sample(5)


# In[ ]:


out_table['volume'].plot.density()


# In[ ]:


out_table.plot.hexbin('x', 'y', gridsize = (5,5))


# # Compare with the Training Values

# In[ ]:


train_values = pd.read_csv('../input/bubble_volume.csv')


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
fig, (ax1, ax2) = plt.subplots(1,2, figsize = (8, 4))
ax1.hist(np.log10(out_table['volume']))
ax1.hist(np.log10(train_values['volume']))
ax1.legend(['Erosion Volumes', 'Training Volumes'])
ax1.set_title('Volume Comparison\n(Log10)')
ax2.plot(out_table['x'], out_table['y'], 'r.',
        train_values['x'], train_values['y'], 'b.')
ax2.legend(['Erosion Bubbles', 'Training Bubbles'])


# In[ ]:




