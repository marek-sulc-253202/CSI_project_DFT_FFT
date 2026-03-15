import math


def sig_gen(F, A):
    # Vzorkovací frekvence
    fvz = 2*max(F)
    # Perioda = 1 s
    T = 1
    # Počet vzorků
    N = int(fvz * T)

    # Vygenerování signálu
    x = []
    for n in range(N):
        time = n/fvz
        value = 0
        for i in range(F):
            value += A(i) * math.sin(2 * math.pi * F(i) * time)
            x.append(value)

    return x