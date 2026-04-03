# Knihovny pro měření statistik (čas a paměť)
import time
import tracemalloc
# Knihovny pro GUI
import tkinter as tk
from tkinter import ttk
# Knihovny pro grafy
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Knihovny pro výpočet DFT/FFT a vlastní moduly
import numpy as np
from core import sig_gen
from algorithms import calculate_dft, calculate_fft, calculate_dft_libs, calculate_fft_libs



# Knihovny pro propojení s implementaci v C
import ctypes
import sys
import os



# --- Načtení Cčekové knihovny na základě operačního systému ---
base_dir = os.path.dirname(os.path.abspath(__file__))

# Vybrání správné koncovky knihovny na základě OS
if sys.platform.startswith("win"):
    lib_name = "dft_c.dll"  # Win
elif sys.platform.startswith("darwin"):
    lib_name = "dft_c.dylib"    # macOS
else:
    lib_name = "dft_c.so"   # Linux

lib_path = os.path.join(base_dir, "algorithms", lib_name)
c_lib = ctypes.CDLL(lib_path)

# Nastavení datových typů pro Cíčkovou fce
# Bere int (N) a 4 pointry na pole doublů
c_lib.calculate_dft_c.argtypes = [
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double)
]




# Deklarace Hlavního okna a paramterů (titulek, velikost a zákaz změny velikosti)
root = tk.Tk()
root.title("Fourierova Transformace — Dashboard")
root.geometry("1500x750")
root.resizable(False, False)






def signal_print():
    
    # Načtení frekvencí a amplitud ze vstupů do polí
    F_values = []                
    A_values = []

    # Projití všech vstupů a spojení pomocí zip
    for f, a in zip(input_F, input_A):
        text_f = f.get().strip()
        text_a = a.get().strip()
        # Pokud nejsou prázdná, tak se zkusí převést na float
        if text_f and text_a:
            try:
                F_values.append(float(text_f))
                A_values.append(float(text_a))
            except ValueError:
                continue    # Ignorování vstupu při zadání nesprávného (písmena nebo znaky)

    # Zavolání funkce sig_gen
    X, t = sig_gen(F_values, A_values)
    N = len(X)
    T = [n / N for n in range(N)]

    # Vyčištění grafu
    axes_fig_sig_graph.clear()
    # Vytvoření křivky
    axes_fig_sig_graph.plot(t, X, color='#1f77b4', linewidth=1)
    freq_str = ", ".join([str(int(f)) if float(f).is_integer() else f"{f:.2f}" for f in F_values])
    # Nastavení vzhledu grafu
    axes_fig_sig_graph.set_xlim(0, 1)
    axes_fig_sig_graph.grid(True, linestyle='--', alpha=0.6)
    axes_fig_sig_graph.set_title("Průběh vygenerovaného signálu", fontsize=10)
    axes_fig_sig_graph.set_xlabel("Čas [s]")
    axes_fig_sig_graph.set_ylabel("Amplituda [V]")
    # Dynamicky nastavit y-lim podle amplitudy složeného signálu
    max_amp = max(abs(v) for v in X) if X else 1.0
    axes_fig_sig_graph.set_ylim(-max(1.1, max_amp * 1.2), max(1.1, max_amp * 1.2))
    # Vykreslení grafu
    canvas_sig_graph.draw_idle()

    return X

