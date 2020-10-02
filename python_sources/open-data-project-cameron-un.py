#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv('../input/meteorite-landings.csv')
valids = data.groupby('nametype').get_group('Valid').copy()
v_fell = valids.groupby('fall').get_group('Fell')
      
fig = plt.figure(num=None, figsize=(36, 16) )
map = Basemap(projection='cyl')
map.drawmapboundary(fill_color='w')
map.drawcoastlines(linewidth=0.5)
map.drawmeridians(range(0, 360, 20),linewidth=0.1)
map.drawparallels([-66.56083,-23.5,0.0,23.5,66.56083], linewidth=0.5)
x, y = map(valids.reclong,valids.reclat)
map.scatter(x, y, marker='x',alpha=0.25,c='red')
plt.title('Global Meteorite Landings Since 2016', fontsize=30)

fig1 = plt.figure(num=None, figsize=(36, 30) )
map = Basemap(projection='cyl',llcrnrlon=112, llcrnrlat=-44., urcrnrlon=154, urcrnrlat=-7,resolution='c')
map.drawmapboundary(fill_color='w')
map.drawcoastlines(linewidth=0.6)
map.drawcountries()
map.drawstates()
h = plt.hist2d(valids.reclong,valids.reclat,bins=(np.arange(112,155,1.0),np.arange(-44,-8,1)))
map.scatter(valids.reclong,valids.reclat,marker='x', alpha=0.5, color='red')
plt.title("Australia's Meteorite Landings", fontsize=30)
sydlat = -33.86785; sydlon = 151.20732
x, y = map(sydlon,sydlat)
syd = plt.plot(x,y,'wo')
plt.setp(syd,'markersize',25.,'markeredgecolor','k')
x, y = map(sydlon,sydlat)
plt.text(x, y, 'Sydney',fontsize=24,fontweight='bold',color='k')

fig2 = plt.figure(num=None, figsize=(36, 16) )
h = plt.hist2d(valids.reclong,valids.reclat,bins=(np.arange(-180,182,2),np.arange(-90,92,2)))
X,Y = np.meshgrid(h[1][:-1]+1.0,h[2][:-1]+1.0)
map = Basemap(projection='cyl')
map.drawmapboundary(fill_color='w')
map.drawcoastlines(linewidth=0.6)
map.drawmeridians(range(0, 360, 20),linewidth=0.1)
map.drawparallels([-66.56083,-23.5,0.0,23.5,66.56083], linewidth=0.6)
data_interp, x, y = map.transform_scalar(np.log10(h[0].T+0.1), X[0], Y[:,0], 360, 360, returnxy=True)
map.pcolormesh(x, y, data_interp,cmap='hot_r')
plt.title('Global Heatmap of Meteorite Impacts', fontsize=30)
map.colorbar()
plt.clim(0, 3)

fig3 = plt.figure(num=None, figsize=(36, 16) )
h = plt.hist2d(v_fell.reclong,v_fell.reclat,bins=(np.arange(-180,182,2),np.arange(-90,92,2)))
X,Y = np.meshgrid(h[1][:-1]+1.0,h[2][:-1]+1.0)
map = Basemap(projection='cyl')
map.drawmapboundary(fill_color='w')
map.drawcoastlines(linewidth=0.6)
map.drawmeridians(range(0, 360, 20),linewidth=0.1)
map.drawparallels([-66.56083,-23.5,0.0,23.5,66.56083], linewidth=0.6)
data_interp, x, y = map.transform_scalar(np.log10(h[0].T+0.1), X[0], Y[:,0], 360, 360, returnxy=True)
map.pcolormesh(x, y, data_interp,cmap='hot_r')
map.colorbar()
plt.clim(0, 1)
plt.title('Global Heatmap of Meteorites Seen Falling', fontsize=30)

fig4 = plt.figure(figsize=(60, 80), edgecolor='w')
m = Basemap(projection='merc', resolution=None)
m.bluemarble(scale=0.7)
plt.title('The Blue Marble Map', fontsize=30)

