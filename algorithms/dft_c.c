// Import knihoven.
#include <math.h>
#include <string.h>

// Definice konstanty PI.
#define PI 3.14159265358979323846

// Funkce pro výpočet DFT.
void calculate_dft_c(int N, double *in_real, double *in_imag, double *out_real, double *out_imag) {

    // Nastavení paměťi pro pole o velikosti N čísel typu dobule, která jsou všechny 0.
    memset(out_real, 0, N * sizeof(double));
    memset(out_imag, 0, N * sizeof(double));

    // Dva vnořené for cykly pro výpočet samotného DFT.
    for (int k = 0; k < N; k++){
        for (int n = 0; n < N; n++){
            // Výpočet fáze (úhlu) pro aktuální vzorek podle Eulerova vzorce
            double angle = 2.0 * PI * k * n / N;
            
            double cos_val = cos(angle);
            double sin_val = sin(angle); 
            
            // Násobení komplexních čísel a suma výsledku do výstupních polí
            // Odpovídá matematickému zápisu: X[k] += x[n] * e^(-j * 2*pi*k*n/N)
            out_real[k] += (in_real[n] * cos_val) + (in_imag[n] * sin_val);
            out_imag[k] += (in_imag[n] * cos_val) - (in_real[n] * sin_val);
        }
    }
}