def stats_print(X):
    # Převod signálu do komplexní roviny
    X_complex = [complex(val, 0) for val in X]

    # Pole pro uložení výsledků.
    dft_traces = []
    fft_traces = []

    # --- DFT (no libs) ---
    if var_dft_nolib.get():
        tracemalloc.start() # Začátek sledování alokované paměti
        start = time.time() # Začátek měření času

        X_dft = calculate_dft(X_complex)

        max_time = time.time() - start  # Konec měření času
        mem, max_mem = tracemalloc.get_traced_memory()  # Uložení sledované paměti
        tracemalloc.stop()  # Konec sledování alokované paměti

        # Převod na milisekundy a kilobajty
        max_time_ms = max_time * 1000
        max_mem_kb = max_mem / 1024.0

        # Výpis do GUI
        lbl_dft_time_nolib.config(text=f"{max_time_ms:.2f}", foreground="#000000")
        lbl_dft_mem_nolib.config(text=f"{max_mem_kb:.2f}", foreground="#000000")
        lbl_dft_comp_nolib.config(text="O(N²)", foreground="#000000")

        # Získání abs hodnot (amplitudy) a uložení křivky
        mag_dft = [abs(v) for v in X_dft]
        # To 'color' a 'linestyle' je zde zbytečný ale už jsem to tu nechal (pak se to přepisuje)
        dft_traces.append((f"DFT", mag_dft, {'color':'#2ca02c','linestyle':'-'}))
    else:
        # Pokud není zašrktnuto -> zašednutí textu
        lbl_dft_time_nolib.config(foreground="#888888")
        lbl_dft_mem_nolib.config(foreground="#888888")
        lbl_dft_comp_nolib.config(foreground="#888888")

    # --- FFT (no libs) ---
    if var_fft_nolib.get():
        tracemalloc.start()
        start = time.time()

        X_fft = calculate_fft(X_complex)

        max_time = time.time() - start
        mem, max_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        max_time_ms = max_time * 1000
        max_mem_kb = max_mem / 1024.0

        lbl_fft_time_nolib.config(text=f"{max_time_ms:.2f}", foreground="#000000")
        lbl_fft_mem_nolib.config(text=f"{max_mem_kb:.2f}", foreground="#000000")
        lbl_fft_comp_nolib.config(text="O(N log N)", foreground="#000000")

        mag_fft = [abs(v) for v in X_fft]
        fft_traces.append((f"FFT", mag_fft, {'color':'#ff7f0e','linestyle':'-'}))
    else:
        lbl_fft_time_nolib.config(foreground="#888888")
        lbl_fft_mem_nolib.config(foreground="#888888")
        lbl_fft_comp_nolib.config(foreground="#888888")

    # --- DFT (math/cmath libs) ---
    if var_dft_lib.get():
        tracemalloc.start()
        start = time.time()

        X_dft_lib = calculate_dft_libs(X_complex)

        max_time = time.time() - start
        mem, max_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        max_time_ms = max_time * 1000
        max_mem_kb = max_mem / 1024.0

        lbl_dft_time_lib.config(text=f"{max_time_ms:.2f}", foreground="#000000")
        lbl_dft_mem_lib.config(text=f"{max_mem_kb:.2f}", foreground="#000000")
        lbl_dft_comp_lib.config(text="O(N²)", foreground="#000000")
        

        mag_dft_lib = [abs(v) for v in X_dft_lib]
        dft_traces.append((f"DFT (math/cmath)", mag_dft_lib, {'color':'#2ca02c','linestyle':'--'}))
    else:
        lbl_dft_time_lib.config(foreground="#888888")
        lbl_dft_mem_lib.config(foreground="#888888")
        lbl_dft_comp_lib.config(foreground="#888888")

    # --- FFT (math/cmath libs) ---
    if var_fft_lib.get():
        tracemalloc.start()
        start = time.time()

        X_fft_lib = calculate_fft_libs(X_complex)

        max_time = time.time() - start
        mem, max_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        max_time_ms = max_time * 1000
        max_mem_kb = max_mem / 1024.0

        lbl_fft_time_lib.config(text=f"{max_time_ms:.2f}", foreground="#000000")
        lbl_fft_mem_lib.config(text=f"{max_mem_kb:.2f}", foreground="#000000")
        lbl_fft_comp_lib.config(text="O(N log N)", foreground="#000000")

        mag_fft_lib = [abs(v) for v in X_fft_lib]
        fft_traces.append((f"FFT (math/cmath)", mag_fft_lib, {'color':'#ff7f0e','linestyle':'--'}))
    else:
        lbl_fft_time_lib.config(foreground="#888888")
        lbl_fft_mem_lib.config(foreground="#888888")
        lbl_fft_comp_lib.config(foreground="#888888")

    # --- DFT (Implement. C) ---
    if var_dft_c.get():
        tracemalloc.start()
        start = time.time()

        N = len(X)
    
        # Rozseknutí python komplex čísla na dvě obyčejná pole
        in_r = [val.real for val in X]
        in_i = [val.imag for val in X]
        
        # Příprava "šablony" pro C-pole o velikosti N
        CArray = ctypes.c_double * N
        
        # Vytvoření vstupního C-pole a naplníme dat z Pythonu
        c_in_r = CArray(*in_r)
        c_in_i = CArray(*in_i)
        
        # Vytvoření prázdného C-pole pro výsledek. 
        c_out_r = CArray()
        c_out_i = CArray()
        
        # Volání C funkce, nic nevrací do žádné proměnné, protože v argumentu
        # má pointery na výše definována pole a pomocí nich do těch polí uloží vypočtené hodnoty.
        c_lib.calculate_dft_c(N, c_in_r, c_in_i, c_out_r, c_out_i)
        
        # Složíme výsledek zpět z C do komplexní rovniy python čísel
        X_dft_c = [complex(c_out_r[k], c_out_i[k]) for k in range(N)]
        
        max_time = time.time() - start
        mem, max_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        max_time_ms = max_time * 1000
        max_mem_kb = max_mem / 1024.0
        
        lbl_dft_time_c.config(text=f"{max_time_ms:.2f}", foreground="#000000")
        lbl_dft_mem_c.config(text=f"{max_mem_kb:.2f}", foreground="#000000")
        lbl_dft_comp_c.config(text="O(N²)", foreground="#000000")

        mag_dft_c = [abs(v) for v in X_dft_c]
        dft_traces.append((f"DFT (C)", mag_dft_c, {'color':'#2ca02c','linestyle':':'}))
    else:
        # Vypnutí labelů, když není zaškrtnuto
        lbl_dft_time_c.config(foreground="#888888")
        lbl_dft_mem_c.config(foreground="#888888")
        lbl_dft_comp_c.config(foreground="#888888")

    # --- FFT (numpy) ---
    if var_fft_numpy.get():
        tracemalloc.start()
        start = time.time()

        X_fft_numpy = np.fft.fft(X)

        max_time = time.time() - start
        mem, max_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        max_time_ms = max_time * 1000
        max_mem_kb = max_mem / 1024.0

        lbl_fft_time_numpy.config(text=f"{max_time_ms:.2f}", foreground="#000000")
        lbl_fft_mem_numpy.config(text=f"{max_mem_kb:.2f}", foreground="#000000")
        lbl_fft_comp_numpy.config(text="O(N log N)", foreground="#000000")

        mag_fft_numpy = [abs(v) for v in X_fft_numpy]
        fft_traces.append((f"FFT (numpy)", mag_fft_numpy, {'color':'#ff7f0e','linestyle':'-.'}))
    else:
        lbl_fft_time_numpy.config(foreground="#888888")
        lbl_fft_mem_numpy.config(foreground="#888888")
        lbl_fft_comp_numpy.config(foreground="#888888")

    return dft_traces, fft_traces

