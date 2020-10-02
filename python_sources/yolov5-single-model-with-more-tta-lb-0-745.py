#!/usr/bin/env python
# coding: utf-8

# Based on [YoloV5 fake or real [Single Model] L.B>0.73](https://www.kaggle.com/orkatz2/yolov5-fake-or-real-single-model-l-b-0-73)

# I checked yolov5 code and find it uses some simple TTA like scale and combination of scale and flip-lr. So I do some experiments on TTA and find that adding some more TTA give a huge boost to LB score.
# 
# 
# FYI:
# - No TTA: 0.7197
# 
# - Yolov5 original TTA: 0.7337
# 
# - Add single flip-lr: 0.7353
# 
# - Add single flip-ud and combination of scale and flip-ud: 0.7458
# 
# 

# For more TTA code in yolov5, you can see it here [yolov5tta](https://www.kaggle.com/wasupandceacar/yolov5tta)

# In[ ]:


import numpy as np 
import pandas as pd 
import os


# In[ ]:


import torch
import sys
sys.path.insert(0, "../input/weightedboxesfusion")
sys.path.insert(0, "../input/yolov5tta/")
from ensemble_boxes import *
import glob


# In[ ]:


import argparse

from utils.datasets import *
from utils.utils import *


def detect(save_img=False):
    weights, imgsz = opt.weights,opt.img_size
    source = '../input/global-wheat-detection/test/'
    
    # Initialize
    device = torch_utils.select_device(opt.device)
    half = False
    # Load model

    model = torch.load(weights, map_location=device)['model'].to(device).eval()

    dataset = LoadImages(source, img_size=1024)

    t0 = time.time()
    img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
    all_path=[]
    all_bboxex =[]
    all_score =[]
    for path, img, im0s, vid_cap in dataset:
        print(im0s.shape)
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = torch_utils.time_synchronized()
        bboxes_2 = []
        score_2 = []
        if True:
            pred = model(img, augment=opt.augment)[0]
            pred = non_max_suppression(pred, 0.4, opt.iou_thres,merge=True, classes=None, agnostic=False)
            t2 = torch_utils.time_synchronized()

            bboxes = []
            score = []
            # Process detections
            for i, det in enumerate(pred):  # detections per image
                p, s, im0 = path, '', im0s
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  #  normalization gain whwh
                if det is not None and len(det):
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class

                    for *xyxy, conf, cls in det:
                        if True:  # Write to file
                            xywh = torch.tensor(xyxy).view(-1).numpy()  # normalized xywh
#                             xywh[2] = xywh[2]-xywh[0]
#                             xywh[3] = xywh[3]-xywh[1]
                            bboxes.append(xywh)
                            score.append(conf)
            bboxes_2.append(bboxes)
            score_2.append(score)
        all_path.append(path)
        all_score.append(score_2)
        all_bboxex.append(bboxes_2)
    return all_path,all_score,all_bboxex


if __name__ == '__main__':
    class opt:
        weights = "../input/yolov5wheattorch/f0/f0best.bin"
        img_size = 1024
        conf_thres = 0.1
        iou_thres = 0.94
        augment = True
        device = '0'
        classes=None
        agnostic_nms = True
        
    opt.img_size = check_img_size(opt.img_size)
    print(opt)

    with torch.no_grad():
        res = detect()


# In[ ]:


def run_wbf(boxes,scores, image_size=1024, iou_thr=0.41, skip_box_thr=0.4, weights=None):
#     boxes =boxes/(image_size-1)
    labels0 = [np.ones(len(scores[idx])) for idx in range(len(scores))]
    boxes, scores, labels = weighted_boxes_fusion(boxes, scores, labels0, weights=None, iou_thr=iou_thr, skip_box_thr=skip_box_thr)
#     boxes = boxes*(image_size-1)
#     boxes = boxes
    return boxes, scores, labels


# In[ ]:


all_path,all_score,all_bboxex = res


# In[ ]:


results =[]
def format_prediction_string(boxes, scores):
    pred_strings = []
    for j in zip(scores, boxes):
        pred_strings.append("{0:.4f} {1} {2} {3} {4}".format(j[0], j[1][0], j[1][1], j[1][2], j[1][3]))
    return " ".join(pred_strings)
for row in range(len(all_path)):
    image_id = all_path[row].split("/")[-1].split(".")[0]
    boxes = all_bboxex[row]
    scores = all_score[row]
    boxes, scores, labels = run_wbf(boxes,scores)
    boxes = (boxes*1024/1024).astype(np.int32).clip(min=0, max=1023)
    boxes[:, 2] = boxes[:, 2] - boxes[:, 0]
    boxes[:, 3] = boxes[:, 3] - boxes[:, 1]
    result = {'image_id': image_id,'PredictionString': format_prediction_string(boxes, scores)}
    results.append(result)
test_df = pd.DataFrame(results, columns=['image_id', 'PredictionString'])


# In[ ]:


test_df.to_csv('submission.csv', index=False)
test_df.head(12)


# In[ ]:


size = 300
idx =-1
font = cv2.FONT_HERSHEY_SIMPLEX 
image = image = cv2.imread(all_path[idx], cv2.IMREAD_COLOR)
# fontScale 
fontScale = 1
# boxes = all_bboxex[idx]
# scores = all_score[idx]
# Blue color in BGR 
color = (255, 0, 0) 

# Line thickness of 2 px 
thickness = 2
for b,s in zip(boxes,scores):
    image = cv2.rectangle(image, (b[0],b[1]), (b[0]+b[2],b[1]+b[3]), (255,0,0), 1) 
    image = cv2.putText(image, '{:.2}'.format(s), (b[0]+np.random.randint(20),b[1]), font,  
                   fontScale, color, thickness, cv2.LINE_AA)
plt.figure(figsize=[20,20])
plt.imshow(image[:,:,::-1])
plt.show()

