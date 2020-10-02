#!/usr/bin/env python
# coding: utf-8

# # Failure Analysis
# 
# In order to improve a model it could be beneficiall to understand when model works and when does it fails. In this notebook we will do an analysis of a model prediction. We will take the submission from this kernel: https://www.kaggle.com/iafoss/unet34-submission-0-89-public-lb, and compare it to the ground truth, which is available for us due to the data leak. Ussualy you would rather do this analysis either on validation or on hold-out set.

# In[ ]:


# First we will just define some auxiliary functions
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

# set the thresholds for the evaluation metrics
thresholds = np.arange(0.5,1,0.05)

# ref: https://www.kaggle.com/paulorzp/run-length-encode-and-decode
def rle_decode(mask_rle, shape=(768, 768)):
    '''
    mask_rle: run-length as string formated (start length)
    shape: (height,width) of array to return 
    Returns numpy array, 1 - mask, 0 - background

    '''
    s = mask_rle.split()
    starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]
    starts -= 1
    ends = starts + lengths
    img = np.zeros(shape[0]*shape[1], dtype=np.uint8)
    for lo, hi in zip(starts, ends):
        img[lo:hi] = 1
    return img.reshape(shape).T  # Needed to align to RLE direction

# ref : https://www.kaggle.com/stkbailey/step-by-step-explanation-of-scoring-metric
def iou_at_thresholds(target_mask, pred_mask, thresholds=np.arange(0.5,1,0.05)):
    '''Returns True if IoU is greater than the thresholds.'''
    intersection = np.logical_and(target_mask, pred_mask)
    union = np.logical_or(target_mask, pred_mask)
    iou = np.sum(intersection > 0) / np.sum(union > 0)
    return iou > thresholds

def calculate_average_precision(x):
    '''Calculates the average precision over a range of thresholds for one observation (with a single class).'''
    
    target_masks, pred_masks = x["EncodedPixels"], x["EncodedPixels_pred"]
    
    if type(pred_masks[0]) is not str:
        pred_masks = []
    
    if type(target_masks[0]) is not str:
        target_masks = []
        
    if len(pred_masks) == 0 and len(target_masks) == 0:
        return 1
    
    if len(pred_masks) == 0 or len(target_masks) == 0:
        return 0
    
    pred_masks = [rle_decode(mask) for mask in pred_masks]
    target_masks = [rle_decode(mask) for mask in target_masks]
    
    iou_tensor = np.zeros([len(thresholds), len(pred_masks), len(target_masks)])
    
    for i, p_mask in enumerate(pred_masks):
        for j, t_mask in enumerate(target_masks):
            iou_tensor[:, i, j] = iou_at_thresholds(t_mask, p_mask, thresholds)

    TP = np.sum((np.sum(iou_tensor, axis=2) == 1), axis=1)
    FP = np.sum((np.sum(iou_tensor, axis=2) == 0), axis=1)
    FN = np.sum((np.sum(iou_tensor, axis=1) == 0), axis=1)

    precision = 5*TP / (5*TP + 4*FN + FP)
    return TP, FP, FN, precision


# ## Evaluation of solution

# In[ ]:


# Change these pathes to do other comparisons
GROUND_TRUTH_FILE = "../input/airbus-ship-detection/test_ship_segmentations.csv"
PREDICTION_FILE = "../input/unet34-submission-0-89-public-lb/submission.csv"
#PREDICTION_FILE = "../input/binary-classifier-submission/submission.csv"

df_gt = pd.read_csv(GROUND_TRUTH_FILE)
df_pred = pd.read_csv(PREDICTION_FILE)

# Combining all schips to one list
df_gt = pd.DataFrame(df_gt.groupby('ImageId')['EncodedPixels'].apply(list))
df_pred = pd.DataFrame(df_pred.groupby('ImageId')['EncodedPixels'].apply(list))


# Here we calculate F2 score, as well as True Positives(TP), False Positives (FP) and False Negatives (FN) according to the explanation of evaluation metric: https://www.kaggle.com/c/airbus-ship-detection#evaluation

# In[ ]:


df = df_pred.join(df_gt, lsuffix="_pred")
precisions = df.apply(calculate_average_precision, axis=1)

df["TP"] = precisions.apply(lambda x : x[0] if (type(x) is not int) else np.nan)
df["FP"] = precisions.apply(lambda x : x[1] if (type(x) is not int) else np.nan)
df["FN"] = precisions.apply(lambda x : x[2] if (type(x) is not int) else np.nan)
df["IoU"] = precisions.apply(lambda x : x[3] if (type(x) is not int) else x)
df["IoU_mean"] = df["IoU"].apply(np.mean)
df["TP_mean"] = df["TP"].apply(np.mean)
df["FP_mean"] = df["FP"].apply(np.mean)
df["FN_mean"] = df["FN"].apply(np.mean)

df.head()


# Now we will calculate the final score, on the leaderboard the score is ~0.892, it is a bit higher, probably due to the fact, that for the leaderboard only 15% of data are used.

# In[ ]:


print ("Solution score:", np.mean(df["IoU_mean"]))


# ## Confusion matrix
# 
# Let's also calculate confusion matrix. Here we count one ship as an instance. The confusion matrix here is the average over all thresholds.

# In[ ]:


cm = [[np.sum(~pd.notna(df["TP_mean"])), np.nansum(df["FP_mean"])],
      [np.nansum(df["FN_mean"]), np.nansum(df["TP_mean"])]]

df_cm = pd.DataFrame(cm, index = [i for i in ["No Ship", "Ship"]],
                          columns = [i for i in  ["No Ship", "Ship"]])
plt.figure(figsize = (10,7))
ax = sn.heatmap(df_cm, annot=True, cmap="YlGnBu")
ax.set(xlabel='Prediction', ylabel='Ground Truth')


# ## Intersection over Union
# 
# Now we exctract the matrix with IoU for each image in every threshold and plot some statistic

# In[ ]:


iou_on_thresholds_matrix = np.asarray([i for i in df["IoU"] if not type(i) is int])

f, ax = plt.subplots(2, 5, figsize=(30,10))

for i in range(2):
    for j in range(5):
        ax[i,j].hist(iou_on_thresholds_matrix[:,i*5 + j])
        ax[i,j].set_title("Threshold: %.2f" % thresholds[i*5 + j])


# ## Ship number and Pixel Occupation
# 
# Here we will excract some additional information from the mask, like the number of ships per image and number of pixels occupied with ships per image

# In[ ]:


def rle_get_mask_size(masks, shape=(768, 768)):
    res = 0
    
    for mask_rle in masks:
        if type(mask_rle) is float:
            return 0
        s = mask_rle.split()
        starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]
        starts -= 1
        ends = starts + lengths
    
        for lo, hi in zip(starts, ends):
            res += hi - lo
            
    return res

df["pred_ship_num"] = df["EncodedPixels_pred"].apply(lambda x : len(x) if type(x[0]) is str else 0)
df["true_ship_num"] = df["EncodedPixels"].apply(lambda x : len(x) if type(x[0]) is str else 0)
df["pred_ship_occupation"] = df["EncodedPixels_pred"].apply(rle_get_mask_size)
df["true_ship_occupation"] = df["EncodedPixels"].apply(rle_get_mask_size)


# Let's plot the real versus predicted occupation of the image.

# In[ ]:


fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(14, 7))
fig.subplots_adjust(hspace=0.5, left=0.07, right=0.93)
hb = ax1.hexbin(df['pred_ship_occupation'], df['true_ship_occupation'], gridsize=50, cmap='BuGn', bins='log')
xmin, xmax = 0, 20000
ax1.plot([xmin, xmax], [xmin, xmax])
ax1.axis([xmin, xmax, xmin, xmax])

ax1.set_ylabel('Prediction')
ax1.set_xlabel('Ground Truth')
ax1.set_title("Pixel Occupation")

ax2.hist(df['pred_ship_occupation'] - df['true_ship_occupation'],  log=True, bins=40)
ax2.axis([-30000, 30000, 1, 100000])


# Here is the plot that shows the correlation beetween how many ships are present in an image and average IoU that we got. It actually make sense that we got the highest IoU when only one ship is present. We also see that it is the most popular class, so it actually makes sense to optimize the model for the case with only few ships.

