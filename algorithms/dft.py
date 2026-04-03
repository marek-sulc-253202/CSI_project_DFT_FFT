from algorithms import mathfce # import implementovaných funkcí z mathfce.py

# Funkce pro výpočet DFT
def calculate_dft(x):
    N = len(x)
    X = [0.0j] * N # připravení výstupní sekvence vzorků a naplnění ji komplexními nulami

    # Spočítáme Taylorovy řady pouze N-krát, kdyby to bylo ve dvou nořených cyklech tak se to bude počítat N^2-krát.
    W = [mathfce.complex_exponential(-2 * mathfce.pi * i / N) for i in range(N)]

    # Algoritmus pro výpočet DFT, v podstatě SUMA v cyklech
    # Vnější cyklus (k) postupně prochází frekvence a vnitřní cyklus (n) prochází signál v čase
    # Kvůli těmto dvou vnořeným cykům to má tak vysokou výpočetní složitost
    for k in range(N):
        for n in range(N):
            # Pomocí periodicity úhlů vždy dostanem za pomocí modula správný index požadovaného úhlu.
            index = (k * n) % N
            X[k] += x[n] * W[index]
    return X