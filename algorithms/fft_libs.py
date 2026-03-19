from math import pi
from cmath import exp

# Výpočet FFT s použitím knihoven math a cmath
def calculate_fft(x):
    N = len(x)

    if N == 1: # pojištění jestliže je signál dlouhý jeden vzorek zároveň se zde ukončí rekurze
        return x
    
    # Toto už bylo provedeno v core/signal_generator.py ale tady to je pro jistotu znova,
    # cyklus zvětší počet vzorků v sekvenci, aby mohla být sekvence rozšířena nulama 
    # na nejbližší vyšší exponent dvou (kvůli rozdělování).
    pow2 = 1
    while pow2 < N:
        pow2 <<= 1 # bitový posun "1" do leva (1 -> 2 -> 4 -> 8 -> 16 -> 32 ...)

    x = x + [0.0j] * (pow2 - N) # doplnění sekvence nulama
    N = len(x) # přepočet počtu vzorků

    # Rozdělení na sudé a liché vzorky pomocí rekurze
    even = calculate_fft(x[0::2])
    odd = calculate_fft(x[1::2])

    # Inicializace výsledného pole komplexních čísel o délce N
    X = [0.0j] * N
    first_half = N // 2
    # Samotný výpočet sekvence vzorků (skládání sudých a lichých částí zpět dohromady)
    for k in range(first_half):
        # Výpočet rotačního faktoru pomocí importovaných fcí z knihoven
        factor = exp(-2j * pi * k / N)
        X[k] = even[k] + factor * odd[k] # výpočet pro první polovinu
        X[k + first_half] = even[k] - factor * odd[k] # výpočet pro druhou polovinu (díky symetrii stačí + -> -)
    
    return X