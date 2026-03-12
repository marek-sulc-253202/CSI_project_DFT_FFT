import mathfce

def calculate_dft(x):
    N = len(x)
    X = [0.0j] * N
    for k in range(N):
        for n in range(N):
            X[k] += x[n] * mathfce.complex_exponential(-2 * mathfce.pi * k * n / N)
    return X