#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
submissionCSV = pd.read_csv('../input/sample_submission.csv',converters={'EncodedPixels': lambda e: ' '})
submissionCSV.to_csv('submission.csv', index=False)

