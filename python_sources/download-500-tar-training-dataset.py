#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python


# Lots of folks confused on the Train dataset - several, including me trying to download the images using one of the offered scripts.  That's not how we get the train images.
# 
# There are 500 seperate tar compressed files.  This script downloads and saves the tar files to a local drive.  Will work tomorrow on script to uncompress.   I am 6 month newbie in Python - so use with care:)
# 
# DOWN LOAD THIS NOTEBOOK AND RUN ON YOUR LOCAL PC.   Since the script is written for local machine only it's filled with error messages here on Kaggle as I can seem to save a clean version without commit - which of course runs the script and generates errors.
# 
# I had lots of starts and stops but guessing 6 hours total time with my 1GB internet connection.

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
from urllib import request, error
from PIL import Image
from io import BytesIO
import csv
import tarfile

import tensorflow as tf
import tempfile
import urllib


# Revision - had one too many tar files listed.

# Not a fan of passing arguments to Python - since my scripts never work right the first 20 times.  So hard wired locations.
# 
# I developed and ran this notebook on a different PC than the one I wanted to save the files on.  (That one was downloading test images).
# 
# So my directory was the local network name for the PC, the drive name and the folder.
# 
# 
# output_dir = "n:/landmark_train" would have been the code if running on the same machine.

# In[ ]:


output_dir = '//msi/msi_n/landmark_TRAIN'


# The names of the tar files and thier url was an excel file to start with - hence why I called the following a data_file.

# In[ ]:


data_file = (
'https://s3.amazonaws.com/google-landmark/train/images_000.tar',
'https://s3.amazonaws.com/google-landmark/train/images_001.tar',
'https://s3.amazonaws.com/google-landmark/train/images_002.tar',
'https://s3.amazonaws.com/google-landmark/train/images_003.tar',
'https://s3.amazonaws.com/google-landmark/train/images_004.tar',
'https://s3.amazonaws.com/google-landmark/train/images_005.tar',
'https://s3.amazonaws.com/google-landmark/train/images_006.tar',
'https://s3.amazonaws.com/google-landmark/train/images_007.tar',
'https://s3.amazonaws.com/google-landmark/train/images_008.tar',
'https://s3.amazonaws.com/google-landmark/train/images_009.tar',
'https://s3.amazonaws.com/google-landmark/train/images_010.tar',
'https://s3.amazonaws.com/google-landmark/train/images_011.tar',
'https://s3.amazonaws.com/google-landmark/train/images_012.tar',
'https://s3.amazonaws.com/google-landmark/train/images_013.tar',
'https://s3.amazonaws.com/google-landmark/train/images_014.tar',
'https://s3.amazonaws.com/google-landmark/train/images_015.tar',
'https://s3.amazonaws.com/google-landmark/train/images_016.tar',
'https://s3.amazonaws.com/google-landmark/train/images_017.tar',
'https://s3.amazonaws.com/google-landmark/train/images_018.tar',
'https://s3.amazonaws.com/google-landmark/train/images_019.tar',
'https://s3.amazonaws.com/google-landmark/train/images_020.tar',
'https://s3.amazonaws.com/google-landmark/train/images_021.tar',
'https://s3.amazonaws.com/google-landmark/train/images_022.tar',
'https://s3.amazonaws.com/google-landmark/train/images_023.tar',
'https://s3.amazonaws.com/google-landmark/train/images_024.tar',
'https://s3.amazonaws.com/google-landmark/train/images_025.tar',
'https://s3.amazonaws.com/google-landmark/train/images_026.tar',
'https://s3.amazonaws.com/google-landmark/train/images_027.tar',
'https://s3.amazonaws.com/google-landmark/train/images_028.tar',
'https://s3.amazonaws.com/google-landmark/train/images_029.tar',
'https://s3.amazonaws.com/google-landmark/train/images_030.tar',
'https://s3.amazonaws.com/google-landmark/train/images_031.tar',
'https://s3.amazonaws.com/google-landmark/train/images_032.tar',
'https://s3.amazonaws.com/google-landmark/train/images_033.tar',
'https://s3.amazonaws.com/google-landmark/train/images_034.tar',
'https://s3.amazonaws.com/google-landmark/train/images_035.tar',
'https://s3.amazonaws.com/google-landmark/train/images_036.tar',
'https://s3.amazonaws.com/google-landmark/train/images_037.tar',
'https://s3.amazonaws.com/google-landmark/train/images_038.tar',
'https://s3.amazonaws.com/google-landmark/train/images_039.tar',
'https://s3.amazonaws.com/google-landmark/train/images_040.tar',
'https://s3.amazonaws.com/google-landmark/train/images_041.tar',
'https://s3.amazonaws.com/google-landmark/train/images_042.tar',
'https://s3.amazonaws.com/google-landmark/train/images_043.tar',
'https://s3.amazonaws.com/google-landmark/train/images_044.tar',
'https://s3.amazonaws.com/google-landmark/train/images_045.tar',
'https://s3.amazonaws.com/google-landmark/train/images_046.tar',
'https://s3.amazonaws.com/google-landmark/train/images_047.tar',
'https://s3.amazonaws.com/google-landmark/train/images_048.tar',
'https://s3.amazonaws.com/google-landmark/train/images_049.tar',
'https://s3.amazonaws.com/google-landmark/train/images_050.tar',
'https://s3.amazonaws.com/google-landmark/train/images_051.tar',
'https://s3.amazonaws.com/google-landmark/train/images_052.tar',
'https://s3.amazonaws.com/google-landmark/train/images_053.tar',
'https://s3.amazonaws.com/google-landmark/train/images_054.tar',
'https://s3.amazonaws.com/google-landmark/train/images_055.tar',
'https://s3.amazonaws.com/google-landmark/train/images_056.tar',
'https://s3.amazonaws.com/google-landmark/train/images_057.tar',
'https://s3.amazonaws.com/google-landmark/train/images_058.tar',
'https://s3.amazonaws.com/google-landmark/train/images_059.tar',
'https://s3.amazonaws.com/google-landmark/train/images_060.tar',
'https://s3.amazonaws.com/google-landmark/train/images_061.tar',
'https://s3.amazonaws.com/google-landmark/train/images_062.tar',
'https://s3.amazonaws.com/google-landmark/train/images_063.tar',
'https://s3.amazonaws.com/google-landmark/train/images_064.tar',
'https://s3.amazonaws.com/google-landmark/train/images_065.tar',
'https://s3.amazonaws.com/google-landmark/train/images_066.tar',
'https://s3.amazonaws.com/google-landmark/train/images_067.tar',
'https://s3.amazonaws.com/google-landmark/train/images_068.tar',
'https://s3.amazonaws.com/google-landmark/train/images_069.tar',
'https://s3.amazonaws.com/google-landmark/train/images_070.tar',
'https://s3.amazonaws.com/google-landmark/train/images_071.tar',
'https://s3.amazonaws.com/google-landmark/train/images_072.tar',
'https://s3.amazonaws.com/google-landmark/train/images_073.tar',
'https://s3.amazonaws.com/google-landmark/train/images_074.tar',
'https://s3.amazonaws.com/google-landmark/train/images_075.tar',
'https://s3.amazonaws.com/google-landmark/train/images_076.tar',
'https://s3.amazonaws.com/google-landmark/train/images_077.tar',
'https://s3.amazonaws.com/google-landmark/train/images_078.tar',
'https://s3.amazonaws.com/google-landmark/train/images_079.tar',
'https://s3.amazonaws.com/google-landmark/train/images_080.tar',
'https://s3.amazonaws.com/google-landmark/train/images_081.tar',
'https://s3.amazonaws.com/google-landmark/train/images_082.tar',
'https://s3.amazonaws.com/google-landmark/train/images_083.tar',
'https://s3.amazonaws.com/google-landmark/train/images_084.tar',
'https://s3.amazonaws.com/google-landmark/train/images_085.tar',
'https://s3.amazonaws.com/google-landmark/train/images_086.tar',
'https://s3.amazonaws.com/google-landmark/train/images_087.tar',
'https://s3.amazonaws.com/google-landmark/train/images_088.tar',
'https://s3.amazonaws.com/google-landmark/train/images_089.tar',
'https://s3.amazonaws.com/google-landmark/train/images_090.tar',
'https://s3.amazonaws.com/google-landmark/train/images_091.tar',
'https://s3.amazonaws.com/google-landmark/train/images_092.tar',
'https://s3.amazonaws.com/google-landmark/train/images_093.tar',
'https://s3.amazonaws.com/google-landmark/train/images_094.tar',
'https://s3.amazonaws.com/google-landmark/train/images_095.tar',
'https://s3.amazonaws.com/google-landmark/train/images_096.tar',
'https://s3.amazonaws.com/google-landmark/train/images_097.tar',
'https://s3.amazonaws.com/google-landmark/train/images_098.tar',
'https://s3.amazonaws.com/google-landmark/train/images_099.tar',
'https://s3.amazonaws.com/google-landmark/train/images_100.tar',
'https://s3.amazonaws.com/google-landmark/train/images_101.tar',
'https://s3.amazonaws.com/google-landmark/train/images_102.tar',
'https://s3.amazonaws.com/google-landmark/train/images_103.tar',
'https://s3.amazonaws.com/google-landmark/train/images_104.tar',
'https://s3.amazonaws.com/google-landmark/train/images_105.tar',
'https://s3.amazonaws.com/google-landmark/train/images_106.tar',
'https://s3.amazonaws.com/google-landmark/train/images_107.tar',
'https://s3.amazonaws.com/google-landmark/train/images_108.tar',
'https://s3.amazonaws.com/google-landmark/train/images_109.tar',
'https://s3.amazonaws.com/google-landmark/train/images_110.tar',
'https://s3.amazonaws.com/google-landmark/train/images_111.tar',
'https://s3.amazonaws.com/google-landmark/train/images_112.tar',
'https://s3.amazonaws.com/google-landmark/train/images_113.tar',
'https://s3.amazonaws.com/google-landmark/train/images_114.tar',
'https://s3.amazonaws.com/google-landmark/train/images_115.tar',
'https://s3.amazonaws.com/google-landmark/train/images_116.tar',
'https://s3.amazonaws.com/google-landmark/train/images_117.tar',
'https://s3.amazonaws.com/google-landmark/train/images_118.tar',
'https://s3.amazonaws.com/google-landmark/train/images_119.tar',
'https://s3.amazonaws.com/google-landmark/train/images_120.tar',
'https://s3.amazonaws.com/google-landmark/train/images_121.tar',
'https://s3.amazonaws.com/google-landmark/train/images_122.tar',
'https://s3.amazonaws.com/google-landmark/train/images_123.tar',
'https://s3.amazonaws.com/google-landmark/train/images_124.tar',
'https://s3.amazonaws.com/google-landmark/train/images_125.tar',
'https://s3.amazonaws.com/google-landmark/train/images_126.tar',
'https://s3.amazonaws.com/google-landmark/train/images_127.tar',
'https://s3.amazonaws.com/google-landmark/train/images_128.tar',
'https://s3.amazonaws.com/google-landmark/train/images_129.tar',
'https://s3.amazonaws.com/google-landmark/train/images_130.tar',
'https://s3.amazonaws.com/google-landmark/train/images_131.tar',
'https://s3.amazonaws.com/google-landmark/train/images_132.tar',
'https://s3.amazonaws.com/google-landmark/train/images_133.tar',
'https://s3.amazonaws.com/google-landmark/train/images_134.tar',
'https://s3.amazonaws.com/google-landmark/train/images_135.tar',
'https://s3.amazonaws.com/google-landmark/train/images_136.tar',
'https://s3.amazonaws.com/google-landmark/train/images_137.tar',
'https://s3.amazonaws.com/google-landmark/train/images_138.tar',
'https://s3.amazonaws.com/google-landmark/train/images_139.tar',
'https://s3.amazonaws.com/google-landmark/train/images_140.tar',
'https://s3.amazonaws.com/google-landmark/train/images_141.tar',
'https://s3.amazonaws.com/google-landmark/train/images_142.tar',
'https://s3.amazonaws.com/google-landmark/train/images_143.tar',
'https://s3.amazonaws.com/google-landmark/train/images_144.tar',
'https://s3.amazonaws.com/google-landmark/train/images_145.tar',
'https://s3.amazonaws.com/google-landmark/train/images_146.tar',
'https://s3.amazonaws.com/google-landmark/train/images_147.tar',
'https://s3.amazonaws.com/google-landmark/train/images_148.tar',
'https://s3.amazonaws.com/google-landmark/train/images_149.tar',
'https://s3.amazonaws.com/google-landmark/train/images_150.tar',
'https://s3.amazonaws.com/google-landmark/train/images_151.tar',
'https://s3.amazonaws.com/google-landmark/train/images_152.tar',
'https://s3.amazonaws.com/google-landmark/train/images_153.tar',
'https://s3.amazonaws.com/google-landmark/train/images_154.tar',
'https://s3.amazonaws.com/google-landmark/train/images_155.tar',
'https://s3.amazonaws.com/google-landmark/train/images_156.tar',
'https://s3.amazonaws.com/google-landmark/train/images_157.tar',
'https://s3.amazonaws.com/google-landmark/train/images_158.tar',
'https://s3.amazonaws.com/google-landmark/train/images_159.tar',
'https://s3.amazonaws.com/google-landmark/train/images_160.tar',
'https://s3.amazonaws.com/google-landmark/train/images_161.tar',
'https://s3.amazonaws.com/google-landmark/train/images_162.tar',
'https://s3.amazonaws.com/google-landmark/train/images_163.tar',
'https://s3.amazonaws.com/google-landmark/train/images_164.tar',
'https://s3.amazonaws.com/google-landmark/train/images_165.tar',
'https://s3.amazonaws.com/google-landmark/train/images_166.tar',
'https://s3.amazonaws.com/google-landmark/train/images_167.tar',
'https://s3.amazonaws.com/google-landmark/train/images_168.tar',
'https://s3.amazonaws.com/google-landmark/train/images_169.tar',
'https://s3.amazonaws.com/google-landmark/train/images_170.tar',
'https://s3.amazonaws.com/google-landmark/train/images_171.tar',
'https://s3.amazonaws.com/google-landmark/train/images_172.tar',
'https://s3.amazonaws.com/google-landmark/train/images_173.tar',
'https://s3.amazonaws.com/google-landmark/train/images_174.tar',
'https://s3.amazonaws.com/google-landmark/train/images_175.tar',
'https://s3.amazonaws.com/google-landmark/train/images_176.tar',
'https://s3.amazonaws.com/google-landmark/train/images_177.tar',
'https://s3.amazonaws.com/google-landmark/train/images_178.tar',
'https://s3.amazonaws.com/google-landmark/train/images_179.tar',
'https://s3.amazonaws.com/google-landmark/train/images_180.tar',
'https://s3.amazonaws.com/google-landmark/train/images_181.tar',
'https://s3.amazonaws.com/google-landmark/train/images_182.tar',
'https://s3.amazonaws.com/google-landmark/train/images_183.tar',
'https://s3.amazonaws.com/google-landmark/train/images_184.tar',
'https://s3.amazonaws.com/google-landmark/train/images_185.tar',
'https://s3.amazonaws.com/google-landmark/train/images_186.tar',
'https://s3.amazonaws.com/google-landmark/train/images_187.tar',
'https://s3.amazonaws.com/google-landmark/train/images_188.tar',
'https://s3.amazonaws.com/google-landmark/train/images_189.tar',
'https://s3.amazonaws.com/google-landmark/train/images_190.tar',
'https://s3.amazonaws.com/google-landmark/train/images_191.tar',
'https://s3.amazonaws.com/google-landmark/train/images_192.tar',
'https://s3.amazonaws.com/google-landmark/train/images_193.tar',
'https://s3.amazonaws.com/google-landmark/train/images_194.tar',
'https://s3.amazonaws.com/google-landmark/train/images_195.tar',
'https://s3.amazonaws.com/google-landmark/train/images_196.tar',
'https://s3.amazonaws.com/google-landmark/train/images_197.tar',
'https://s3.amazonaws.com/google-landmark/train/images_198.tar',
'https://s3.amazonaws.com/google-landmark/train/images_199.tar',
'https://s3.amazonaws.com/google-landmark/train/images_200.tar',
'https://s3.amazonaws.com/google-landmark/train/images_201.tar',
'https://s3.amazonaws.com/google-landmark/train/images_202.tar',
'https://s3.amazonaws.com/google-landmark/train/images_203.tar',
'https://s3.amazonaws.com/google-landmark/train/images_204.tar',
'https://s3.amazonaws.com/google-landmark/train/images_205.tar',
'https://s3.amazonaws.com/google-landmark/train/images_206.tar',
'https://s3.amazonaws.com/google-landmark/train/images_207.tar',
'https://s3.amazonaws.com/google-landmark/train/images_208.tar',
'https://s3.amazonaws.com/google-landmark/train/images_209.tar',
'https://s3.amazonaws.com/google-landmark/train/images_210.tar',
'https://s3.amazonaws.com/google-landmark/train/images_211.tar',
'https://s3.amazonaws.com/google-landmark/train/images_212.tar',
'https://s3.amazonaws.com/google-landmark/train/images_213.tar',
'https://s3.amazonaws.com/google-landmark/train/images_214.tar',
'https://s3.amazonaws.com/google-landmark/train/images_215.tar',
'https://s3.amazonaws.com/google-landmark/train/images_216.tar',
'https://s3.amazonaws.com/google-landmark/train/images_217.tar',
'https://s3.amazonaws.com/google-landmark/train/images_218.tar',
'https://s3.amazonaws.com/google-landmark/train/images_219.tar',
'https://s3.amazonaws.com/google-landmark/train/images_220.tar',
'https://s3.amazonaws.com/google-landmark/train/images_221.tar',
'https://s3.amazonaws.com/google-landmark/train/images_222.tar',
'https://s3.amazonaws.com/google-landmark/train/images_223.tar',
'https://s3.amazonaws.com/google-landmark/train/images_224.tar',
'https://s3.amazonaws.com/google-landmark/train/images_225.tar',
'https://s3.amazonaws.com/google-landmark/train/images_226.tar',
'https://s3.amazonaws.com/google-landmark/train/images_227.tar',
'https://s3.amazonaws.com/google-landmark/train/images_228.tar',
'https://s3.amazonaws.com/google-landmark/train/images_229.tar',
'https://s3.amazonaws.com/google-landmark/train/images_230.tar',
'https://s3.amazonaws.com/google-landmark/train/images_231.tar',
'https://s3.amazonaws.com/google-landmark/train/images_232.tar',
'https://s3.amazonaws.com/google-landmark/train/images_233.tar',
'https://s3.amazonaws.com/google-landmark/train/images_234.tar',
'https://s3.amazonaws.com/google-landmark/train/images_235.tar',
'https://s3.amazonaws.com/google-landmark/train/images_236.tar',
'https://s3.amazonaws.com/google-landmark/train/images_237.tar',
'https://s3.amazonaws.com/google-landmark/train/images_238.tar',
'https://s3.amazonaws.com/google-landmark/train/images_239.tar',
'https://s3.amazonaws.com/google-landmark/train/images_240.tar',
'https://s3.amazonaws.com/google-landmark/train/images_241.tar',
'https://s3.amazonaws.com/google-landmark/train/images_242.tar',
'https://s3.amazonaws.com/google-landmark/train/images_243.tar',
'https://s3.amazonaws.com/google-landmark/train/images_244.tar',
'https://s3.amazonaws.com/google-landmark/train/images_245.tar',
'https://s3.amazonaws.com/google-landmark/train/images_246.tar',
'https://s3.amazonaws.com/google-landmark/train/images_247.tar',
'https://s3.amazonaws.com/google-landmark/train/images_248.tar',
'https://s3.amazonaws.com/google-landmark/train/images_249.tar',
'https://s3.amazonaws.com/google-landmark/train/images_250.tar',
'https://s3.amazonaws.com/google-landmark/train/images_251.tar',
'https://s3.amazonaws.com/google-landmark/train/images_252.tar',
'https://s3.amazonaws.com/google-landmark/train/images_253.tar',
'https://s3.amazonaws.com/google-landmark/train/images_254.tar',
'https://s3.amazonaws.com/google-landmark/train/images_255.tar',
'https://s3.amazonaws.com/google-landmark/train/images_256.tar',
'https://s3.amazonaws.com/google-landmark/train/images_257.tar',
'https://s3.amazonaws.com/google-landmark/train/images_258.tar',
'https://s3.amazonaws.com/google-landmark/train/images_259.tar',
'https://s3.amazonaws.com/google-landmark/train/images_260.tar',
'https://s3.amazonaws.com/google-landmark/train/images_261.tar',
'https://s3.amazonaws.com/google-landmark/train/images_262.tar',
'https://s3.amazonaws.com/google-landmark/train/images_263.tar',
'https://s3.amazonaws.com/google-landmark/train/images_264.tar',
'https://s3.amazonaws.com/google-landmark/train/images_265.tar',
'https://s3.amazonaws.com/google-landmark/train/images_266.tar',
'https://s3.amazonaws.com/google-landmark/train/images_267.tar',
'https://s3.amazonaws.com/google-landmark/train/images_268.tar',
'https://s3.amazonaws.com/google-landmark/train/images_269.tar',
'https://s3.amazonaws.com/google-landmark/train/images_270.tar',
'https://s3.amazonaws.com/google-landmark/train/images_271.tar',
'https://s3.amazonaws.com/google-landmark/train/images_272.tar',
'https://s3.amazonaws.com/google-landmark/train/images_273.tar',
'https://s3.amazonaws.com/google-landmark/train/images_274.tar',
'https://s3.amazonaws.com/google-landmark/train/images_275.tar',
'https://s3.amazonaws.com/google-landmark/train/images_276.tar',
'https://s3.amazonaws.com/google-landmark/train/images_277.tar',
'https://s3.amazonaws.com/google-landmark/train/images_278.tar',
'https://s3.amazonaws.com/google-landmark/train/images_279.tar',
'https://s3.amazonaws.com/google-landmark/train/images_280.tar',
'https://s3.amazonaws.com/google-landmark/train/images_281.tar',
'https://s3.amazonaws.com/google-landmark/train/images_282.tar',
'https://s3.amazonaws.com/google-landmark/train/images_283.tar',
'https://s3.amazonaws.com/google-landmark/train/images_284.tar',
'https://s3.amazonaws.com/google-landmark/train/images_285.tar',
'https://s3.amazonaws.com/google-landmark/train/images_286.tar',
'https://s3.amazonaws.com/google-landmark/train/images_287.tar',
'https://s3.amazonaws.com/google-landmark/train/images_288.tar',
'https://s3.amazonaws.com/google-landmark/train/images_289.tar',
'https://s3.amazonaws.com/google-landmark/train/images_290.tar',
'https://s3.amazonaws.com/google-landmark/train/images_291.tar',
'https://s3.amazonaws.com/google-landmark/train/images_292.tar',
'https://s3.amazonaws.com/google-landmark/train/images_293.tar',
'https://s3.amazonaws.com/google-landmark/train/images_294.tar',
'https://s3.amazonaws.com/google-landmark/train/images_295.tar',
'https://s3.amazonaws.com/google-landmark/train/images_296.tar',
'https://s3.amazonaws.com/google-landmark/train/images_297.tar',
'https://s3.amazonaws.com/google-landmark/train/images_298.tar',
'https://s3.amazonaws.com/google-landmark/train/images_299.tar',
'https://s3.amazonaws.com/google-landmark/train/images_300.tar',
'https://s3.amazonaws.com/google-landmark/train/images_301.tar',
'https://s3.amazonaws.com/google-landmark/train/images_302.tar',
'https://s3.amazonaws.com/google-landmark/train/images_303.tar',
'https://s3.amazonaws.com/google-landmark/train/images_304.tar',
'https://s3.amazonaws.com/google-landmark/train/images_305.tar',
'https://s3.amazonaws.com/google-landmark/train/images_306.tar',
'https://s3.amazonaws.com/google-landmark/train/images_307.tar',
'https://s3.amazonaws.com/google-landmark/train/images_308.tar',
'https://s3.amazonaws.com/google-landmark/train/images_309.tar',
'https://s3.amazonaws.com/google-landmark/train/images_310.tar',
'https://s3.amazonaws.com/google-landmark/train/images_311.tar',
'https://s3.amazonaws.com/google-landmark/train/images_312.tar',
'https://s3.amazonaws.com/google-landmark/train/images_313.tar',
'https://s3.amazonaws.com/google-landmark/train/images_314.tar',
'https://s3.amazonaws.com/google-landmark/train/images_315.tar',
'https://s3.amazonaws.com/google-landmark/train/images_316.tar',
'https://s3.amazonaws.com/google-landmark/train/images_317.tar',
'https://s3.amazonaws.com/google-landmark/train/images_318.tar',
'https://s3.amazonaws.com/google-landmark/train/images_319.tar',
'https://s3.amazonaws.com/google-landmark/train/images_320.tar',
'https://s3.amazonaws.com/google-landmark/train/images_321.tar',
'https://s3.amazonaws.com/google-landmark/train/images_322.tar',
'https://s3.amazonaws.com/google-landmark/train/images_323.tar',
'https://s3.amazonaws.com/google-landmark/train/images_324.tar',
'https://s3.amazonaws.com/google-landmark/train/images_325.tar',
'https://s3.amazonaws.com/google-landmark/train/images_326.tar',
'https://s3.amazonaws.com/google-landmark/train/images_327.tar',
'https://s3.amazonaws.com/google-landmark/train/images_328.tar',
'https://s3.amazonaws.com/google-landmark/train/images_329.tar',
'https://s3.amazonaws.com/google-landmark/train/images_330.tar',
'https://s3.amazonaws.com/google-landmark/train/images_331.tar',
'https://s3.amazonaws.com/google-landmark/train/images_332.tar',
'https://s3.amazonaws.com/google-landmark/train/images_333.tar',
'https://s3.amazonaws.com/google-landmark/train/images_334.tar',
'https://s3.amazonaws.com/google-landmark/train/images_335.tar',
'https://s3.amazonaws.com/google-landmark/train/images_336.tar',
'https://s3.amazonaws.com/google-landmark/train/images_337.tar',
'https://s3.amazonaws.com/google-landmark/train/images_338.tar',
'https://s3.amazonaws.com/google-landmark/train/images_339.tar',
'https://s3.amazonaws.com/google-landmark/train/images_340.tar',
'https://s3.amazonaws.com/google-landmark/train/images_341.tar',
'https://s3.amazonaws.com/google-landmark/train/images_342.tar',
'https://s3.amazonaws.com/google-landmark/train/images_343.tar',
'https://s3.amazonaws.com/google-landmark/train/images_344.tar',
'https://s3.amazonaws.com/google-landmark/train/images_345.tar',
'https://s3.amazonaws.com/google-landmark/train/images_346.tar',
'https://s3.amazonaws.com/google-landmark/train/images_347.tar',
'https://s3.amazonaws.com/google-landmark/train/images_348.tar',
'https://s3.amazonaws.com/google-landmark/train/images_349.tar',
'https://s3.amazonaws.com/google-landmark/train/images_350.tar',
'https://s3.amazonaws.com/google-landmark/train/images_351.tar',
'https://s3.amazonaws.com/google-landmark/train/images_352.tar',
'https://s3.amazonaws.com/google-landmark/train/images_353.tar',
'https://s3.amazonaws.com/google-landmark/train/images_354.tar',
'https://s3.amazonaws.com/google-landmark/train/images_355.tar',
'https://s3.amazonaws.com/google-landmark/train/images_356.tar',
'https://s3.amazonaws.com/google-landmark/train/images_357.tar',
'https://s3.amazonaws.com/google-landmark/train/images_358.tar',
'https://s3.amazonaws.com/google-landmark/train/images_359.tar',
'https://s3.amazonaws.com/google-landmark/train/images_360.tar',
'https://s3.amazonaws.com/google-landmark/train/images_361.tar',
'https://s3.amazonaws.com/google-landmark/train/images_362.tar',
'https://s3.amazonaws.com/google-landmark/train/images_363.tar',
'https://s3.amazonaws.com/google-landmark/train/images_364.tar',
'https://s3.amazonaws.com/google-landmark/train/images_365.tar',
'https://s3.amazonaws.com/google-landmark/train/images_366.tar',
'https://s3.amazonaws.com/google-landmark/train/images_367.tar',
'https://s3.amazonaws.com/google-landmark/train/images_368.tar',
'https://s3.amazonaws.com/google-landmark/train/images_369.tar',
'https://s3.amazonaws.com/google-landmark/train/images_370.tar',
'https://s3.amazonaws.com/google-landmark/train/images_371.tar',
'https://s3.amazonaws.com/google-landmark/train/images_372.tar',
'https://s3.amazonaws.com/google-landmark/train/images_373.tar',
'https://s3.amazonaws.com/google-landmark/train/images_374.tar',
'https://s3.amazonaws.com/google-landmark/train/images_375.tar',
'https://s3.amazonaws.com/google-landmark/train/images_376.tar',
'https://s3.amazonaws.com/google-landmark/train/images_377.tar',
'https://s3.amazonaws.com/google-landmark/train/images_378.tar',
'https://s3.amazonaws.com/google-landmark/train/images_379.tar',
'https://s3.amazonaws.com/google-landmark/train/images_380.tar',
'https://s3.amazonaws.com/google-landmark/train/images_381.tar',
'https://s3.amazonaws.com/google-landmark/train/images_382.tar',
'https://s3.amazonaws.com/google-landmark/train/images_383.tar',
'https://s3.amazonaws.com/google-landmark/train/images_384.tar',
'https://s3.amazonaws.com/google-landmark/train/images_385.tar',
'https://s3.amazonaws.com/google-landmark/train/images_386.tar',
'https://s3.amazonaws.com/google-landmark/train/images_387.tar',
'https://s3.amazonaws.com/google-landmark/train/images_388.tar',
'https://s3.amazonaws.com/google-landmark/train/images_389.tar',
'https://s3.amazonaws.com/google-landmark/train/images_390.tar',
'https://s3.amazonaws.com/google-landmark/train/images_391.tar',
'https://s3.amazonaws.com/google-landmark/train/images_392.tar',
'https://s3.amazonaws.com/google-landmark/train/images_393.tar',
'https://s3.amazonaws.com/google-landmark/train/images_394.tar',
'https://s3.amazonaws.com/google-landmark/train/images_395.tar',
'https://s3.amazonaws.com/google-landmark/train/images_396.tar',
'https://s3.amazonaws.com/google-landmark/train/images_397.tar',
'https://s3.amazonaws.com/google-landmark/train/images_398.tar',
'https://s3.amazonaws.com/google-landmark/train/images_399.tar',
'https://s3.amazonaws.com/google-landmark/train/images_400.tar',
'https://s3.amazonaws.com/google-landmark/train/images_401.tar',
'https://s3.amazonaws.com/google-landmark/train/images_402.tar',
'https://s3.amazonaws.com/google-landmark/train/images_403.tar',
'https://s3.amazonaws.com/google-landmark/train/images_404.tar',
'https://s3.amazonaws.com/google-landmark/train/images_405.tar',
'https://s3.amazonaws.com/google-landmark/train/images_406.tar',
'https://s3.amazonaws.com/google-landmark/train/images_407.tar',
'https://s3.amazonaws.com/google-landmark/train/images_408.tar',
'https://s3.amazonaws.com/google-landmark/train/images_409.tar',
'https://s3.amazonaws.com/google-landmark/train/images_410.tar',
'https://s3.amazonaws.com/google-landmark/train/images_411.tar',
'https://s3.amazonaws.com/google-landmark/train/images_412.tar',
'https://s3.amazonaws.com/google-landmark/train/images_413.tar',
'https://s3.amazonaws.com/google-landmark/train/images_414.tar',
'https://s3.amazonaws.com/google-landmark/train/images_415.tar',
'https://s3.amazonaws.com/google-landmark/train/images_416.tar',
'https://s3.amazonaws.com/google-landmark/train/images_417.tar',
'https://s3.amazonaws.com/google-landmark/train/images_418.tar',
'https://s3.amazonaws.com/google-landmark/train/images_419.tar',
'https://s3.amazonaws.com/google-landmark/train/images_420.tar',
'https://s3.amazonaws.com/google-landmark/train/images_421.tar',
'https://s3.amazonaws.com/google-landmark/train/images_422.tar',
'https://s3.amazonaws.com/google-landmark/train/images_423.tar',
'https://s3.amazonaws.com/google-landmark/train/images_424.tar',
'https://s3.amazonaws.com/google-landmark/train/images_425.tar',
'https://s3.amazonaws.com/google-landmark/train/images_426.tar',
'https://s3.amazonaws.com/google-landmark/train/images_427.tar',
'https://s3.amazonaws.com/google-landmark/train/images_428.tar',
'https://s3.amazonaws.com/google-landmark/train/images_429.tar',
'https://s3.amazonaws.com/google-landmark/train/images_430.tar',
'https://s3.amazonaws.com/google-landmark/train/images_431.tar',
'https://s3.amazonaws.com/google-landmark/train/images_432.tar',
'https://s3.amazonaws.com/google-landmark/train/images_433.tar',
'https://s3.amazonaws.com/google-landmark/train/images_434.tar',
'https://s3.amazonaws.com/google-landmark/train/images_435.tar',
'https://s3.amazonaws.com/google-landmark/train/images_436.tar',
'https://s3.amazonaws.com/google-landmark/train/images_437.tar',
'https://s3.amazonaws.com/google-landmark/train/images_438.tar',
'https://s3.amazonaws.com/google-landmark/train/images_439.tar',
'https://s3.amazonaws.com/google-landmark/train/images_440.tar',
'https://s3.amazonaws.com/google-landmark/train/images_441.tar',
'https://s3.amazonaws.com/google-landmark/train/images_442.tar',
'https://s3.amazonaws.com/google-landmark/train/images_443.tar',
'https://s3.amazonaws.com/google-landmark/train/images_444.tar',
'https://s3.amazonaws.com/google-landmark/train/images_445.tar',
'https://s3.amazonaws.com/google-landmark/train/images_446.tar',
'https://s3.amazonaws.com/google-landmark/train/images_447.tar',
'https://s3.amazonaws.com/google-landmark/train/images_448.tar',
'https://s3.amazonaws.com/google-landmark/train/images_449.tar',
'https://s3.amazonaws.com/google-landmark/train/images_450.tar',
'https://s3.amazonaws.com/google-landmark/train/images_451.tar',
'https://s3.amazonaws.com/google-landmark/train/images_452.tar',
'https://s3.amazonaws.com/google-landmark/train/images_453.tar',
'https://s3.amazonaws.com/google-landmark/train/images_454.tar',
'https://s3.amazonaws.com/google-landmark/train/images_455.tar',
'https://s3.amazonaws.com/google-landmark/train/images_456.tar',
'https://s3.amazonaws.com/google-landmark/train/images_457.tar',
'https://s3.amazonaws.com/google-landmark/train/images_458.tar',
'https://s3.amazonaws.com/google-landmark/train/images_459.tar',
'https://s3.amazonaws.com/google-landmark/train/images_460.tar',
'https://s3.amazonaws.com/google-landmark/train/images_461.tar',
'https://s3.amazonaws.com/google-landmark/train/images_462.tar',
'https://s3.amazonaws.com/google-landmark/train/images_463.tar',
'https://s3.amazonaws.com/google-landmark/train/images_464.tar',
'https://s3.amazonaws.com/google-landmark/train/images_465.tar',
'https://s3.amazonaws.com/google-landmark/train/images_466.tar',
'https://s3.amazonaws.com/google-landmark/train/images_467.tar',
'https://s3.amazonaws.com/google-landmark/train/images_468.tar',
'https://s3.amazonaws.com/google-landmark/train/images_469.tar',
'https://s3.amazonaws.com/google-landmark/train/images_470.tar',
'https://s3.amazonaws.com/google-landmark/train/images_471.tar',
'https://s3.amazonaws.com/google-landmark/train/images_472.tar',
'https://s3.amazonaws.com/google-landmark/train/images_473.tar',
'https://s3.amazonaws.com/google-landmark/train/images_474.tar',
'https://s3.amazonaws.com/google-landmark/train/images_475.tar',
'https://s3.amazonaws.com/google-landmark/train/images_476.tar',
'https://s3.amazonaws.com/google-landmark/train/images_477.tar',
'https://s3.amazonaws.com/google-landmark/train/images_478.tar',
'https://s3.amazonaws.com/google-landmark/train/images_479.tar',
'https://s3.amazonaws.com/google-landmark/train/images_480.tar',
'https://s3.amazonaws.com/google-landmark/train/images_481.tar',
'https://s3.amazonaws.com/google-landmark/train/images_482.tar',
'https://s3.amazonaws.com/google-landmark/train/images_483.tar',
'https://s3.amazonaws.com/google-landmark/train/images_484.tar',
'https://s3.amazonaws.com/google-landmark/train/images_485.tar',
'https://s3.amazonaws.com/google-landmark/train/images_486.tar',
'https://s3.amazonaws.com/google-landmark/train/images_487.tar',
'https://s3.amazonaws.com/google-landmark/train/images_488.tar',
'https://s3.amazonaws.com/google-landmark/train/images_489.tar',
'https://s3.amazonaws.com/google-landmark/train/images_490.tar',
'https://s3.amazonaws.com/google-landmark/train/images_491.tar',
'https://s3.amazonaws.com/google-landmark/train/images_492.tar',
'https://s3.amazonaws.com/google-landmark/train/images_493.tar',
'https://s3.amazonaws.com/google-landmark/train/images_494.tar',
'https://s3.amazonaws.com/google-landmark/train/images_495.tar',
'https://s3.amazonaws.com/google-landmark/train/images_496.tar',
'https://s3.amazonaws.com/google-landmark/train/images_497.tar',
'https://s3.amazonaws.com/google-landmark/train/images_498.tar',
'https://s3.amazonaws.com/google-landmark/train/images_499.tar'


)


