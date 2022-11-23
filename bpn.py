import math
import random
import numpy as np 

D = np.array([
    [0,0,0],
    [0,0,1],
    [0,1,0],
    [0,1,1],
    [1,0,0],
    [1,0,1],
    [1,1,0],
    [1,1,1],
])

Y = np.array([
    [1,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,0,0,1,0,0,0],
    [0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,1],
])

test = D

nX = D.shape[1] # Число нейронов входного слоя
nY = Y.shape[1] # Число нейронов выходного слоя
nH = 10         # Число нейронов скрытого слоя

# Функции активации

def sigmoid(x):
    return np.tanh(x)

def dsigmoid(y):
    return 1.0 - y**2

class BackPropagateNet:

    def __init__(self, ni, nh, no):

        # Число входных, скрытых и выходных нейронов
        self.ni = ni + 1 # +1 - узел смещения
        self.nh = nh
        self.no = no

        # Состояния активации нейронов
        self.ai = np.ones((self.ni))
        self.ah = np.ones((self.nh))
        self.ao = np.ones((self.no))

        # Создание матриц весов
        self.wi = np.random.random((self.ni, self.nh))
        self.wo = np.random.random((self.nh, self.no))

        # изменения весов за последний шаг
        self.ci = np.zeros((self.ni, self.nh))
        self.co = np.zeros((self.nh, self.no))
        

    def update(self, inputs):
        # активация входных нейронов сигмой
        self.ai[0:len(inputs)] = sigmoid(inputs)

        # активация нейронов скрытого слоя
        for j in range(self.nh):
            summ = 0.0
            for i in range(self.ni):
                summ = summ + self.ai[i] * self.wi[i][j]
            self.ah[j] = sigmoid(summ)

        # активация нейронов выходного слоя
        for k in range(self.no):
            summ = 0.0
            for j in range(self.nh):
                summ = summ + self.ah[j] * self.wo[j][k]
            self.ao[k] = sigmoid(summ)

        return np.copy(self.ao)


    def back_propagate(self, targets, N, M):

        # расчет ошибок для выходного слоя
        output_deltas = np.zeros((self.no))
        for k in range(self.no):
            error = targets[k]-self.ao[k]
            output_deltas[k] = dsigmoid(self.ao[k]) * error

        # расчет ошибок для скрытого слоя
        hidden_deltas = np.zeros((self.nh))
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error = error + output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = dsigmoid(self.ah[j]) * error

        # обновление весов выходного слоя
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k]*self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
                self.co[j][k] = change

        # обновление весов входного слоя
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
                self.ci[i][j] = change

        # расчет ошибки
        error = 0.0
        for k in range(len(targets)):
            error = error + 0.5*(targets[k]-self.ao[k])**2
        return error


    def test(self, X):
        for x in X:
            out = [ round(a, 2) for a in self.update(x) ]
            print(x, '->', out, '->', np.argmax(out))

    # обучение сети обратного распространения
    def train(self, D, Y, iterations=10000, N=0.5, M=0.01):
        # N: скорость обучения
        # M: фактор обновления весов
        for i in range(iterations):
            error = 0
            for x, y in zip(D, Y):
                self.update(x) 
                error = error + self.back_propagate(y, N, M)
            if i % 100 == 0: 
                print(error)


def demo():
    print(f'bpn = BackPropagateNet({nX, nH, nY})')
    bpn = BackPropagateNet(nX, nH, nY)
    bpn.train(D, Y)
    bpn.test(test)

if __name__ == '__main__':
    demo()


