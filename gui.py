import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from core import sig_gen






# Deklarace Hlavního okna
root = tk.Tk()
root.title("Fourierova Transformace — Dashboard")
root.geometry("1500x750")






def signal_print():
    
    # Načtení frekvencí a amplitud ze vstupů do polí
    F_values = []                
    A_values = []
    for f, a in zip(input_F, input_A):
        text_f = f.get().strip()
        text_a = a.get().strip()
        if text_f and text_a:
            try:
                F_values.append(float(text_f))
                A_values.append(float(text_a))
            except ValueError:
                continue

    # 1. Tady zavoláme TVOJI funkci a získáme jen to pole x
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


def button_fce():
    signal_print()






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
var_fft_numpy = tk.BooleanVar(value=False)
ttk.Checkbutton(impl_frame, text="DFT bez knihoven", variable=var_dft_nolib).grid(row=0, column=0, sticky="w", pady=2, padx=(0, 10))
ttk.Checkbutton(impl_frame, text="FFT bez knihoven", variable=var_fft_nolib).grid(row=0, column=1, sticky="w", pady=2)
ttk.Checkbutton(impl_frame, text="DFT s knihovnami", variable=var_dft_lib).grid(row=1, column=0, sticky="w", pady=2, padx=(0, 10))
ttk.Checkbutton(impl_frame, text="FFT s knihovnami", variable=var_fft_lib).grid(row=1, column=1, sticky="w", pady=2)
ttk.Checkbutton(impl_frame, text="FFT z numpy", variable=var_fft_numpy).grid(row=2, column=1, sticky="w", pady=2)




# --- 1.3. SEKCE: Tlačítko ---
# Třetí horizontální čára
ttk.Separator(conf_params, orient="horizontal").pack(fill="x", pady=(5, 10))

btn_gen = ttk.Button(conf_params, text="VYGENEROVAT SIGNÁL", command=button_fce, style="TButton")
btn_gen.pack(pady=(0, 10), ipady=2)


# --- 1.4. SEKCE: Sig Graf ---
fig_sig_graph = Figure(figsize=(6, 3), dpi=100)
fig_sig_graph.subplots_adjust(left=0.08, right=0.98, top=0.9, bottom=0.15)
# Přidání os
axes_fig_sig_graph = fig_sig_graph.add_subplot(111)
# 3. Nastavení "prázdného" vzhledu (zatím bez dat)
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
ttk.Label(dft_stats, text="DFT statistiky", font=("Arial", 9, "bold")).grid(row=0, column=0, columnspan=5, pady=(5, 2))

# --- Horizontální oddělovací čára ---
ttk.Separator(dft_stats, orient="horizontal").grid(row=1, column=0, columnspan=5, sticky="ew", pady=(0, 5))

# --- Hlavičky sloupců (Vlastnosti) ---
ttk.Label(dft_stats, text="Čas").grid(row=2, column=2, padx=10, pady=2)
ttk.Label(dft_stats, text="Paměťová\nnáročnost").grid(row=2, column=3, padx=10, pady=2)
ttk.Label(dft_stats, text="Výpočetní\nnáročnost").grid(row=2, column=4, padx=10, pady=2)

# --- Vertikální oddělovací čára ---
separator_dft_vert = ttk.Separator(dft_stats, orient="vertical")
separator_dft_vert.grid(row=2, column=1, rowspan=3, sticky="ns", padx=5)


# --- 1. Řádek: bez knihoven ---
ttk.Label(dft_stats, text="bez knihoven:").grid(row=3, column=0, sticky="e", padx=5, pady=2)

lbl_dft_time_nolib = ttk.Label(dft_stats, text="###")
lbl_dft_time_nolib.grid(row=3, column=2, pady=2)

lbl_dft_mem_nolib = ttk.Label(dft_stats, text="###")
lbl_dft_mem_nolib.grid(row=3, column=3, pady=2)

lbl_dft_comp_nolib = ttk.Label(dft_stats, text="###")
lbl_dft_comp_nolib.grid(row=3, column=4, pady=2)


# --- 2. Řádek: s knihovnami ---
ttk.Label(dft_stats, text="s knihovnami:").grid(row=4, column=0, sticky="e", padx=5, pady=2)

lbl_dft_time_lib = ttk.Label(dft_stats, text="###")
lbl_dft_time_lib.grid(row=4, column=2, pady=2)

lbl_dft_mem_lib = ttk.Label(dft_stats, text="###")
lbl_dft_mem_lib.grid(row=4, column=3, pady=2)

lbl_dft_comp_lib = ttk.Label(dft_stats, text="###")
lbl_dft_comp_lib.grid(row=4, column=4, pady=2)




# --- 2.2. SEKCE: FFT statistiky ---
ttk.Label(fft_stats, text="FFT statistiky", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=5, pady=(25, 5))

# --- Horizontální oddělovací čára ---
ttk.Separator(fft_stats, orient="horizontal").grid(row=1, column=0, columnspan=5, sticky="ew", pady=(0, 5))

# --- Hlavičky sloupců (Vlastnosti) ---
ttk.Label(fft_stats, text="Čas").grid(row=2, column=2, padx=10, pady=2)
ttk.Label(fft_stats, text="Paměťová\nnáročnost").grid(row=2, column=3, padx=10, pady=2)
ttk.Label(fft_stats, text="Výpočetní\nnáročnost").grid(row=2, column=4, padx=10, pady=2)

# --- Vertikální oddělovací čára ---
# Zde je rowspan=4, protože FFT má 3 řádky dat (bez, s knih., numpy)
separator_fft_vert = ttk.Separator(fft_stats, orient="vertical")
separator_fft_vert.grid(row=2, column=1, rowspan=4, sticky="ns", padx=5)


# --- 1. Řádek: bez knihoven ---
ttk.Label(fft_stats, text="bez knihoven:").grid(row=3, column=0, sticky="e", padx=5, pady=2)

lbl_fft_time_nolib = ttk.Label(fft_stats, text="###")
lbl_fft_time_nolib.grid(row=3, column=2, pady=2)

lbl_fft_mem_nolib = ttk.Label(fft_stats, text="###")
lbl_fft_mem_nolib.grid(row=3, column=3, pady=2)

lbl_fft_comp_nolib = ttk.Label(fft_stats, text="###")
lbl_fft_comp_nolib.grid(row=3, column=4, pady=2)


# --- 2. Řádek: s knihovnami ---
ttk.Label(fft_stats, text="s knihovnami:").grid(row=4, column=0, sticky="e", padx=5, pady=2)

lbl_fft_time_lib = ttk.Label(fft_stats, text="###")
lbl_fft_time_lib.grid(row=4, column=2, pady=2)

lbl_fft_mem_lib = ttk.Label(fft_stats, text="###")
lbl_fft_mem_lib.grid(row=4, column=3, pady=2)

lbl_fft_comp_lib = ttk.Label(fft_stats, text="###")
lbl_fft_comp_lib.grid(row=4, column=4, pady=2)


# --- 3. Řádek: z numpy ---
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
# 3. Nastavení "prázdného" vzhledu (zatím bez dat)
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
# 3. Nastavení "prázdného" vzhledu (zatím bez dat)
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