def spectrum_print(X, dft_traces, fft_traces):
    # Příprava osy X (fekvence) pro spektrum
    N = len(X)
    T = 1.0 # Předpokládaná délka záznamu je 1 sekunda.
    fs = N / T
    half = N // 2   # Zobrazení pouze první poloviny spektra

    # Vygenerování pole reálných frekvencí (0 až fs/2)
    freqs = [k * fs / N for k in range(half)]
    
    axes_fig_dft_spectrum.clear()
    axes_fig_fft_spectrum.clear()

    # -- Vykreslení DFT spekter ---
    if dft_traces:  # Provede se, jen pokud je zaškrtlá aspoň jedna DFT metoda
        amps_dft = []
        for k in range(half):
            mag = dft_traces[0][1][k]
            # Normalizace amplitudy - stejnosměrná složka se dělí N, ostatní 2/N
            if k == 0:
                amps_dft.append(mag / N)
            else:
                amps_dft.append(2 * mag / N)

        # Vykreslení (zelená barva C2 pro DFT)
        axes_fig_dft_spectrum.stem(freqs, amps_dft, linefmt='C2-', markerfmt='C2o', basefmt='k-')
        
        # Chytré oříznutí osy X (najde max frekvenci s amplitudou > 0.01 V)
        act_f = [f for f, a in zip(freqs, amps_dft) if a > 0.01]
        max_f = max(act_f) * 1.1 if act_f else 10
        axes_fig_dft_spectrum.set_xlim(0, max_f)
        
        max_amp = max(amps_dft) if amps_dft else 1
        axes_fig_dft_spectrum.set_ylim(0, max_amp * 1.2)
    else:
        # Výchozí limit, když není nic zaškrtnuto
        axes_fig_dft_spectrum.set_xlim(0, 10)
        axes_fig_dft_spectrum.set_ylim(0, 1)
        axes_fig_dft_spectrum.clear()


    # --- Vykreslení FFT spekter ---
    if fft_traces:  # Provede se, jen pokud je zaškrtlá aspoň jedna FFT metoda
        amps_fft = []
        for k in range(half):
            mag = fft_traces[0][1][k]
            if k == 0:
                amps_fft.append(mag / N)
            else:
                amps_fft.append(2 * mag / N)

        # Vykreslení (zelená barva C2 pro FFT)
        axes_fig_fft_spectrum.stem(freqs, amps_fft, linefmt='C2-', markerfmt='C2o', basefmt='k-')
        
        # Chytré oříznutí osy X (najde max frekvenci s amplitudou > 0.01 V)
        act_f = [f for f, a in zip(freqs, amps_fft) if a > 0.01]
        max_f = max(act_f) * 1.1 if act_f else 10
        axes_fig_fft_spectrum.set_xlim(0, max_f)
        
        max_amp = max(amps_fft) if amps_fft else 1
        axes_fig_fft_spectrum.set_ylim(0, max_amp * 1.2)
    else:
        # Výchozí limit, když není nic zaškrtnuto
        axes_fig_fft_spectrum.set_xlim(0, 10)
        axes_fig_fft_spectrum.set_ylim(0, 1)
        axes_fig_fft_spectrum.clear()

    # Obnova vzhledu DFT grafu
    axes_fig_dft_spectrum.grid(True, linestyle='--', alpha=0.6)
    axes_fig_fft_spectrum.grid(True, linestyle='--', alpha=0.6)
    axes_fig_dft_spectrum.set_title("DFT spektrum signálu", fontsize=10)
    axes_fig_fft_spectrum.set_title("FFT spektrum signálu", fontsize=10)
    axes_fig_dft_spectrum.set_xlabel("Frekvence [Hz]")
    axes_fig_fft_spectrum.set_xlabel("Frekvence [Hz]")
    axes_fig_dft_spectrum.set_ylabel("Amplituda [V]")
    axes_fig_fft_spectrum.set_ylabel("Amplituda [V]")
    canvas_dft_spectrum.draw_idle()
    canvas_fft_spectrum.draw_idle()