# In[ ]:


fig, (ax) = plt.subplots(ncols=1, figsize=(14, 7))

means = df.groupby("true_ship_num")["IoU_mean"].mean()
vars = df.groupby("true_ship_num")["IoU_mean"].var()
count = df.groupby("true_ship_num")["IoU_mean"].count()

ax.bar(np.arange(1,16), count[1:]/10000.)
ax.errorbar(np.arange(1,16), means[1:], yerr=vars[1:,], fmt='-or')
ax.legend(labels=("Class count", "IoU"))
ax.set_xlabel("Number of ships")
ax.set_ylabel("IoU / Class count")


# ## Visualization of images
# 
# Here we will plot some of FN, FP and TP images to better understand when it works and when not.

# In[ ]:


from skimage.io import imread
from skimage.util import montage

montage_rgb = lambda x: np.stack([montage(x[:, :, :, i]) for i in range(x.shape[3])], -1)


# In[ ]:


img_names = df[df["FN_mean"] > 10].index[:49].values.tolist()
img = np.stack([imread("../input/airbus-ship-detection/test/" + img_name) for img_name in img_names])

fig, (ax1) = plt.subplots(1, 1, figsize = (40, 20))
ax1.imshow(montage_rgb(img))
ax1.set_title('False negatives')


# Now we will plot some of the images with high False Positive rate.

# In[ ]:


img_names = df[df["FP_mean"] > 10].index[:49].values.tolist()
img = np.stack([imread("../input/airbus-ship-detection/test/" + img_name) for img_name in img_names])

fig, (ax1) = plt.subplots(1, 1, figsize = (40, 20))
ax1.imshow(montage_rgb(img))
ax1.set_title('False positives')


# And at the end, let's plot some images where we got high IoU.

# In[ ]:


img_names = df[df["TP_mean"] > 0.9].index[:49].values.tolist()
img = np.stack([imread("../input/airbus-ship-detection/test/" + img_name) for img_name in img_names])

fig, (ax1) = plt.subplots(1, 1, figsize = (40, 20))
ax1.imshow(montage_rgb(img))
ax1.set_title('True positives')


# ## Understanding False Positives and False Negatives
# 
# Let's start with false positives. In order to understand why we have high false positive rate even if it seems, that ships are present in the image, let's plot the segmentation prediction and ground truth. From the image below it is seen, that models predicts a lot of small objects that are not in ground truth.

# In[ ]:


img_name = df[df["FP_mean"] > 10].index[1]
img = imread("../input/airbus-ship-detection/test/" + img_name)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize = (22, 12))
ax1.imshow(img)      
ax1.set_title("Original Image")

mask = np.sum([rle_decode(df.loc[img_name]["EncodedPixels"][i]) for i in range(len(df.loc[img_name]["EncodedPixels"]))], axis=0)
ax2.imshow(mask)
ax2.set_title("Ground gruth")

mask = np.sum([rle_decode(df.loc[img_name]["EncodedPixels_pred"][i]) for i in range(len(df.loc[img_name]["EncodedPixels_pred"]))], axis=0)
ax3.imshow(mask)
ax3.set_title("Prediction")


# Let's also plot segmentation masks for one of the false negative example. Here it is clearly seen that objects are very close to each other and model merge them into one.

# In[ ]:


img_name = df[df["FN_mean"] > 10].index[:49][5]

img = imread("../input/airbus-ship-detection/test/" + img_name)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize = (22, 12))
ax1.imshow(img)      
ax1.set_title("Original Image")

mask = np.sum([rle_decode(df.loc[img_name]["EncodedPixels"][i]) for i in range(len(df.loc[img_name]["EncodedPixels"]))], axis=0)
ax2.imshow(mask)
ax2.set_title("Ground gruth")

mask = np.sum([rle_decode(df.loc[img_name]["EncodedPixels_pred"][i]) for i in range(len(df.loc[img_name]["EncodedPixels_pred"]))], axis=0)
ax3.imshow(mask)
ax3.set_title("Prediction")

