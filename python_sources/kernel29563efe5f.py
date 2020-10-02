#!/usr/bin/env python
# coding: utf-8

# # Step 1: Using 4 MaskRCNN Models for SuperCategory Prediction

# In[ ]:


from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn as sns
import pandas as pd
import numpy as np
import cv2
import os
import sys
import json
import time
import random
import pickle
from tqdm import tqdm, tqdm_pandas
from scipy.signal import argrelextrema
from sklearn.model_selection import StratifiedKFold, KFold


# ## Introduction

# 1) IoU Mask Check, will not be executed ever again ~ Done<br>
# 2) For each four models, step 3, 4 will be implemented<br>
# 3) Pre-Processing, includes data creation for training<br>
# 4) Train, all 4 models will be trained

# In[ ]:


image = Image.open("/kaggle/input/imaterialist-fashion-2020-fgvc7/train/00000663ed1ff0c4e0132b9b9ac53f6e.jpg")
image = np.array(image)
print(image.shape)
plt.imshow(image)


# In[ ]:


dataDir = "/kaggle/input/imaterialist-fashion-2020-fgvc7/"
workDir = "/kaggle/working/"
os.listdir(dataDir)


# In[ ]:


sample_submission = pd.read_csv(os.path.join(dataDir, 'sample_submission.csv'))
sample_submission


# In[ ]:


## Extracting info from JSON file
labelFile = os.path.join(dataDir, 'label_descriptions.json')
with open(labelFile) as file:
    data = file.read()
    labelDes = json.loads(data)

supercategories = []
for val in labelDes['categories']:
    if val['supercategory'] not in supercategories:
        supercategories.append(val['supercategory'])
supercategories_dict = { val:i for i, val in enumerate(supercategories) }

superattributes = []
for val in labelDes['attributes']:
    if val['supercategory'] not in superattributes:
        superattributes.append(val['supercategory'])
superattributes.append('na')
superattributes_dict = { val:i for i, val in enumerate(superattributes) }

category_dict = { i['id']:[i['name'], i['supercategory'], i['level']] for i in labelDes['categories'] }
attribute_dict = { i['id']:[i['name'], i['supercategory'], i['level']] for i in labelDes['attributes'] }
attribute_dict[341] = ['na', 'na', 0]


# In[ ]:


category2super_dict = {}
for key, val in zip(category_dict.keys(), category_dict.values()):
    if supercategories_dict[val[1]] not in category2super_dict.keys():
        category2super_dict[supercategories_dict[val[1]]] = [key]
    else:
        category2super_dict[supercategories_dict[val[1]]].append(key)

attribute2super_dict = {}
for key, val in zip(attribute_dict.keys(), attribute_dict.values()):
    if superattributes_dict[val[1]] not in attribute2super_dict.keys():
        attribute2super_dict[superattributes_dict[val[1]]] = [key]
    else:
        attribute2super_dict[superattributes_dict[val[1]]].append(key)


# ## IoU Mask Check

# In[ ]:


#train = pd.read_csv('/kaggle/input/newtrain4attr/train.csv').drop(['index'], axis=1)


# In[ ]:


#train['SuperCategory'].value_counts()


# In[ ]:


#Masks = train.groupby('ImageId')['MaskBB', 'SuperCategory'].agg(lambda x: list(x))


# In[ ]:


'''def cal_iou(bb1, bb2):
    bb1 = np.array(bb1[1:-1].split(', ')).astype(int)
    bb2 = np.array(bb2[1:-1].split(', ')).astype(int)
    
    hmin1, hmax1, wmin1, wmax1 = bb1
    hmin2, hmax2, wmin2, wmax2 = bb2
    
    area1 = (hmax1 - hmin1)*(wmax1 - wmin1)
    area2 = (hmax2 - hmin2)*(wmax2 - wmin2)
    
    inter_hmin = max(hmin1, hmin2)
    inter_hmax = min(hmax1, hmax2)
    inter_wmin = max(wmin1, wmin2)
    inter_wmax = min(wmax1, wmax2)
    
    intersection = (inter_hmax - inter_hmin)*(inter_wmax - inter_wmin)
    union = area1 + area2 - intersection
    
    return intersection/union, min(area1, area2)/max(area1, area2)

matrix1 = np.zeros((12, 12))
matrix2 = np.zeros((12, 12))
for i, row in tqdm(Masks.iterrows()):
    SCats = row.SuperCategory
    masks = row.MaskBB
    for x in range(len(SCats)):
        for y in range(x+1, len(SCats)):
            if SCats[x] != SCats[y]:
                iou, minmax = cal_iou(masks[x], masks[y])
                if iou == minmax:
                    matrix1[SCats[x], SCats[y]] += 1
                    matrix1[SCats[y], SCats[x]] += 1
                else:
                    matrix2[SCats[x], SCats[y]] += 1
                    matrix2[SCats[y], SCats[x]] += 1'''


# In[ ]:


'''plt.figure(figsize=(13.5, 12))
sns.heatmap(matrix1/1000, linewidths=0.3, annot=True, xticklabels=list(supercategories_dict.keys()), yticklabels=list(supercategories_dict.keys()))
plt.show()
plt.figure(figsize=(13.5, 12))
sns.heatmap(matrix2/1000, linewidths=0.3, annot=True, xticklabels=list(supercategories_dict.keys()), yticklabels=list(supercategories_dict.keys()))
plt.show()'''


# In[ ]:


'''del Masks
del matrix1
del matrix2
del train'''


# ## Pre-Processing & Training for each Network

# In[ ]:


get_ipython().system('cp -avr /kaggle/input/maskrcnn16/maskrcnn16 /kaggle/working/Mask_RCNN')


# In[ ]:


os.chdir('Mask_RCNN')
get_ipython().system('rm -rf .git # to prevent an error when the kernel is committed')
get_ipython().system('rm -rf images assets # to prevent displaying images at the bottom of a kernel')


# In[ ]:


get_ipython().system('rm mrcnn/model.py')


# In[ ]:


get_ipython().run_cell_magic('writefile', 'mrcnn/model.py', '"""\nMask R-CNN\nThe main Mask R-CNN model implementation.\n\nCopyright (c) 2017 Matterport, Inc.\nLicensed under the MIT License (see LICENSE for details)\nWritten by Waleed Abdulla\n"""\n\nimport os\nimport random\nimport datetime\nimport re\nimport math\nimport logging\nfrom collections import OrderedDict\nimport multiprocessing\nimport numpy as np\nimport tensorflow as tf\nimport keras\nimport tensorflow.keras.backend as K\nimport tensorflow.keras.layers as KL\nimport keras.engine as KE\nimport tensorflow.keras.models as KM\n\nfrom mrcnn import utils\n\n# Requires TensorFlow 1.3+ and Keras 2.0.8+.\nfrom distutils.version import LooseVersion\nassert LooseVersion(tf.__version__) >= LooseVersion("1.3")\nassert LooseVersion(keras.__version__) >= LooseVersion(\'2.0.8\')\ntf.compat.v1.disable_eager_execution()\n\n############################################################\n#  Utility Functions\n############################################################\n\ndef log(text, array=None):\n    """Prints a text message. And, optionally, if a Numpy array is provided it\n    prints it\'s shape, min, and max values.\n    """\n    if array is not None:\n        text = text.ljust(25)\n        text += ("shape: {:20}  ".format(str(array.shape)))\n        if array.size:\n            text += ("min: {:10.5f}  max: {:10.5f}".format(array.min(),array.max()))\n        else:\n            text += ("min: {:10}  max: {:10}".format("",""))\n        text += "  {}".format(array.dtype)\n    print(text)\n\n\nclass BatchNorm(KL.BatchNormalization):\n    """Extends the Keras BatchNormalization class to allow a central place\n    to make changes if needed.\n\n    Batch normalization has a negative effect on training if batches are small\n    so this layer is often frozen (via setting in Config class) and functions\n    as linear layer.\n    """\n    def call(self, inputs, training=None):\n        """\n        Note about training values:\n            None: Train BN layers. This is the normal mode\n            False: Freeze BN layers. Good when batch size is small\n            True: (don\'t use). Set layer in training mode even when making inferences\n        """\n        return super(self.__class__, self).call(inputs, training=training)\n\n\ndef compute_backbone_shapes(config, image_shape):\n    """Computes the width and height of each stage of the backbone network.\n\n    Returns:\n        [N, (height, width)]. Where N is the number of stages\n    """\n    if callable(config.BACKBONE):\n        return config.COMPUTE_BACKBONE_SHAPE(image_shape)\n\n    # Currently supports ResNet only\n    assert config.BACKBONE in ["resnet50", "resnet101"]\n    return np.array(\n        [[int(math.ceil(image_shape[0] / stride)),\n            int(math.ceil(image_shape[1] / stride))]\n            for stride in config.BACKBONE_STRIDES])\n\n\n############################################################\n#  Resnet Graph\n############################################################\n\n# Code adopted from:\n# https://github.com/fchollet/deep-learning-models/blob/master/resnet50.py\n\ndef identity_block(input_tensor, kernel_size, filters, stage, block,\n                   use_bias=True, train_bn=True):\n    """The identity_block is the block that has no conv layer at shortcut\n    # Arguments\n        input_tensor: input tensor\n        kernel_size: default 3, the kernel size of middle conv layer at main path\n        filters: list of integers, the nb_filters of 3 conv layer at main path\n        stage: integer, current stage label, used for generating layer names\n        block: \'a\',\'b\'..., current block label, used for generating layer names\n        use_bias: Boolean. To use or not use a bias in conv layers.\n        train_bn: Boolean. Train or freeze Batch Norm layers\n    """\n    nb_filter1, nb_filter2, nb_filter3 = filters\n    conv_name_base = \'res\' + str(stage) + block + \'_branch\'\n    bn_name_base = \'bn\' + str(stage) + block + \'_branch\'\n\n    x = KL.Conv2D(nb_filter1, (1, 1), name=conv_name_base + \'2a\',\n                  use_bias=use_bias)(input_tensor)\n    x = BatchNorm(name=bn_name_base + \'2a\')(x, training=train_bn)\n    x = KL.Activation(\'relu\')(x)\n\n    x = KL.Conv2D(nb_filter2, (kernel_size, kernel_size), padding=\'same\',\n                  name=conv_name_base + \'2b\', use_bias=use_bias)(x)\n    x = BatchNorm(name=bn_name_base + \'2b\')(x, training=train_bn)\n    x = KL.Activation(\'relu\')(x)\n\n    x = KL.Conv2D(nb_filter3, (1, 1), name=conv_name_base + \'2c\',\n                  use_bias=use_bias)(x)\n    x = BatchNorm(name=bn_name_base + \'2c\')(x, training=train_bn)\n\n    x = KL.Add()([x, input_tensor])\n    x = KL.Activation(\'relu\', name=\'res\' + str(stage) + block + \'_out\')(x)\n    return x\n\n\ndef conv_block(input_tensor, kernel_size, filters, stage, block,\n               strides=(2, 2), use_bias=True, train_bn=True):\n    """conv_block is the block that has a conv layer at shortcut\n    # Arguments\n        input_tensor: input tensor\n        kernel_size: default 3, the kernel size of middle conv layer at main path\n        filters: list of integers, the nb_filters of 3 conv layer at main path\n        stage: integer, current stage label, used for generating layer names\n        block: \'a\',\'b\'..., current block label, used for generating layer names\n        use_bias: Boolean. To use or not use a bias in conv layers.\n        train_bn: Boolean. Train or freeze Batch Norm layers\n    Note that from stage 3, the first conv layer at main path is with subsample=(2,2)\n    And the shortcut should have subsample=(2,2) as well\n    """\n    nb_filter1, nb_filter2, nb_filter3 = filters\n    conv_name_base = \'res\' + str(stage) + block + \'_branch\'\n    bn_name_base = \'bn\' + str(stage) + block + \'_branch\'\n\n    x = KL.Conv2D(nb_filter1, (1, 1), strides=strides,\n                  name=conv_name_base + \'2a\', use_bias=use_bias)(input_tensor)\n    x = BatchNorm(name=bn_name_base + \'2a\')(x, training=train_bn)\n    x = KL.Activation(\'relu\')(x)\n\n    x = KL.Conv2D(nb_filter2, (kernel_size, kernel_size), padding=\'same\',\n                  name=conv_name_base + \'2b\', use_bias=use_bias)(x)\n    x = BatchNorm(name=bn_name_base + \'2b\')(x, training=train_bn)\n    x = KL.Activation(\'relu\')(x)\n\n    x = KL.Conv2D(nb_filter3, (1, 1), name=conv_name_base +\n                  \'2c\', use_bias=use_bias)(x)\n    x = BatchNorm(name=bn_name_base + \'2c\')(x, training=train_bn)\n\n    shortcut = KL.Conv2D(nb_filter3, (1, 1), strides=strides,\n                         name=conv_name_base + \'1\', use_bias=use_bias)(input_tensor)\n    shortcut = BatchNorm(name=bn_name_base + \'1\')(shortcut, training=train_bn)\n\n    x = KL.Add()([x, shortcut])\n    x = KL.Activation(\'relu\', name=\'res\' + str(stage) + block + \'_out\')(x)\n    return x\n\n\ndef resnet_graph(input_image, architecture, stage5=False, train_bn=True):\n    """Build a ResNet graph.\n        architecture: Can be resnet50 or resnet101\n        stage5: Boolean. If False, stage5 of the network is not created\n        train_bn: Boolean. Train or freeze Batch Norm layers\n    """\n    assert architecture in ["resnet50", "resnet101"]\n    # Stage 1\n    x = KL.ZeroPadding2D((3, 3))(input_image)\n    x = KL.Conv2D(64, (7, 7), strides=(2, 2), name=\'conv1\', use_bias=True)(x)\n    x = BatchNorm(name=\'bn_conv1\')(x, training=train_bn)\n    x = KL.Activation(\'relu\')(x)\n    C1 = x = KL.MaxPooling2D((3, 3), strides=(2, 2), padding="same")(x)\n    # Stage 2\n    x = conv_block(x, 3, [64, 64, 256], stage=2, block=\'a\', strides=(1, 1), train_bn=train_bn)\n    x = identity_block(x, 3, [64, 64, 256], stage=2, block=\'b\', train_bn=train_bn)\n    C2 = x = identity_block(x, 3, [64, 64, 256], stage=2, block=\'c\', train_bn=train_bn)\n    # Stage 3\n    x = conv_block(x, 3, [128, 128, 512], stage=3, block=\'a\', train_bn=train_bn)\n    x = identity_block(x, 3, [128, 128, 512], stage=3, block=\'b\', train_bn=train_bn)\n    x = identity_block(x, 3, [128, 128, 512], stage=3, block=\'c\', train_bn=train_bn)\n    C3 = x = identity_block(x, 3, [128, 128, 512], stage=3, block=\'d\', train_bn=train_bn)\n    # Stage 4\n    x = conv_block(x, 3, [256, 256, 1024], stage=4, block=\'a\', train_bn=train_bn)\n    block_count = {"resnet50": 5, "resnet101": 22}[architecture]\n    for i in range(block_count):\n        x = identity_block(x, 3, [256, 256, 1024], stage=4, block=chr(98 + i), train_bn=train_bn)\n    C4 = x\n    # Stage 5\n    if stage5:\n        x = conv_block(x, 3, [512, 512, 2048], stage=5, block=\'a\', train_bn=train_bn)\n        x = identity_block(x, 3, [512, 512, 2048], stage=5, block=\'b\', train_bn=train_bn)\n        C5 = x = identity_block(x, 3, [512, 512, 2048], stage=5, block=\'c\', train_bn=train_bn)\n    else:\n        C5 = None\n    return [C1, C2, C3, C4, C5]\n\n\n############################################################\n#  Proposal Layer\n############################################################\n\ndef apply_box_deltas_graph(boxes, deltas):\n    """Applies the given deltas to the given boxes.\n    boxes: [N, (y1, x1, y2, x2)] boxes to update\n    deltas: [N, (dy, dx, log(dh), log(dw))] refinements to apply\n    """\n    # Convert to y, x, h, w\n    height = boxes[:, 2] - boxes[:, 0]\n    width = boxes[:, 3] - boxes[:, 1]\n    center_y = boxes[:, 0] + 0.5 * height\n    center_x = boxes[:, 1] + 0.5 * width\n    # Apply deltas\n    center_y += deltas[:, 0] * height\n    center_x += deltas[:, 1] * width\n    height *= tf.exp(deltas[:, 2])\n    width *= tf.exp(deltas[:, 3])\n    # Convert back to y1, x1, y2, x2\n    y1 = center_y - 0.5 * height\n    x1 = center_x - 0.5 * width\n    y2 = y1 + height\n    x2 = x1 + width\n    result = tf.stack([y1, x1, y2, x2], axis=1, name="apply_box_deltas_out")\n    return result\n\n\ndef clip_boxes_graph(boxes, window):\n    """\n    boxes: [N, (y1, x1, y2, x2)]\n    window: [4] in the form y1, x1, y2, x2\n    """\n    # Split\n    wy1, wx1, wy2, wx2 = tf.split(window, 4)\n    y1, x1, y2, x2 = tf.split(boxes, 4, axis=1)\n    # Clip\n    y1 = tf.maximum(tf.minimum(y1, wy2), wy1)\n    x1 = tf.maximum(tf.minimum(x1, wx2), wx1)\n    y2 = tf.maximum(tf.minimum(y2, wy2), wy1)\n    x2 = tf.maximum(tf.minimum(x2, wx2), wx1)\n    clipped = tf.concat([y1, x1, y2, x2], axis=1, name="clipped_boxes")\n    clipped.set_shape((clipped.shape[0], 4))\n    return clipped\n\n\nclass ProposalLayer(KL.Layer):\n    """Receives anchor scores and selects a subset to pass as proposals\n    to the second stage. Filtering is done based on anchor scores and\n    non-max suppression to remove overlaps. It also applies bounding\n    box refinement deltas to anchors.\n\n    Inputs:\n        rpn_probs: [batch, num_anchors, (bg prob, fg prob)]\n        rpn_bbox: [batch, num_anchors, (dy, dx, log(dh), log(dw))]\n        anchors: [batch, num_anchors, (y1, x1, y2, x2)] anchors in normalized coordinates\n\n    Returns:\n        Proposals in normalized coordinates [batch, rois, (y1, x1, y2, x2)]\n    """\n\n    def __init__(self, proposal_count, nms_threshold, config=None, **kwargs):\n        super(ProposalLayer, self).__init__(**kwargs)\n        self.config = config\n        self.proposal_count = proposal_count\n        self.nms_threshold = nms_threshold\n\n    def call(self, inputs):\n        # Box Scores. Use the foreground class confidence. [Batch, num_rois, 1]\n        scores = inputs[0][:, :, 1]\n        # Box deltas [batch, num_rois, 4]\n        deltas = inputs[1]\n        deltas = deltas * np.reshape(self.config.RPN_BBOX_STD_DEV, [1, 1, 4])\n        # Anchors\n        anchors = inputs[2]\n\n        # Improve performance by trimming to top anchors by score\n        # and doing the rest on the smaller subset.\n        pre_nms_limit = tf.minimum(self.config.PRE_NMS_LIMIT, tf.shape(anchors)[1])\n        ix = tf.nn.top_k(scores, pre_nms_limit, sorted=True,\n                         name="top_anchors").indices\n        scores = utils.batch_slice([scores, ix], lambda x, y: tf.gather(x, y),\n                                   self.config.IMAGES_PER_GPU)\n        deltas = utils.batch_slice([deltas, ix], lambda x, y: tf.gather(x, y),\n                                   self.config.IMAGES_PER_GPU)\n        pre_nms_anchors = utils.batch_slice([anchors, ix], lambda a, x: tf.gather(a, x),\n                                    self.config.IMAGES_PER_GPU,\n                                    names=["pre_nms_anchors"])\n\n        # Apply deltas to anchors to get refined anchors.\n        # [batch, N, (y1, x1, y2, x2)]\n        boxes = utils.batch_slice([pre_nms_anchors, deltas],\n                                  lambda x, y: apply_box_deltas_graph(x, y),\n                                  self.config.IMAGES_PER_GPU,\n                                  names=["refined_anchors"])\n\n        # Clip to image boundaries. Since we\'re in normalized coordinates,\n        # clip to 0..1 range. [batch, N, (y1, x1, y2, x2)]\n        window = np.array([0, 0, 1, 1], dtype=np.float32)\n        boxes = utils.batch_slice(boxes,\n                                  lambda x: clip_boxes_graph(x, window),\n                                  self.config.IMAGES_PER_GPU,\n                                  names=["refined_anchors_clipped"])\n\n        # Filter out small boxes\n        # According to Xinlei Chen\'s paper, this reduces detection accuracy\n        # for small objects, so we\'re skipping it.\n\n        # Non-max suppression\n        def nms(boxes, scores):\n            indices = tf.image.non_max_suppression(\n                boxes, scores, self.proposal_count,\n                self.nms_threshold, name="rpn_non_max_suppression")\n            proposals = tf.gather(boxes, indices)\n            # Pad if needed\n            padding = tf.maximum(self.proposal_count - tf.shape(proposals)[0], 0)\n            proposals = tf.pad(proposals, [(0, padding), (0, 0)])\n            return proposals\n        proposals = utils.batch_slice([boxes, scores], nms,\n                                      self.config.IMAGES_PER_GPU)\n        return proposals\n\n    def compute_output_shape(self, input_shape):\n        return (None, self.proposal_count, 4)\n\n\n############################################################\n#  ROIAlign Layer\n############################################################\n\ndef log2_graph(x):\n    """Implementation of Log2. TF doesn\'t have a native implementation."""\n    return tf.math.log(x) / tf.math.log(2.0)\n\n\nclass PyramidROIAlign(KL.Layer):\n    """Implements ROI Pooling on multiple levels of the feature pyramid.\n\n    Params:\n    - pool_shape: [pool_height, pool_width] of the output pooled regions. Usually [7, 7]\n\n    Inputs:\n    - boxes: [batch, num_boxes, (y1, x1, y2, x2)] in normalized\n             coordinates. Possibly padded with zeros if not enough\n             boxes to fill the array.\n    - image_meta: [batch, (meta data)] Image details. See compose_image_meta()\n    - feature_maps: List of feature maps from different levels of the pyramid.\n                    Each is [batch, height, width, channels]\n\n    Output:\n    Pooled regions in the shape: [batch, num_boxes, pool_height, pool_width, channels].\n    The width and height are those specific in the pool_shape in the layer\n    constructor.\n    """\n\n    def __init__(self, pool_shape, **kwargs):\n        super(PyramidROIAlign, self).__init__(**kwargs)\n        self.pool_shape = tuple(pool_shape)\n\n    def call(self, inputs):\n        # Crop boxes [batch, num_boxes, (y1, x1, y2, x2)] in normalized coords\n        boxes = inputs[0]\n\n        # Image meta\n        # Holds details about the image. See compose_image_meta()\n        image_meta = inputs[1]\n\n        # Feature Maps. List of feature maps from different level of the\n        # feature pyramid. Each is [batch, height, width, channels]\n        feature_maps = inputs[2:]\n\n        # Assign each ROI to a level in the pyramid based on the ROI area.\n        y1, x1, y2, x2 = tf.split(boxes, 4, axis=2)\n        h = y2 - y1\n        w = x2 - x1\n        # Use shape of first image. Images in a batch must have the same size.\n        image_shape = parse_image_meta_graph(image_meta)[\'image_shape\'][0]\n        # Equation 1 in the Feature Pyramid Networks paper. Account for\n        # the fact that our coordinates are normalized here.\n        # e.g. a 224x224 ROI (in pixels) maps to P4\n        image_area = tf.cast(image_shape[0] * image_shape[1], tf.float32)\n        roi_level = log2_graph(tf.sqrt(h * w) / (224.0 / tf.sqrt(image_area)))\n        roi_level = tf.minimum(5, tf.maximum(\n            2, 4 + tf.cast(tf.round(roi_level), tf.int32)))\n        roi_level = tf.squeeze(roi_level, 2)\n\n        # Loop through levels and apply ROI pooling to each. P2 to P5.\n        pooled = []\n        box_to_level = []\n        for i, level in enumerate(range(2, 6)):\n            ix = tf.where(tf.equal(roi_level, level))\n            level_boxes = tf.gather_nd(boxes, ix)\n\n            # Box indices for crop_and_resize.\n            box_indices = tf.cast(ix[:, 0], tf.int32)\n\n            # Keep track of which box is mapped to which level\n            box_to_level.append(ix)\n\n            # Stop gradient propogation to ROI proposals\n            level_boxes = tf.stop_gradient(level_boxes)\n            box_indices = tf.stop_gradient(box_indices)\n\n            # Crop and Resize\n            # From Mask R-CNN paper: "We sample four regular locations, so\n            # that we can evaluate either max or average pooling. In fact,\n            # interpolating only a single value at each bin center (without\n            # pooling) is nearly as effective."\n            #\n            # Here we use the simplified approach of a single value per bin,\n            # which is how it\'s done in tf.crop_and_resize()\n            # Result: [batch * num_boxes, pool_height, pool_width, channels]\n            pooled.append(tf.image.crop_and_resize(\n                feature_maps[i], level_boxes, box_indices, self.pool_shape,\n                method="bilinear"))\n\n        # Pack pooled features into one tensor\n        pooled = tf.concat(pooled, axis=0)\n\n        # Pack box_to_level mapping into one array and add another\n        # column representing the order of pooled boxes\n        box_to_level = tf.concat(box_to_level, axis=0)\n        box_range = tf.expand_dims(tf.range(tf.shape(box_to_level)[0]), 1)\n        box_to_level = tf.concat([tf.cast(box_to_level, tf.int32), box_range],\n                                 axis=1)\n\n        # Rearrange pooled features to match the order of the original boxes\n        # Sort box_to_level by batch then box index\n        # TF doesn\'t have a way to sort by two columns, so merge them and sort.\n        sorting_tensor = box_to_level[:, 0] * 100000 + box_to_level[:, 1]\n        ix = tf.nn.top_k(sorting_tensor, k=tf.shape(\n            box_to_level)[0]).indices[::-1]\n        ix = tf.gather(box_to_level[:, 2], ix)\n        pooled = tf.gather(pooled, ix)\n\n        # Re-add the batch dimension\n        shape = tf.concat([tf.shape(boxes)[:2], tf.shape(pooled)[1:]], axis=0)\n        pooled = tf.reshape(pooled, shape)\n        return pooled\n\n    def compute_output_shape(self, input_shape):\n        return input_shape[0][:2] + self.pool_shape + (input_shape[2][-1], )\n\n\n############################################################\n#  Detection Target Layer\n############################################################\n\ndef overlaps_graph(boxes1, boxes2):\n    """Computes IoU overlaps between two sets of boxes.\n    boxes1, boxes2: [N, (y1, x1, y2, x2)].\n    """\n    # 1. Tile boxes2 and repeat boxes1. This allows us to compare\n    # every boxes1 against every boxes2 without loops.\n    # TF doesn\'t have an equivalent to np.repeat() so simulate it\n    # using tf.tile() and tf.reshape.\n    b1 = tf.reshape(tf.tile(tf.expand_dims(boxes1, 1),\n                            [1, 1, tf.shape(boxes2)[0]]), [-1, 4])\n    b2 = tf.tile(boxes2, [tf.shape(boxes1)[0], 1])\n    # 2. Compute intersections\n    b1_y1, b1_x1, b1_y2, b1_x2 = tf.split(b1, 4, axis=1)\n    b2_y1, b2_x1, b2_y2, b2_x2 = tf.split(b2, 4, axis=1)\n    y1 = tf.maximum(b1_y1, b2_y1)\n    x1 = tf.maximum(b1_x1, b2_x1)\n    y2 = tf.minimum(b1_y2, b2_y2)\n    x2 = tf.minimum(b1_x2, b2_x2)\n    intersection = tf.maximum(x2 - x1, 0) * tf.maximum(y2 - y1, 0)\n    # 3. Compute unions\n    b1_area = (b1_y2 - b1_y1) * (b1_x2 - b1_x1)\n    b2_area = (b2_y2 - b2_y1) * (b2_x2 - b2_x1)\n    union = b1_area + b2_area - intersection\n    # 4. Compute IoU and reshape to [boxes1, boxes2]\n    iou = intersection / union\n    overlaps = tf.reshape(iou, [tf.shape(boxes1)[0], tf.shape(boxes2)[0]])\n    return overlaps\n\n\ndef detection_targets_graph(proposals, gt_class_ids, gt_boxes, gt_masks, config):\n    """Generates detection targets for one image. Subsamples proposals and\n    generates target class IDs, bounding box deltas, and masks for each.\n\n    Inputs:\n    proposals: [POST_NMS_ROIS_TRAINING, (y1, x1, y2, x2)] in normalized coordinates. Might\n               be zero padded if there are not enough proposals.\n    gt_class_ids: [MAX_GT_INSTANCES] int class IDs\n    gt_boxes: [MAX_GT_INSTANCES, (y1, x1, y2, x2)] in normalized coordinates.\n    gt_masks: [height, width, MAX_GT_INSTANCES] of boolean type.\n\n    Returns: Target ROIs and corresponding class IDs, bounding box shifts,\n    and masks.\n    rois: [TRAIN_ROIS_PER_IMAGE, (y1, x1, y2, x2)] in normalized coordinates\n    class_ids: [TRAIN_ROIS_PER_IMAGE]. Integer class IDs. Zero padded.\n    deltas: [TRAIN_ROIS_PER_IMAGE, (dy, dx, log(dh), log(dw))]\n    masks: [TRAIN_ROIS_PER_IMAGE, height, width]. Masks cropped to bbox\n           boundaries and resized to neural network output size.\n\n    Note: Returned arrays might be zero padded if not enough target ROIs.\n    """\n    # Assertions\n    asserts = [\n        tf.Assert(tf.greater(tf.shape(proposals)[0], 0), [proposals],\n                  name="roi_assertion"),\n    ]\n    with tf.control_dependencies(asserts):\n        proposals = tf.identity(proposals)\n\n    # Remove zero padding\n    proposals, _ = trim_zeros_graph(proposals, name="trim_proposals")\n    gt_boxes, non_zeros = trim_zeros_graph(gt_boxes, name="trim_gt_boxes")\n    gt_class_ids = tf.boolean_mask(gt_class_ids, non_zeros,\n                                   name="trim_gt_class_ids")\n    gt_masks = tf.gather(gt_masks, tf.where(non_zeros)[:, 0], axis=2,\n                         name="trim_gt_masks")\n\n    # Handle COCO crowds\n    # A crowd box in COCO is a bounding box around several instances. Exclude\n    # them from training. A crowd box is given a negative class ID.\n    crowd_ix = tf.where(gt_class_ids < 0)[:, 0]\n    non_crowd_ix = tf.where(gt_class_ids > 0)[:, 0]\n    crowd_boxes = tf.gather(gt_boxes, crowd_ix)\n    gt_class_ids = tf.gather(gt_class_ids, non_crowd_ix)\n    gt_boxes = tf.gather(gt_boxes, non_crowd_ix)\n    gt_masks = tf.gather(gt_masks, non_crowd_ix, axis=2)\n\n    # Compute overlaps matrix [proposals, gt_boxes]\n    overlaps = overlaps_graph(proposals, gt_boxes)\n\n    # Compute overlaps with crowd boxes [proposals, crowd_boxes]\n    crowd_overlaps = overlaps_graph(proposals, crowd_boxes)\n    crowd_iou_max = tf.reduce_max(crowd_overlaps, axis=1)\n    no_crowd_bool = (crowd_iou_max < 0.001)\n\n    # Determine positive and negative ROIs\n    roi_iou_max = tf.reduce_max(overlaps, axis=1)\n    # 1. Positive ROIs are those with >= 0.5 IoU with a GT box\n    positive_roi_bool = (roi_iou_max >= 0.5)\n    positive_indices = tf.where(positive_roi_bool)[:, 0]\n    # 2. Negative ROIs are those with < 0.5 with every GT box. Skip crowds.\n    negative_indices = tf.where(tf.logical_and(roi_iou_max < 0.5, no_crowd_bool))[:, 0]\n\n    # Subsample ROIs. Aim for 33% positive\n    # Positive ROIs\n    positive_count = int(config.TRAIN_ROIS_PER_IMAGE *\n                         config.ROI_POSITIVE_RATIO)\n    positive_indices = tf.random.shuffle(positive_indices)[:positive_count]\n    positive_count = tf.shape(positive_indices)[0]\n    # Negative ROIs. Add enough to maintain positive:negative ratio.\n    r = 1.0 / config.ROI_POSITIVE_RATIO\n    negative_count = tf.cast(r * tf.cast(positive_count, tf.float32), tf.int32) - positive_count\n    negative_indices = tf.random.shuffle(negative_indices)[:negative_count]\n    # Gather selected ROIs\n    positive_rois = tf.gather(proposals, positive_indices)\n    negative_rois = tf.gather(proposals, negative_indices)\n\n    # Assign positive ROIs to GT boxes.\n    positive_overlaps = tf.gather(overlaps, positive_indices)\n    roi_gt_box_assignment = tf.cond(\n        tf.greater(tf.shape(positive_overlaps)[1], 0),\n        true_fn = lambda: tf.argmax(positive_overlaps, axis=1),\n        false_fn = lambda: tf.cast(tf.constant([]),tf.int64)\n    )\n    roi_gt_boxes = tf.gather(gt_boxes, roi_gt_box_assignment)\n    roi_gt_class_ids = tf.gather(gt_class_ids, roi_gt_box_assignment)\n\n    # Compute bbox refinement for positive ROIs\n    deltas = utils.box_refinement_graph(positive_rois, roi_gt_boxes)\n    deltas /= config.BBOX_STD_DEV\n\n    # Assign positive ROIs to GT masks\n    # Permute masks to [N, height, width, 1]\n    transposed_masks = tf.expand_dims(tf.transpose(gt_masks, [2, 0, 1]), -1)\n    # Pick the right mask for each ROI\n    roi_masks = tf.gather(transposed_masks, roi_gt_box_assignment)\n\n    # Compute mask targets\n    boxes = positive_rois\n    if config.USE_MINI_MASK:\n        # Transform ROI coordinates from normalized image space\n        # to normalized mini-mask space.\n        y1, x1, y2, x2 = tf.split(positive_rois, 4, axis=1)\n        gt_y1, gt_x1, gt_y2, gt_x2 = tf.split(roi_gt_boxes, 4, axis=1)\n        gt_h = gt_y2 - gt_y1\n        gt_w = gt_x2 - gt_x1\n        y1 = (y1 - gt_y1) / gt_h\n        x1 = (x1 - gt_x1) / gt_w\n        y2 = (y2 - gt_y1) / gt_h\n        x2 = (x2 - gt_x1) / gt_w\n        boxes = tf.concat([y1, x1, y2, x2], 1)\n    box_ids = tf.range(0, tf.shape(roi_masks)[0])\n    masks = tf.image.crop_and_resize(tf.cast(roi_masks, tf.float32), boxes,\n                                     box_ids,\n                                     config.MASK_SHAPE)\n    # Remove the extra dimension from masks.\n    masks = tf.squeeze(masks, axis=3)\n\n    # Threshold mask pixels at 0.5 to have GT masks be 0 or 1 to use with\n    # binary cross entropy loss.\n    masks = tf.round(masks)\n\n    # Append negative ROIs and pad bbox deltas and masks that\n    # are not used for negative ROIs with zeros.\n    rois = tf.concat([positive_rois, negative_rois], axis=0)\n    N = tf.shape(negative_rois)[0]\n    P = tf.maximum(config.TRAIN_ROIS_PER_IMAGE - tf.shape(rois)[0], 0)\n    rois = tf.pad(rois, [(0, P), (0, 0)])\n    roi_gt_boxes = tf.pad(roi_gt_boxes, [(0, N + P), (0, 0)])\n    roi_gt_class_ids = tf.pad(roi_gt_class_ids, [(0, N + P)])\n    deltas = tf.pad(deltas, [(0, N + P), (0, 0)])\n    masks = tf.pad(masks, [[0, N + P], (0, 0), (0, 0)])\n\n    return rois, roi_gt_class_ids, deltas, masks\n\n\nclass DetectionTargetLayer(KL.Layer):\n    """Subsamples proposals and generates target box refinement, class_ids,\n    and masks for each.\n\n    Inputs:\n    proposals: [batch, N, (y1, x1, y2, x2)] in normalized coordinates. Might\n               be zero padded if there are not enough proposals.\n    gt_class_ids: [batch, MAX_GT_INSTANCES] Integer class IDs.\n    gt_boxes: [batch, MAX_GT_INSTANCES, (y1, x1, y2, x2)] in normalized\n              coordinates.\n    gt_masks: [batch, height, width, MAX_GT_INSTANCES] of boolean type\n\n    Returns: Target ROIs and corresponding class IDs, bounding box shifts,\n    and masks.\n    rois: [batch, TRAIN_ROIS_PER_IMAGE, (y1, x1, y2, x2)] in normalized\n          coordinates\n    target_class_ids: [batch, TRAIN_ROIS_PER_IMAGE]. Integer class IDs.\n    target_deltas: [batch, TRAIN_ROIS_PER_IMAGE, (dy, dx, log(dh), log(dw)]\n    target_mask: [batch, TRAIN_ROIS_PER_IMAGE, height, width]\n                 Masks cropped to bbox boundaries and resized to neural\n                 network output size.\n\n    Note: Returned arrays might be zero padded if not enough target ROIs.\n    """\n\n    def __init__(self, config, **kwargs):\n        super(DetectionTargetLayer, self).__init__(**kwargs)\n        self.config = config\n\n    def call(self, inputs):\n        proposals = inputs[0]\n        gt_class_ids = inputs[1]\n        gt_boxes = inputs[2]\n        gt_masks = inputs[3]\n\n        # Slice the batch and run a graph for each slice\n        # TODO: Rename target_bbox to target_deltas for clarity\n        names = ["rois", "target_class_ids", "target_bbox", "target_mask"]\n        outputs = utils.batch_slice(\n            [proposals, gt_class_ids, gt_boxes, gt_masks],\n            lambda w, x, y, z: detection_targets_graph(\n                w, x, y, z, self.config),\n            self.config.IMAGES_PER_GPU, names=names)\n        return outputs\n\n    def compute_output_shape(self, input_shape):\n        return [\n            (None, self.config.TRAIN_ROIS_PER_IMAGE, 4),  # rois\n            (None, self.config.TRAIN_ROIS_PER_IMAGE),  # class_ids\n            (None, self.config.TRAIN_ROIS_PER_IMAGE, 4),  # deltas\n            (None, self.config.TRAIN_ROIS_PER_IMAGE, self.config.MASK_SHAPE[0],\n             self.config.MASK_SHAPE[1])  # masks\n        ]\n\n    def compute_mask(self, inputs, mask=None):\n        return [None, None, None, None]\n\n\n############################################################\n#  Detection Layer\n############################################################\n\ndef refine_detections_graph(rois, probs, deltas, window, config):\n    """Refine classified proposals and filter overlaps and return final\n    detections.\n\n    Inputs:\n        rois: [N, (y1, x1, y2, x2)] in normalized coordinates\n        probs: [N, num_classes]. Class probabilities.\n        deltas: [N, num_classes, (dy, dx, log(dh), log(dw))]. Class-specific\n                bounding box deltas.\n        window: (y1, x1, y2, x2) in normalized coordinates. The part of the image\n            that contains the image excluding the padding.\n\n    Returns detections shaped: [num_detections, (y1, x1, y2, x2, class_id, score)] where\n        coordinates are normalized.\n    """\n    # Class IDs per ROI\n    class_ids = tf.argmax(probs, axis=1, output_type=tf.int32)\n    # Class probability of the top class of each ROI\n    #print(rois.shape, probs.shape, deltas.shape)\n    indices = tf.stack([tf.range(1000), class_ids], axis=1)\n    class_scores = tf.gather_nd(probs, indices)\n    # Class-specific bounding box deltas\n    deltas_specific = tf.gather_nd(deltas, indices)\n    # Apply bounding box deltas\n    # Shape: [boxes, (y1, x1, y2, x2)] in normalized coordinates\n    refined_rois = apply_box_deltas_graph(\n        rois, deltas_specific * config.BBOX_STD_DEV)\n    # Clip boxes to image window\n    refined_rois = clip_boxes_graph(refined_rois, window)\n\n    # TODO: Filter out boxes with zero area\n\n    # Filter out background boxes\n    keep = tf.where(class_ids > 0)[:, 0]\n    # Filter out low confidence boxes\n    if config.DETECTION_MIN_CONFIDENCE:\n        conf_keep = tf.where(class_scores >= config.DETECTION_MIN_CONFIDENCE)[:, 0]\n        keep = tf.sets.intersection(tf.expand_dims(keep, 0),\n                                        tf.expand_dims(conf_keep, 0))\n        keep = tf.sparse.to_dense(keep)[0]\n\n    # Apply per-class NMS\n    # 1. Prepare variables\n    pre_nms_class_ids = tf.gather(class_ids, keep)\n    pre_nms_scores = tf.gather(class_scores, keep)\n    pre_nms_rois = tf.gather(refined_rois,   keep)\n    unique_pre_nms_class_ids = tf.unique(pre_nms_class_ids)[0]\n\n    def nms_keep_map(class_id):\n        """Apply Non-Maximum Suppression on ROIs of the given class."""\n        # Indices of ROIs of the given class\n        ixs = tf.where(tf.equal(pre_nms_class_ids, class_id))[:, 0]\n        # Apply NMS\n        class_keep = tf.image.non_max_suppression(\n                tf.gather(pre_nms_rois, ixs),\n                tf.gather(pre_nms_scores, ixs),\n                max_output_size=config.DETECTION_MAX_INSTANCES,\n                iou_threshold=config.DETECTION_NMS_THRESHOLD)\n        # Map indices\n        class_keep = tf.gather(keep, tf.gather(ixs, class_keep))\n        # Pad with -1 so returned tensors have the same shape\n        gap = config.DETECTION_MAX_INSTANCES - tf.shape(class_keep)[0]\n        class_keep = tf.pad(class_keep, [(0, gap)],\n                            mode=\'CONSTANT\', constant_values=-1)\n        # Set shape so map_fn() can infer result shape\n        class_keep.set_shape([config.DETECTION_MAX_INSTANCES])\n        return class_keep\n\n    # 2. Map over class IDs\n    nms_keep = tf.map_fn(nms_keep_map, unique_pre_nms_class_ids,\n                         dtype=tf.int64)\n    # 3. Merge results into one list, and remove -1 padding\n    nms_keep = tf.reshape(nms_keep, [-1])\n    nms_keep = tf.gather(nms_keep, tf.where(nms_keep > -1)[:, 0])\n    # 4. Compute intersection between keep and nms_keep\n    keep = tf.sets.intersection(tf.expand_dims(keep, 0),\n                                    tf.expand_dims(nms_keep, 0))\n    keep = tf.sparse.to_dense(keep)[0]\n    # Keep top detections\n    roi_count = config.DETECTION_MAX_INSTANCES\n    class_scores_keep = tf.gather(class_scores, keep)\n    num_keep = tf.minimum(tf.shape(class_scores_keep)[0], roi_count)\n    top_ids = tf.nn.top_k(class_scores_keep, k=num_keep, sorted=True)[1]\n    keep = tf.gather(keep, top_ids)\n\n    # Arrange output as [N, (y1, x1, y2, x2, class_id, score)]\n    # Coordinates are normalized.\n    detections = tf.concat([\n        tf.gather(refined_rois, keep),\n        tf.cast((tf.gather(class_ids, keep))[..., tf.newaxis], tf.float32),\n        tf.gather(class_scores, keep)[..., tf.newaxis]\n        ], axis=1)\n\n    # Pad with zeros if detections < DETECTION_MAX_INSTANCES\n    gap = config.DETECTION_MAX_INSTANCES - tf.shape(detections)[0]\n    detections = tf.pad(detections, [(0, gap), (0, 0)], "CONSTANT")\n    return detections\n\n\nclass DetectionLayer(KL.Layer):\n    """Takes classified proposal boxes and their bounding box deltas and\n    returns the final detection boxes.\n\n    Returns:\n    [batch, num_detections, (y1, x1, y2, x2, class_id, class_score)] where\n    coordinates are normalized.\n    """\n\n    def __init__(self, config=None, **kwargs):\n        super(DetectionLayer, self).__init__(**kwargs)\n        self.config = config\n\n    def call(self, inputs):\n        rois = inputs[0]\n        mrcnn_class = inputs[1]\n        mrcnn_bbox = inputs[2]\n        image_meta = inputs[3]\n\n        # Get windows of images in normalized coordinates. Windows are the area\n        # in the image that excludes the padding.\n        # Use the shape of the first image in the batch to normalize the window\n        # because we know that all images get resized to the same size.\n        m = parse_image_meta_graph(image_meta)\n        image_shape = m[\'image_shape\'][0]\n        window = norm_boxes_graph(m[\'window\'], image_shape[:2])\n\n        # Run detection refinement graph on each item in the batch\n        detections_batch = utils.batch_slice(\n            [rois, mrcnn_class, mrcnn_bbox, window],\n            lambda x, y, w, z: refine_detections_graph(x, y, w, z, self.config),\n            self.config.IMAGES_PER_GPU)\n\n        # Reshape output\n        # [batch, num_detections, (y1, x1, y2, x2, class_id, class_score)] in\n        # normalized coordinates\n        return tf.reshape(\n            detections_batch,\n            [self.config.BATCH_SIZE, self.config.DETECTION_MAX_INSTANCES, 6])\n\n    def compute_output_shape(self, input_shape):\n        return (None, self.config.DETECTION_MAX_INSTANCES, 6)\n\n\n############################################################\n#  Region Proposal Network (RPN)\n############################################################\n\ndef rpn_graph(feature_map, anchors_per_location, anchor_stride):\n    """Builds the computation graph of Region Proposal Network.\n\n    feature_map: backbone features [batch, height, width, depth]\n    anchors_per_location: number of anchors per pixel in the feature map\n    anchor_stride: Controls the density of anchors. Typically 1 (anchors for\n                   every pixel in the feature map), or 2 (every other pixel).\n\n    Returns:\n        rpn_class_logits: [batch, H * W * anchors_per_location, 2] Anchor classifier logits (before softmax)\n        rpn_probs: [batch, H * W * anchors_per_location, 2] Anchor classifier probabilities.\n        rpn_bbox: [batch, H * W * anchors_per_location, (dy, dx, log(dh), log(dw))] Deltas to be\n                  applied to anchors.\n    """\n    # TODO: check if stride of 2 causes alignment issues if the feature map\n    # is not even.\n    # Shared convolutional base of the RPN\n    shared = KL.Conv2D(512, (3, 3), padding=\'same\', activation=\'relu\',\n                       strides=anchor_stride,\n                       name=\'rpn_conv_shared\')(feature_map)\n\n    # Anchor Score. [batch, height, width, anchors per location * 2].\n    x = KL.Conv2D(2 * anchors_per_location, (1, 1), padding=\'valid\',\n                  activation=\'linear\', name=\'rpn_class_raw\')(shared)\n\n    # Reshape to [batch, anchors, 2]\n    rpn_class_logits = KL.Lambda(\n        lambda t: tf.reshape(t, [tf.shape(t)[0], -1, 2]))(x)\n\n    # Softmax on last dimension of BG/FG.\n    rpn_probs = KL.Activation(\n        "softmax", name="rpn_class_xxx")(rpn_class_logits)\n\n    # Bounding box refinement. [batch, H, W, anchors per location * depth]\n    # where depth is [x, y, log(w), log(h)]\n    x = KL.Conv2D(anchors_per_location * 4, (1, 1), padding="valid",\n                  activation=\'linear\', name=\'rpn_bbox_pred\')(shared)\n\n    # Reshape to [batch, anchors, 4]\n    rpn_bbox = KL.Lambda(lambda t: tf.reshape(t, [tf.shape(t)[0], -1, 4]))(x)\n\n    return [rpn_class_logits, rpn_probs, rpn_bbox]\n\n\ndef build_rpn_model(anchor_stride, anchors_per_location, depth):\n    """Builds a Keras model of the Region Proposal Network.\n    It wraps the RPN graph so it can be used multiple times with shared\n    weights.\n\n    anchors_per_location: number of anchors per pixel in the feature map\n    anchor_stride: Controls the density of anchors. Typically 1 (anchors for\n                   every pixel in the feature map), or 2 (every other pixel).\n    depth: Depth of the backbone feature map.\n\n    Returns a Keras Model object. The model outputs, when called, are:\n    rpn_class_logits: [batch, H * W * anchors_per_location, 2] Anchor classifier logits (before softmax)\n    rpn_probs: [batch, H * W * anchors_per_location, 2] Anchor classifier probabilities.\n    rpn_bbox: [batch, H * W * anchors_per_location, (dy, dx, log(dh), log(dw))] Deltas to be\n                applied to anchors.\n    """\n    input_feature_map = KL.Input(shape=[None, None, depth],\n                                 name="input_rpn_feature_map")\n    outputs = rpn_graph(input_feature_map, anchors_per_location, anchor_stride)\n    return KM.Model([input_feature_map], outputs, name="rpn_model")\n\n\n############################################################\n#  Feature Pyramid Network Heads\n############################################################\n\ndef fpn_classifier_graph(rois, feature_maps, image_meta,\n                         pool_size, num_classes, train_bn=True,\n                         fc_layers_size=1024):\n    """Builds the computation graph of the feature pyramid network classifier\n    and regressor heads.\n\n    rois: [batch, num_rois, (y1, x1, y2, x2)] Proposal boxes in normalized\n          coordinates.\n    feature_maps: List of feature maps from different layers of the pyramid,\n                  [P2, P3, P4, P5]. Each has a different resolution.\n    image_meta: [batch, (meta data)] Image details. See compose_image_meta()\n    pool_size: The width of the square feature map generated from ROI Pooling.\n    num_classes: number of classes, which determines the depth of the results\n    train_bn: Boolean. Train or freeze Batch Norm layers\n    fc_layers_size: Size of the 2 FC layers\n\n    Returns:\n        logits: [batch, num_rois, NUM_CLASSES] classifier logits (before softmax)\n        probs: [batch, num_rois, NUM_CLASSES] classifier probabilities\n        bbox_deltas: [batch, num_rois, NUM_CLASSES, (dy, dx, log(dh), log(dw))] Deltas to apply to\n                     proposal boxes\n    """\n    # ROI Pooling\n    # Shape: [batch, num_rois, POOL_SIZE, POOL_SIZE, channels]\n    x = PyramidROIAlign([pool_size, pool_size],\n                        name="roi_align_classifier")([rois, image_meta] + feature_maps)\n    # Two 1024 FC layers (implemented with Conv2D for consistency)\n    x = KL.TimeDistributed(KL.Conv2D(fc_layers_size, (pool_size, pool_size), padding="valid"),\n                           name="mrcnn_class_conv1")(x)\n    x = KL.TimeDistributed(BatchNorm(), name=\'mrcnn_class_bn1\')(x, training=train_bn)\n    x = KL.Activation(\'relu\')(x)\n    x = KL.TimeDistributed(KL.Conv2D(fc_layers_size, (1, 1)),\n                           name="mrcnn_class_conv2")(x)\n    x = KL.TimeDistributed(BatchNorm(), name=\'mrcnn_class_bn2\')(x, training=train_bn)\n    x = KL.Activation(\'relu\')(x)\n\n    shared = KL.Lambda(lambda x: K.squeeze(K.squeeze(x, 3), 2),\n                       name="pool_squeeze")(x)\n\n    # Classifier head\n    mrcnn_class_logits = KL.TimeDistributed(KL.Dense(num_classes),\n                                            name=\'mrcnn_class_logits\')(shared)\n    mrcnn_probs = KL.TimeDistributed(KL.Activation("softmax"),\n                                     name="mrcnn_class")(mrcnn_class_logits)\n\n    # BBox head\n    # [batch, num_rois, NUM_CLASSES * (dy, dx, log(dh), log(dw))]\n    x = KL.TimeDistributed(KL.Dense(num_classes * 4, activation=\'linear\'),\n                           name=\'mrcnn_bbox_fc\')(shared)\n    # Reshape to [batch, num_rois, NUM_CLASSES, (dy, dx, log(dh), log(dw))]\n    s = K.int_shape(x)\n    #print(s, (s[1], num_classes, 4))\n    mrcnn_bbox = KL.Reshape((-1, num_classes, 4), name="mrcnn_bbox")(x)\n\n    return mrcnn_class_logits, mrcnn_probs, mrcnn_bbox\n\n\ndef build_fpn_mask_graph(rois, feature_maps, image_meta,\n                         pool_size, num_classes, train_bn=True):\n    """Builds the computation graph of the mask head of Feature Pyramid Network.\n\n    rois: [batch, num_rois, (y1, x1, y2, x2)] Proposal boxes in normalized\n          coordinates.\n    feature_maps: List of feature maps from different layers of the pyramid,\n                  [P2, P3, P4, P5]. Each has a different resolution.\n    image_meta: [batch, (meta data)] Image details. See compose_image_meta()\n    pool_size: The width of the square feature map generated from ROI Pooling.\n    num_classes: number of classes, which determines the depth of the results\n    train_bn: Boolean. Train or freeze Batch Norm layers\n\n    Returns: Masks [batch, num_rois, MASK_POOL_SIZE, MASK_POOL_SIZE, NUM_CLASSES]\n    """\n    # ROI Pooling\n    # Shape: [batch, num_rois, MASK_POOL_SIZE, MASK_POOL_SIZE, channels]\n    x = PyramidROIAlign([pool_size, pool_size],\n                        name="roi_align_mask")([rois, image_meta] + feature_maps)\n\n    # Conv layers\n    x = KL.TimeDistributed(KL.Conv2D(256, (3, 3), padding="same"),\n                           name="mrcnn_mask_conv1")(x)\n    x = KL.TimeDistributed(BatchNorm(),\n                           name=\'mrcnn_mask_bn1\')(x, training=train_bn)\n    x = KL.Activation(\'relu\')(x)\n\n    x = KL.TimeDistributed(KL.Conv2D(256, (3, 3), padding="same"),\n                           name="mrcnn_mask_conv2")(x)\n    x = KL.TimeDistributed(BatchNorm(),\n                           name=\'mrcnn_mask_bn2\')(x, training=train_bn)\n    x = KL.Activation(\'relu\')(x)\n\n    x = KL.TimeDistributed(KL.Conv2D(256, (3, 3), padding="same"),\n                           name="mrcnn_mask_conv3")(x)\n    x = KL.TimeDistributed(BatchNorm(),\n                           name=\'mrcnn_mask_bn3\')(x, training=train_bn)\n    x = KL.Activation(\'relu\')(x)\n\n    x = KL.TimeDistributed(KL.Conv2D(256, (3, 3), padding="same"),\n                           name="mrcnn_mask_conv4")(x)\n    x = KL.TimeDistributed(BatchNorm(),\n                           name=\'mrcnn_mask_bn4\')(x, training=train_bn)\n    x = KL.Activation(\'relu\')(x)\n\n    x = KL.TimeDistributed(KL.Conv2DTranspose(256, (2, 2), strides=2, activation="relu"),\n                           name="mrcnn_mask_deconv")(x)\n    x = KL.TimeDistributed(KL.Conv2D(num_classes, (1, 1), strides=1, activation="sigmoid"),\n                           name="mrcnn_mask")(x)\n    return x\n\n\n############################################################\n#  Loss Functions\n############################################################\n\ndef smooth_l1_loss(y_true, y_pred):\n    """Implements Smooth-L1 loss.\n    y_true and y_pred are typically: [N, 4], but could be any shape.\n    """\n    diff = K.abs(y_true - y_pred)\n    less_than_one = K.cast(K.less(diff, 1.0), "float32")\n    loss = (less_than_one * 0.5 * diff**2) + (1 - less_than_one) * (diff - 0.5)\n    return loss\n\n\ndef rpn_class_loss_graph(rpn_match, rpn_class_logits):\n    """RPN anchor classifier loss.\n\n    rpn_match: [batch, anchors, 1]. Anchor match type. 1=positive,\n               -1=negative, 0=neutral anchor.\n    rpn_class_logits: [batch, anchors, 2]. RPN classifier logits for BG/FG.\n    """\n    # Squeeze last dim to simplify\n    rpn_match = tf.squeeze(rpn_match, -1)\n    # Get anchor classes. Convert the -1/+1 match to 0/1 values.\n    anchor_class = K.cast(K.equal(rpn_match, 1), tf.int32)\n    # Positive and Negative anchors contribute to the loss,\n    # but neutral anchors (match value = 0) don\'t.\n    indices = tf.where(K.not_equal(rpn_match, 0))\n    # Pick rows that contribute to the loss and filter out the rest.\n    rpn_class_logits = tf.gather_nd(rpn_class_logits, indices)\n    anchor_class = tf.gather_nd(anchor_class, indices)\n    # Cross entropy loss\n    loss = K.sparse_categorical_crossentropy(target=anchor_class,\n                                             output=rpn_class_logits,\n                                             from_logits=True)\n    loss = K.switch(tf.size(loss) > 0, K.mean(loss), tf.constant(0.0))\n    return loss\n\n\ndef rpn_bbox_loss_graph(config, target_bbox, rpn_match, rpn_bbox):\n    """Return the RPN bounding box loss graph.\n\n    config: the model config object.\n    target_bbox: [batch, max positive anchors, (dy, dx, log(dh), log(dw))].\n        Uses 0 padding to fill in unsed bbox deltas.\n    rpn_match: [batch, anchors, 1]. Anchor match type. 1=positive,\n               -1=negative, 0=neutral anchor.\n    rpn_bbox: [batch, anchors, (dy, dx, log(dh), log(dw))]\n    """\n    # Positive anchors contribute to the loss, but negative and\n    # neutral anchors (match value of 0 or -1) don\'t.\n    rpn_match = K.squeeze(rpn_match, -1)\n    indices = tf.where(K.equal(rpn_match, 1))\n\n    # Pick bbox deltas that contribute to the loss\n    rpn_bbox = tf.gather_nd(rpn_bbox, indices)\n\n    # Trim target bounding box deltas to the same length as rpn_bbox.\n    batch_counts = K.sum(K.cast(K.equal(rpn_match, 1), tf.int32), axis=1)\n    target_bbox = batch_pack_graph(target_bbox, batch_counts,\n                                   config.IMAGES_PER_GPU)\n\n    loss = smooth_l1_loss(target_bbox, rpn_bbox)\n    \n    loss = K.switch(tf.size(loss) > 0, K.mean(loss), tf.constant(0.0))\n    return loss\n\n\ndef mrcnn_class_loss_graph(target_class_ids, pred_class_logits,\n                           active_class_ids):\n    """Loss for the classifier head of Mask RCNN.\n\n    target_class_ids: [batch, num_rois]. Integer class IDs. Uses zero\n        padding to fill in the array.\n    pred_class_logits: [batch, num_rois, num_classes]\n    active_class_ids: [batch, num_classes]. Has a value of 1 for\n        classes that are in the dataset of the image, and 0\n        for classes that are not in the dataset.\n    """\n    # During model building, Keras calls this function with\n    # target_class_ids of type float32. Unclear why. Cast it\n    # to int to get around it.\n    target_class_ids = tf.cast(target_class_ids, \'int64\')\n\n    # Find predictions of classes that are not in the dataset.\n    pred_class_ids = tf.argmax(pred_class_logits, axis=2)\n    # TODO: Update this line to work with batch > 1. Right now it assumes all\n    #       images in a batch have the same active_class_ids\n    pred_active = tf.gather(active_class_ids[0], pred_class_ids)\n\n    # Loss\n    loss = tf.nn.sparse_softmax_cross_entropy_with_logits(\n        labels=target_class_ids, logits=pred_class_logits)\n\n    # Erase losses of predictions of classes that are not in the active\n    # classes of the image.\n    loss = loss * pred_active\n\n    # Computer loss mean. Use only predictions that contribute\n    # to the loss to get a correct mean.\n    loss = tf.reduce_sum(loss) / tf.reduce_sum(pred_active)\n    return loss\n\n\ndef mrcnn_bbox_loss_graph(target_bbox, target_class_ids, pred_bbox):\n    """Loss for Mask R-CNN bounding box refinement.\n\n    target_bbox: [batch, num_rois, (dy, dx, log(dh), log(dw))]\n    target_class_ids: [batch, num_rois]. Integer class IDs.\n    pred_bbox: [batch, num_rois, num_classes, (dy, dx, log(dh), log(dw))]\n    """\n    # Reshape to merge batch and roi dimensions for simplicity.\n    target_class_ids = K.reshape(target_class_ids, (-1,))\n    target_bbox = K.reshape(target_bbox, (-1, 4))\n    pred_bbox = K.reshape(pred_bbox, (-1, K.int_shape(pred_bbox)[2], 4))\n\n    # Only positive ROIs contribute to the loss. And only\n    # the right class_id of each ROI. Get their indices.\n    positive_roi_ix = tf.where(target_class_ids > 0)[:, 0]\n    positive_roi_class_ids = tf.cast(\n        tf.gather(target_class_ids, positive_roi_ix), tf.int64)\n    indices = tf.stack([positive_roi_ix, positive_roi_class_ids], axis=1)\n\n    # Gather the deltas (predicted and true) that contribute to loss\n    target_bbox = tf.gather(target_bbox, positive_roi_ix)\n    pred_bbox = tf.gather_nd(pred_bbox, indices)\n\n    # Smooth-L1 Loss\n    loss = K.switch(tf.size(target_bbox) > 0,\n                    smooth_l1_loss(y_true=target_bbox, y_pred=pred_bbox),\n                    tf.constant(0.0))\n    loss = K.mean(loss)\n    return loss\n\n\ndef mrcnn_mask_loss_graph(target_masks, target_class_ids, pred_masks):\n    """Mask binary cross-entropy loss for the masks head.\n\n    target_masks: [batch, num_rois, height, width].\n        A float32 tensor of values 0 or 1. Uses zero padding to fill array.\n    target_class_ids: [batch, num_rois]. Integer class IDs. Zero padded.\n    pred_masks: [batch, proposals, height, width, num_classes] float32 tensor\n                with values from 0 to 1.\n    """\n    # Reshape for simplicity. Merge first two dimensions into one.\n    target_class_ids = K.reshape(target_class_ids, (-1,))\n    mask_shape = tf.shape(target_masks)\n    target_masks = K.reshape(target_masks, (-1, mask_shape[2], mask_shape[3]))\n    pred_shape = tf.shape(pred_masks)\n    pred_masks = K.reshape(pred_masks,\n                           (-1, pred_shape[2], pred_shape[3], pred_shape[4]))\n    # Permute predicted masks to [N, num_classes, height, width]\n    pred_masks = tf.transpose(pred_masks, [0, 3, 1, 2])\n\n    # Only positive ROIs contribute to the loss. And only\n    # the class specific mask of each ROI.\n    positive_ix = tf.where(target_class_ids > 0)[:, 0]\n    positive_class_ids = tf.cast(\n        tf.gather(target_class_ids, positive_ix), tf.int64)\n    indices = tf.stack([positive_ix, positive_class_ids], axis=1)\n\n    # Gather the masks (predicted and true) that contribute to loss\n    y_true = tf.gather(target_masks, positive_ix)\n    y_pred = tf.gather_nd(pred_masks, indices)\n\n    # Compute binary cross entropy. If no positive ROIs, then return 0.\n    # shape: [batch, roi, num_classes]\n    loss = K.switch(tf.size(y_true) > 0,\n                    K.binary_crossentropy(target=y_true, output=y_pred),\n                    tf.constant(0.0))\n    loss = K.mean(loss)\n    return loss\n\n\n############################################################\n#  Data Generator\n############################################################\n\ndef load_image_gt(dataset, config, image_id, augment=False, augmentation=None,\n                  use_mini_mask=False):\n    """Load and return ground truth data for an image (image, mask, bounding boxes).\n\n    augment: (deprecated. Use augmentation instead). If true, apply random\n        image augmentation. Currently, only horizontal flipping is offered.\n    augmentation: Optional. An imgaug (https://github.com/aleju/imgaug) augmentation.\n        For example, passing imgaug.augmenters.Fliplr(0.5) flips images\n        right/left 50% of the time.\n    use_mini_mask: If False, returns full-size masks that are the same height\n        and width as the original image. These can be big, for example\n        1024x1024x100 (for 100 instances). Mini masks are smaller, typically,\n        224x224 and are generated by extracting the bounding box of the\n        object and resizing it to MINI_MASK_SHAPE.\n\n    Returns:\n    image: [height, width, 3]\n    shape: the original shape of the image before resizing and cropping.\n    class_ids: [instance_count] Integer class IDs\n    bbox: [instance_count, (y1, x1, y2, x2)]\n    mask: [height, width, instance_count]. The height and width are those\n        of the image unless use_mini_mask is True, in which case they are\n        defined in MINI_MASK_SHAPE.\n    """\n    # Load image and mask\n    image = dataset.load_image(image_id)\n    mask, class_ids = dataset.load_mask(image_id)\n    original_shape = image.shape\n    image, window, scale, padding, crop = utils.resize_image(\n        image,\n        min_dim=config.IMAGE_MIN_DIM,\n        min_scale=config.IMAGE_MIN_SCALE,\n        max_dim=config.IMAGE_MAX_DIM,\n        mode=config.IMAGE_RESIZE_MODE)\n    mask = utils.resize_mask(mask, scale, padding, crop)\n\n    # Random horizontal flips.\n    # TODO: will be removed in a future update in favor of augmentation\n    if augment:\n        logging.warning("\'augment\' is deprecated. Use \'augmentation\' instead.")\n        if random.randint(0, 1):\n            image = np.fliplr(image)\n            mask = np.fliplr(mask)\n\n    # Augmentation\n    # This requires the imgaug lib (https://github.com/aleju/imgaug)\n    if augmentation:\n        import imgaug\n\n        # Augmenters that are safe to apply to masks\n        # Some, such as Affine, have settings that make them unsafe, so always\n        # test your augmentation on masks\n        MASK_AUGMENTERS = ["Sequential", "SomeOf", "OneOf", "Sometimes",\n                           "Fliplr", "Flipud", "CropAndPad",\n                           "Affine", "PiecewiseAffine"]\n\n        def hook(images, augmenter, parents, default):\n            """Determines which augmenters to apply to masks."""\n            return augmenter.__class__.__name__ in MASK_AUGMENTERS\n\n        # Store shapes before augmentation to compare\n        image_shape = image.shape\n        mask_shape = mask.shape\n        # Make augmenters deterministic to apply similarly to images and masks\n        det = augmentation.to_deterministic()\n        image = det.augment_image(image)\n        # Change mask to np.uint8 because imgaug doesn\'t support np.bool\n        mask = det.augment_image(mask.astype(np.uint8),\n                                 hooks=imgaug.HooksImages(activator=hook))\n        # Verify that shapes didn\'t change\n        assert image.shape == image_shape, "Augmentation shouldn\'t change image size"\n        assert mask.shape == mask_shape, "Augmentation shouldn\'t change mask size"\n        # Change mask back to bool\n        mask = mask.astype(np.bool)\n\n    # Note that some boxes might be all zeros if the corresponding mask got cropped out.\n    # and here is to filter them out\n    _idx = np.sum(mask, axis=(0, 1)) > 0\n    mask = mask[:, :, _idx]\n    class_ids = class_ids[_idx]\n    # Bounding boxes. Note that some boxes might be all zeros\n    # if the corresponding mask got cropped out.\n    # bbox: [num_instances, (y1, x1, y2, x2)]\n    bbox = utils.extract_bboxes(mask)\n\n    # Active classes\n    # Different datasets have different classes, so track the\n    # classes supported in the dataset of this image.\n    active_class_ids = np.zeros([dataset.num_classes], dtype=np.int32)\n    source_class_ids = dataset.source_class_ids[dataset.image_info[image_id]["source"]]\n    active_class_ids[source_class_ids] = 1\n\n    # Resize masks to smaller size to reduce memory usage\n    if use_mini_mask:\n        mask = utils.minimize_mask(bbox, mask, config.MINI_MASK_SHAPE)\n\n    # Image meta data\n    image_meta = compose_image_meta(image_id, original_shape, image.shape,\n                                    window, scale, active_class_ids)\n\n    return image, image_meta, class_ids, bbox, mask\n\n\ndef build_detection_targets(rpn_rois, gt_class_ids, gt_boxes, gt_masks, config):\n    """Generate targets for training Stage 2 classifier and mask heads.\n    This is not used in normal training. It\'s useful for debugging or to train\n    the Mask RCNN heads without using the RPN head.\n\n    Inputs:\n    rpn_rois: [N, (y1, x1, y2, x2)] proposal boxes.\n    gt_class_ids: [instance count] Integer class IDs\n    gt_boxes: [instance count, (y1, x1, y2, x2)]\n    gt_masks: [height, width, instance count] Ground truth masks. Can be full\n              size or mini-masks.\n\n    Returns:\n    rois: [TRAIN_ROIS_PER_IMAGE, (y1, x1, y2, x2)]\n    class_ids: [TRAIN_ROIS_PER_IMAGE]. Integer class IDs.\n    bboxes: [TRAIN_ROIS_PER_IMAGE, NUM_CLASSES, (y, x, log(h), log(w))]. Class-specific\n            bbox refinements.\n    masks: [TRAIN_ROIS_PER_IMAGE, height, width, NUM_CLASSES). Class specific masks cropped\n           to bbox boundaries and resized to neural network output size.\n    """\n    assert rpn_rois.shape[0] > 0\n    assert gt_class_ids.dtype == np.int32, "Expected int but got {}".format(\n        gt_class_ids.dtype)\n    assert gt_boxes.dtype == np.int32, "Expected int but got {}".format(\n        gt_boxes.dtype)\n    assert gt_masks.dtype == np.bool_, "Expected bool but got {}".format(\n        gt_masks.dtype)\n\n    # It\'s common to add GT Boxes to ROIs but we don\'t do that here because\n    # according to XinLei Chen\'s paper, it doesn\'t help.\n\n    # Trim empty padding in gt_boxes and gt_masks parts\n    instance_ids = np.where(gt_class_ids > 0)[0]\n    assert instance_ids.shape[0] > 0, "Image must contain instances."\n    gt_class_ids = gt_class_ids[instance_ids]\n    gt_boxes = gt_boxes[instance_ids]\n    gt_masks = gt_masks[:, :, instance_ids]\n\n    # Compute areas of ROIs and ground truth boxes.\n    rpn_roi_area = (rpn_rois[:, 2] - rpn_rois[:, 0]) * \\\n        (rpn_rois[:, 3] - rpn_rois[:, 1])\n    gt_box_area = (gt_boxes[:, 2] - gt_boxes[:, 0]) * \\\n        (gt_boxes[:, 3] - gt_boxes[:, 1])\n\n    # Compute overlaps [rpn_rois, gt_boxes]\n    overlaps = np.zeros((rpn_rois.shape[0], gt_boxes.shape[0]))\n    for i in range(overlaps.shape[1]):\n        gt = gt_boxes[i]\n        overlaps[:, i] = utils.compute_iou(\n            gt, rpn_rois, gt_box_area[i], rpn_roi_area)\n\n    # Assign ROIs to GT boxes\n    rpn_roi_iou_argmax = np.argmax(overlaps, axis=1)\n    rpn_roi_iou_max = overlaps[np.arange(\n        overlaps.shape[0]), rpn_roi_iou_argmax]\n    # GT box assigned to each ROI\n    rpn_roi_gt_boxes = gt_boxes[rpn_roi_iou_argmax]\n    rpn_roi_gt_class_ids = gt_class_ids[rpn_roi_iou_argmax]\n\n    # Positive ROIs are those with >= 0.5 IoU with a GT box.\n    fg_ids = np.where(rpn_roi_iou_max > 0.5)[0]\n\n    # Negative ROIs are those with max IoU 0.1-0.5 (hard example mining)\n    # TODO: To hard example mine or not to hard example mine, that\'s the question\n    # bg_ids = np.where((rpn_roi_iou_max >= 0.1) & (rpn_roi_iou_max < 0.5))[0]\n    bg_ids = np.where(rpn_roi_iou_max < 0.5)[0]\n\n    # Subsample ROIs. Aim for 33% foreground.\n    # FG\n    fg_roi_count = int(config.TRAIN_ROIS_PER_IMAGE * config.ROI_POSITIVE_RATIO)\n    if fg_ids.shape[0] > fg_roi_count:\n        keep_fg_ids = np.random.choice(fg_ids, fg_roi_count, replace=False)\n    else:\n        keep_fg_ids = fg_ids\n    # BG\n    remaining = config.TRAIN_ROIS_PER_IMAGE - keep_fg_ids.shape[0]\n    if bg_ids.shape[0] > remaining:\n        keep_bg_ids = np.random.choice(bg_ids, remaining, replace=False)\n    else:\n        keep_bg_ids = bg_ids\n    # Combine indices of ROIs to keep\n    keep = np.concatenate([keep_fg_ids, keep_bg_ids])\n    # Need more?\n    remaining = config.TRAIN_ROIS_PER_IMAGE - keep.shape[0]\n    if remaining > 0:\n        # Looks like we don\'t have enough samples to maintain the desired\n        # balance. Reduce requirements and fill in the rest. This is\n        # likely different from the Mask RCNN paper.\n\n        # There is a small chance we have neither fg nor bg samples.\n        if keep.shape[0] == 0:\n            # Pick bg regions with easier IoU threshold\n            bg_ids = np.where(rpn_roi_iou_max < 0.5)[0]\n            assert bg_ids.shape[0] >= remaining\n            keep_bg_ids = np.random.choice(bg_ids, remaining, replace=False)\n            assert keep_bg_ids.shape[0] == remaining\n            keep = np.concatenate([keep, keep_bg_ids])\n        else:\n            # Fill the rest with repeated bg rois.\n            keep_extra_ids = np.random.choice(\n                keep_bg_ids, remaining, replace=True)\n            keep = np.concatenate([keep, keep_extra_ids])\n    assert keep.shape[0] == config.TRAIN_ROIS_PER_IMAGE, \\\n        "keep doesn\'t match ROI batch size {}, {}".format(\n            keep.shape[0], config.TRAIN_ROIS_PER_IMAGE)\n\n    # Reset the gt boxes assigned to BG ROIs.\n    rpn_roi_gt_boxes[keep_bg_ids, :] = 0\n    rpn_roi_gt_class_ids[keep_bg_ids] = 0\n\n    # For each kept ROI, assign a class_id, and for FG ROIs also add bbox refinement.\n    rois = rpn_rois[keep]\n    roi_gt_boxes = rpn_roi_gt_boxes[keep]\n    roi_gt_class_ids = rpn_roi_gt_class_ids[keep]\n    roi_gt_assignment = rpn_roi_iou_argmax[keep]\n\n    # Class-aware bbox deltas. [y, x, log(h), log(w)]\n    bboxes = np.zeros((config.TRAIN_ROIS_PER_IMAGE,\n                       config.NUM_CLASSES, 4), dtype=np.float32)\n    pos_ids = np.where(roi_gt_class_ids > 0)[0]\n    bboxes[pos_ids, roi_gt_class_ids[pos_ids]] = utils.box_refinement(\n        rois[pos_ids], roi_gt_boxes[pos_ids, :4])\n    # Normalize bbox refinements\n    bboxes /= config.BBOX_STD_DEV\n\n    # Generate class-specific target masks\n    masks = np.zeros((config.TRAIN_ROIS_PER_IMAGE, config.MASK_SHAPE[0], config.MASK_SHAPE[1], config.NUM_CLASSES),\n                     dtype=np.float32)\n    for i in pos_ids:\n        class_id = roi_gt_class_ids[i]\n        assert class_id > 0, "class id must be greater than 0"\n        gt_id = roi_gt_assignment[i]\n        class_mask = gt_masks[:, :, gt_id]\n\n        if config.USE_MINI_MASK:\n            # Create a mask placeholder, the size of the image\n            placeholder = np.zeros(config.IMAGE_SHAPE[:2], dtype=bool)\n            # GT box\n            gt_y1, gt_x1, gt_y2, gt_x2 = gt_boxes[gt_id]\n            gt_w = gt_x2 - gt_x1\n            gt_h = gt_y2 - gt_y1\n            # Resize mini mask to size of GT box\n            placeholder[gt_y1:gt_y2, gt_x1:gt_x2] = \\\n                np.round(utils.resize(class_mask, (gt_h, gt_w))).astype(bool)\n            # Place the mini batch in the placeholder\n            class_mask = placeholder\n\n        # Pick part of the mask and resize it\n        y1, x1, y2, x2 = rois[i].astype(np.int32)\n        m = class_mask[y1:y2, x1:x2]\n        mask = utils.resize(m, config.MASK_SHAPE)\n        masks[i, :, :, class_id] = mask\n\n    return rois, roi_gt_class_ids, bboxes, masks\n\n\ndef build_rpn_targets(image_shape, anchors, gt_class_ids, gt_boxes, config):\n    """Given the anchors and GT boxes, compute overlaps and identify positive\n    anchors and deltas to refine them to match their corresponding GT boxes.\n\n    anchors: [num_anchors, (y1, x1, y2, x2)]\n    gt_class_ids: [num_gt_boxes] Integer class IDs.\n    gt_boxes: [num_gt_boxes, (y1, x1, y2, x2)]\n\n    Returns:\n    rpn_match: [N] (int32) matches between anchors and GT boxes.\n               1 = positive anchor, -1 = negative anchor, 0 = neutral\n    rpn_bbox: [N, (dy, dx, log(dh), log(dw))] Anchor bbox deltas.\n    """\n    # RPN Match: 1 = positive anchor, -1 = negative anchor, 0 = neutral\n    rpn_match = np.zeros([anchors.shape[0]], dtype=np.int32)\n    # RPN bounding boxes: [max anchors per image, (dy, dx, log(dh), log(dw))]\n    rpn_bbox = np.zeros((config.RPN_TRAIN_ANCHORS_PER_IMAGE, 4))\n\n    # Handle COCO crowds\n    # A crowd box in COCO is a bounding box around several instances. Exclude\n    # them from training. A crowd box is given a negative class ID.\n    crowd_ix = np.where(gt_class_ids < 0)[0]\n    if crowd_ix.shape[0] > 0:\n        # Filter out crowds from ground truth class IDs and boxes\n        non_crowd_ix = np.where(gt_class_ids > 0)[0]\n        crowd_boxes = gt_boxes[crowd_ix]\n        gt_class_ids = gt_class_ids[non_crowd_ix]\n        gt_boxes = gt_boxes[non_crowd_ix]\n        # Compute overlaps with crowd boxes [anchors, crowds]\n        crowd_overlaps = utils.compute_overlaps(anchors, crowd_boxes)\n        crowd_iou_max = np.amax(crowd_overlaps, axis=1)\n        no_crowd_bool = (crowd_iou_max < 0.001)\n    else:\n        # All anchors don\'t intersect a crowd\n        no_crowd_bool = np.ones([anchors.shape[0]], dtype=bool)\n\n    # Compute overlaps [num_anchors, num_gt_boxes]\n    overlaps = utils.compute_overlaps(anchors, gt_boxes)\n\n    # Match anchors to GT Boxes\n    # If an anchor overlaps a GT box with IoU >= 0.7 then it\'s positive.\n    # If an anchor overlaps a GT box with IoU < 0.3 then it\'s negative.\n    # Neutral anchors are those that don\'t match the conditions above,\n    # and they don\'t influence the loss function.\n    # However, don\'t keep any GT box unmatched (rare, but happens). Instead,\n    # match it to the closest anchor (even if its max IoU is < 0.3).\n    #\n    # 1. Set negative anchors first. They get overwritten below if a GT box is\n    # matched to them. Skip boxes in crowd areas.\n    anchor_iou_argmax = np.argmax(overlaps, axis=1)\n    anchor_iou_max = overlaps[np.arange(overlaps.shape[0]), anchor_iou_argmax]\n    rpn_match[(anchor_iou_max < 0.3) & (no_crowd_bool)] = -1\n    # 2. Set an anchor for each GT box (regardless of IoU value).\n    # If multiple anchors have the same IoU match all of them\n    gt_iou_argmax = np.argwhere(overlaps == np.max(overlaps, axis=0))[:,0]\n    rpn_match[gt_iou_argmax] = 1\n    # 3. Set anchors with high overlap as positive.\n    rpn_match[anchor_iou_max >= 0.7] = 1\n\n    # Subsample to balance positive and negative anchors\n    # Don\'t let positives be more than half the anchors\n    ids = np.where(rpn_match == 1)[0]\n    extra = len(ids) - (config.RPN_TRAIN_ANCHORS_PER_IMAGE // 2)\n    if extra > 0:\n        # Reset the extra ones to neutral\n        ids = np.random.choice(ids, extra, replace=False)\n        rpn_match[ids] = 0\n    # Same for negative proposals\n    ids = np.where(rpn_match == -1)[0]\n    extra = len(ids) - (config.RPN_TRAIN_ANCHORS_PER_IMAGE -\n                        np.sum(rpn_match == 1))\n    if extra > 0:\n        # Rest the extra ones to neutral\n        ids = np.random.choice(ids, extra, replace=False)\n        rpn_match[ids] = 0\n\n    # For positive anchors, compute shift and scale needed to transform them\n    # to match the corresponding GT boxes.\n    ids = np.where(rpn_match == 1)[0]\n    ix = 0  # index into rpn_bbox\n    # TODO: use box_refinement() rather than duplicating the code here\n    for i, a in zip(ids, anchors[ids]):\n        # Closest gt box (it might have IoU < 0.7)\n        gt = gt_boxes[anchor_iou_argmax[i]]\n\n        # Convert coordinates to center plus width/height.\n        # GT Box\n        gt_h = gt[2] - gt[0]\n        gt_w = gt[3] - gt[1]\n        gt_center_y = gt[0] + 0.5 * gt_h\n        gt_center_x = gt[1] + 0.5 * gt_w\n        # Anchor\n        a_h = a[2] - a[0]\n        a_w = a[3] - a[1]\n        a_center_y = a[0] + 0.5 * a_h\n        a_center_x = a[1] + 0.5 * a_w\n\n        # Compute the bbox refinement that the RPN should predict.\n        rpn_bbox[ix] = [\n            (gt_center_y - a_center_y) / a_h,\n            (gt_center_x - a_center_x) / a_w,\n            np.log(gt_h / a_h),\n            np.log(gt_w / a_w),\n        ]\n        # Normalize\n        rpn_bbox[ix] /= config.RPN_BBOX_STD_DEV\n        ix += 1\n\n    return rpn_match, rpn_bbox\n\n\ndef generate_random_rois(image_shape, count, gt_class_ids, gt_boxes):\n    """Generates ROI proposals similar to what a region proposal network\n    would generate.\n\n    image_shape: [Height, Width, Depth]\n    count: Number of ROIs to generate\n    gt_class_ids: [N] Integer ground truth class IDs\n    gt_boxes: [N, (y1, x1, y2, x2)] Ground truth boxes in pixels.\n\n    Returns: [count, (y1, x1, y2, x2)] ROI boxes in pixels.\n    """\n    # placeholder\n    rois = np.zeros((count, 4), dtype=np.int32)\n\n    # Generate random ROIs around GT boxes (90% of count)\n    rois_per_box = int(0.9 * count / gt_boxes.shape[0])\n    for i in range(gt_boxes.shape[0]):\n        gt_y1, gt_x1, gt_y2, gt_x2 = gt_boxes[i]\n        h = gt_y2 - gt_y1\n        w = gt_x2 - gt_x1\n        # random boundaries\n        r_y1 = max(gt_y1 - h, 0)\n        r_y2 = min(gt_y2 + h, image_shape[0])\n        r_x1 = max(gt_x1 - w, 0)\n        r_x2 = min(gt_x2 + w, image_shape[1])\n\n        # To avoid generating boxes with zero area, we generate double what\n        # we need and filter out the extra. If we get fewer valid boxes\n        # than we need, we loop and try again.\n        while True:\n            y1y2 = np.random.randint(r_y1, r_y2, (rois_per_box * 2, 2))\n            x1x2 = np.random.randint(r_x1, r_x2, (rois_per_box * 2, 2))\n            # Filter out zero area boxes\n            threshold = 1\n            y1y2 = y1y2[np.abs(y1y2[:, 0] - y1y2[:, 1]) >=\n                        threshold][:rois_per_box]\n            x1x2 = x1x2[np.abs(x1x2[:, 0] - x1x2[:, 1]) >=\n                        threshold][:rois_per_box]\n            if y1y2.shape[0] == rois_per_box and x1x2.shape[0] == rois_per_box:\n                break\n\n        # Sort on axis 1 to ensure x1 <= x2 and y1 <= y2 and then reshape\n        # into x1, y1, x2, y2 order\n        x1, x2 = np.split(np.sort(x1x2, axis=1), 2, axis=1)\n        y1, y2 = np.split(np.sort(y1y2, axis=1), 2, axis=1)\n        box_rois = np.hstack([y1, x1, y2, x2])\n        rois[rois_per_box * i:rois_per_box * (i + 1)] = box_rois\n\n    # Generate random ROIs anywhere in the image (10% of count)\n    remaining_count = count - (rois_per_box * gt_boxes.shape[0])\n    # To avoid generating boxes with zero area, we generate double what\n    # we need and filter out the extra. If we get fewer valid boxes\n    # than we need, we loop and try again.\n    while True:\n        y1y2 = np.random.randint(0, image_shape[0], (remaining_count * 2, 2))\n        x1x2 = np.random.randint(0, image_shape[1], (remaining_count * 2, 2))\n        # Filter out zero area boxes\n        threshold = 1\n        y1y2 = y1y2[np.abs(y1y2[:, 0] - y1y2[:, 1]) >=\n                    threshold][:remaining_count]\n        x1x2 = x1x2[np.abs(x1x2[:, 0] - x1x2[:, 1]) >=\n                    threshold][:remaining_count]\n        if y1y2.shape[0] == remaining_count and x1x2.shape[0] == remaining_count:\n            break\n\n    # Sort on axis 1 to ensure x1 <= x2 and y1 <= y2 and then reshape\n    # into x1, y1, x2, y2 order\n    x1, x2 = np.split(np.sort(x1x2, axis=1), 2, axis=1)\n    y1, y2 = np.split(np.sort(y1y2, axis=1), 2, axis=1)\n    global_rois = np.hstack([y1, x1, y2, x2])\n    rois[-remaining_count:] = global_rois\n    return rois\n\n\ndef data_generator(dataset, config, shuffle=True, augment=False, augmentation=None,\n                   random_rois=0, batch_size=1, detection_targets=False,\n                   no_augmentation_sources=None):\n    """A generator that returns images and corresponding target class ids,\n    bounding box deltas, and masks.\n\n    dataset: The Dataset object to pick data from\n    config: The model config object\n    shuffle: If True, shuffles the samples before every epoch\n    augment: (deprecated. Use augmentation instead). If true, apply random\n        image augmentation. Currently, only horizontal flipping is offered.\n    augmentation: Optional. An imgaug (https://github.com/aleju/imgaug) augmentation.\n        For example, passing imgaug.augmenters.Fliplr(0.5) flips images\n        right/left 50% of the time.\n    random_rois: If > 0 then generate proposals to be used to train the\n                 network classifier and mask heads. Useful if training\n                 the Mask RCNN part without the RPN.\n    batch_size: How many images to return in each call\n    detection_targets: If True, generate detection targets (class IDs, bbox\n        deltas, and masks). Typically for debugging or visualizations because\n        in trainig detection targets are generated by DetectionTargetLayer.\n    no_augmentation_sources: Optional. List of sources to exclude for\n        augmentation. A source is string that identifies a dataset and is\n        defined in the Dataset class.\n\n    Returns a Python generator. Upon calling next() on it, the\n    generator returns two lists, inputs and outputs. The contents\n    of the lists differs depending on the received arguments:\n    inputs list:\n    - images: [batch, H, W, C]\n    - image_meta: [batch, (meta data)] Image details. See compose_image_meta()\n    - rpn_match: [batch, N] Integer (1=positive anchor, -1=negative, 0=neutral)\n    - rpn_bbox: [batch, N, (dy, dx, log(dh), log(dw))] Anchor bbox deltas.\n    - gt_class_ids: [batch, MAX_GT_INSTANCES] Integer class IDs\n    - gt_boxes: [batch, MAX_GT_INSTANCES, (y1, x1, y2, x2)]\n    - gt_masks: [batch, height, width, MAX_GT_INSTANCES]. The height and width\n                are those of the image unless use_mini_mask is True, in which\n                case they are defined in MINI_MASK_SHAPE.\n\n    outputs list: Usually empty in regular training. But if detection_targets\n        is True then the outputs list contains target class_ids, bbox deltas,\n        and masks.\n    """\n    b = 0  # batch item index\n    image_index = -1\n    image_ids = np.copy(dataset.image_ids)\n    error_count = 0\n    no_augmentation_sources = no_augmentation_sources or []\n\n    # Anchors\n    # [anchor_count, (y1, x1, y2, x2)]\n    backbone_shapes = compute_backbone_shapes(config, config.IMAGE_SHAPE)\n    anchors = utils.generate_pyramid_anchors(config.RPN_ANCHOR_SCALES,\n                                             config.RPN_ANCHOR_RATIOS,\n                                             backbone_shapes,\n                                             config.BACKBONE_STRIDES,\n                                             config.RPN_ANCHOR_STRIDE)\n\n    # Keras requires a generator to run indefinitely.\n    while True:\n        try:\n            # Increment index to pick next image. Shuffle if at the start of an epoch.\n            image_index = (image_index + 1) % len(image_ids)\n            if shuffle and image_index == 0:\n                np.random.shuffle(image_ids)\n\n            # Get GT bounding boxes and masks for image.\n            image_id = image_ids[image_index]\n\n            # If the image source is not to be augmented pass None as augmentation\n            if dataset.image_info[image_id][\'source\'] in no_augmentation_sources:\n                image, image_meta, gt_class_ids, gt_boxes, gt_masks = \\\n                load_image_gt(dataset, config, image_id, augment=augment,\n                              augmentation=None,\n                              use_mini_mask=config.USE_MINI_MASK)\n            else:\n                image, image_meta, gt_class_ids, gt_boxes, gt_masks = \\\n                    load_image_gt(dataset, config, image_id, augment=augment,\n                                augmentation=augmentation,\n                                use_mini_mask=config.USE_MINI_MASK)\n            \n            # Skip images that have no instances. This can happen in cases\n            # where we train on a subset of classes and the image doesn\'t\n            # have any of the classes we care about.\n            if not np.any(gt_class_ids > 0):\n                continue\n\n            # RPN Targets\n            rpn_match, rpn_bbox = build_rpn_targets(image.shape, anchors,\n                                                    gt_class_ids, gt_boxes, config)\n\n            # Mask R-CNN Targets\n            if random_rois:\n                rpn_rois = generate_random_rois(\n                    image.shape, random_rois, gt_class_ids, gt_boxes)\n                if detection_targets:\n                    rois, mrcnn_class_ids, mrcnn_bbox, mrcnn_mask =\\\n                        build_detection_targets(\n                            rpn_rois, gt_class_ids, gt_boxes, gt_masks, config)\n\n            # Init batch arrays\n            if b == 0:\n                batch_image_meta = np.zeros(\n                    (batch_size,) + image_meta.shape, dtype=image_meta.dtype)\n                batch_rpn_match = np.zeros(\n                    [batch_size, anchors.shape[0], 1], dtype=rpn_match.dtype)\n                batch_rpn_bbox = np.zeros(\n                    [batch_size, config.RPN_TRAIN_ANCHORS_PER_IMAGE, 4], dtype=rpn_bbox.dtype)\n                batch_images = np.zeros(\n                    (batch_size,) + image.shape, dtype=np.float32)\n                batch_gt_class_ids = np.zeros(\n                    (batch_size, config.MAX_GT_INSTANCES), dtype=np.int32)\n                batch_gt_boxes = np.zeros(\n                    (batch_size, config.MAX_GT_INSTANCES, 4), dtype=np.int32)\n                batch_gt_masks = np.zeros(\n                    (batch_size, gt_masks.shape[0], gt_masks.shape[1],\n                     config.MAX_GT_INSTANCES), dtype=gt_masks.dtype)\n                if random_rois:\n                    batch_rpn_rois = np.zeros(\n                        (batch_size, rpn_rois.shape[0], 4), dtype=rpn_rois.dtype)\n                    if detection_targets:\n                        batch_rois = np.zeros(\n                            (batch_size,) + rois.shape, dtype=rois.dtype)\n                        batch_mrcnn_class_ids = np.zeros(\n                            (batch_size,) + mrcnn_class_ids.shape, dtype=mrcnn_class_ids.dtype)\n                        batch_mrcnn_bbox = np.zeros(\n                            (batch_size,) + mrcnn_bbox.shape, dtype=mrcnn_bbox.dtype)\n                        batch_mrcnn_mask = np.zeros(\n                            (batch_size,) + mrcnn_mask.shape, dtype=mrcnn_mask.dtype)\n\n            # If more instances than fits in the array, sub-sample from them.\n            if gt_boxes.shape[0] > config.MAX_GT_INSTANCES:\n                ids = np.random.choice(\n                    np.arange(gt_boxes.shape[0]), config.MAX_GT_INSTANCES, replace=False)\n                gt_class_ids = gt_class_ids[ids]\n                gt_boxes = gt_boxes[ids]\n                gt_masks = gt_masks[:, :, ids]\n            #print(b)\n            # Add to batch\n            batch_image_meta[b] = image_meta\n            batch_rpn_match[b] = rpn_match[:, np.newaxis]\n            batch_rpn_bbox[b] = rpn_bbox\n            batch_images[b] = mold_image(image.astype(np.float32), config)\n            batch_gt_class_ids[b, :gt_class_ids.shape[0]] = gt_class_ids\n            batch_gt_boxes[b, :gt_boxes.shape[0]] = gt_boxes\n            batch_gt_masks[b, :, :, :gt_masks.shape[-1]] = gt_masks\n            if random_rois:\n                batch_rpn_rois[b] = rpn_rois\n                if detection_targets:\n                    batch_rois[b] = rois\n                    batch_mrcnn_class_ids[b] = mrcnn_class_ids\n                    batch_mrcnn_bbox[b] = mrcnn_bbox\n                    batch_mrcnn_mask[b] = mrcnn_mask\n            b += 1\n\n            # Batch full?\n            if b >= batch_size:\n                inputs = [batch_images, batch_image_meta, batch_rpn_match, batch_rpn_bbox,\n                          batch_gt_class_ids, batch_gt_boxes, batch_gt_masks]\n                outputs = []\n\n                if random_rois:\n                    inputs.extend([batch_rpn_rois])\n                    if detection_targets:\n                        inputs.extend([batch_rois])\n                        # Keras requires that output and targets have the same number of dimensions\n                        batch_mrcnn_class_ids = np.expand_dims(\n                            batch_mrcnn_class_ids, -1)\n                        outputs.extend(\n                            [batch_mrcnn_class_ids, batch_mrcnn_bbox, batch_mrcnn_mask])\n\n                yield inputs, outputs\n                \n                #Start a new batch\n                b = 0            \n        except (GeneratorExit, KeyboardInterrupt):\n            raise\n        except:\n            # Log it and skip the image\n            logging.exception("Error processing image {}".format(\n                dataset.image_info[image_id]))\n            error_count += 1\n            if error_count > 5:\n                raise\n\n############################################################\n#  Anchors Class Coz of TF2.0\n############################################################\n\nclass Anchors(KL.Layer):\n    def __init__(self, anchors):\n        super(Anchors, self).__init__()\n        self.anchors = tf.Variable(anchors, trainable = True)\n    \n    def call(self, x):\n        return self.anchors\n\n############################################################\n#  MaskRCNN Class\n############################################################\n\nclass MaskRCNN():\n    """Encapsulates the Mask RCNN model functionality.\n\n    The actual Keras model is in the keras_model property.\n    """\n\n    def __init__(self, mode, config, model_dir):\n        """\n        mode: Either "training" or "inference"\n        config: A Sub-class of the Config class\n        model_dir: Directory to save training logs and trained weights\n        """\n        assert mode in [\'training\', \'inference\']\n        self.mode = mode\n        self.config = config\n        self.model_dir = model_dir\n        self.set_log_dir()\n        self.keras_model = self.build(mode=mode, config=config)\n\n    def build(self, mode, config):\n        """Build Mask R-CNN architecture.\n            input_shape: The shape of the input image.\n            mode: Either "training" or "inference". The inputs and\n                outputs of the model differ accordingly.\n        """\n        assert mode in [\'training\', \'inference\']\n\n        # Image size must be dividable by 2 multiple times\n        h, w = config.IMAGE_SHAPE[:2]\n        if h / 2**6 != int(h / 2**6) or w / 2**6 != int(w / 2**6):\n            raise Exception("Image size must be dividable by 2 at least 6 times "\n                            "to avoid fractions when downscaling and upscaling."\n                            "For example, use 256, 320, 384, 448, 512, ... etc. ")\n        \n        # Inputs\n        input_image = KL.Input(\n            shape=[None, None, config.IMAGE_SHAPE[2]], name="input_image")\n        input_image_meta = KL.Input(shape=[config.IMAGE_META_SIZE],\n                                    name="input_image_meta")\n        if mode == "training":\n            # RPN GT\n            input_rpn_match = KL.Input(\n                shape=[None, 1], name="input_rpn_match", dtype=tf.int32)\n            input_rpn_bbox = KL.Input(\n                shape=[None, 4], name="input_rpn_bbox", dtype=tf.float32)\n\n            # Detection GT (class IDs, bounding boxes, and masks)\n            # 1. GT Class IDs (zero padded)\n            input_gt_class_ids = KL.Input(\n                shape=[None], name="input_gt_class_ids", dtype=tf.int32)\n            # 2. GT Boxes in pixels (zero padded)\n            # [batch, MAX_GT_INSTANCES, (y1, x1, y2, x2)] in image coordinates\n            input_gt_boxes = KL.Input(\n                shape=[None, 4], name="input_gt_boxes", dtype=tf.float32)\n            # Normalize coordinates\n            gt_boxes = KL.Lambda(lambda x: norm_boxes_graph(\n                x, K.shape(input_image)[1:3]))(input_gt_boxes)\n            # 3. GT Masks (zero padded)\n            # [batch, height, width, MAX_GT_INSTANCES]\n            if config.USE_MINI_MASK:\n                input_gt_masks = KL.Input(\n                    shape=[config.MINI_MASK_SHAPE[0],\n                           config.MINI_MASK_SHAPE[1], None],\n                    name="input_gt_masks", dtype=bool)\n            else:\n                input_gt_masks = KL.Input(\n                    shape=[config.IMAGE_SHAPE[0], config.IMAGE_SHAPE[1], None],\n                    name="input_gt_masks", dtype=bool)\n        elif mode == "inference":\n            # Anchors in normalized coordinates\n            input_anchors = KL.Input(shape=[None, 4], name="input_anchors")\n\n        # Build the shared convolutional layers.\n        # Bottom-up Layers\n        # Returns a list of the last layers of each stage, 5 in total.\n        # Don\'t create the thead (stage 5), so we pick the 4th item in the list.\n        if callable(config.BACKBONE):\n            _, C2, C3, C4, C5 = config.BACKBONE(input_image, stage5=True,\n                                                train_bn=config.TRAIN_BN)\n        else:\n            _, C2, C3, C4, C5 = resnet_graph(input_image, config.BACKBONE,\n                                             stage5=True, train_bn=config.TRAIN_BN)\n        # Top-down Layers\n        # TODO: add assert to varify feature map sizes match what\'s in config\n        P5 = KL.Conv2D(config.TOP_DOWN_PYRAMID_SIZE, (1, 1), name=\'fpn_c5p5\')(C5)\n        P4 = KL.Add(name="fpn_p4add")([\n            KL.UpSampling2D(size=(2, 2), name="fpn_p5upsampled")(P5),\n            KL.Conv2D(config.TOP_DOWN_PYRAMID_SIZE, (1, 1), name=\'fpn_c4p4\')(C4)])\n        P3 = KL.Add(name="fpn_p3add")([\n            KL.UpSampling2D(size=(2, 2), name="fpn_p4upsampled")(P4),\n            KL.Conv2D(config.TOP_DOWN_PYRAMID_SIZE, (1, 1), name=\'fpn_c3p3\')(C3)])\n        P2 = KL.Add(name="fpn_p2add")([\n            KL.UpSampling2D(size=(2, 2), name="fpn_p3upsampled")(P3),\n            KL.Conv2D(config.TOP_DOWN_PYRAMID_SIZE, (1, 1), name=\'fpn_c2p2\')(C2)])\n        # Attach 3x3 conv to all P layers to get the final feature maps.\n        P2 = KL.Conv2D(config.TOP_DOWN_PYRAMID_SIZE, (3, 3), padding="SAME", name="fpn_p2")(P2)\n        P3 = KL.Conv2D(config.TOP_DOWN_PYRAMID_SIZE, (3, 3), padding="SAME", name="fpn_p3")(P3)\n        P4 = KL.Conv2D(config.TOP_DOWN_PYRAMID_SIZE, (3, 3), padding="SAME", name="fpn_p4")(P4)\n        P5 = KL.Conv2D(config.TOP_DOWN_PYRAMID_SIZE, (3, 3), padding="SAME", name="fpn_p5")(P5)\n        # P6 is used for the 5th anchor scale in RPN. Generated by\n        # subsampling from P5 with stride of 2.\n        P6 = KL.MaxPooling2D(pool_size=(1, 1), strides=2, name="fpn_p6")(P5)\n\n        # Note that P6 is used in RPN, but not in the classifier heads.\n        rpn_feature_maps = [P2, P3, P4, P5, P6]\n        mrcnn_feature_maps = [P2, P3, P4, P5]\n        \n        # Anchors\n        if mode == "training":\n            anchors = self.get_anchors(config.IMAGE_SHAPE)\n            # Duplicate across the batch dimension because Keras requires it\n            # TODO: can this be optimized to avoid duplicating the anchors?\n            anchors = np.broadcast_to(anchors, (config.BATCH_SIZE,) + anchors.shape)\n            #print(anchors.shape)\n            # A hack to get around Keras\'s bad support for constants\n            #anchors = KL.Lambda(lambda x: tf.Variable(anchors), name="anchors")(input_image)\n            anchors = Anchors(anchors)(input_image)\n        else:\n            anchors = input_anchors\n\n        # RPN Model\n        rpn = build_rpn_model(config.RPN_ANCHOR_STRIDE,\n                              len(config.RPN_ANCHOR_RATIOS), config.TOP_DOWN_PYRAMID_SIZE)\n        # Loop through pyramid layers\n        layer_outputs = []  # list of lists\n        for p in rpn_feature_maps:\n            layer_outputs.append(rpn([p]))\n        # Concatenate layer outputs\n        # Convert from list of lists of level outputs to list of lists\n        # of outputs across levels.\n        # e.g. [[a1, b1, c1], [a2, b2, c2]] => [[a1, a2], [b1, b2], [c1, c2]]\n        output_names = ["rpn_class_logits", "rpn_class", "rpn_bbox"]\n        outputs = list(zip(*layer_outputs))\n        outputs = [KL.Concatenate(axis=1, name=n)(list(o))\n                   for o, n in zip(outputs, output_names)]\n\n        rpn_class_logits, rpn_class, rpn_bbox = outputs\n\n        # Generate proposals\n        # Proposals are [batch, N, (y1, x1, y2, x2)] in normalized coordinates\n        # and zero padded.\n        proposal_count = config.POST_NMS_ROIS_TRAINING if mode == "training"\\\n            else config.POST_NMS_ROIS_INFERENCE\n        rpn_rois = ProposalLayer(\n            proposal_count=proposal_count,\n            nms_threshold=config.RPN_NMS_THRESHOLD,\n            name="ROI",\n            config=config)([rpn_class, rpn_bbox, anchors])\n\n        if mode == "training":\n            # Class ID mask to mark class IDs supported by the dataset the image\n            # came from.\n            active_class_ids = KL.Lambda(\n                lambda x: parse_image_meta_graph(x)["active_class_ids"]\n                )(input_image_meta)\n\n            if not config.USE_RPN_ROIS:\n                # Ignore predicted ROIs and use ROIs provided as an input.\n                input_rois = KL.Input(shape=[config.POST_NMS_ROIS_TRAINING, 4],\n                                      name="input_roi", dtype=np.int32)\n                # Normalize coordinates\n                target_rois = KL.Lambda(lambda x: norm_boxes_graph(\n                    x, K.shape(input_image)[1:3]))(input_rois)\n            else:\n                target_rois = rpn_rois\n\n            # Generate detection targets\n            # Subsamples proposals and generates target outputs for training\n            # Note that proposal class IDs, gt_boxes, and gt_masks are zero\n            # padded. Equally, returned rois and targets are zero padded.\n            rois, target_class_ids, target_bbox, target_mask =\\\n                DetectionTargetLayer(config, name="proposal_targets")([\n                    target_rois, input_gt_class_ids, gt_boxes, input_gt_masks])\n\n            # Network Heads\n            # TODO: verify that this handles zero padded ROIs\n            mrcnn_class_logits, mrcnn_class, mrcnn_bbox =\\\n                fpn_classifier_graph(rois, mrcnn_feature_maps, input_image_meta,\n                                     config.POOL_SIZE, config.NUM_CLASSES,\n                                     train_bn=config.TRAIN_BN,\n                                     fc_layers_size=config.FPN_CLASSIF_FC_LAYERS_SIZE)\n\n            mrcnn_mask = build_fpn_mask_graph(rois, mrcnn_feature_maps,\n                                              input_image_meta,\n                                              config.MASK_POOL_SIZE,\n                                              config.NUM_CLASSES,\n                                              train_bn=config.TRAIN_BN)\n\n            # TODO: clean up (use tf.identify if necessary)\n            output_rois = KL.Lambda(lambda x: x * 1, name="output_rois")(rois)\n\n            # Losses\n            rpn_class_loss = KL.Lambda(lambda x: rpn_class_loss_graph(*x), name="rpn_class_loss")(\n                [input_rpn_match, rpn_class_logits])\n            rpn_bbox_loss = KL.Lambda(lambda x: rpn_bbox_loss_graph(config, *x), name="rpn_bbox_loss")(\n                [input_rpn_bbox, input_rpn_match, rpn_bbox])\n            class_loss = KL.Lambda(lambda x: mrcnn_class_loss_graph(*x), name="mrcnn_class_loss")(\n                [target_class_ids, mrcnn_class_logits, active_class_ids])\n            bbox_loss = KL.Lambda(lambda x: mrcnn_bbox_loss_graph(*x), name="mrcnn_bbox_loss")(\n                [target_bbox, target_class_ids, mrcnn_bbox])\n            mask_loss = KL.Lambda(lambda x: mrcnn_mask_loss_graph(*x), name="mrcnn_mask_loss")(\n                [target_mask, target_class_ids, mrcnn_mask])\n\n            # Model\n            inputs = [input_image, input_image_meta,\n                      input_rpn_match, input_rpn_bbox, input_gt_class_ids, input_gt_boxes, input_gt_masks]\n            if not config.USE_RPN_ROIS:\n                inputs.append(input_rois)\n            outputs = [rpn_class_logits, rpn_class, rpn_bbox,\n                       mrcnn_class_logits, mrcnn_class, mrcnn_bbox, mrcnn_mask,\n                       rpn_rois, output_rois,\n                       rpn_class_loss, rpn_bbox_loss, class_loss, bbox_loss, mask_loss]\n            model = KM.Model(inputs, outputs, name=\'mask_rcnn\')\n        else:\n            # Network Heads\n            # Proposal classifier and BBox regressor heads\n            mrcnn_class_logits, mrcnn_class, mrcnn_bbox =\\\n                fpn_classifier_graph(rpn_rois, mrcnn_feature_maps, input_image_meta,\n                                     config.POOL_SIZE, config.NUM_CLASSES,\n                                     train_bn=config.TRAIN_BN,\n                                     fc_layers_size=config.FPN_CLASSIF_FC_LAYERS_SIZE)\n\n            # Detections\n            # output is [batch, num_detections, (y1, x1, y2, x2, class_id, score)] in\n            # normalized coordinates\n            detections = DetectionLayer(config, name="mrcnn_detection")(\n                [rpn_rois, mrcnn_class, mrcnn_bbox, input_image_meta])\n\n            # Create masks for detections\n            detection_boxes = KL.Lambda(lambda x: x[..., :4])(detections)\n            mrcnn_mask = build_fpn_mask_graph(detection_boxes, mrcnn_feature_maps,\n                                              input_image_meta,\n                                              config.MASK_POOL_SIZE,\n                                              config.NUM_CLASSES,\n                                              train_bn=config.TRAIN_BN)\n\n            model = KM.Model([input_image, input_image_meta, input_anchors],\n                             [detections, mrcnn_class, mrcnn_bbox,\n                                 mrcnn_mask, rpn_rois, rpn_class, rpn_bbox],\n                             name=\'mask_rcnn\')\n\n        # Add multi-GPU support.\n        if config.GPU_COUNT > 1:\n            from mrcnn.parallel_model import ParallelModel\n            model = ParallelModel(model, config.GPU_COUNT)\n\n        return model\n\n    def find_last(self):\n        """Finds the last checkpoint file of the last trained model in the\n        model directory.\n        Returns:\n            The path of the last checkpoint file\n        """\n        # Get directory names. Each directory corresponds to a model\n        dir_names = next(os.walk(self.model_dir))[1]\n        key = self.config.NAME.lower()\n        dir_names = filter(lambda f: f.startswith(key), dir_names)\n        dir_names = sorted(dir_names)\n        if not dir_names:\n            import errno\n            raise FileNotFoundError(\n                errno.ENOENT,\n                "Could not find model directory under {}".format(self.model_dir))\n        # Pick last directory\n        dir_name = os.path.join(self.model_dir, dir_names[-1])\n        # Find the last checkpoint\n        checkpoints = next(os.walk(dir_name))[2]\n        checkpoints = filter(lambda f: f.startswith("mask_rcnn"), checkpoints)\n        checkpoints = sorted(checkpoints)\n        if not checkpoints:\n            import errno\n            raise FileNotFoundError(\n                errno.ENOENT, "Could not find weight files in {}".format(dir_name))\n        checkpoint = os.path.join(dir_name, checkpoints[-1])\n        return checkpoint\n\n    def load_weights(self, filepath, by_name=False, exclude=None):\n        """Modified version of the corresponding Keras function with\n        the addition of multi-GPU support and the ability to exclude\n        some layers from loading.\n        exclude: list of layer names to exclude\n        """\n        import h5py\n        # Conditional import to support versions of Keras before 2.2\n        # TODO: remove in about 6 months (end of 2018)\n        try:\n            from keras.engine import saving\n        except ImportError:\n            # Keras before 2.2 used the \'topology\' namespace.\n            from keras.engine import topology as saving\n\n        if exclude:\n            by_name = True\n\n        if h5py is None:\n            raise ImportError(\'`load_weights` requires h5py.\')\n        f = h5py.File(filepath, mode=\'r\')\n        if \'layer_names\' not in f.attrs and \'model_weights\' in f:\n            f = f[\'model_weights\']\n\n        # In multi-GPU training, we wrap the model. Get layers\n        # of the inner model because they have the weights.\n        keras_model = self.keras_model\n        layers = keras_model.inner_model.layers if hasattr(keras_model, "inner_model")\\\n            else keras_model.layers\n\n        # Exclude some layers\n        if exclude:\n            layers = filter(lambda l: l.name not in exclude, layers)\n\n        if by_name:\n            saving.load_weights_from_hdf5_group_by_name(f, layers)\n        else:\n            saving.load_weights_from_hdf5_group(f, layers)\n        if hasattr(f, \'close\'):\n            f.close()\n\n        # Update the log directory\n        self.set_log_dir(filepath)\n\n    def get_imagenet_weights(self):\n        """Downloads ImageNet trained weights from Keras.\n        Returns path to weights file.\n        """\n        from tf.keras.utils.data_utils import get_file\n        TF_WEIGHTS_PATH_NO_TOP = \'https://github.com/fchollet/deep-learning-models/\'\\\n                                 \'releases/download/v0.2/\'\\\n                                 \'resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5\'\n        weights_path = get_file(\'resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5\',\n                                TF_WEIGHTS_PATH_NO_TOP,\n                                cache_subdir=\'models\',\n                                md5_hash=\'a268eb855778b3df3c7506639542a6af\')\n        return weights_path\n\n    def compile(self, learning_rate, momentum):\n        """Gets the model ready for training. Adds losses, regularization, and\n        metrics. Then calls the Keras compile() function.\n        """\n        # Optimizer object\n        optimizer = tf.keras.optimizers.SGD(\n            lr=learning_rate, momentum=momentum,\n            clipnorm=self.config.GRADIENT_CLIP_NORM)\n        # Add Losses\n        # First, clear previously set losses to avoid duplication\n        #print(self.keras_model._losses)\n        #self.keras_model._losses = []\n        #self.keras_model._per_input_losses = {}\n        loss_names = [\n            "rpn_class_loss",  "rpn_bbox_loss",\n            "mrcnn_class_loss", "mrcnn_bbox_loss", "mrcnn_mask_loss"]\n        for name in loss_names:\n            layer = self.keras_model.get_layer(name)\n            if layer.output in self.keras_model.losses:\n                continue\n            loss = tf.math.reduce_mean(layer.output, keepdims=True) * self.config.LOSS_WEIGHTS.get(name, 1.)\n            print(loss)\n            self.keras_model.add_loss(loss)\n\n        # Add L2 Regularization\n        # Skip gamma and beta weights of batch normalization layers.\n        reg_losses = [\n            tf.keras.regularizers.l2(self.config.WEIGHT_DECAY)(w) / tf.cast(tf.size(w), tf.float32)\n            for w in self.keras_model.trainable_weights\n            if \'gamma\' not in w.name and \'beta\' not in w.name]\n        self.keras_model.add_loss(tf.add_n(reg_losses))\n\n        # Compile\n        self.keras_model.compile(\n            optimizer=optimizer,\n            loss=[None] * len(self.keras_model.outputs))\n\n        # Add metrics for losses\n        for name in loss_names:\n            if name in self.keras_model.metrics_names:\n                continue\n            layer = self.keras_model.get_layer(name)\n            self.keras_model.metrics_names.append(name)\n            loss = (\n                tf.math.reduce_mean(layer.output, keepdims=True)\n                * self.config.LOSS_WEIGHTS.get(name, 1.))\n            self.keras_model.metrics.append(loss)\n        #print(self.keras_model._losses, self.keras_model._per_input_losses)\n\n    def set_trainable(self, layer_regex, keras_model=None, indent=0, verbose=1):\n        """Sets model layers as trainable if their names match\n        the given regular expression.\n        """\n        # Print message on the first call (but not on recursive calls)\n        if verbose > 0 and keras_model is None:\n            log("Selecting layers to train")\n\n        keras_model = keras_model or self.keras_model\n\n        # In multi-GPU training, we wrap the model. Get layers\n        # of the inner model because they have the weights.\n        layers = keras_model.inner_model.layers if hasattr(keras_model, "inner_model")\\\n            else keras_model.layers\n\n        for layer in layers:\n            # Is the layer a model?\n            if layer.__class__.__name__ == \'Model\':\n                print("In model: ", layer.name)\n                self.set_trainable(\n                    layer_regex, keras_model=layer, indent=indent + 4)\n                continue\n\n            if not layer.weights:\n                continue\n            # Is it trainable?\n            trainable = bool(re.fullmatch(layer_regex, layer.name))\n            # Update layer. If layer is a container, update inner layer.\n            if layer.__class__.__name__ == \'TimeDistributed\':\n                layer.layer.trainable = trainable\n            else:\n                layer.trainable = trainable\n            # Print trainable layer names\n            if trainable and verbose > 0:\n                log("{}{:20}   ({})".format(" " * indent, layer.name,\n                                            layer.__class__.__name__))\n\n    def set_log_dir(self, model_path=None):\n        """Sets the model log directory and epoch counter.\n\n        model_path: If None, or a format different from what this code uses\n            then set a new log directory and start epochs from 0. Otherwise,\n            extract the log directory and the epoch counter from the file\n            name.\n        """\n        # Set date and epoch counter as if starting a new model\n        self.epoch = 0\n        now = datetime.datetime.now()\n\n        # If we have a model path with date and epochs use them\n        if model_path:\n            # Continue from we left of. Get epoch and date from the file name\n            # A sample model path might look like:\n            # \\path\\to\\logs\\coco20171029T2315\\mask_rcnn_coco_0001.h5 (Windows)\n            # /path/to/logs/coco20171029T2315/mask_rcnn_coco_0001.h5 (Linux)\n            regex = r".*[/\\\\][\\w-]+(\\d{4})(\\d{2})(\\d{2})T(\\d{2})(\\d{2})[/\\\\]mask\\_rcnn\\_[\\w-]+(\\d{4})\\.h5"\n            m = re.match(regex, model_path)\n            if m:\n                now = datetime.datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),\n                                        int(m.group(4)), int(m.group(5)))\n                # Epoch number in file is 1-based, and in Keras code it\'s 0-based.\n                # So, adjust for that then increment by one to start from the next epoch\n                self.epoch = int(m.group(6)) - 1 + 1\n                print(\'Re-starting from epoch %d\' % self.epoch)\n\n        # Directory for training logs\n        self.log_dir = os.path.join(self.model_dir, "{}{:%Y%m%dT%H%M}".format(\n            self.config.NAME.lower(), now))\n\n        # Path to save after each epoch. Include placeholders that get filled by Keras.\n        self.checkpoint_path = os.path.join(self.log_dir, "mask_rcnn_{}_*epoch*.h5".format(\n            self.config.NAME.lower()))\n        self.checkpoint_path = self.checkpoint_path.replace(\n            "*epoch*", "{epoch:04d}")\n\n    def train(self, train_dataset, val_dataset, learning_rate, epochs, layers,\n              augmentation=None, custom_callbacks=None, no_augmentation_sources=None):\n        """Train the model.\n        train_dataset, val_dataset: Training and validation Dataset objects.\n        learning_rate: The learning rate to train with\n        epochs: Number of training epochs. Note that previous training epochs\n                are considered to be done alreay, so this actually determines\n                the epochs to train in total rather than in this particaular\n                call.\n        layers: Allows selecting wich layers to train. It can be:\n            - A regular expression to match layer names to train\n            - One of these predefined values:\n              heads: The RPN, classifier and mask heads of the network\n              all: All the layers\n              3+: Train Resnet stage 3 and up\n              4+: Train Resnet stage 4 and up\n              5+: Train Resnet stage 5 and up\n        augmentation: Optional. An imgaug (https://github.com/aleju/imgaug)\n            augmentation. For example, passing imgaug.augmenters.Fliplr(0.5)\n            flips images right/left 50% of the time. You can pass complex\n            augmentations as well. This augmentation applies 50% of the\n            time, and when it does it flips images right/left half the time\n            and adds a Gaussian blur with a random sigma in range 0 to 5.\n\n                augmentation = imgaug.augmenters.Sometimes(0.5, [\n                    imgaug.augmenters.Fliplr(0.5),\n                    imgaug.augmenters.GaussianBlur(sigma=(0.0, 5.0))\n                ])\n\t    custom_callbacks: Optional. Add custom callbacks to be called\n\t        with the keras fit_generator method. Must be list of type keras.callbacks.\n        no_augmentation_sources: Optional. List of sources to exclude for\n            augmentation. A source is string that identifies a dataset and is\n            defined in the Dataset class.\n        """\n        assert self.mode == "training", "Create model in training mode."\n\n        # Pre-defined layer regular expressions\n        layer_regex = {\n            # all layers but the backbone\n            "heads": r"(mrcnn\\_.*)|(rpn\\_.*)|(fpn\\_.*)",\n            # From a specific Resnet stage and up\n            "3+": r"(res3.*)|(bn3.*)|(res4.*)|(bn4.*)|(res5.*)|(bn5.*)|(mrcnn\\_.*)|(rpn\\_.*)|(fpn\\_.*)",\n            "4+": r"(res4.*)|(bn4.*)|(res5.*)|(bn5.*)|(mrcnn\\_.*)|(rpn\\_.*)|(fpn\\_.*)",\n            "5+": r"(res5.*)|(bn5.*)|(mrcnn\\_.*)|(rpn\\_.*)|(fpn\\_.*)",\n            # All layers\n            "all": ".*",\n        }\n        if layers in layer_regex.keys():\n            layers = layer_regex[layers]\n\n        # Data generators\n        train_generator = data_generator(train_dataset, self.config, shuffle=True,\n                                         augmentation=augmentation,\n                                         batch_size=self.config.BATCH_SIZE,\n                                         no_augmentation_sources=no_augmentation_sources)\n        val_generator = data_generator(val_dataset, self.config, shuffle=True,\n                                       batch_size=self.config.BATCH_SIZE)\n\n        # Create log_dir if it does not exist\n        if not os.path.exists(self.log_dir):\n            os.makedirs(self.log_dir)\n\n        # Callbacks\n        callbacks = [\n            #keras.callbacks.TensorBoard(log_dir=self.log_dir,\n            #                            histogram_freq=0, write_graph=True, write_images=False),\n            keras.callbacks.ModelCheckpoint(self.checkpoint_path,\n                                            verbose=1, save_weights_only=True),\n        ]\n\n        # Add custom callbacks to the list\n        if custom_callbacks:\n            callbacks += custom_callbacks\n\n        # Train\n        log("\\nStarting at epoch {}. LR={}\\n".format(self.epoch, learning_rate))\n        log("Checkpoint Path: {}".format(self.checkpoint_path))\n        self.set_trainable(layers)\n        self.compile(learning_rate, self.config.LEARNING_MOMENTUM)\n\n        # Work-around for Windows: Keras fails on Windows when using\n        # multiprocessing workers. See discussion here:\n        # https://github.com/matterport/Mask_RCNN/issues/13#issuecomment-353124009\n        if os.name is \'nt\':\n            workers = 0\n        else:\n            workers = multiprocessing.cpu_count()\n        print(workers)\n        self.keras_model.fit_generator(\n            train_generator,\n            initial_epoch=self.epoch,\n            epochs=epochs,\n            steps_per_epoch=self.config.STEPS_PER_EPOCH,\n            #callbacks=callbacks,\n            validation_data=val_generator,\n            validation_steps=self.config.VALIDATION_STEPS,\n            max_queue_size=100,\n            workers=1,\n            use_multiprocessing=False,\n        )\n        self.epoch = max(self.epoch, epochs)\n\n    def mold_inputs(self, images):\n        """Takes a list of images and modifies them to the format expected\n        as an input to the neural network.\n        images: List of image matrices [height,width,depth]. Images can have\n            different sizes.\n\n        Returns 3 Numpy matrices:\n        molded_images: [N, h, w, 3]. Images resized and normalized.\n        image_metas: [N, length of meta data]. Details about each image.\n        windows: [N, (y1, x1, y2, x2)]. The portion of the image that has the\n            original image (padding excluded).\n        """\n        molded_images = []\n        image_metas = []\n        windows = []\n        for image in images:\n            # Resize image\n            # TODO: move resizing to mold_image()\n            molded_image, window, scale, padding, crop = utils.resize_image(\n                image,\n                min_dim=self.config.IMAGE_MIN_DIM,\n                min_scale=self.config.IMAGE_MIN_SCALE,\n                max_dim=self.config.IMAGE_MAX_DIM,\n                mode=self.config.IMAGE_RESIZE_MODE)\n            molded_image = mold_image(molded_image, self.config)\n            # Build image_meta\n            image_meta = compose_image_meta(\n                0, image.shape, molded_image.shape, window, scale,\n                np.zeros([self.config.NUM_CLASSES], dtype=np.int32))\n            # Append\n            molded_images.append(molded_image)\n            windows.append(window)\n            image_metas.append(image_meta)\n        # Pack into arrays\n        molded_images = np.stack(molded_images)\n        image_metas = np.stack(image_metas)\n        windows = np.stack(windows)\n        return molded_images, image_metas, windows\n\n    def unmold_detections(self, detections, mrcnn_mask, original_image_shape,\n                          image_shape, window):\n        """Reformats the detections of one image from the format of the neural\n        network output to a format suitable for use in the rest of the\n        application.\n\n        detections: [N, (y1, x1, y2, x2, class_id, score)] in normalized coordinates\n        mrcnn_mask: [N, height, width, num_classes]\n        original_image_shape: [H, W, C] Original image shape before resizing\n        image_shape: [H, W, C] Shape of the image after resizing and padding\n        window: [y1, x1, y2, x2] Pixel coordinates of box in the image where the real\n                image is excluding the padding.\n\n        Returns:\n        boxes: [N, (y1, x1, y2, x2)] Bounding boxes in pixels\n        class_ids: [N] Integer class IDs for each bounding box\n        scores: [N] Float probability scores of the class_id\n        masks: [height, width, num_instances] Instance masks\n        """\n        # How many detections do we have?\n        # Detections array is padded with zeros. Find the first class_id == 0.\n        zero_ix = np.where(detections[:, 4] == 0)[0]\n        N = zero_ix[0] if zero_ix.shape[0] > 0 else detections.shape[0]\n\n        # Extract boxes, class_ids, scores, and class-specific masks\n        boxes = detections[:N, :4]\n        class_ids = detections[:N, 4].astype(np.int32)\n        scores = detections[:N, 5]\n        masks = mrcnn_mask[np.arange(N), :, :, class_ids]\n\n        # Translate normalized coordinates in the resized image to pixel\n        # coordinates in the original image before resizing\n        window = utils.norm_boxes(window, image_shape[:2])\n        wy1, wx1, wy2, wx2 = window\n        shift = np.array([wy1, wx1, wy1, wx1])\n        wh = wy2 - wy1  # window height\n        ww = wx2 - wx1  # window width\n        scale = np.array([wh, ww, wh, ww])\n        # Convert boxes to normalized coordinates on the window\n        boxes = np.divide(boxes - shift, scale)\n        # Convert boxes to pixel coordinates on the original image\n        boxes = utils.denorm_boxes(boxes, original_image_shape[:2])\n\n        # Filter out detections with zero area. Happens in early training when\n        # network weights are still random\n        exclude_ix = np.where(\n            (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1]) <= 0)[0]\n        if exclude_ix.shape[0] > 0:\n            boxes = np.delete(boxes, exclude_ix, axis=0)\n            class_ids = np.delete(class_ids, exclude_ix, axis=0)\n            scores = np.delete(scores, exclude_ix, axis=0)\n            masks = np.delete(masks, exclude_ix, axis=0)\n            N = class_ids.shape[0]\n\n        # Resize masks to original image size and set boundary threshold.\n        full_masks = []\n        for i in range(N):\n            # Convert neural network mask to full size mask\n            full_mask = utils.unmold_mask(masks[i], boxes[i], original_image_shape)\n            full_masks.append(full_mask)\n        full_masks = np.stack(full_masks, axis=-1)\\\n            if full_masks else np.empty(original_image_shape[:2] + (0,))\n\n        return boxes, class_ids, scores, full_masks\n\n    def detect(self, images, verbose=0):\n        """Runs the detection pipeline.\n\n        images: List of images, potentially of different sizes.\n\n        Returns a list of dicts, one dict per image. The dict contains:\n        rois: [N, (y1, x1, y2, x2)] detection bounding boxes\n        class_ids: [N] int class IDs\n        scores: [N] float probability scores for the class IDs\n        masks: [H, W, N] instance binary masks\n        """\n        assert self.mode == "inference", "Create model in inference mode."\n        assert len(\n            images) == self.config.BATCH_SIZE, "len(images) must be equal to BATCH_SIZE"\n\n        if verbose:\n            log("Processing {} images".format(len(images)))\n            for image in images:\n                log("image", image)\n\n        # Mold inputs to format expected by the neural network\n        molded_images, image_metas, windows = self.mold_inputs(images)\n\n        # Validate image sizes\n        # All images in a batch MUST be of the same size\n        image_shape = molded_images[0].shape\n        for g in molded_images[1:]:\n            assert g.shape == image_shape,\\\n                "After resizing, all images must have the same size. Check IMAGE_RESIZE_MODE and image sizes."\n\n        # Anchors\n        anchors = self.get_anchors(image_shape)\n        # Duplicate across the batch dimension because Keras requires it\n        # TODO: can this be optimized to avoid duplicating the anchors?\n        anchors = np.broadcast_to(anchors, (self.config.BATCH_SIZE,) + anchors.shape)\n\n        if verbose:\n            log("molded_images", molded_images)\n            log("image_metas", image_metas)\n            log("anchors", anchors)\n        # Run object detection\n        #print(molded_images.shape, image_metas.shape, anchors.shape)\n        detections, _, _, mrcnn_mask, _, _, _ =\\\n            self.keras_model.predict([molded_images, image_metas, anchors], verbose=0)\n        # Process detections\n        results = []\n        for i, image in enumerate(images):\n            final_rois, final_class_ids, final_scores, final_masks =\\\n                self.unmold_detections(detections[i], mrcnn_mask[i],\n                                       image.shape, molded_images[i].shape,\n                                       windows[i])\n            results.append({\n                "rois": final_rois,\n                "class_ids": final_class_ids,\n                "scores": final_scores,\n                "masks": final_masks,\n            })\n        return results\n\n    def detect_molded(self, molded_images, image_metas, verbose=0):\n        """Runs the detection pipeline, but expect inputs that are\n        molded already. Used mostly for debugging and inspecting\n        the model.\n\n        molded_images: List of images loaded using load_image_gt()\n        image_metas: image meta data, also returned by load_image_gt()\n\n        Returns a list of dicts, one dict per image. The dict contains:\n        rois: [N, (y1, x1, y2, x2)] detection bounding boxes\n        class_ids: [N] int class IDs\n        scores: [N] float probability scores for the class IDs\n        masks: [H, W, N] instance binary masks\n        """\n        assert self.mode == "inference", "Create model in inference mode."\n        assert len(molded_images) == self.config.BATCH_SIZE,\\\n            "Number of images must be equal to BATCH_SIZE"\n\n        if verbose:\n            log("Processing {} images".format(len(molded_images)))\n            for image in molded_images:\n                log("image", image)\n\n        # Validate image sizes\n        # All images in a batch MUST be of the same size\n        image_shape = molded_images[0].shape\n        for g in molded_images[1:]:\n            assert g.shape == image_shape, "Images must have the same size"\n\n        # Anchors\n        anchors = self.get_anchors(image_shape)\n        # Duplicate across the batch dimension because Keras requires it\n        # TODO: can this be optimized to avoid duplicating the anchors?\n        anchors = np.broadcast_to(anchors, (self.config.BATCH_SIZE,) + anchors.shape)\n\n        if verbose:\n            log("molded_images", molded_images)\n            log("image_metas", image_metas)\n            log("anchors", anchors)\n        # Run object detection\n        detections, _, _, mrcnn_mask, _, _, _ =\\\n            self.keras_model.predict([molded_images, image_metas, anchors], verbose=0)\n        # Process detections\n        results = []\n        for i, image in enumerate(molded_images):\n            window = [0, 0, image.shape[0], image.shape[1]]\n            final_rois, final_class_ids, final_scores, final_masks =\\\n                self.unmold_detections(detections[i], mrcnn_mask[i],\n                                       image.shape, molded_images[i].shape,\n                                       window)\n            results.append({\n                "rois": final_rois,\n                "class_ids": final_class_ids,\n                "scores": final_scores,\n                "masks": final_masks,\n            })\n        return results\n\n    def get_anchors(self, image_shape):\n        """Returns anchor pyramid for the given image size."""\n        backbone_shapes = compute_backbone_shapes(self.config, image_shape)\n        # Cache anchors and reuse if image shape is the same\n        if not hasattr(self, "_anchor_cache"):\n            self._anchor_cache = {}\n        if not tuple(image_shape) in self._anchor_cache:\n            # Generate Anchors\n            a = utils.generate_pyramid_anchors(\n                self.config.RPN_ANCHOR_SCALES,\n                self.config.RPN_ANCHOR_RATIOS,\n                backbone_shapes,\n                self.config.BACKBONE_STRIDES,\n                self.config.RPN_ANCHOR_STRIDE)\n            # Keep a copy of the latest anchors in pixel coordinates because\n            # it\'s used in inspect_model notebooks.\n            # TODO: Remove this after the notebook are refactored to not use it\n            self.anchors = a\n            # Normalize coordinates\n            self._anchor_cache[tuple(image_shape)] = utils.norm_boxes(a, image_shape[:2])\n        return self._anchor_cache[tuple(image_shape)]\n\n    def ancestor(self, tensor, name, checked=None):\n        """Finds the ancestor of a TF tensor in the computation graph.\n        tensor: TensorFlow symbolic tensor.\n        name: Name of ancestor tensor to find\n        checked: For internal use. A list of tensors that were already\n                 searched to avoid loops in traversing the graph.\n        """\n        checked = checked if checked is not None else []\n        # Put a limit on how deep we go to avoid very long loops\n        if len(checked) > 500:\n            return None\n        # Convert name to a regex and allow matching a number prefix\n        # because Keras adds them automatically\n        if isinstance(name, str):\n            name = re.compile(name.replace("/", r"(\\_\\d+)*/"))\n\n        parents = tensor.op.inputs\n        for p in parents:\n            if p in checked:\n                continue\n            if bool(re.fullmatch(name, p.name)):\n                return p\n            checked.append(p)\n            a = self.ancestor(p, name, checked)\n            if a is not None:\n                return a\n        return None\n\n    def find_trainable_layer(self, layer):\n        """If a layer is encapsulated by another layer, this function\n        digs through the encapsulation and returns the layer that holds\n        the weights.\n        """\n        if layer.__class__.__name__ == \'TimeDistributed\':\n            return self.find_trainable_layer(layer.layer)\n        return layer\n\n    def get_trainable_layers(self):\n        """Returns a list of layers that have weights."""\n        layers = []\n        # Loop through all layers\n        for l in self.keras_model.layers:\n            # If layer is a wrapper, find inner trainable layer\n            l = self.find_trainable_layer(l)\n            # Include layer if it has weights\n            if l.get_weights():\n                layers.append(l)\n        return layers\n\n    def run_graph(self, images, outputs, image_metas=None):\n        """Runs a sub-set of the computation graph that computes the given\n        outputs.\n\n        image_metas: If provided, the images are assumed to be already\n            molded (i.e. resized, padded, and normalized)\n\n        outputs: List of tuples (name, tensor) to compute. The tensors are\n            symbolic TensorFlow tensors and the names are for easy tracking.\n\n        Returns an ordered dict of results. Keys are the names received in the\n        input and values are Numpy arrays.\n        """\n        model = self.keras_model\n\n        # Organize desired outputs into an ordered dict\n        outputs = OrderedDict(outputs)\n        for o in outputs.values():\n            assert o is not None\n\n        # Build a Keras function to run parts of the computation graph\n        inputs = model.inputs\n        if model.uses_learning_phase and not isinstance(K.learning_phase(), int):\n            inputs += [K.learning_phase()]\n        kf = K.function(model.inputs, list(outputs.values()))\n\n        # Prepare inputs\n        if image_metas is None:\n            molded_images, image_metas, _ = self.mold_inputs(images)\n        else:\n            molded_images = images\n        image_shape = molded_images[0].shape\n        # Anchors\n        anchors = self.get_anchors(image_shape)\n        # Duplicate across the batch dimension because Keras requires it\n        # TODO: can this be optimized to avoid duplicating the anchors?\n        anchors = np.broadcast_to(anchors, (self.config.BATCH_SIZE,) + anchors.shape)\n        model_in = [molded_images, image_metas, anchors]\n\n        # Run inference\n        if model.uses_learning_phase and not isinstance(K.learning_phase(), int):\n            model_in.append(0.)\n        outputs_np = kf(model_in)\n\n        # Pack the generated Numpy arrays into a a dict and log the results.\n        outputs_np = OrderedDict([(k, v)\n                                  for k, v in zip(outputs.keys(), outputs_np)])\n        for k, v in outputs_np.items():\n            log(k, v)\n        return outputs_np\n\n\n############################################################\n#  Data Formatting\n############################################################\n\ndef compose_image_meta(image_id, original_image_shape, image_shape,\n                       window, scale, active_class_ids):\n    """Takes attributes of an image and puts them in one 1D array.\n\n    image_id: An int ID of the image. Useful for debugging.\n    original_image_shape: [H, W, C] before resizing or padding.\n    image_shape: [H, W, C] after resizing and padding\n    window: (y1, x1, y2, x2) in pixels. The area of the image where the real\n            image is (excluding the padding)\n    scale: The scaling factor applied to the original image (float32)\n    active_class_ids: List of class_ids available in the dataset from which\n        the image came. Useful if training on images from multiple datasets\n        where not all classes are present in all datasets.\n    """\n    meta = np.array(\n        [image_id] +                  # size=1\n        list(original_image_shape) +  # size=3\n        list(image_shape) +           # size=3\n        list(window) +                # size=4 (y1, x1, y2, x2) in image cooredinates\n        [scale] +                     # size=1\n        list(active_class_ids)        # size=num_classes\n    )\n    return meta\n\n\ndef parse_image_meta(meta):\n    """Parses an array that contains image attributes to its components.\n    See compose_image_meta() for more details.\n\n    meta: [batch, meta length] where meta length depends on NUM_CLASSES\n\n    Returns a dict of the parsed values.\n    """\n    image_id = meta[:, 0]\n    original_image_shape = meta[:, 1:4]\n    image_shape = meta[:, 4:7]\n    window = meta[:, 7:11]  # (y1, x1, y2, x2) window of image in in pixels\n    scale = meta[:, 11]\n    active_class_ids = meta[:, 12:]\n    return {\n        "image_id": image_id.astype(np.int32),\n        "original_image_shape": original_image_shape.astype(np.int32),\n        "image_shape": image_shape.astype(np.int32),\n        "window": window.astype(np.int32),\n        "scale": scale.astype(np.float32),\n        "active_class_ids": active_class_ids.astype(np.int32),\n    }\n\n\ndef parse_image_meta_graph(meta):\n    """Parses a tensor that contains image attributes to its components.\n    See compose_image_meta() for more details.\n\n    meta: [batch, meta length] where meta length depends on NUM_CLASSES\n\n    Returns a dict of the parsed tensors.\n    """\n    image_id = meta[:, 0]\n    original_image_shape = meta[:, 1:4]\n    image_shape = meta[:, 4:7]\n    window = meta[:, 7:11]  # (y1, x1, y2, x2) window of image in in pixels\n    scale = meta[:, 11]\n    active_class_ids = meta[:, 12:]\n    return {\n        "image_id": image_id,\n        "original_image_shape": original_image_shape,\n        "image_shape": image_shape,\n        "window": window,\n        "scale": scale,\n        "active_class_ids": active_class_ids,\n    }\n\n\ndef mold_image(images, config):\n    """Expects an RGB image (or array of images) and subtracts\n    the mean pixel and converts it to float. Expects image\n    colors in RGB order.\n    """\n    return images.astype(np.float32) - config.MEAN_PIXEL\n\n\ndef unmold_image(normalized_images, config):\n    """Takes a image normalized with mold() and returns the original."""\n    return (normalized_images + config.MEAN_PIXEL).astype(np.uint8)\n\n\n############################################################\n#  Miscellenous Graph Functions\n############################################################\n\ndef trim_zeros_graph(boxes, name=\'trim_zeros\'):\n    """Often boxes are represented with matrices of shape [N, 4] and\n    are padded with zeros. This removes zero boxes.\n\n    boxes: [N, 4] matrix of boxes.\n    non_zeros: [N] a 1D boolean mask identifying the rows to keep\n    """\n    non_zeros = tf.cast(tf.reduce_sum(tf.abs(boxes), axis=1), tf.bool)\n    boxes = tf.boolean_mask(boxes, non_zeros, name=name)\n    return boxes, non_zeros\n\n\ndef batch_pack_graph(x, counts, num_rows):\n    """Picks different number of values from each row\n    in x depending on the values in counts.\n    """\n    outputs = []\n    for i in range(num_rows):\n        outputs.append(x[i, :counts[i]])\n    return tf.concat(outputs, axis=0)\n\n\ndef norm_boxes_graph(boxes, shape):\n    """Converts boxes from pixel coordinates to normalized coordinates.\n    boxes: [..., (y1, x1, y2, x2)] in pixel coordinates\n    shape: [..., (height, width)] in pixels\n\n    Note: In pixel coordinates (y2, x2) is outside the box. But in normalized\n    coordinates it\'s inside the box.\n\n    Returns:\n        [..., (y1, x1, y2, x2)] in normalized coordinates\n    """\n    h, w = tf.split(tf.cast(shape, tf.float32), 2)\n    scale = tf.concat([h, w, h, w], axis=-1) - tf.constant(1.0)\n    shift = tf.constant([0., 0., 1., 1.])\n    return tf.divide(boxes - shift, scale)\n\n\ndef denorm_boxes_graph(boxes, shape):\n    """Converts boxes from normalized coordinates to pixel coordinates.\n    boxes: [..., (y1, x1, y2, x2)] in normalized coordinates\n    shape: [..., (height, width)] in pixels\n\n    Note: In pixel coordinates (y2, x2) is outside the box. But in normalized\n    coordinates it\'s inside the box.\n\n    Returns:\n        [..., (y1, x1, y2, x2)] in pixel coordinates\n    """\n    h, w = tf.split(tf.cast(shape, tf.float32), 2)\n    scale = tf.concat([h, w, h, w], axis=-1) - tf.constant(1.0)\n    shift = tf.constant([0., 0., 1., 1.])\n    return tf.cast(tf.round(tf.multiply(boxes, scale) + shift), tf.int32)')


