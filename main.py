import matplotlib.pyplot as plt
import math
import numpy as np
import time  # Nová knihovna pro měření času!

# Importujeme obě naše funkce ze souboru dft.py
from dft import calculate_dft
from fft import calculate_fft

def main():
    print("Generuji delší signál pro testování rychlosti...")
    
    # 1. Nastavení parametrů (Zvětšili jsme N na 1024, což je přesně mocnina 2)
    vzorkovaci_frekvence = 1024  
    doba_trvani = 1.0           
    N = int(vzorkovaci_frekvence * doba_trvani)
    f1, f2, f3 = 5, 15, 30 

    # 2. Vygenerování složeného signálu
    x = []
    for n in range(N):
        cas = n / vzorkovaci_frekvence
        hodnota = (math.sin(2 * math.pi * f1 * cas) + 
                   math.sin(2 * math.pi * f2 * cas) + 
                   math.sin(2 * math.pi * f3 * cas))
        x.append(hodnota)

    print(f"Signál má {N} vzorků. Jdeme měřit čas!\n")
    print("-" * 40)

    # --- MĚŘENÍ 1: NAŠE STARÁ POMALÁ DFT ---
    start_cas = time.time()
    X_dft = calculate_dft(x)
    konec_cas = time.time()
    cas_dft = konec_cas - start_cas
    print(f"1. Naše původní DFT trvala:  {cas_dft:.4f} sekund")

    # --- MĚŘENÍ 2: NAŠE NOVÁ RYCHLÁ FFT ---
    start_cas = time.time()
    X_fft = calculate_fft(x)
    konec_cas = time.time()
    cas_fft = konec_cas - start_cas
    print(f"2. Naše nová FFT trvala:     {cas_fft:.4f} sekund")

    # --- MĚŘENÍ 3: PROFESIONÁLNÍ NUMPY FFT ---
    start_cas = time.time()
    X_numpy = np.fft.fft(x)
    konec_cas = time.time()
    cas_numpy = konec_cas - start_cas
    print(f"3. Knihovna Numpy trvala:    {cas_numpy:.4f} sekund")
    
    print("-" * 40)
    
    # Výpočet zrychlení
    if cas_fft > 0:
        zrychleni = cas_dft / cas_fft
        print(f"Tvoje FFT je {zrychleni:.1f}x rychlejší než tvoje DFT!")

    # 4. Zpracování výsledků pro graf (použijeme naši novou FFT)
    amplitudy_fft = [abs(hodnota) for hodnota in X_fft]
    amplitudy_numpy = [abs(hodnota) for hodnota in X_numpy]

    # 5. Vykreslení
    polovina = N // 2
    frekvence_osa = list(range(polovina))

    plt.figure(figsize=(10, 8))

    # Graf 1: Složený signál (vykreslíme jen část, ať z toho není jednolitá čmouha)
    plt.subplot(3, 1, 1)
    plt.plot(x[:200]) # Kreslíme jen prvních 200 vzorků pro přehlednost
    plt.title("Vstupní signál (prvních 200 vzorků)")
    plt.ylabel("Amplituda")
    plt.grid(True)

    # Graf 2: Naše nová FFT
    plt.subplot(3, 1, 2)
    plt.plot(frekvence_osa[:50], amplitudy_fft[:50], color='orange')
    plt.title("Naše vlastní rychlá FFT (zobrazeno do 50 Hz)")
    plt.ylabel("Velikost")
    plt.grid(True)

    # Graf 3: Numpy FFT
    plt.subplot(3, 1, 3)
    plt.plot(frekvence_osa[:50], amplitudy_numpy[:50], color='green', linestyle='--')
    plt.title("Numpy FFT pro porovnání")
    plt.xlabel("Frekvence (Hz)")
    plt.ylabel("Velikost")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()