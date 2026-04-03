// Import knihoven.
#include <math.h>
#include <string.h>

// Deklarace konstanty PI.
#define PI 3.14159265358979323846

// Funkce pro výpočet DFT.
void calculate_dft_c(int N, double *in_real, double *in_imag, double *out_real, double *out_imag) {

    // Tohle by se nemuselo dělat ale je to tu pro ověření, že pole jsou polná nul.
    // V podstatě to pro ty pole alokuje paměť pro N čísel typu double a všechny jsou 0.
    memset(out_real, 0, N * sizeof(double));
    memset(out_imag, 0, N * sizeof(double));

    // Dva vnořené for cykly pro výpočet samotného DFT.
    for (int k = 0; k < N; k++){
        for (int n = 0; n < N; n++){
            double angle = 2.0 * PI * k * n / N;
            
            double cos_val = cos(angle);
            double sin_val = sin(angle); 
            
            out_real[k] += (in_real[n] * cos_val) + (in_imag[n] * sin_val);
            out_imag[k] += (in_imag[n] * cos_val) - (in_real[n] * sin_val);
        }
    }
}