# In[ ]:


sys.path.append('/kaggle/working/Mask_RCNN')
from mrcnn.config import Config
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
from mrcnn.model import log


# In[ ]:


#!wget --quiet https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5
get_ipython().system('cp /kaggle/input/training-mask-r-cnn-to-be-a-fashionista-lb-0-07/Mask_RCNN/mask_rcnn_coco.h5 /kaggle/working/Mask_RCNN/mask_rcnn_coco.h5')
get_ipython().system('ls -lh mask_rcnn_coco.h5')

COCO_WEIGHTS_PATH = 'mask_rcnn_coco.h5'


# In[ ]:


def resize_image(ImgPath):
    image = cv2.imread(ImgPath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_AREA)  
    return image


# ### Network-1 : SuperCategory = 0, 1, 2

# In[ ]:


supercategories_dict


# In[ ]:


SuperCategoryImagesGrouped = pd.read_csv('/kaggle/input/imaterialist-fashion-2020-fgvc7/train.csv')
SuperCategoryImagesGrouped


# In[ ]:


GarmentClassIds = []
ClassNames = []
for i, val in category_dict.items():
    if val[1] == 'others' or val[1] == 'closures' or val[1] == 'decorations':
        print(i, val[0])
        GarmentClassIds.append(i)
        ClassNames.append(val[0])


