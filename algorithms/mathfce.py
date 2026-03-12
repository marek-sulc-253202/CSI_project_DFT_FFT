pi = 3.141592653589793

def faktorial(n):
    if n == 0:
        return 1
    else:
        return n * faktorial(n - 1)
    
def sin(x):
    x = x % (2 * pi)  # Normalizace do rozsahu [0, 2π]
    vysledek = 0.0
    for n in range(15):  # Počet členů v Taylorově řadě
        vysledek += ((-1)**n * x**(2*n + 1)) / faktorial(2*n + 1)
    return vysledek

def cos(x):
    x = x % (2 * pi)  # Normalizace do rozsahu [0, 2π]
    vysledek = 0.0
    for n in range(15):  # Počet členů v Taylorově řadě
        vysledek += ((-1)**n * x**(2*n)) / faktorial(2*n)
    return vysledek

def complex_exponential(x):
    return cos(x) + 1j * sin(x)