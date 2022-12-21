import numpy as np
import matplotlib.pyplot as plt

# 2.1 Сгенерировать программно произвольный периодический сигнал s(k)
def s(k, f=5):
    signal = np.sin(f*k)
    
    return signal

# 2.2 Добавить к полученному сигналу белый гауссовский шум
def n(k):
    length = k.shape[0]
    μ, σ = 0, 0.1
    noise = np.random.normal(μ, σ, size=length)

    return noise
    
k = np.linspace(-np.pi,np.pi,100)

# fig, ax = plt.subplots(figsize=(16, 9))
S = s(k)
# ax.plot(k, S, label='s(k)')
F = S + n(k)
# ax.plot(k, F, label='s(k)+n(k)')
# ax.set_xlabel('k')
# ax.set_ylabel('v')
# ax.set_title("Графики результирующих сигналов d(k) и f(k)")
# ax.legend();  

# plt.show()

# 5.1 Применить метод синхронной фильтрации
def sync_filter(a, period=20):
    b = np.zeros_like(a)
    for i, j in zip(np.arange(len(b)), np.arange(len(b)-1,0,-1)):
        b[j] = -np.mean(a[i::period])
#       Очередное значение величины сигнала
#       есть среднее значение всех известных
#       величин сигнала в этой же фазе
#       Т.к. сигнал представлен массивом,
#       идем от конца к началу.
    return b

period = 20
# k = np.linspace(-np.pi,np.pi,100)
# Т.к. мы имеем 100 значений k в диапазоне [-π, π]
# а частота равна 5, то на этом интервале мы имеем
# 5 периодов, т.е. длина периода - 100/5 = 20

fig, ax = plt.subplots(figsize=(16, 9))
ax.plot(k[0:period], S[0:period], label='s(k)')
ax.plot(k[0:period], F[0:period], label='s(k)+n(k)')
ax.plot(k[0:period], sync_filter(F)[0:20], label='Sync filter')
ax.set_xlabel('k')
ax.set_ylabel('v')
ax.set_title("Синхронная фильтрация")
ax.legend();  

plt.show()