# In[ ]:


SuperCategoryImagesGrouped = SuperCategoryImagesGrouped[SuperCategoryImagesGrouped['ClassId'].apply(lambda val: True if val in GarmentClassIds else False)]
SuperCategoryImagesGrouped.columns = ['ImageId', 'EncodedPixels', 'Height', 'Width', 'SuperCategory', 'AttributesIds']
di = { val : i for i, val in enumerate(GarmentClassIds) }
SuperCategoryImagesGrouped['SuperCategory'] = SuperCategoryImagesGrouped['SuperCategory'].map(di)
SuperCategoryImagesGrouped


# In[ ]:


'''del_rows = (SuperCategoryImage['SuperCategory'] == 5) | (SuperCategoryImage['SuperCategory'] == 7)
SuperCategoryImagesGrouped = SuperCategoryImage[del_rows.values].reset_index()'''


# In[ ]:


supercategories_dict = {
    'bag, wallet' : 0,
    'scarf' : 1,
    'umbrella' : 2,
    'buckle' : 3,
    'zipper' : 4,
    'applique' : 5,
    'bead' : 6,
    'bow' : 7,
    'flower' : 8,
    'fringe' : 9,
    'ribbon' : 10,
    'rivet' : 11,
    'ruffle' : 12,
    'sequin' : 13,
    'tassel' : 14
}


