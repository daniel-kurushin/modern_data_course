import numpy as np
import matplotlib.pyplot as plt

from math import sin

x = [ round(x / 10 + 10 * sin(x / 10),2) for x in range(314) ]

D = []
Y0 = []
for i in range(60):
    D += [np.array(x[i:i+5])]
    Y0 += [x[i+5:i+6]]

Y0 = np.array(Y0)

w = np.zeros(D[0].shape)

α = 0.000002
β = -0.4
σ = lambda x: x

def f(x):
    s = β + np.sum(x @ w)
    return σ(s)

def train():
    global w
    _w = w.copy()
    for x, y in zip(D, Y0):
        w += α * (y - f(x)) * x
    return (w != _w).any()
            
for i in range(10000):
    train()
    print(w)

T = []
for d in D:
    T += [f(d)]
    
x = np.array([ x / 10 + round(10 * sin(x / 10),2) for x in range(300, 900) ])
x += np.random.randint(-3, 3, len(x))
D = []
Y0 = []
for i in range(200):
    D += [np.array(x[i:i+5])]
    Y0 += [x[i+5:i+6]]
    
T = []
for d in D:
    T += [f(d)]
    
   
d0 = D[0]
T = []
for i in range(200):
    y = f(d0)
    T += [y]
    d0 = np.concatenate([d0[1:],[y]])
    
plt.plot(Y0, color='red')
plt.plot(T, color='blue')
plt.show()
