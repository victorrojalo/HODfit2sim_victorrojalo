import numpy as np
import matplotlib.pyplot as plt
import os
import sys

RESULTS_DIR = "output"

xi_real, xi_real_shuf = [], []
xi_red, xi_red_shuf = [], []
r_bins = None

print("Recolectando todos los archivos 2PCF de los 64 volúmenes...")

for i in range(64):
    f_real = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_vol{i}_.txt")
    f_real_shuf = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_shuffled_vol{i}.txt")
    f_red = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_redshift_vol{i}.txt")
    f_red_shuf = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_redshift_shuffled_vol{i}.txt")
    
    if os.path.exists(f_real) and os.path.exists(f_real_shuf) and os.path.exists(f_red) and os.path.exists(f_red_shuf):
        try:
            # MAGIA AQUÍ: Intentamos leer saltando la cabecera si la hay (skiprows=1) 
            # y usando comments='#' por si acaso
            d_real = np.loadtxt(f_real, comments='#', delimiter=',')
            d_real_shuf = np.loadtxt(f_real_shuf, comments='#', delimiter=',')
            d_red = np.loadtxt(f_red, comments='#', delimiter=',')
            d_red_shuf = np.loadtxt(f_red_shuf, comments='#', delimiter=',')
            
            if r_bins is None:
                r_bins = d_real[:, 0]
                
            xi_real.append(d_real[:, 1])
            xi_real_shuf.append(d_real_shuf[:, 1])
            xi_red.append(d_red[:, 1])
            xi_red_shuf.append(d_red_shuf[:, 1])
            
        except Exception as e:
            # ¡El CHIVATO! Si algo falla, que nos lo diga por pantalla
            print(f"  [!] Error al leer los datos del volumen {i}: {e}")

# Convertimos a matrices
xi_real, xi_real_shuf = np.array(xi_real), np.array(xi_real_shuf)
xi_red, xi_red_shuf = np.array(xi_red), np.array(xi_red_shuf)

N_vols = len(xi_real)

# PARADA DE EMERGENCIA
if N_vols == 0:
    print("\n🚨 ERROR CRÍTICO: No se ha podido leer ningún dato.")
    sys.exit()

print(f"¡Éxito! Promediando {N_vols} volúmenes válidos...")

def calcular_stats(matriz):
    mean = np.mean(matriz, axis=0)
    err = np.std(matriz, axis=0) / np.sqrt(N_vols)
    return mean, err

mean_real, err_real = calcular_stats(xi_real)
mean_real_shuf, err_real_shuf = calcular_stats(xi_real_shuf)
mean_red, err_red = calcular_stats(xi_red)
mean_red_shuf, err_red_shuf = calcular_stats(xi_red_shuf)

kaiser_ratio = mean_red / mean_real
#kaiser_err = kaiser_ratio * np.abs((err_red/mean_red)**2 + (err_real/mean_real)**2)
kaiser_err = np.abs(kaiser_ratio) * np.sqrt((err_red/mean_red)**2 + (err_real/mean_real)**2)
# --- GRÁFICA 1 ---
print("Generando Gráfica 1: Espacio Real...")
plt.figure(figsize=(8, 6))
plt.errorbar(r_bins, mean_real, yerr=err_real, fmt='-o', color='black', label='Catálogo Normal', capsize=3)
plt.errorbar(r_bins, mean_real_shuf, yerr=err_real_shuf, fmt='--s', color='red', label='Catálogo Barajado (Shuffled)', capsize=3)
plt.title("Función de Correlación: Espacio Real (Centrales)", fontsize=14)
plt.xlabel(r"$r \ [h^{-1} \mathrm{Mpc}]$", fontsize=13)
plt.ylabel(r"$\xi(r)$", fontsize=13)
plt.xscale('log')
plt.yscale('log')
plt.grid(True, which="both", ls="--", alpha=0.4)
plt.legend(fontsize=12)
plt.savefig("Grafica_TFM_1_2PCF_Real.png", dpi=300, bbox_inches='tight')
plt.close()

# --- GRÁFICA 2 ---
print("Generando Gráfica 2: Espacio Redshift...")
plt.figure(figsize=(8, 6))
plt.errorbar(r_bins, mean_red, yerr=err_red, fmt='-o', color='black', label='Catálogo Normal', capsize=3)
plt.errorbar(r_bins, mean_red_shuf, yerr=err_red_shuf, fmt='--s', color='blue', label='Catálogo Barajado (Shuffled)', capsize=3)
plt.title("Función de Correlación: Espacio Redshift (Centrales)", fontsize=14)
plt.xlabel(r"$s \ [h^{-1} \mathrm{Mpc}]$", fontsize=13)
plt.ylabel(r"$\xi(s)$", fontsize=13)
plt.xscale('log')
plt.yscale('log')
plt.grid(True, which="both", ls="--", alpha=0.4)
plt.legend(fontsize=12)
plt.savefig("Grafica_TFM_2_2PCF_Redshift.png", dpi=300, bbox_inches='tight')
plt.close()

# --- GRÁFICA 3 ---
print("Generando Gráfica 3: Efecto Kaiser...")
plt.figure(figsize=(8, 6))
plt.errorbar(r_bins, kaiser_ratio, yerr=kaiser_err, fmt='-o', color='purple', capsize=3)
plt.axhline(1.0, color='gray', linestyle='--')
plt.title("Efecto Kaiser (Espacio Redshift / Espacio Real)", fontsize=14)
plt.xlabel(r"Distancia \ $[h^{-1} \mathrm{Mpc}]$", fontsize=13)
plt.ylabel(r"$\xi(s) / \xi(r)$", fontsize=13)
plt.xscale('log')
plt.ylim(0.5, 2.0)
plt.grid(True, which="both", ls="--", alpha=0.4)
plt.savefig("Grafica_TFM_3_Kaiser_Ratio.png", dpi=300, bbox_inches='tight')
plt.close()

print("¡Proceso completado con éxito!")