# Funkce která se spustí při kliknutí na tlačítko.
def button_fce():
    X = signal_print()
    dft_traces, fft_traces = stats_print(X)
    spectrum_print(X, dft_traces, fft_traces)






# +--------------------------+
# | ŘÁDEK 1: Original signal |
# +--------------------------+
# Deklarace konteineru pro vygenerovaní signál a jeho zarovnání
row1_container = ttk.Frame(root, padding=(10, 10, 10, 5), borderwidth=1, relief="solid")
row1_container.pack(side="top", fill="both", expand=True, padx=10, pady=(10, 5))
# Deklarace konteineru pro konfigurační parametry originálního signálu a jeho zarovnání
conf_params = ttk.Frame(row1_container, padding=5)
conf_params.pack(side="left")
# Deklarace separátoru mezi konf. parametry a grafem signálu
separator_row1 = ttk.Separator(row1_container, orient="vertical")
separator_row1.pack(side="left", fill="y", padx=(5, 0))
# Deklarace konteineru pro graf originální signálu a jeho zarovnání
sig_graph = ttk.Frame(row1_container, padding=5)
sig_graph.pack(side="left", fill="both", expand=True)




# --- 1.1. SEKCE: Frekvence a Amplitudy ---
ttk.Label(conf_params, text="Frekvence a amplitudy složek signálu", font=("Arial", 10, "bold")).pack(side="top",pady=(5, 2))

# První horizontální čára
ttk.Separator(conf_params, orient="horizontal").pack(fill="x", pady=2)

# Frame pro tabulku 5 vstupů
inputs_frame = ttk.Frame(conf_params)
inputs_frame.pack(pady=5)

# Seznamy, pro uložení hodnot ze vstupů
input_F = []
input_A = []

for i in range(1, 6): # 1 až 5
    # Číslo řádku
    ttk.Label(inputs_frame, text=f"{i}:").grid(row=i, column=0, sticky="e", padx=(0, 2), pady=2)
    
    # Vstup pro frekvenci
    entry_f = ttk.Entry(inputs_frame, width=6)
    entry_f.grid(row=i, column=1, padx=2, pady=2)
    input_F.append(entry_f)
    
    # Jednotka Hz
    ttk.Label(inputs_frame, text="Hz").grid(row=i, column=2, sticky="w", padx=(0, 10), pady=2)
    
    # Vstup pro amplitudu
    entry_a = ttk.Entry(inputs_frame, width=6)
    entry_a.grid(row=i, column=3, padx=2, pady=2)
    input_A.append(entry_a)
    
    # Jednotka V
    ttk.Label(inputs_frame, text="V").grid(row=i, column=4, sticky="w", padx=(0, 2), pady=2)


