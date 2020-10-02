#!/usr/bin/env python
# coding: utf-8

# # Activation Functions

# In[21]:


import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[22]:


x = np.arange(-5, 5, 0.01)


# In[23]:


def plot(func, yaxis=(-1.4, 1.4)):
    plt.ylim(yaxis)
    plt.locator_params(nbins=5)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.axhline(lw=1, c='black')
    plt.axvline(lw=1, c='black')
    plt.grid(alpha=0.4, ls='-.')
    plt.box(on=None)
    plt.plot(x, func(x), c='r', lw=3)


# ## Binary Step

# $$
# f(x) = \left\{
#         \begin{array}{lll}
#             0 & for & x \leq 0  \\
#             1 & for & x > 0
#         \end{array}
#     \right.
# $$

# $$
# f'(x) = \left\{
#         \begin{array}{lll}
#             0 & for & x \neq 0  \\
#             ? & for & x = 0
#         \end{array}
#     \right.
# $$

# In[24]:


binary_step = np.vectorize(lambda x: 1 if x > 0 else 0, otypes=[np.float])


# In[25]:


plot(binary_step, yaxis=(-0.4, 1.4))


# ## Piecewise Linear

# $$
# f(x) = \left\{
#         \begin{array}{lll}
#             0 & for & x < x_{min} \\
#             mx+b & for & x_{min} \leq x \leq x_{max}  \\
#             1 & for & x > x_{max}
#         \end{array}
#     \right.
# $$

# $$
# f'(x) = \left\{
#         \begin{array}{lll}
#             0 & for & x < x_{min} \\
#             m & for & x_{min} \leq x \leq x_{max}  \\
#             0 & for & x > x_{max}
#         \end{array}
#     \right.
# $$

# In[26]:


piecewise_linear = np.vectorize(lambda x: 1 if x > 3 else 0 if x < -3 else 1/6*x+1/2, otypes=[np.float])


# In[27]:


plot(piecewise_linear, yaxis=(-0.4, 1.4))


# ## Bipolar

# $$
# f(x) = \left\{
#         \begin{array}{lll}
#             -1 & for & x \leq 0  \\
#             1 & for & x > 0
#         \end{array}
#     \right.
# $$

# $$
# f'(x) = \left\{
#         \begin{array}{lll}
#             0 & for & x \neq 0  \\
#             ? & for & x = 0
#         \end{array}
#     \right.
# $$

# In[28]:


bipolar = np.vectorize(lambda x: 1 if x > 0 else -1, otypes=[np.float])


# In[29]:


plot(bipolar)


# ## Sigmoid

# $$
# f(x)={\frac {1}{1+e^{-x}}}
# $$

# $$
# f'(x)=f(x)(1-f(x))
# $$

# In[30]:


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# In[31]:


plot(sigmoid, yaxis=(-0.4, 1.4))


# ## Bipolar Sigmoid

# $$
# f(x)={\frac {1-e^{-x}}{1+e^{-x}}}
# $$

# $$
# f'(x)={\frac {2e^x}{(e^x+1)^2}}
# $$

# In[32]:


def bipolar_sigmoid(x):
    return (1 - np.exp(-x)) / (1 + np.exp(-x))


# In[33]:


plot(bipolar_sigmoid)


# ## Hyperbolic Tangent, TanH

# $$
# f(x)={\frac {2}{1+e^{-2x}}}-1
# $$

# $$
# f'(x)=1-f(x)^2
# $$

# In[34]:


def tanh(x):
    return 2 / (1 + np.exp(-2 * x)) -1


# In[35]:


plot(tanh)


# ## Arctangent, ArcTan

# $$
# f(x)=tan^{-1}(x)
# $$

# $$
# f'(x)={\frac {1}{1+x^2}}
# $$

# In[36]:


def arctan(x):
    return np.arctan(x)


# In[37]:


plot(arctan)


# ## Rectified Linear Units, ReLU

# $$
# f(x) = \left\{
#         \begin{array}{lll}
#             0 & for & x \leq 0  \\
#             x & for & x > 0
#         \end{array}
#     \right.
# $$

# $$
# f'(x) = \left\{
#         \begin{array}{lll}
#             0 & for & x \leq 0  \\
#             1 & for & x > 0
#         \end{array}
#     \right.
# $$

# In[38]:


relu = np.vectorize(lambda x: x if x > 0 else 0, otypes=[np.float])


# In[39]:


plot(relu, yaxis=(-0.4, 1.4))


# ## Leaky Rectified Linear Units, Leaky ReLU

# $$
# f(x) = \left\{
#         \begin{array}{lll}
#             ax & for & x \leq 0  \\
#             x & for & x > 0
#         \end{array}
#     \right.
# $$

# $$
# f'(x) = \left\{
#         \begin{array}{lll}
#             a & for & x \leq 0  \\
#             1 & for & x > 0
#         \end{array}
#     \right.
# $$

# In[40]:


leaky_relu = np.vectorize(lambda x: max(0.1 * x, x), otypes=[np.float])


# In[41]:


plot(leaky_relu)


# Parametric ReLU is similar to Leaky ReLU but coefficient of leakage is learned as parameter of neural network

# ## Exponential Linear Units, ELU

# $$
# f(x) = \left\{
#         \begin{array}{lll}
#             a(e^x-1) & for & x \leq 0  \\
#             x & for & x > 0
#         \end{array}
#     \right.
# $$

# $$
# f'(x) = \left\{
#         \begin{array}{lll}
#             f(x)+a & for & x \leq 0  \\
#             1 & for & x > 0
#         \end{array}
#     \right.
# $$

# In[42]:


elu = np.vectorize(lambda x: x if x > 0 else 0.5 * (np.exp(x) - 1), otypes=[np.float])


# In[43]:


plot(elu)


# ## SoftPlus

# $$
# f(x)=ln(1+e^x)
# $$

# $$
# f'(x)={\frac {1}{1+e^{-x}}}
# $$

# In[44]:


def softplus(x):
    return np.log(1+np.exp(x))


# In[45]:


plot(softplus, yaxis=(-0.4, 1.4))

