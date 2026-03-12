from math import pi
from cmath import exp

def calculate_fft(x):
    N = len(x)

    if N == 1:
        return x
    
    expOfTwo = 1
    while expOfTwo < N:
        expOfTwo *= 2

    if expOfTwo > N:
        x = x + [0.0j] * (expOfTwo - N)
        N = len(x)

    even = calculate_fft(x[0::2])
    odd = calculate_fft(x[1::2])

    X = [0.0j] * N
    first_half = N // 2
    for k in range(first_half):
        factor = exp(-2j * pi * k / N)
        X[k] = even[k] + factor * odd[k]
        X[k + first_half] = even[k] - factor * odd[k]
    
    return X