# I found the download def below on csv libriary example set - it saves things to the current working python directory - not where we want these guys!  So change the working directory to the location for the train image tar files

# In[ ]:


os.chdir(output_dir)


# The download def about contains a commented out line to remove the temp file after its copied to the final location.  It always created error for me as the line above was not finished with the file when it tried to execute.  I assume that this occurred because I was downloading on one PC and final location was on a second.  Remove the comment and try the notebook.  If you leave the comment in place than you have 500 temp files you will need to manualy delete.

# **Because I had a small hard drive for my system the script did run out of room on the hard drive for the temp files**

# I deleted them from C:\Users\james\AppData\Local\Temp\   - Python cannot be "open" for the delete to work.
# 
# 

# In[ ]:


def download(directory, url, filename):
  """Download a tar file from the train dataset if not already done. This permits you to rerun and not download already existing tar files from previous attempts."""
  filepath = os.path.join(directory, filename)
  # if the file is already present we don't want to do anything but ack its presence
  if tf.gfile.Exists(filepath):
    return filepath
  if not tf.gfile.Exists(directory):
    tf.gfile.MakeDirs(directory)

  _, zipped_filepath = tempfile.mkstemp(suffix='.tar')
  print('Downloading %s to %s' % (url, zipped_filepath))
  urllib.request.urlretrieve(url, zipped_filepath)
  tf.gfile.Copy(zipped_filepath, filepath)
    
  #os.remove(zipped_filepath)

  return filepath


# In[ ]:


for row in data_file:
        amazon_location = row
        file_name = amazon_location[-14:]
        print(amazon_location)
        print(file_name)
        download(output_dir, amazon_location, file_name)


# In[ ]:


print('Down Loading completed  ...')


# The tar files now need to be uncompressed - there is a recommendation on how to orgainze the directories.   I will be updating script later to do the uncompression in this next cell.
