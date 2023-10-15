import auxmod as m
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
d1 = list()
for i in m.d.keys():
    try:
        for j in m.d[i]:
            d1 += j
    except IndexError:
        continue
Dated = dict()
NoDated = list()
n = -1
nums = list()
for i in d1:
    n += 1
    if len(list(i.keys())) == 2:
        NoDated.append(i)
        nums.append(n)
    else:
        continue

for j in range(0,len(nums)):
    d1.pop(nums[j] - j)

for i in range(1940,2023):
    Dated[i] = 0
    for j in d1:
        if j['date'] == i:
            Dated[i] += 1
        else:
            continue

"""
def weib(x,w1,a1,b1,c1,d1,xo1,w2,a2,b2,c2,d2,xo2):
    return np.piecewise(x,[x <= xo1 , x > xo2], [lambda x: 0, lambda x:(w1*((((x-xo1)/a1)**b1)*np.exp(-((x-xo1)/c1)**d1)) + w2*((((x-xo2)/a2)**b2)*np.exp(-((x-xo2)/c2)**d2))), lambda x:(w1*((((x-xo1)/a1)**b1)*np.exp(-((x-xo1)/c1)**d1)))])
"""
"""
def weib1(x,w1,a1,b1,c1,d1,xo1):
    return np.piecewise(x,[x <= xo1], [lambda x: 0, lambda x:w1*((((x-xo1)/a1)**b1)*np.exp(-((x-xo1)/c1)**d1))])

"""

def weib(x,w1,k1,l1,o1,w2,k2,l2,o2):
    return np.piecewise(x, [x <= o1, x > o2], [lambda x: 0, lambda x: (w1 * (k1/l1) * ((((x - o1) / l1) ** (k1-1)) * np.exp(-((x - o1) / l1) ** k1)) + w2 * (k2/l2)*((((x - o2) / l2) ** (k2-1)) * np.exp(-((x - o2) / l2) ** k2))), lambda x: (w1 * (k1/l1) *((((x - o1) / l1) ** (k1-1)) * np.exp(-((x - o1) / l1) ** k1)))])

def weib1(x,w1,k1,l1,xo1):
    return np.piecewise(x,[x <= xo1], [lambda x: 0, lambda x:w1*(k1/l1)*((((x-xo1)/l1)**(k1-1))*np.exp(-((x-xo1)/l1)**k1))])

mathematicadata = '{'
for i in range(1940,2023):
    mathematicadata += '{'
    mathematicadata += f'{i},'
    mathematicadata += f'{Dated[i]}'
    mathematicadata += '} ,'

mathematicadata += '}'

po = [3800,1.97,27,1940,1000,4,20,2000]


popt,pcov = curve_fit(weib, list(Dated.keys()), list(Dated.values()),p0=po,maxfev=100000)

popt1 = np.zeros(4)
popt2 = np.zeros(4)
for i in range(0,4):
    popt1[i] = popt[i]
    popt2[i] = popt[4+i]


for j in range(2023,2051):
    Dated[j] = 0

Pred = dict()

for i in range(1940,2023):
    Pred[i] = 0

for i in range(2023,2051):
    Pred[i] = weib(i,*popt)

myline = np.linspace(1940,2051,1000)
histo = plt.bar(list(Dated.keys()),list(Dated.values()),width=1,color='blue',label='citas anuales')
histo1 = plt.bar(list(Pred.keys()),list(Pred.values()),width=1,color='green',label='predicción local')
plt.plot(myline,weib(myline,*popt),color='red')

plt.plot(myline,weib1(myline,*popt1),'k--')
plt.plot(myline,weib1(myline,*popt2),'k--')

paperdates = dict()
for i in range(1940,1990):
    paperdates[i] = 10* m.paperdates[i]

histo2 = plt.bar(list(paperdates.keys()),list(paperdates.values()),width=1,color='red',alpha=0.3,label='10*publicaciones anuales')
plt.legend()
plt.show()