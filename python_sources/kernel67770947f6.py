#!/usr/bin/env python
# coding: utf-8

# In[ ]:


__import__('pandas').read_csv('../input/deepfake-detection-challenge/sample_submission.csv',converters={'label':lambda e:.5000000001}).to_csv('submission.csv',index=False)


# In[ ]:




