# Import knihoven pro GUI
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
# Import knihoven pro grafy
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Import knihoven pro statistiky a algoritmy
import time
import math
import numpy as np
from algorithms import calculate_dft, calculate_fft, calculate_dft_libs, calculate_fft_libs




def spustit_vypocet():
    """Generuje signál podle prvního zadaného kmitočtu, spustí DFT/FFT a vykreslí výsledky.

    Zachová původní myšlenku (10 vstupních polí, generace signálu, porovnání DFT/FFT),
    ale zobrazí výsledky přehledněji a opraví chyby v aktualizaci štítků.
    """
    # 1) Přečíst frekvence z políček (vezmeme první nenulovou / neprázdnou)
    freqs = []
    for e in vstupy_frekvence:
        txt = e.get().strip()
        if txt:
            try:
                freqs.append(float(txt))
            except ValueError:
                continue

    # Pokud nejsou žádné frekvence, použijeme výchozí 5 Hz
    if len(freqs) == 0:
        freqs = [5.0]

    # 2) Nastavit vzorkovací frekvenci na základě nejvyšší zadané frekvence
    # Chceme dostatečné rozlišení signálu (počet vzorků na periodu)
    max_freq = max(abs(f) for f in freqs)
    samples_per_period = 20  # kolik vzorků na jednu periodu (více = hladší signál)
    min_samples = 256
    fs_candidate = max(min_samples, int(math.ceil(max_freq * samples_per_period)))

    # Délka signálu v sekundách
    duration = 1.0
    N = int(fs_candidate * duration)

    # Zaokrouhlit N na další mocninu dvou (výhoda pro FFT/padding)
    pow2 = 1
    while pow2 < N:
        pow2 <<= 1
    N = pow2

    fs = int(N / duration)
    t = [n / fs for n in range(N)]

    # Vygenerovat složený signál jako součet sinusů pro všechny frekvence
    x = [sum(math.sin(2 * math.pi * f * tn) for f in freqs) for tn in t]

    # 3) Aktualizovat graf signálu
    ax_signal.clear()
    ax_signal.plot(t, x, color='#1f77b4', linewidth=1)
    freq_str = ", ".join([str(int(f)) if float(f).is_integer() else f"{f:.2f}" for f in freqs])
    ax_signal.set_title(f"Generovaný signál — frekvence: {freq_str} Hz", fontsize=11)
    ax_signal.set_xlim(0, 1)
    ax_signal.set_ylabel('Amplitude')
    # Dynamicky nastavit y-lim podle amplitudy složeného signálu
    max_amp = max(abs(v) for v in x) if x else 1.0
    ax_signal.set_ylim(-max(1.1, max_amp * 1.2), max(1.1, max_amp * 1.2))
    ax_signal.grid(True, alpha=0.3)
    canvas_signal.draw_idle()

    # 4) Spustit výpočty jen pro vybrané algoritmy (převést na komplexní hodnoty)
    x_complex = [complex(val, 0) for val in x]

    # Připravené kontejnery pro výsledky
    dft_traces = []  # každá položka: (label, mag_list, style_dict)
    fft_traces = []

    # --- DFT (no libs) ---
    if var_dft_nolib.get():
        start = time.time()
        X_dft = calculate_dft(x_complex)
        time_dft = time.time() - start
        mag_dft = [abs(v) for v in X_dft]
        dft_traces.append((f"DFT (no libs)", mag_dft, {'color':'#2ca02c','linestyle':'-'}))
    else:
        time_dft = None

    # --- FFT (no libs) ---
    if var_fft_nolib.get():
        start = time.time()
        X_fft = calculate_fft(x_complex)
        time_fft = time.time() - start
        mag_fft = [abs(v) for v in X_fft]
        fft_traces.append((f"FFT (no libs)", mag_fft, {'color':'#ff7f0e','linestyle':'-'}))
    else:
        time_fft = None

    # --- DFT (math/cmath libs) ---
    if var_dft_lib.get():
        start = time.time()
        X_dft_lib = calculate_dft_libs(x_complex)
        time_dft_lib = time.time() - start
        mag_dft_lib = [abs(v) for v in X_dft_lib]
        dft_traces.append((f"DFT (math/cmath)", mag_dft_lib, {'color':'#2ca02c','linestyle':'--'}))
    else:
        time_dft_lib = None

    # --- FFT (math/cmath libs) ---
    if var_fft_lib.get():
        start = time.time()
        X_fft_lib = calculate_fft_libs(x_complex)
        time_fft_lib = time.time() - start
        mag_fft_lib = [abs(v) for v in X_fft_lib]
        fft_traces.append((f"FFT (math/cmath)", mag_fft_lib, {'color':'#ff7f0e','linestyle':'--'}))
    else:
        time_fft_lib = None

    # --- FFT (numpy) ---
    if var_fft_numpy.get():
        start = time.time()
        X_fft_numpy = np.fft.fft(x)
        time_fft_numpy = time.time() - start
        mag_fft_numpy = [abs(v) for v in X_fft_numpy]
        fft_traces.append((f"FFT (numpy)", mag_fft_numpy, {'color':'#1f77b4','linestyle':'-.'}))
    else:
        time_fft_numpy = None

    # 5) Připravit spektrum (magnituda) a vykreslit (použijeme polovinu spektra)
    # Vezmeme délku výsledných spekter z první dostupné stopy
    any_mag = None
    if dft_traces:
        any_mag = dft_traces[0][1]
    elif fft_traces:
        any_mag = fft_traces[0][1]
    else:
        any_mag = [0] * N

    half = len(any_mag) // 2

    # Vypočítat osu frekvencí v Hz (každý bin odpovídá fs/N Hz)
    freqs_axis = [k * (fs / (2*half)) * 2 for k in range(half)] if half>0 else [0]
    # (simpler) each bin = fs / N
    freqs_axis = [k * (fs / (2*half) if half>0 else 1) for k in range(half)] if half>0 else [0]
    # actually correct bin width:
    if half>0:
        bin_hz = fs / (2*half) * 2 / 2  # simplified to fs/N but keep safe
        freqs_axis = [k * (fs / (2*half) * 2 / 2) for k in range(half)]
        # fix simpler: fs / N
        freqs_axis = [k * (fs / (2*half) * 2 / 2) for k in range(half)]
        # final correct value:
        freqs_axis = [k * (fs / (2*half) * 2 / 2) for k in range(half)]
    else:
        freqs_axis = [0]

    # Simpler and correct: each bin = fs / N
    freqs_axis = [k * (fs / N) for k in range(half)]

    # Vlevo: DFT (stats + spektrum) - vykreslíme všechny zvolená DFT spektra
    ax_dft.clear()
    if dft_traces:
        legend_handles = []
        legend_labels = []
        for lbl, mag, style in dft_traces:
            # Nejprve vykreslíme hladkou referenční křivku (světlá) - aby spektrum zůstalo spojité
            ax_dft.plot(freqs_axis, mag[:half], color=style.get('color', '#2ca02c'), alpha=0.35, linewidth=1)
            # Poté překreslíme svislé čáry pro výrazné peaky
            ax_dft.vlines(freqs_axis, [0], mag[:half], colors=style.get('color', '#2ca02c'), linestyles=style.get('linestyle', '-'), linewidth=1, alpha=0.9)
            # přidáme proxy plot pro legendu
            lh, = ax_dft.plot([], [], color=style.get('color', '#2ca02c'), linestyle=style.get('linestyle', '-'))
            legend_handles.append(lh)
            legend_labels.append(lbl)
    else:
        ax_dft.text(0.5, 0.5, 'DFT nebylo vybráno', ha='center', va='center', alpha=0.6)

    ax_dft.set_title('DFT — spektrum')
    ax_dft.set_xlabel('Frequency (Hz)')
    ax_dft.set_ylabel('Magnitude')
    ax_dft.grid(True, alpha=0.3)
    canvas_dft.draw_idle()

    # Vpravo: FFT (stats + spektrum)
    # Vpravo: FFT (stats + spektrum) - vykreslíme všechny zvolené FFT spektra
    ax_fft.clear()
    if fft_traces:
        legend_handles = []
        legend_labels = []
        for lbl, mag, style in fft_traces:
            ax_fft.plot(freqs_axis, mag[:half], color=style.get('color', '#ff7f0e'), alpha=0.35, linewidth=1)
            ax_fft.vlines(freqs_axis, [0], mag[:half], colors=style.get('color', '#ff7f0e'), linestyles=style.get('linestyle', '-'), linewidth=1, alpha=0.9)
            lh, = ax_fft.plot([], [], color=style.get('color', '#ff7f0e'), linestyle=style.get('linestyle', '-'))
            legend_handles.append(lh)
            legend_labels.append(lbl)
    else:
        ax_fft.text(0.5, 0.5, 'FFT nebylo vybráno', ha='center', va='center', alpha=0.6)

    ax_fft.set_title('FFT — spektrum')
    ax_fft.set_xlabel('Frequency (Hz)')
    ax_fft.set_ylabel('Magnitude')
    ax_fft.grid(True, alpha=0.3)
    canvas_fft.draw_idle()

    # 6) Aktualizovat štítky se statistikami (rozdělené)
    # 6) Aktualizovat štítky se statistikami (rozdělené)
    # DFT label: složíme text z dostupných časů
    dft_time_texts = []
    if time_dft is not None:
        dft_time_texts.append(f"no-libs: {time_dft:.4f}s")
    if time_dft_lib is not None:
        dft_time_texts.append(f"libs: {time_dft_lib:.4f}s")
    label_time_dft.config(text=(", ".join(dft_time_texts) if dft_time_texts else "-") )
    label_samples_dft.config(text=f"Samples: {N}  (fs={fs} Hz)")

    # FFT label
    fft_time_texts = []
    if time_fft is not None:
        fft_time_texts.append(f"no-libs: {time_fft:.4f}s")
    if time_fft_lib is not None:
        fft_time_texts.append(f"libs: {time_fft_lib:.4f}s")
    if time_fft_numpy is not None:
        fft_time_texts.append(f"numpy: {time_fft_numpy:.4f}s")
    label_time_fft.config(text=(", ".join(fft_time_texts) if fft_time_texts else "-"))
    label_samples_fft.config(text=f"Samples: {N}  (fs={fs} Hz)")





