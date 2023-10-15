import auxmod as m
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import SymLogNorm, Normalize, LogNorm, FuncNorm
from matplotlib.ticker import MaxNLocator

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

dz = list()

for i,xi in enumerate(x.flatten()):
    dz.append((d3d[xi])[(y.flatten())[i]])

dz = np.array(dz)
z = dz.reshape(ly.shape[0],lx.shape[0])

def _forward(x):
    return (x-20)**3 - (z.min()-20)**3

def _inverse(x):
    return (x+(z.min()-20)**3)**(1/3) + 20


fig, ax = plt.subplots()
norm = FuncNorm((_forward, _inverse), vmin=z.min(), vmax=z.max())
pcm = ax.pcolormesh(x, y, z, norm=norm, cmap='jet', shading='auto')
ax.set_title('FuncNorm(x)')
plt.show()
