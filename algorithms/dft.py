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

# def calculate_dft_c(x):
#     N = len(x)

#     # Rozdělení pole vzorků na imaginární a reálnou část
#     in_r = [val.real for val in x]
#     in_i = [val.imag for val in x]

#     # Připravení C datového typu
#     CArray = ctypes.c_double * N

#     # 2. Vstupy - tady pořád musíme data do C-pole překopírovat z in_r a in_i
#     c_in_r = CArray(*in_r)
#     c_in_i = CArray(*in_i)

#     # 3. VÝSTUPY - TVŮJ TRIK!
#     # Tady jen zavoláme CArray(), což v paměti vytvoří prázdný blok pro N čísel.
#     # Nepředáváme do toho žádný pythonní list, takže se nic nekopíruje!
#     c_out_r = CArray()
#     c_out_i = CArray()

#     # 4. Volání C funkce (Céčko si ta prázdná pole přes memset vynuluje a pak naplní)
#     c_lib.calculate_dft_c(N, c_in_r, c_in_i, c_out_r, c_out_i)

#     # 5. Zpětné složení do Pythonu
#     return [complex(c_out_r[k], c_out_i[k]) for k in range(N)]