# Deklarace Hlavního okna
root = tk.Tk()
root.title("Fourierova Transformace — Dashboard")
# Zvýšil jsem rozměry okna, aby se všechny ovladače vešly; okno zůstane fixní
root.geometry("1200x800")
root.resizable(False, False)

# Definování stylu GUI
style = ttk.Style(root)
try:
    style.theme_use('clam')
except Exception:
    pass
style.configure("TButton", font=("Arial", 10, "bold"), padding=6)
style.configure("TLabel", font=("Arial", 10))
heading_font = tkfont.Font(family="Arial", size=12, weight="bold")


# +--------------------------+
# | ŘÁDEK 1: Original signal |
# +--------------------------+
# 1. Hlavní kontejner
# --- ŘÁDEK 1: Originální signál a ovládání ---
row1_container = ttk.Frame(root, padding=(10, 8))
row1_container.grid(row=0, column=0, sticky='nsew')

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Levý panel: ovládání
controls_frame = ttk.LabelFrame(row1_container, text='Ovládání', padding=8)
controls_frame.grid(row=0, column=0, sticky='nsw', padx=(0,10), pady=0)
controls_frame.configure(width=360)
# Neznepropagujeme velikost výšky - chceme, aby se ovládací prvky vešly
# (necháme grid handle velikost výšky)

ttk.Label(controls_frame, text="Vstupní frekvence (Hz)").grid(row=0, column=0, columnspan=3, pady=(0,6))

vstupy_frekvence = []
for i in range(10):
    r = 1 + (i % 5)
    c = (i // 5) * 3
    ttk.Label(controls_frame, text=f"{i+1:02d}:").grid(row=r, column=c, sticky='e')
    ent = ttk.Entry(controls_frame, width=6)
    ent.grid(row=r, column=c+1, padx=(4,6), pady=2)
    ttk.Label(controls_frame, text="Hz").grid(row=r, column=c+2, sticky='w')
    vstupy_frekvence.append(ent)

btn_start = ttk.Button(controls_frame, command=spustit_vypocet, text="Generovat signál", style="TButton")
btn_start.grid(row=7, column=0, columnspan=3, pady=(8,0))

# Volba, které algoritmy počítat (checkboxes)
alg_frame = ttk.LabelFrame(controls_frame, text='Počítat algoritmy', padding=(6,4))
alg_frame.grid(row=8, column=0, columnspan=3, pady=(8,0))

var_dft_nolib = tk.BooleanVar(value=False)
var_fft_nolib = tk.BooleanVar(value=False)
var_dft_lib = tk.BooleanVar(value=False)
var_fft_lib = tk.BooleanVar(value=False)
var_fft_numpy = tk.BooleanVar(value=False)

ttk.Checkbutton(alg_frame, text='DFT (no libs)', variable=var_dft_nolib).grid(row=0, column=0, sticky='w')
ttk.Checkbutton(alg_frame, text='FFT (no libs)', variable=var_fft_nolib).grid(row=0, column=1, sticky='w')
ttk.Checkbutton(alg_frame, text='DFT (math/cmath)', variable=var_dft_lib).grid(row=1, column=0, sticky='w')
ttk.Checkbutton(alg_frame, text='FFT (math/cmath)', variable=var_fft_lib).grid(row=1, column=1, sticky='w')
ttk.Checkbutton(alg_frame, text='FFT (numpy)', variable=var_fft_numpy).grid(row=2, column=1, sticky='w')

# Pravý panel: graf signálu
signal_frame = ttk.LabelFrame(row1_container, text='Originální signál', padding=6)
signal_frame.grid(row=0, column=1, sticky='nsew')
row1_container.grid_columnconfigure(1, weight=1)
signal_frame.grid_rowconfigure(1, weight=1)
signal_frame.grid_columnconfigure(0, weight=1)

# Figure pro signál
fig1 = Figure(figsize=(6, 2.4), dpi=100)
fig1.subplots_adjust(left=0.08, right=0.98, top=0.9, bottom=0.18)
ax_signal = fig1.add_subplot(111)
ax_signal.set_xlim(0, 1)
ax_signal.set_ylim(-1.1, 1.1)
ax_signal.set_ylabel('Amp')

canvas_signal = FigureCanvasTkAgg(fig1, master=signal_frame)
# Vložíme canvas na první řádek signálového panelu a necháme ho zabrat prostor
canvas_signal.get_tk_widget().grid(row=0, column=0, sticky='nsew')
signal_frame.grid_rowconfigure(0, weight=1)
signal_frame.grid_columnconfigure(0, weight=1)



# +-----------------------------+
# | ŘÁDEK 2: Výsledky (rozděleno) |
# +-----------------------------+
row2_container = ttk.Frame(root, padding=(10, 8))
row2_container.grid(row=1, column=0, sticky='nsew')
row2_container.grid_columnconfigure(0, weight=1)
row2_container.grid_columnconfigure(1, weight=1)

# Levá polovina: DFT (stats + spektrum)
left_frame = ttk.LabelFrame(row2_container, text='DFT — statistiky a spektrum', padding=8)
left_frame.grid(row=0, column=0, sticky='nsew', padx=(0,6))
left_frame.grid_rowconfigure(1, weight=1)
left_frame.grid_columnconfigure(0, weight=1)

stats_dft = ttk.Frame(left_frame)
stats_dft.grid(row=0, column=0, sticky='w')
ttk.Label(stats_dft, text="DFT time:").grid(row=0, column=0, sticky='e', padx=(0,6))
label_time_dft = ttk.Label(stats_dft, text="------")
label_time_dft.grid(row=0, column=1, sticky='w')
ttk.Label(stats_dft, text="Samples:").grid(row=1, column=0, sticky='e', padx=(0,6))
label_samples_dft = ttk.Label(stats_dft, text="------")
label_samples_dft.grid(row=1, column=1, sticky='w')

fig_dft = Figure(figsize=(5, 2.6), dpi=100)
fig_dft.subplots_adjust(left=0.07, right=0.98, top=0.9, bottom=0.15)
ax_dft = fig_dft.add_subplot(111)
canvas_dft = FigureCanvasTkAgg(fig_dft, master=left_frame)
canvas_dft.get_tk_widget().grid(row=1, column=0, sticky='nsew')


# Pravá polovina: FFT (stats + spektrum)
right_frame = ttk.LabelFrame(row2_container, text='FFT — statistiky a spektrum', padding=8)
right_frame.grid(row=0, column=1, sticky='nsew', padx=(6,0))
right_frame.grid_rowconfigure(1, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

stats_fft = ttk.Frame(right_frame)
stats_fft.grid(row=0, column=0, sticky='w')
ttk.Label(stats_fft, text="FFT time:").grid(row=0, column=0, sticky='e', padx=(0,6))
label_time_fft = ttk.Label(stats_fft, text="------")
label_time_fft.grid(row=0, column=1, sticky='w')
ttk.Label(stats_fft, text="Samples:").grid(row=1, column=0, sticky='e', padx=(0,6))
label_samples_fft = ttk.Label(stats_fft, text="------")
label_samples_fft.grid(row=1, column=1, sticky='w')

fig_fft = Figure(figsize=(5, 2.6), dpi=100)
fig_fft.subplots_adjust(left=0.07, right=0.98, top=0.9, bottom=0.15)
ax_fft = fig_fft.add_subplot(111)
canvas_fft = FigureCanvasTkAgg(fig_fft, master=right_frame)
canvas_fft.get_tk_widget().grid(row=1, column=0, sticky='nsew')


# Spuštění okna
root.mainloop()