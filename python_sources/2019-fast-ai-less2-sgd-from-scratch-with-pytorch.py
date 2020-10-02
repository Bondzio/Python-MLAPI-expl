#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
from fastai.basics import *
import matplotlib.pyplot as plt
import numpy as np


# ### Linear Regression problem

# In[ ]:


n = 1000


# In[ ]:


x = torch.ones(n,2)
x[:,0].uniform_(-1,1)
x[:5]


# In[ ]:


a  = tensor(3., 2.); a


# In[ ]:


y = x@a + torch.randn(n)


# In[ ]:


plt.scatter(x[:,0], y)


# In[ ]:


def mse(y_hat, y): return ((y_hat - y)**2).mean()
def mae(y_hat, y): return abs(y_hat - y).mean()

history = {'loss_mse': [], 'loss_mae': []}


# In[ ]:


a = tensor(-1., 1)


# In[ ]:


y_hat = x@a
print('Mean squared error: {:.4f}'.format(mse(y_hat, y)))
print('Mean absolute error: {:.4f}'.format(mae(y_hat, y)))


# In[ ]:


plt.plot(x[:,0], y,'o')
plt.plot(x[:,0], y_hat,'-')


# ## Gradient descent

# ### Squared loss

# In[ ]:


a = nn.Parameter(a); a


# In[ ]:


def update():
    y_hat = x@a
    loss = mse(y, y_hat)
    history['loss_mse'].append(loss)
    if t % 10 == 0: print(loss)
    loss.backward()
    with torch.no_grad():
        a.sub_(lr * a.grad)
        a.grad.zero_()


# In[ ]:


lr = 1e-1
for t in range(100): update()


# In[ ]:


fig, axes = plt.subplots(1,2)
axes[0].plot(x[:,0], y,'o')
axes[0].plot(x[:,0], x@a,'-')
axes[1].plot(history['loss_mse'])


# ### Absolute loss

# In[ ]:


b = tensor(1.,-1)
b = nn.Parameter(b);b


# In[ ]:


def update_abs():
    y_hat = x@b
    loss = mae(y, y_hat)
    history['loss_mae'].append(loss)
    if t % 10 == 0: print(loss)
    loss.backward()
    with torch.no_grad():
        b.sub_(lr * b.grad)
        b.grad.zero_()


# In[ ]:


lr = 1e-1
for t in range(100): update_abs()


# In[ ]:


fig, axes = plt.subplots(1,2, figsize=(18.5, 10.5))
axes[0].plot(x[:,0], y,'o')
axes[0].plot(x[:,0], x@a,'-', label='squared loss', color='black')
axes[0].plot(x[:,0], x@b,'-', label = 'absolute loss', color='red')
axes[0].legend()
axes[1].plot(history['loss_mse'], color='black')
axes[1].plot(history['loss_mae'], color='red')


# ## Animations

# ### Squared loss

# In[ ]:


from matplotlib import animation, rc
rc('animation', html='jshtml')


# In[ ]:


a = nn.Parameter(tensor(-1.,1))

fig = plt.figure()
plt.scatter(x[:,0],y,c='orange')
line, = plt.plot(x[:,0], x@a)
plt.close()

def animate(i):
    update()
    line.set_ydata(x@a)
    return line,

animation.FuncAnimation(fig, animate, np.arange(0, 200), interval=20)


# ### Absolute loss

# In[ ]:


b = nn.Parameter(tensor(-1.,1))

fig = plt.figure()
plt.scatter(x[:,0],y,c='orange')
line, = plt.plot(x[:,0], x@b)
plt.close()

def animate(i):
    update()
    update_abs()
    line.set_ydata(x@b)
    return line,

animation.FuncAnimation(fig, animate, np.arange(0, 200), interval=20)


# In[ ]:




