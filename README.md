# Fourierova Transformace — Dashboard

Tato desktopová aplikace slouží k demonstraci, výpočtu a vizualizaci Diskrétní Fourierovy transformace (DFT) a Rychlé Fourierovy transformace (FFT). Umožňuje uživateli vygenerovat si složený signál na základě zadaných frekvencí a amplitud a následně porovnat výpočetní náročnost (čas a paměť) různých implementací algoritmů.

## Hlavní funkce
* **Generátor signálu:** Vytvoření signálu až z 5 různých frekvenčních složek.
* **Vlastní implementace:** Výpočet DFT a FFT pomocí čistého Pythonu (s využitím i bez využití matematických knihoven `math`/`cmath`).
* **Numpy implementace:** Rychlý výpočet FFT pomocí optimalizované knihovny `numpy`.
* **implementace pomocí C:** Výpočet DFT za pomocí jazyka C, kód je zkompilován do knihoen pro systémy linux (`.so`), windows (`.dll`) a macos (`.dylib`).
* **Měření výkonu:** Srovnání výpočetního času (v ms) a paměťové náročnosti (v Kb) jednotlivých metod.
* **Vizualizace:** Vykreslení časového průběhu signálu a jeho frekvenčních spekter (DFT a FFT) s automatickým přizpůsobením os.

## 🚀 Instalace a spuštění

Pro bezpečné spuštění bez narušení tvého systému doporučujeme použít virtuální prostředí (venv).

Vytvoření vyrtuálního porstředí:
```bash
python3 -m venv DFT_FFT_venv
```

Přepnutí do virtuálního prostředí:

(linux/macOS)
```bash
source DFT_FFT_venv/bin/activate
```
(windows)
```bash
DFT_FFT_venv\Scripts\activate
```

Pro plnou funkčnost je potřeba nainstalovat potřebné python knihovny, které jsou vypsané v `requirements.txt`.

Instalace potřebných knihoven: 
```bash
pip install -r requirements.txt
```

Spuštění aplikace:
```bash
python run.py
```