#!/usr/bin/env python
# coding: utf-8

# Credits to **Hans Rosling**

# In[ ]:


import plotly_express as px


# In[ ]:


px.scatter(px.data.gapminder(), x = "gdpPercap", y = "lifeExp", animation_frame = "year", animation_group = "country",
          size = "pop", color = "country", log_x = True, size_max = 45,
          range_x = [100, 100000], range_y = [25, 90])


# In[ ]:




