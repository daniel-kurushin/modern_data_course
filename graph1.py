import numpy as np
import matplotlib.pyplot as plt

# 1.1 Сгенерировать программно произвольный непериодический сигнал s(k)
def s(k):
    length = k.shape[0]
    randoms = np.random.random(length)
    signal = (k > randoms).astype(float)
    
    return signal

# 1.2 Добавить к полученному сигналу белый гауссовский шум
def n(k):
    length = k.shape[0]
    μ, σ = 0, 0.05
    noise = np.random.normal(μ, σ, size=length)

    return noise
    
# 1.3 Добавить к сигналу некоторое постоянное значение a=const: 
a = 0.2

k = np.linspace(-1,1,100)

# fig, ax = plt.subplots(figsize=(16, 9))
S = s(k)
# ax.plot(k, S, label='s(k)')
D = S + n(k)
# ax.plot(k, D, label='s(k)+n(k)')
F = D + a
# ax.plot(k, F, label='s(k)+n(k)+a')
# ax.set_xlabel('k')
# ax.set_ylabel('v')
# ax.set_title("Графики результирующих сигналов d(k) и f(k)")
# ax.legend();  

# plt.show()


# 2. Вычислить для сигналов f(k) и d(k) значения SNR и CV.

def signaltonoise(a, ddof=0):
    μ = a.mean()
    σ = a.std(ddof=ddof)

    return μ/σ

def coefficient_variation(a, ddof=0):
    μ = a.mean()
    σ = a.std(ddof=ddof)

    return σ/μ * 100

print(f'SNR(D) = {signaltonoise(D)}')
print(f'SNR(F) = {signaltonoise(F)}')
print(f'CV(D) = {coefficient_variation(D)}')
print(f'CV(F) = {coefficient_variation(F)}')

# 3. Применить к полученному сигналу f(k) способ скользящего среднего

def moving_average(a, n=3) :
    Σ = np.cumsum(a, dtype=float)
    Σ[n:] = Σ[n:] - Σ[:-n]
    return Σ[n - 1:] / n

fig, ax = plt.subplots(figsize=(16, 9))

for K in sorted([2, 5, 10] + list(set(np.random.randint(5,50,size=10)))):
    S = moving_average(F, n=K)
    k = np.linspace(-1, 1, len(S))
    SNR, CV = signaltonoise(S), coefficient_variation(S)
    ax.plot(k, S, label=f'Скользящее среднее, K={K}, SNR={round(SNR,2)}, CV={round(CV,2)}')

ax.set_title("Графики сигналов c различным К")
ax.legend();  

plt.show()
