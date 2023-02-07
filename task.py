# 1) Используя numpy и matplotlib создать серию 
#    изображений с графиками функций.

import numpy as np
import matplotlib.pyplot as plt

# Берем Х
x = np.linspace(-1,1,100)

# Список функций
funcs = [ lambda x: x**2, lambda x: x**3 ]
# Список текстовых описаний
names = ['y = x²','y = x³']
for f, title in zip(funcs, names):
    plt.figure()
    plt.plot(x, f(x))
    plt.title(title) 
    plt.savefig(f'graph-{title}.png')
    plt.close()    













