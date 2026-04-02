#include <math.h>
#include <string.h>

#define PI 3.14159265358979323846

void calculated_dft(int N, double *in_real, double *in_imag, double *out_real, double *out_imag) {

    memset(out_real, 0, N * sizeof(double));
    memset(out_imag, 0, N * sizeof(double));

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