# In[ ]:


SuperCategoryImagesGrouped = SuperCategoryImagesGrouped.groupby('ImageId')['EncodedPixels', 'SuperCategory', 'Height', 'Width'].agg(lambda x: list(x))
SuperCategoryImagesGrouped['Height'] = SuperCategoryImagesGrouped['Height'].apply(lambda x: x[0])
SuperCategoryImagesGrouped['Width'] = SuperCategoryImagesGrouped['Width'].apply(lambda x: x[0])
SuperCategoryImagesGrouped


# In[ ]:


def CombineEncodedPixels(row):
    ImgDict = {}
    ImgDict['EncodedPixels'] = []
    ImgDict['SuperCategory'] = []
    ImgDict['Height'] = row.Height
    ImgDict['Width'] = row.Width
    temp_dict = {}
    for i in range(len(row.SuperCategory)):
        if row.SuperCategory[i] in temp_dict.keys():
            temp = temp_dict[row.SuperCategory[i]]
            ImgDict['EncodedPixels'][temp] = ImgDict['EncodedPixels'][temp] + ' ' + row.EncodedPixels[i]
        else:
            temp_dict[row.SuperCategory[i]] = len(ImgDict['SuperCategory'])
            ImgDict['EncodedPixels'].append(row.EncodedPixels[i])
            ImgDict['SuperCategory'].append(row.SuperCategory[i])
    return pd.Series(ImgDict)

