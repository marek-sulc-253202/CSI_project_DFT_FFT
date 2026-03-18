# Inicializace čísla pi
pi = 3.141592653589793

# Funkce výpočtu faktoriálu s argumentem "n"
def faktorial(n):
    fakt = 1
    while n > 0: # jestliže je n=0 cyklus se ani neprovede a vrácená hodnota bude 1, 
                 # jinak se postupně bude "fakt" navyšovat násobkem snižujícího se "n" o 1
        fakt *= n
        n -= 1
    return fakt

# Funkce výpočtu sinusu
def sin(x):
    x = x % (2 * pi) # Normalizace do rozsahu [0, 2π]
    vysledek = 0.0
    for n in range(15): # 15 -> 16 počtu členů v Taylorově řadě
        vysledek += ((-1)**n * x**(2*n + 1)) / faktorial(2*n + 1)
    return vysledek # vrátí vypočítaný výsledek pomocí Taylorových řad

# Funkce výpočtu cosinu
def cos(x):
    x = x % (2 * pi) # Normalizace do rozsahu [0, 2π]
    vysledek = 0.0
    for n in range(15): # 15 -> 16 počtu členů v Taylorově řadě
        vysledek += ((-1)**n * x**(2*n)) / faktorial(2*n)
    return vysledek # vrátí vypočítaný výsledek pomocí Taylorových řad

# Funkce pro převod hodnoty "x" do komplexní roviny pomocí Eulerova vzorce
def complex_exponential(x):
    return cos(x) + 1j * sin(x)