import numpy as np
import pandas as pd

boats = pd.ExcelFile("boats.xlsx")
boat_prices = boats.parse('Лист1')

D = np.hstack((boat_prices.values[:,1:5], 
               boat_prices.values[:,6:7]) ).astype(np.int32)
Y = boat_prices.values[:,5:6].astype(np.int32).flatten()

w0 = np.zeros((len(D[0])))
w1 = np.zeros_like(w0)
w2 = np.zeros_like(w0)
w3 = np.zeros_like(w0)
w4 = np.zeros_like(w0)
w5 = np.zeros_like(w0)
w6 = np.zeros_like(w0)
w7 = np.zeros_like(w0)
w8 = np.zeros_like(w0)

Y0 = np.zeros_like(Y)
Y1 = np.zeros_like(Y)
Y2 = np.zeros_like(Y)
Y3 = np.zeros_like(Y)
Y4 = np.zeros_like(Y)
Y5 = np.zeros_like(Y)
Y6 = np.zeros_like(Y)
Y7 = np.zeros_like(Y)
Y8 = np.zeros_like(Y)

Y0[np.where(Y==  5)] = 1
Y1[np.where(Y== 10)] = 1
Y2[np.where(Y== 15)] = 1
Y3[np.where(Y== 30)] = 1
Y4[np.where(Y== 50)] = 1
Y5[np.where(Y== 70)] = 1
Y6[np.where(Y==100)] = 1
Y7[np.where(Y==140)] = 1
Y8[np.where(Y==150)] = 1

for y in [Y0, Y1, Y2, Y3, Y4, Y5, Y6, Y7, Y8]:
    print(y)

α =  0.2 
β = -0.4 
σ = lambda x: 1 if x > 0 else 0

def f(x, _w):
    s = β + np.sum(x @ _w)
    return σ(s)

def train(w, D, Y):
    _w = w.copy()
    for x, y in zip(D, Y):
        w += α * (y - f(x, w)) * x
    return (w != _w).any()

while train(w0, D, Y0) and \
      train(w1, D, Y1) and \
      train(w2, D, Y2) and \
      train(w3, D, Y3) and \
      train(w4, D, Y4) and \
      train(w5, D, Y5) and \
      train(w6, D, Y6) and \
      train(w7, D, Y7) and \
      train(w8, D, Y8):
    print([ round(x) for x in w1 ])


for x in D:
    print(x, end=' > ')
    for w in [w0,w1,w2,w3,w4,w5,w6,w7,w8]:
        print(f(x,w), end=', ')
    print()