tqdm.pandas()
SuperCategoryImagesGrouped = SuperCategoryImagesGrouped.progress_apply(CombineEncodedPixels, axis=1)
SuperCategoryImagesGrouped


# In[ ]:


'''def bias(row):
    SCat = row.SuperCategory
    if (7 in SCat) or (1 in SCat) or (2 in SCat) or (8 in SCat) or (9 in SCat) or (10 in SCat) or (13 in SCat) or (14 in SCat):
        return True
    return False

tqdm.pandas()
SuperCategoryImagesGrouped = SuperCategoryImagesGrouped[SuperCategoryImagesGrouped.progress_apply(bias, axis=1)]'''


# In[ ]:


class FashionDataset(utils.Dataset):

    def __init__(self, df):
        super().__init__(self)
        
        # Add classes
        for i, name in enumerate(supercategories_dict):
            self.add_class("fashion", i+1, name)
        
        # Add images 
        for i, row in df.iterrows():
            self.add_image("fashion", 
                           image_id=row.name, 
                           path=os.path.join(dataDir, 'train', row.name+'.jpg'), 
                           labels=row['SuperCategory'],
                           annotations=row['EncodedPixels'], 
                           height=int(row['Height']), width=int(row['Width']))

    def image_reference(self, image_id):
        info = self.image_info[image_id]
        inverted_dict = dict([[v,k] for k,v in supercategories_dict.items()])
        return info['path'], [inverted_dict[int(x)] for x in info['labels']]
    
    def load_image(self, image_id):
        return resize_image(self.image_info[image_id]['path'])

    def load_mask(self, image_id):
        info = self.image_info[image_id]
                
        mask = np.zeros((IMG_SIZE, IMG_SIZE, len(info['annotations'])), dtype=np.uint8)
        labels = []
        
        for m, (annotation, label) in enumerate(zip(info['annotations'], info['labels'])):
            sub_mask = np.full(info['height']*info['width'], 0, dtype=np.uint8)
            annotation = [int(x) for x in annotation.split(' ')]
            
            for i, start_pixel in enumerate(annotation[::2]):
                sub_mask[start_pixel: start_pixel+annotation[2*i+1]] = 1

            sub_mask = sub_mask.reshape((info['height'], info['width']), order='F')
            sub_mask = cv2.resize(sub_mask, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_NEAREST)
            
            mask[:, :, m] = sub_mask
            labels.append(int(label)+1)
            
        return mask, np.array(labels)


