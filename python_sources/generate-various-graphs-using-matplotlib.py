#!/usr/bin/env python
# coding: utf-8

# # Various graphs using Matplotlib library:
# - Line; scatter; Bubble; Bar (Horizontal and Vertical); Stacked bar plot
# - Histogram; Pie; Stem; Lolipop; Area
# - Mixed plot; smooth plot; contour plot; Image plot
# - Editing property of Plots
# - Draw Horizontal or Vertical Line in plot
# - Write some text in middle of plot
# - Subplotting and resizing plot size
# - 3D plot
# - Dual axis plot
# 
# 

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ###### Lets have some X-axis value and random values for Y-axis

# In[ ]:


x = np.linspace(1,100,100,dtype="int8")
y1 = np.random.randint(1,100,100)
y2 = np.random.randint(1,100,100)


# ## Line plot

# In[ ]:


plt.figure(figsize=(16,4))
plt.plot(x,y1)


# ## Scatter plot

# In[ ]:


plt.figure(figsize=(16,4))
plt.scatter(x,y1,alpha=.7,color="red") # alpha is for transparency


# ## Bubble plot

# In[ ]:


plt.figure(figsize=(16,4))
for idx in range(len(x)):
    plt.scatter(x[idx],y1[idx],alpha=.2,color="red",s=.08*np.pi*y1[idx]**2) # s = size


# ## Bar plot (Default is vertical plot)

# In[ ]:


plt.figure(figsize=(16,4))
plt.bar(x[:10],y1[:10],width=.7,color="red")


# ## Bar-Horizontal plot

# In[ ]:


plt.figure(figsize=(16,4))
plt.barh(x[:10],y1[:10],color="orange")


# ## Stacked Bar plot

# In[ ]:


y3 = np.random.randint(1,100,100)
plt.figure(figsize=(16,4))
plt.bar(x[:20],y1[:20],width=.8)
plt.bar(x[:20],y2[:20],width=.8,bottom=y1[:20])
plt.bar(x[:20],y3[:20],width=.8,bottom=y1[:20]+y2[:20])


# ## Stacked Bar plot with labels

# In[ ]:


y3 = np.random.randint(1,100,100)
plt.figure(figsize=(16,4))
for id in range(len(x[:20])):    
    plt.bar(x[:20][id],y1[:20][id],width=.8)
    plt.text(x[:20][id],y1[:20][id],y1[:20][id])
    
    plt.bar(x[:20][id],y2[:20][id],width=.8,bottom=y1[:20][id])
    plt.text(x[:20][id],y1[:20][id]+y2[:20][id],y2[:20][id])
    
    plt.bar(x[:20][id],y3[:20][id],width=.8,bottom=y1[:20][id]+y2[:20][id])
    plt.text(x[:20][id],y1[:20][id]+y2[:20][id]+y3[:20][id],y3[:20][id])
plt.xticks(range(1,21)) # fix the x-axis values
plt.yticks(range(1,300,25)) # fix the y-axis values
plt.show()


# ## Histogram

# In[ ]:


plt.figure(figsize=(16,4))
plt.hist(y1,rwidth=.9,bins=10,color="blue",align="mid")


# ## Pie

# In[ ]:


plt.figure(figsize=(5,5))
y = [5,7,3,8,3,9,3,1]
plt.pie(y,shadow=True,labels=y,labeldistance=.8,center=(1,2),explode=[0,0,0,.1,0,0,.1,0])
plt.show()


# ## Stem

# In[ ]:


plt.figure(figsize=(16,4))
plt.stem(x,y1)


# ## Lolipop

# In[ ]:


plt.figure(figsize=(16,4))
plt.figure(figsize=(16,4))
for idx in range(len(x)):
    plt.scatter(x[idx],y1[idx],alpha=.8,color="green",s=.03*np.pi*y1[idx]**2)
plt.bar(x,y1,width=.2,alpha=.2) # Change the width of bar to make lolipop graph


# ## Area plot

# In[ ]:


plt.figure(figsize=(16,4))
plt.fill_between(x,y1)
plt.show()


# ## Mixed plot

# In[ ]:


plt.figure(figsize=(16,4))
plt.scatter(x,y1)
plt.plot(x,y1)
plt.stem(x,y1)
plt.show()


# ## Smooth Plot

# In[ ]:


from scipy.interpolate import spline # Required for smooth plot
plt.figure(figsize=(16,4))

xnew = np.linspace(x.min(),x.max(),600)
power_smooth = spline(x,y1,xnew)
plt.plot(x,y1,label="Original")
plt.plot(xnew,power_smooth,label="Smooth")
plt.legend()
plt.show()


# ## Contour Plot

# In[ ]:


plt.figure(figsize=(16,4))
delta = 0.025

def f(x, y):
    return np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

x1 = np.arange(-3.0, 3.0, delta)
y1 = np.arange(-2.0, 2.0, delta)
X,Y = np.meshgrid(x1,y1)
Z = f(X,Y)
CS = plt.contour(X, Y, Z,color="black")
plt.clabel(CS, inline=1, fontsize=10)
# CS = plt.contourf(x1,x2,Z) # to fill the area
# plt.clabel(CS, inline=1, fontsize=10)
plt.colorbar()


# 
# ## Image Plot (Can be used for HeatMap)

# In[ ]:


plt.figure(figsize=(16,4))
im = np.random.randint(1,100,64).reshape(4,16)
y_axis = [0,1,2,3]
plt.yticks([0,1,2,3])
plt.imshow(im)
for i in range(4):
#     print(im[i])
    for j in range(16):
        if im[i][j]>60:
            plt.text(j,i,im[i][j],color="red")
        else:
            plt.text(j,i,im[i][j],color="yellow")