# --- 1.2. SEKCE: Použití implementace ---
# Druhá horizontální čára
ttk.Separator(conf_params, orient="horizontal").pack(fill="x", pady=(5, 2))
ttk.Label(conf_params, text="Použití implementace", font=("Arial", 9)).pack(pady=2)

# Frame pro zaškrtávací políčka
impl_frame = ttk.Frame(conf_params)
impl_frame.pack(fill="x", pady=5)

# Checkbuttony pro vybrání implemetace pro výpočet
var_dft_nolib = tk.BooleanVar(value=False)
var_fft_nolib = tk.BooleanVar(value=False)
var_dft_lib = tk.BooleanVar(value=False)
var_fft_lib = tk.BooleanVar(value=False)
var_dft_c = tk.BooleanVar(value=False)
var_fft_numpy = tk.BooleanVar(value=False)
ttk.Checkbutton(impl_frame, text="DFT", variable=var_dft_nolib).grid(row=0, column=0, sticky="w", pady=2, padx=(0, 10))
ttk.Checkbutton(impl_frame, text="FFT", variable=var_fft_nolib).grid(row=0, column=1, sticky="w", pady=2)
ttk.Checkbutton(impl_frame, text="DFT (math/cmath)", variable=var_dft_lib).grid(row=1, column=0, sticky="w", pady=2, padx=(0, 10))
ttk.Checkbutton(impl_frame, text="FFT (math/cmath)", variable=var_fft_lib).grid(row=1, column=1, sticky="w", pady=2)
ttk.Checkbutton(impl_frame, text="DFT (C)", variable=var_dft_c).grid(row=2, column=0, sticky="w", pady=2, padx=(0, 10))
ttk.Checkbutton(impl_frame, text="FFT (numpy)", variable=var_fft_numpy).grid(row=2, column=1, sticky="w", pady=2)




# --- 1.3. SEKCE: Tlačítko ---
# Třetí horizontální čára
ttk.Separator(conf_params, orient="horizontal").pack(fill="x", pady=(5, 10))

# Tlačítko pro spuštění generování signálu a zaškrtnutých inplementací
btn_gen = ttk.Button(conf_params, text="VYGENEROVAT SIGNÁL", command=button_fce, style="TButton")
btn_gen.pack(pady=(0, 10), ipady=2)


# --- 1.4. SEKCE: Sig Graf ---
fig_sig_graph = Figure(figsize=(6, 3), dpi=100)
fig_sig_graph.subplots_adjust(left=0.08, right=0.98, top=0.9, bottom=0.15)
# Přidání os
axes_fig_sig_graph = fig_sig_graph.add_subplot(111)
# 3. Nastavení "prázdného" vzhledu (bez dat)
axes_fig_sig_graph.set_xlim(0, 1)
axes_fig_sig_graph.set_ylim(-10, 10)
axes_fig_sig_graph.grid(True, linestyle='--', alpha=0.6)
axes_fig_sig_graph.set_title("Průběh vygenerovaného signálu", fontsize=10)
axes_fig_sig_graph.set_xlabel("Čas [s]")
axes_fig_sig_graph.set_ylabel("Amplituda [V]")
# 4. Propojení Matplotlibu s Tkinterem
canvas_sig_graph = FigureCanvasTkAgg(fig_sig_graph, master=sig_graph)
canvas_sig_graph.get_tk_widget().pack(fill="both", expand=True)