# In[ ]:


MAX_NUM = 0
for i, li in enumerate(SuperCategoryImagesGrouped.SuperCategory.values):
    if MAX_NUM < len(li):
        MAX_NUM = len(li)
MAX_NUM


# In[ ]:


NUM_CATS = len(supercategories_dict)
IMG_SIZE = 1024
class FashionConfig(Config):
    NAME = "fashion"
    NUM_CLASSES = NUM_CATS + 1 # +1 for the background class
    BACKBONE = 'resnet50'
    
    GPU_COUNT = 1
    IMAGES_PER_GPU = 2 # a memory error occurs when IMAGES_PER_GPU is too high
    
    IMAGE_MIN_DIM = IMG_SIZE
    IMAGE_MAX_DIM = IMG_SIZE  
    IMAGE_RESIZE_MODE = 'none'
    USE_MINI_MASK = False
    MAX_GT_INSTANCES = MAX_NUM
    
    RPN_ANCHOR_SCALES = (16, 32, 64, 128, 256)
    #DETECTION_NMS_THRESHOLD = 0.0
    
    # STEPS_PER_EPOCH should be the number of instances 
    # divided by (GPU_COUNT*IMAGES_PER_GPU), and so should VALIDATION_STEPS;
    # however, due to the time limit, I set them so that this kernel can be run in 9 hours
    STEPS_PER_EPOCH = 1000
    VALIDATION_STEPS = 50
    
