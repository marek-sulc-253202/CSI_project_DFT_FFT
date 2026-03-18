# Fourierova Transformace — Dashboard

Tato desktopová aplikace slouží k demonstraci, výpočtu a vizualizaci Diskrétní Fourierovy transformace (DFT) a Rychlé Fourierovy transformace (FFT). Umožňuje uživateli vygenerovat si složený signál na základě zadaných frekvencí a amplitud a následně porovnat výpočetní náročnost (čas a paměť) různých implementací algoritmů.

## 🌟 Hlavní funkce
* **Generátor signálu:** Vytvoření signálu až z 5 různých frekvenčních složek.
* **Vlastní implementace:** Výpočet DFT a FFT pomocí čistého Pythonu (s využitím i bez využití matematických knihoven `math`/`cmath`).
* **Numpy implementace:** Rychlý výpočet FFT pomocí optimalizované knihovny `numpy`.
* **Měření výkonu:** Srovnání výpočetního času (v ms) a paměťové náročnosti (v Kb) jednotlivých metod.
* **Vizualizace:** Vykreslení časového průběhu signálu a jeho frekvenčních spekter (DFT a FFT) s automatickým přizpůsobením os.

## 🚀 Instalace a spuštění

Projekt využívá moderní systém správy závislostí pomocí `pyproject.toml`. Pro bezpečné spuštění bez narušení tvého systému doporučujeme použít virtuální prostředí (venv).

### 1. Vytvoření virtuálního prostředí
Otevři terminál ve složce s projektem a zadej:
```bash
python3 -m venv venv