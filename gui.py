import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from core import sig_gen


# Deklarace Hlavního okna
root = tk.Tk()
root.title("Fourierova Transformace — Dashboard")
root.geometry("1750x800")






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
ttk.Label(conf_params, text="Frekvence a amplitudy složek signálu", font=("Arial", 9, "bold")).pack(side="top",pady=(5, 2))

# První horizontální čára
ttk.Separator(conf_params, orient="horizontal").pack(fill="x", pady=2)

# Frame pro tabulku 5 vstupů
inputs_frame = ttk.Frame(conf_params)
inputs_frame.pack(pady=5)

# Seznamy, pro uložení hodnot ze vstupů
vstupy_frekvence = []
vstupy_amplitudy = []

for i in range(1, 6): # 1 až 5
    # Číslo řádku
    ttk.Label(inputs_frame, text=f"{i}:").grid(row=i, column=0, sticky="e", padx=(0, 2), pady=2)
    
    # Vstup pro frekvenci
    entry_f = ttk.Entry(inputs_frame, width=6)
    entry_f.grid(row=i, column=1, padx=2, pady=2)
    vstupy_frekvence.append(entry_f)
    
    # Jednotka Hz
    ttk.Label(inputs_frame, text="Hz").grid(row=i, column=2, sticky="w", padx=(0, 10), pady=2)
    
    # Vstup pro amplitudu
    entry_a = ttk.Entry(inputs_frame, width=6)
    entry_a.grid(row=i, column=3, padx=2, pady=2)
    vstupy_amplitudy.append(entry_a)
    
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
var_fft_numpy = tk.BooleanVar(value=False)
ttk.Checkbutton(impl_frame, text="DFT bez knihoven", variable=var_dft_nolib).grid(row=0, column=0, sticky="w", pady=2, padx=(0, 10))
ttk.Checkbutton(impl_frame, text="FFT bez knihoven", variable=var_fft_nolib).grid(row=0, column=1, sticky="w", pady=2)
ttk.Checkbutton(impl_frame, text="DFT s knihovnami", variable=var_dft_lib).grid(row=1, column=0, sticky="w", pady=2, padx=(0, 10))
ttk.Checkbutton(impl_frame, text="FFT s knihovnami", variable=var_fft_lib).grid(row=1, column=1, sticky="w", pady=2)
ttk.Checkbutton(impl_frame, text="FFT z numpy", variable=var_fft_numpy).grid(row=2, column=1, sticky="w", pady=2)




# --- 1.3. SEKCE: Tlačítko ---
# Třetí horizontální čára
ttk.Separator(conf_params, orient="horizontal").pack(fill="x", pady=(5, 10))

btn_gen = ttk.Button(conf_params, text="VYGENEROVAT SIGNÁL", style="TButton")
btn_gen.pack(pady=(0, 10), ipady=2)


# --- 2.1. SEKCE: Sig Graf ---
fig_sig_graph = Figure(figsize=(6, 3), dpi=100)
fig_sig_graph.subplots_adjust(left=0.08, right=0.98, top=0.9, bottom=0.15)
# Přidání os
axes_fig_sig_graph = fig_sig_graph.add_subplot(111)
# 3. Nastavení "prázdného" vzhledu (zatím bez dat)
axes_fig_sig_graph.set_xlim(0, 1)
axes_fig_sig_graph.set_ylim(-10, 10)
axes_fig_sig_graph.grid(True, linestyle='--', alpha=0.6)
axes_fig_sig_graph.set_title("Průběh vygenerovaného signálu v 1 sekundě", fontsize=10)
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
dft_stats = ttk.Frame(row2_container, padding=5)
dft_stats.pack(side="left")
# Deklarace separátoru
separator1_row2 = ttk.Separator(row2_container, orient="vertical")
separator1_row2.pack(side="left", fill="y")
# Deklarace konteineru pro DFT spektrum a jeho zarovnání
dft_spectrum = ttk.Frame(row2_container, padding=5)
dft_spectrum.pack(side="left", fill="both", expand=True)
# Deklarace separátoru
separator2_row2 = ttk.Separator(row2_container, orient="vertical")
separator2_row2.pack(side="left", fill="y")
# Deklarace konteineru pro FFT statistiky a jeho zarovnání
fft_stats = ttk.Frame(row2_container, padding=5)
fft_stats.pack(side="left")
# Deklarace separátoru
separator3_row2 = ttk.Separator(row2_container, orient="vertical")
separator3_row2.pack(side="left", fill="y")
# Deklarace konteineru pro FFT spektrum a jeho zarovnání
fft_spectrum = ttk.Frame(row2_container, padding=5)
fft_spectrum.pack(side="left", fill="both", expand=True)



# Spuštění okna
root.mainloop()