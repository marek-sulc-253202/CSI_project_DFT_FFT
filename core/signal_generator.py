import math


def sig_gen(F, A):

    # Pojistka proti prázdnému vstupu
    if not F or not A:
        return [], []

    # Perioda = 1 s
    T = 1.0
    # Počet vzorků
    fvz = 100 * max(F) if max(F) > 0 else 1000
    N = int(fvz * T)

    # Zaokrouhlit N na další mocninu dvou, kvůli FFT 
    pow2 = 1
    while pow2 < N:
        pow2 <<= 1
    N = pow2

    # Vzorkovací frekvence a časová osa
    fs = int(N / T)
    t = [n / fs for n in range(N)]

    # Vygenerování signálu
    X = [sum(A[i] * math.sin(2 * math.pi * F[i] * tn) for i in range(len(F))) for tn in t]


    return X, t