# +-----------------------------+
# | ŘÁDEK 2: Frekvenční spektra |
# +-----------------------------+
# Deklarace konteineru pro statistyky a frekvenční spektra signálu a jeho zarovnání
row2_container = ttk.Frame(root, padding=(10, 5, 10, 10), borderwidth=1, relief="solid")
row2_container.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))
# Deklarace konteineru pro DFT statistiky a jeho zarovnání
stats = ttk.Frame(row2_container, padding=5)
stats.pack(side="left")
dft_stats = ttk.Frame(stats)
dft_stats.pack(side="top")
fft_stats = ttk.Frame(stats)
fft_stats.pack(side="top")
# Deklarace separátoru
separator1_row2 = ttk.Separator(row2_container, orient="vertical")
separator1_row2.pack(side="left", fill="y")
# Deklarace konteineru pro DFT spektrum a jeho zarovnání
dft_spectrum = ttk.Frame(row2_container, padding=5)
dft_spectrum.pack(side="left", fill="both", expand=True)
# Deklarace separátoru
separator2_row2 = ttk.Separator(row2_container, orient="vertical")
separator2_row2.pack(side="left", fill="y")
# Deklarace konteineru pro FFT spektrum a jeho zarovnání
fft_spectrum = ttk.Frame(row2_container, padding=5)
fft_spectrum.pack(side="left", fill="both", expand=True)






# --- 2.1. SEKCE: DFT statistiky ---
ttk.Label(dft_stats, text="DFT statistiky", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=5, pady=(5, 2))

# Horizontální oddělovací čára
ttk.Separator(dft_stats, orient="horizontal").grid(row=1, column=0, columnspan=5, sticky="ew", pady=(0, 5))

# Hlavičky sloupců
ttk.Label(dft_stats, text="Čas [ms]").grid(row=2, column=2, padx=10, pady=2)
ttk.Label(dft_stats, text="Paměť [Kb]").grid(row=2, column=3, padx=10, pady=2)
ttk.Label(dft_stats, text="Výpočet").grid(row=2, column=4, padx=10, pady=2)

# Vertikální oddělovací čára
separator_dft_vert = ttk.Separator(dft_stats, orient="vertical")
separator_dft_vert.grid(row=2, column=1, rowspan=3, sticky="ns", padx=5)


# 1. Řádek: bez knihoven
ttk.Label(dft_stats, text="bez knihoven:").grid(row=3, column=0, sticky="e", padx=5, pady=2)

lbl_dft_time_nolib = ttk.Label(dft_stats, text="###")
lbl_dft_time_nolib.grid(row=3, column=2, pady=2)

lbl_dft_mem_nolib = ttk.Label(dft_stats, text="###")
lbl_dft_mem_nolib.grid(row=3, column=3, pady=2)

lbl_dft_comp_nolib = ttk.Label(dft_stats, text="###")
lbl_dft_comp_nolib.grid(row=3, column=4, pady=2)


# 2. Řádek: s knihovnami
ttk.Label(dft_stats, text="s math/cmath:").grid(row=4, column=0, sticky="e", padx=5, pady=2)

lbl_dft_time_lib = ttk.Label(dft_stats, text="###")
lbl_dft_time_lib.grid(row=4, column=2, pady=2)

lbl_dft_mem_lib = ttk.Label(dft_stats, text="###")
lbl_dft_mem_lib.grid(row=4, column=3, pady=2)

lbl_dft_comp_lib = ttk.Label(dft_stats, text="###")
lbl_dft_comp_lib.grid(row=4, column=4, pady=2)


# 2. Řádek: C
ttk.Label(dft_stats, text="implement. C:").grid(row=5, column=0, sticky="e", padx=5, pady=2)

lbl_dft_time_c = ttk.Label(dft_stats, text="###")
lbl_dft_time_c.grid(row=5, column=2, pady=2)

lbl_dft_mem_c = ttk.Label(dft_stats, text="###")
lbl_dft_mem_c.grid(row=5, column=3, pady=2)

lbl_dft_comp_c = ttk.Label(dft_stats, text="###")
lbl_dft_comp_c.grid(row=5, column=4, pady=2)




# --- 2.2. SEKCE: FFT statistiky ---
ttk.Label(fft_stats, text="FFT statistiky", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=5, pady=(25, 5))

# Horizontální oddělovací čára
ttk.Separator(fft_stats, orient="horizontal").grid(row=1, column=0, columnspan=5, sticky="ew", pady=(0, 5))

# Hlavičky sloupců
ttk.Label(fft_stats, text="Čas [ms]").grid(row=2, column=2, padx=10, pady=2)
ttk.Label(fft_stats, text="Paměť [Kb]").grid(row=2, column=3, padx=10, pady=2)
ttk.Label(fft_stats, text="Výpočet").grid(row=2, column=4, padx=10, pady=2)

# Vertikální oddělovací čára
separator_fft_vert = ttk.Separator(fft_stats, orient="vertical")
separator_fft_vert.grid(row=2, column=1, rowspan=4, sticky="ns", padx=5)


