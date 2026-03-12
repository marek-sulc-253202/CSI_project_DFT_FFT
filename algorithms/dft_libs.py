from math import pi
from cmath import exp

def calculate_dft(x):
    N = len(x)
    X = [0.0j] * N
    for k in range(N):
        for n in range(N):
            X[k] += x[n] * exp(-2j * pi * k * n / N)
    return X