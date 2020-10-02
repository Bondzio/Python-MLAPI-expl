#!/usr/bin/env python
# coding: utf-8

# # NFL Rules Wordcloud

# In[ ]:


from wordcloud import WordCloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


# In[ ]:


egg_mask = np.array(Image.open('../input/externalnfl/egg.png'))
punter_mask = np.array(Image.open('../input/externalnfl/punter.png'))
with open('../input/externalnfl/rules_nlp.txt', 'r') as txt:
    rules = ' '.join([line for line in txt]).title()


# In[ ]:


wc = WordCloud(background_color='white', max_words=2000, mask=egg_mask)
wc.generate(rules)
wc.to_file('ball_rule_word_cloud.png')
wc.to_image()


# In[ ]:


wc = WordCloud(background_color='white', max_words=2000, mask=punter_mask)
wc.generate(rules)
wc.to_file('punter_rule_word_cloud.png')
wc.to_image()

