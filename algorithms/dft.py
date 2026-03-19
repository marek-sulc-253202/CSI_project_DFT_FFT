from algorithms import mathfce # import implementovaných funkcí z mathfce.py

# Funkce pro výpočet DFT
def calculate_dft(x):
    N = len(x)
    X = [0.0j] * N # připravení výstupní sekvence vzorků a naplnění ji komplexními nulami

    # Algoritmus pro výpočet DFT, v podstatě SUMA v cyklech
    # Vnější cyklus (k) postupně prochází frekvence a vnitřní cyklus (n) prochází signál v čase
    # Kvůli těmto dvou vnořeným cykům to má tak vysokou výpočetní složitost
    for k in range(N):
        for n in range(N):
            X[k] += x[n] * mathfce.complex_exponential(-2 * mathfce.pi * k * n / N)
    return X