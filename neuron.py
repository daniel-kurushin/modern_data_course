import numpy as np

w = np.zeros((3))

D = np.array([
    [0,0,0],
    [0,0,1],
    [0,1,0],
    [1,0,0],
    [0,1,1],
])

Y0 = np.array([0,1,0,0,1])

α = 0.2
β = -0.4
σ = lambda x: 1 if x > 0 else 0

def f(x):
    s = β + np.sum(x @ w)
    return σ(s)

def train():
    global w
    _w = w.copy()
    for x, y in zip(D, Y0):
        w += α * (y - f(x)) * x
    return (w != _w).any()
            
while train():
    print(w)

print(f([1,1,1]))
print(f([1,1,0]))
