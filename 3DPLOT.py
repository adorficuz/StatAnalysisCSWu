import auxmod as m
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from mpl_toolkits.mplot3d import Axes3D

d3d = dict()
for i in m.d.keys():
    d3d[i] = dict()
    for j in range(1940,2023):
        (d3d[i])[j] = 0
        for k in m.d[i]:
            for l in k:
                try:
                    if l['date'] == j:
                        (d3d[i])[j] += 1
                    else:
                        continue
                except KeyError:
                    continue

lx = np.array(list(d3d.keys()))
ly = np.array(list((d3d[1940].keys())))
x,y = np.meshgrid(lx,ly)

x = x.flatten()
y = y.flatten()

dz = list()

for i,xi in enumerate(x):
    dz.append((d3d[xi])[y[i]])

dz = np.array(dz)


z = dz.reshape(ly.shape[0],lx.shape[0])

plt.imshow( z , cmap = 'jet' , interpolation = 'gaussian' , origin='lower',
           aspect='equal',  extent = [min(x), max(x), min(y), max(y)] )
plt.colorbar()
plt.show()