plt.colorbar()
plt.xticks(range(0,16))
plt.show()


# # Editing property of Plots

# In[ ]:


plt.figure(figsize=(16,4))
x = np.linspace(1,100,100,dtype="int8")
t1 = np.random.randint(1,100,100)

for idx in range(len(x)):
    if t1[idx] >70:
        plt.scatter(x[idx],t1[idx],alpha=.2,color="red",s=.03*np.pi*t1[idx]**2)
    elif t1[idx] <70 and t1[idx] >50 :
        plt.scatter(x[idx],t1[idx],alpha=.2,color="blue",s=.03*np.pi*t1[idx]**2,marker="^")
    elif t1[idx] <50 and t1[idx] >30 :
        plt.scatter(x[idx],t1[idx],alpha=.6,color="orange",s=.03*np.pi*t1[idx]**2,marker="v")
    else:
        plt.scatter(x[idx],t1[idx],alpha=.9,color="cyan",s=.03*np.pi*t1[idx]**2,marker="*")
    plt.text(x[idx],t1[idx],t1[idx])
plt.xlabel("X-Axis")
plt.ylabel("Y-Axis")
plt.xticks(range(0,len(t1),2))
plt.yticks(range(0,max(t1),5))
plt.title("Scatter Plot")
plt.show()


# ## Draw Horizontal or vertical line in plot

# In[ ]:


plt.figure(figsize=(16,4))
x = np.linspace(1,100,100,dtype="int8")
t1 = np.random.randint(1,100,100)
plt.plot(x,t1)
plt.axhline(40,linewidth=4,color="red")
plt.axvline(40,linewidth=12,color="orange",alpha=.4)
plt.text(40,95,"This is Vertical Line")

# another way to add text
plt.annotate('This is Horizontal Line', xy=(15, 40), xytext=(20, 85),arrowprops=dict(facecolor='black', shrink=-0.02))
plt.annotate('This is Vertical Line', xy=(40, 60), xytext=(35, 85),arrowprops=dict(facecolor='green', shrink=-0.02))

plt.show()


# ## Subplot and resizing

# In[ ]:


plt.figure(figsize=(16,4))
x = np.linspace(1,100,100,dtype="int8")
t1 = np.random.randint(1,100,100)
t2 = np.random.randint(1,100,100)
t3 = np.random.randint(1,100,100)
t4 = np.random.randint(1,100,100)
t5 = np.random.randint(1,100,100)
t6 = np.random.randint(1,100,100)
t7 = np.random.randint(1,100,100)
t8 = np.random.randint(1,100,100)
t9 = np.random.randint(1,100,100)
plt.subplot(3,3,1)
plt.plot(x,t1)
plt.subplot(3,3,2)
plt.scatter(x,t2)
plt.subplot(3,3,3)
plt.bar(x,t3)
plt.subplot(3,3,4)
plt.hist(t4)
plt.subplot(3,3,5)
plt.pie(t5)
plt.subplot(3,3,6)
plt.barh(x,t6)
plt.subplot(3,3,7)
plt.stem(x,t7)
plt.subplot(3,3,8)
plt.scatter(x,t8,marker="*",color="red")
plt.subplot(3,3,9)
plt.plot(x,t9,"^b")
plt.plot(x,t9,color="orange")
plt.show()


# ## Subplot with shared X- axis

# In[ ]:


plt.figure(figsize=(16,4))
x = np.linspace(1,100,100,dtype="int8")
t1 = np.random.randint(1,100,100)
t2 = np.random.randint(1,100,100)
t3 = np.random.randint(1,100,100)
t4 = np.random.randint(1,100,100)
f,ax_arr=plt.subplots(2,2,sharex=True)
ax_arr[0][0].plot(x,t1)
ax_arr[0][1].scatter(x,t2)
ax_arr[1][0].bar(x,t3)
ax_arr[1][1].hist(t4)
plt.show()


# ## Subplot with shared Y- axis and X- axis

# In[ ]:


plt.figure(figsize=(16,4))
x = np.linspace(1,100,100,dtype="int8")
t1 = np.random.randint(1,100,100)
t2 = np.random.randint(1,100,100)
t3 = np.random.randint(1,100,100)
t4 = np.random.randint(1,100,100)
f,ax_arr=plt.subplots(2,2,sharey=True,sharex=True)
ax_arr[0][0].plot(x,t1)
ax_arr[0][1].scatter(x,t2)
ax_arr[1][0].bar(x,t3)
ax_arr[1][1].hist(t4)
plt.show()


# # 3D plot

# In[ ]:


from mpl_toolkits.mplot3d import Axes3D


# In[ ]:


# %matplotlib notebook
# plt.figure(figsize=(10,6))
x = np.linspace(1,100,100,dtype="int8")
xs = np.random.randint(1,100,100)
ys = np.random.randint(1,100,100)
zs = xs**2/ys**.2
# ax = fig.add_subplot(111, projection='3d')
ax = plt.subplot(1,1,1, projection='3d')
ax.scatter(xs, ys, zs,s=80,alpha=.5)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()


# ## Dual axis plot

# In[ ]:


plt.figure(figsize=(16,4))
x = np.linspace(1,100,100,dtype="int8")
t1 = np.random.randint(1,100,100)
t2 = np.random.randint(1,100,100)
plt.plot(x,t1,label="1st-Y-axis-data")
plt.plot(x,t2,"--r",label="2nd-Y-axis-data")
plt.legend(loc=2) # Location 0 to 10 can be used
plt.twinx()
plt.show()

