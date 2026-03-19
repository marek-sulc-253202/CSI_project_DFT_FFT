import math

def sig_gen(F, A): # argumenty jsou nastavené frekvence a amplitudy

    # Pojistka proti prázdnému vstupu, jestliže je F nebo A prázdné tak fce vrátí prázdné řetězce
    if not F or not A:
        return [], []

    # Perioda = 1 s
    T = 1.0
    # Výpočet adekvátní vzorkovací frekvence a počtu vzorků
    fs = 50 * max(F) if max(F) > 0 else 1000
    N = int(fs * T)

    # Zaokrouhlit N na další mocninu dvou, kvůli FFT (rozděluje sekvenci na poloviny)
    pow2 = 1
    while pow2 < N:
        pow2 <<= 1 # bitový posun "1" do leva (1 -> 2 -> 4 -> 8 -> 16 -> 32 ...)
    N = pow2

    # Přepočet vzorkovací frekvence a výpočet časové osy (t)
    fs = int(N / T)
    t = [n / fs for n in range(N)]

    # Vygenerování signálu
    X = [sum(A[i] * math.sin(2 * math.pi * F[i] * tn) for i in range(len(F))) for tn in t]

    # Vrácení vygenerovaného signálu X a vzorků pro časovou osu
    return X, t