# 1. Řádek: bez knihoven
ttk.Label(fft_stats, text="bez knihoven:").grid(row=3, column=0, sticky="e", padx=5, pady=2)

lbl_fft_time_nolib = ttk.Label(fft_stats, text="###")
lbl_fft_time_nolib.grid(row=3, column=2, pady=2)

lbl_fft_mem_nolib = ttk.Label(fft_stats, text="###")
lbl_fft_mem_nolib.grid(row=3, column=3, pady=2)

lbl_fft_comp_nolib = ttk.Label(fft_stats, text="###")
lbl_fft_comp_nolib.grid(row=3, column=4, pady=2)


# 2. Řádek: s knihovnami
ttk.Label(fft_stats, text="s math/cmath:").grid(row=4, column=0, sticky="e", padx=5, pady=2)

lbl_fft_time_lib = ttk.Label(fft_stats, text="###")
lbl_fft_time_lib.grid(row=4, column=2, pady=2)

lbl_fft_mem_lib = ttk.Label(fft_stats, text="###")
lbl_fft_mem_lib.grid(row=4, column=3, pady=2)

lbl_fft_comp_lib = ttk.Label(fft_stats, text="###")
lbl_fft_comp_lib.grid(row=4, column=4, pady=2)


# 3. Řádek: z numpy
ttk.Label(fft_stats, text="z numpy:").grid(row=5, column=0, sticky="e", padx=5, pady=2)

lbl_fft_time_numpy = ttk.Label(fft_stats, text="###")
lbl_fft_time_numpy.grid(row=5, column=2, pady=2)

lbl_fft_mem_numpy = ttk.Label(fft_stats, text="###")
lbl_fft_mem_numpy.grid(row=5, column=3, pady=2)

lbl_fft_comp_numpy = ttk.Label(fft_stats, text="###")
lbl_fft_comp_numpy.grid(row=5, column=4, pady=2)




# --- 2.3. SEKCE: DFT spektrum ---
fig_dft_spectrum = Figure(figsize=(4, 3), dpi=100, layout="tight")
fig_dft_spectrum.subplots_adjust(left=0.08, right=0.98, top=0.9, bottom=0.15)
# Přidání os
axes_fig_dft_spectrum = fig_dft_spectrum.add_subplot(111)
# 3. Nastavení "prázdného" vzhledu (bez dat)
axes_fig_dft_spectrum.set_xlim(0, 1)
axes_fig_dft_spectrum.set_ylim(0, 1)
axes_fig_dft_spectrum.grid(True, linestyle='--', alpha=0.6)
axes_fig_dft_spectrum.set_title("DFT spektrum signálu", fontsize=10)
axes_fig_dft_spectrum.set_xlabel("Frekvence [Hz]")
axes_fig_dft_spectrum.set_ylabel("Amplituda [V]")
# 4. Propojení Matplotlibu s Tkinterem
canvas_dft_spectrum = FigureCanvasTkAgg(fig_dft_spectrum, master=dft_spectrum)
canvas_dft_spectrum.get_tk_widget().pack(fill="both", expand=True)



# --- 2.4. SEKCE: FFT spektrum ---
fig_fft_spectrum = Figure(figsize=(4, 3), dpi=100, layout="tight")
fig_fft_spectrum.subplots_adjust(left=0.08, right=0.98, top=0.9, bottom=0.15)
# Přidání os
axes_fig_fft_spectrum = fig_fft_spectrum.add_subplot(111)
# 3. Nastavení "prázdného" vzhledu (bez dat)
axes_fig_fft_spectrum.set_xlim(0, 1)
axes_fig_fft_spectrum.set_ylim(0, 1)
axes_fig_fft_spectrum.grid(True, linestyle='--', alpha=0.6)
axes_fig_fft_spectrum.set_title("FFT spektrum signálu", fontsize=10)
axes_fig_fft_spectrum.set_xlabel("Frekvence [Hz]")
axes_fig_fft_spectrum.set_ylabel("Amplituda [V]")
# 4. Propojení Matplotlibu s Tkinterem
canvas_fft_spectrum = FigureCanvasTkAgg(fig_fft_spectrum, master=fft_spectrum)
canvas_fft_spectrum.get_tk_widget().pack(fill="both", expand=True)









# Spuštění okna
root.mainloop()