config = FashionConfig()
config.display()


# In[ ]:


'''dataset = FashionDataset(SuperCategoryImagesGrouped)
dataset.prepare()'''


# In[ ]:


'''for i in range(2):
    image_id = random.choice(dataset.image_ids)
    print(dataset.image_reference(image_id))
    
    image = dataset.load_image(image_id)
    mask, class_ids = dataset.load_mask(image_id)
    visualize.display_top_masks(image, mask, class_ids, dataset.class_names, limit=3)'''


# In[ ]:


# This code partially supports k-fold training, 
# you can specify the fold to train and the total number of folds here
FOLD = 0
N_FOLDS = 5

kf = KFold(n_splits=N_FOLDS, random_state=42, shuffle=True)
splits = kf.split(SuperCategoryImagesGrouped) # ideally, this should be multilabel stratification

def get_fold():    
    for i, (train_index, valid_index) in enumerate(splits):
        if i == FOLD:
            return SuperCategoryImagesGrouped.iloc[train_index], SuperCategoryImagesGrouped.iloc[valid_index]
        
train_df, valid_df = get_fold()

train_dataset = FashionDataset(train_df)
train_dataset.prepare()

valid_dataset = FashionDataset(valid_df)
valid_dataset.prepare()


# In[ ]:


train_segments = np.concatenate(train_df['SuperCategory'].values).astype(int)
print("Total train images: ", len(train_df))
print("Total train segments: ", len(train_segments))

plt.figure(figsize=(6, 3))
values, counts = np.unique(train_segments, return_counts=True)
print(values)
plt.bar(values, counts)
plt.xticks(values, list(supercategories_dict.keys()), rotation='vertical')
plt.show()

valid_segments = np.concatenate(valid_df['SuperCategory'].values).astype(int)
print("Total train images: ", len(valid_df))
print("Total validation segments: ", len(valid_segments))

plt.figure(figsize=(6, 3))
values, counts = np.unique(valid_segments, return_counts=True)
plt.bar(values, counts)
plt.xticks(values, list(supercategories_dict.keys()), rotation='vertical')
plt.show()


# In[ ]:


# Note that any hyperparameters here, such as LR, may still not be optimal
LR = 1e-4
EPOCHS = [2, 6, 8]

import warnings 
warnings.filterwarnings("ignore")


# In[ ]:


model1 = modellib.MaskRCNN(mode='training', config=config, model_dir='/kaggle/working/')

model1.load_weights(COCO_WEIGHTS_PATH, by_name=True, exclude=[
    'mrcnn_class_logits', 'mrcnn_bbox_fc', 'mrcnn_bbox', 'mrcnn_mask'])


# In[ ]:


'''model1 = modellib.MaskRCNN(mode='training', config=config, model_dir='/kaggle/working/')

model1.load_weights('/kaggle/working/SuperMaskCat3to7All2.h5', by_name=True)'''


# In[ ]:


get_ipython().run_cell_magic('time', '', "model1.train(train_dataset, valid_dataset,\n            learning_rate=LR*4, # train heads with higher lr to speedup learning\n            epochs=EPOCHS[0],\n            layers='heads',\n            augmentation=None)\n\nhistory = model1.keras_model.history.history\n\n%cd ..\nmodel1.keras_model.save_weights('SuperMaskCat8to11Head1.h5')\n#pickle.dump(history, open('SuperMaskCat3to7Head1.pkl', 'ab'))\n%cd Mask_RCNN")


# In[ ]:


get_ipython().run_cell_magic('time', '', "model1.train(train_dataset, valid_dataset,\n            learning_rate=LR*2,\n            epochs=EPOCHS[1],\n            layers='all',\n            augmentation=None)\n\nnew_history = model1.keras_model.history.history\n#for k in new_history: history[k] = history[k] + new_history[k]\n\n%cd ..\nmodel1.keras_model.save_weights('SuperMaskCat8to11All1.h5')\n#pickle.dump(history, open('SuperMaskCat3to7All1.pkl', 'ab'))\n%cd Mask_RCNN")


# In[ ]:


get_ipython().run_cell_magic('time', '', "model1.train(train_dataset, valid_dataset,\n            learning_rate=LR,\n            epochs=EPOCHS[2],\n            layers='all',\n            augmentation=None)\n\nnew_history = model1.keras_model.history.history\n#for k in new_history: history[k] = history[k] + new_history[k]\n\n%cd ..\nmodel1.keras_model.save_weights('SuperMaskCat8to11All2.h5')\n#pickle.dump(history, open('SuperMaskCat3to7All2.pkl', 'ab'))\n%cd Mask_RCNN")


# In[ ]:


'''%%time
model1.train(train_dataset, valid_dataset,
            learning_rate=LR/5,
            epochs=EPOCHS[3],
            layers='all',
            augmentation=None)

new_history = model1.keras_model.history.history
for k in new_history: history[k] = history[k] + new_history[k]

%cd ..
model1.keras_model.save_weights('SuperMaskCat3to7All.h5')
pickle.dump(history, open('SuperMaskCat3to7All3.pkl', 'ab'))
%cd Mask_RCNN'''


# In[ ]:


'''epochs = range(EPOCHS[-1])

plt.figure(figsize=(18, 6))

plt.subplot(131)
plt.plot(epochs, history['loss'], label="train loss")
plt.plot(epochs, history['val_loss'], label="valid loss")
plt.legend()
plt.subplot(132)
plt.plot(epochs, history['mrcnn_class_loss'], label="train class loss")
plt.plot(epochs, history['val_mrcnn_class_loss'], label="valid class loss")
plt.legend()
plt.subplot(133)
plt.plot(epochs, history['mrcnn_mask_loss'], label="train mask loss")
plt.plot(epochs, history['val_mrcnn_mask_loss'], label="valid mask loss")
plt.legend()

plt.show()'''


# ### Predict

# In[ ]:


class InferenceConfig(FashionConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

inference_config = InferenceConfig()
inference_config.display()


# In[ ]:


model_path = '/kaggle/working/SuperMaskCat8to11All2.h5'
model = modellib.MaskRCNN(mode='inference', 
                          config=inference_config,
                          model_dir='/kaggle/working/')
print("Loading weights from ", model_path)
model.load_weights(model_path, by_name=True)


# In[ ]:


import itertools
def to_rle(bits):
    rle = []
    pos = 0
    for bit, group in itertools.groupby(bits):
        group_list = list(group)
        if bit:
            rle.extend([pos, sum(group_list)])
        pos += len(group_list)
    return rle

def refine_masks(masks, rois):
    areas = np.sum(masks.reshape(-1, masks.shape[-1]), axis=0)
    mask_index = np.argsort(areas)
    union_mask = np.zeros(masks.shape[:-1], dtype=bool)
    for m in mask_index:
        masks[:, :, m] = np.logical_and(masks[:, :, m], np.logical_not(union_mask))
        union_mask = np.logical_or(masks[:, :, m], union_mask)
    for m in range(masks.shape[-1]):
        mask_pos = np.where(masks[:, :, m]==True)
        if np.any(mask_pos):
            y1, x1 = np.min(mask_pos, axis=1)
            y2, x2 = np.max(mask_pos, axis=1)
            rois[m, :] = [y1, x1, y2, x2]
    return masks, rois


# In[ ]:


ImageId = pd.Series(valid_df.index)
valid_df = valid_df.set_index(pd.Index(list(range(len(valid_df)))))
valid_df['ImageId'] = ImageId
valid_df = valid_df.iloc[:20]
valid_df


# In[ ]:


get_ipython().run_cell_magic('time', '', "sub_list = []\nmissing_count = 0\nfor i, row in tqdm(valid_df.iterrows(), total=len(valid_df)):\n    image = resize_image(os.path.join(dataDir, 'train', row['ImageId']+'.jpg'))\n    result = model.detect([image])[0]\n    if result['masks'].size > 0:\n        masks, _ = refine_masks(result['masks'], result['rois'])\n        for m in range(masks.shape[-1]):\n            mask = masks[:, :, m].ravel(order='F')\n            rle = to_rle(mask)\n            label = result['class_ids'][m] - 1\n            sub_list.append([row['ImageId'], ' '.join(list(map(str, rle))), label])\n    else:\n        # The system does not allow missing ids, this is an easy way to fill them \n        sub_list.append([row['ImageId'], '1 1', 23])\n        missing_count += 1")


# In[ ]:


valid_pred_df = pd.DataFrame(sub_list)
valid_pred_df.columns = ['ImageId', 'EncodedPixels', 'ClassId']
valid_pred_df = valid_pred_df.groupby('ImageId')['EncodedPixels', 'ClassId'].agg(lambda x: list(x))

ImageId = pd.Series(valid_pred_df.index)
valid_pred_df.index = pd.Index(list(range(len(valid_pred_df))))
valid_pred_df['ImageId'] = ImageId
valid_pred_df


# In[ ]:


def compare_mask(Arow, Prow):
    if Arow.ImageId != Prow.ImageId:
        print('Images not same')
        return 'No'
    if Prow.ClassId[0] == 23:
        #print('Not Predicted Correctly')
        return 'No'
    img = np.array(Image.open(os.path.join(dataDir, 'train', Arow.ImageId+'.jpg')))
    H, W, _ = img.shape
    
    actual_mask = np.zeros(H*W)
    for j in range(len(Arow.SuperCategory)):
        pixels = Arow.EncodedPixels[j][1:].split(' ')
        label = Arow.SuperCategory[j] + 1
        for i in range(len(pixels)//2):
            start = int(pixels[2*i])
            end = start + int(pixels[2*i + 1])
            actual_mask[start:end] = label
    actual_mask = actual_mask.reshape((H, W), order='F')
        
    pred_mask = np.zeros(1024*1024)
    for j in range(len(Prow.EncodedPixels)):
        pixels = Prow.EncodedPixels[j].split(' ')
        label = Prow.ClassId[j] + 1
        for i in range(len(pixels)//2):
            start = int(pixels[2*i])
            end = start + int(pixels[2*i + 1])
            pred_mask[start:end] = label
    pred_mask = pred_mask.reshape((1024, 1024), order='F')
    
    return img, actual_mask, pred_mask


# In[ ]:


num = min(20, len(valid_df))
output = []
for i in tqdm(range(num)):
    out = compare_mask(valid_df.iloc[i], valid_pred_df.iloc[i])
    if out != 'No':
        output.append(out)

fig, ax = plt.subplots(len(output), 3, figsize=(15,5*len(output)))
for i in range(len(output)):
    ax[i,0].imshow(output[i][0])
    ax[i,1].imshow(output[i][1])
    ax[i,2].imshow(output[i][2])
plt.show()


# In[ ]:


for i in range(20):
    image_id = valid_df['ImageId'].iloc[i]
    image_path = os.path.join(dataDir, 'train', image_id+'.jpg')
    
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    result = model.detect([resize_image(image_path)])
    r = result[0]
    
    if r['masks'].size > 0:
        masks = np.zeros((img.shape[0], img.shape[1], r['masks'].shape[-1]), dtype=np.uint8)
        for m in range(r['masks'].shape[-1]):
            masks[:, :, m] = cv2.resize(r['masks'][:, :, m].astype('uint8'), 
                                        (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST)
        
        y_scale = img.shape[0]/1024
        x_scale = img.shape[1]/1024
        rois = (r['rois'] * [y_scale, x_scale, y_scale, x_scale]).astype(int)
        
        masks, rois = refine_masks(masks, rois)
    else:
        masks, rois = r['masks'], r['rois']
        
    visualize.display_instances(img, rois, masks, r['class_ids'], 
                                ['bg']+list(supercategories_dict.keys()), r['scores'],
                                title=image_id, figsize=(12, 12))


# In[ ]:


'''backtorgb = cv2.cvtColor(temp,cv2.COLOR_GRAY2RGB)
plt.imshow(backtorgb)'''

