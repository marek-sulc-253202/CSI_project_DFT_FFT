# import cmath
import math
from mathfce import complex_exponential

def calculate_dft(x):
    N = len(x)
    X = [0.0j] * N
    for k in range(N):
        for n in range(N):
            # X[k] += x[n] * cmath.exp(-2j*math.pi*k*n/N)
            X[k] += x[n] * complex_exponential(-2 * math.pi * k * n / N)
    return X