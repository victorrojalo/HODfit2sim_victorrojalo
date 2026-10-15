import numpy as np
import matplotlib.pyplot as plt
import os

RESULTS_DIR = "output"

# Listas para guardar las 4 curvas de los 64 volúmenes
xi_real, xi_real_shuf = [], []
xi_red, xi_red_shuf = [], []
r_bins = None

print("Recolectando todos los archivos 2PCF de los 64 volúmenes...")

# 1. Bucle de lectura
for i in range(64):
    f_real = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_vol{i}_.txt")
    f_real_shuf = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_shuffled_vol{i}.txt")
    f_red = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_redshift_vol{i}.txt")
    f_red_shuf = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_redshift_shuffled_vol{i}.txt")
    
    # Solo intentamos leer si existen TODOS los archivos de ese volumen
    if os.path.exists(f_real) and os.path.exists(f_real_shuf) and os.path.exists(f_red) and os.path.exists(f_red_shuf):
        try:
            d_real = np.loadtxt(f_real)
            d_real_shuf = np.loadtxt(f_real_shuf)
            d_red = np.loadtxt(f_red)
            d_red_shuf = np.loadtxt(f_red_shuf)
            
            if r_bins is None:
                r_bins = d_real[:, 0] # Guardamos el eje X
                
            xi_real.append(d_real[:, 1])
            xi_real_shuf.append(d_real_shuf[:, 1])
            xi_red.append(d_red[:, 1])
            xi_red_shuf.append(d_red_shuf[:, 1])
        except:
            pass

# Convertimos a matrices de numpy
xi_real = np.array(xi_real)
xi_real_shuf = np.array(xi_real_shuf)
xi_red = np.array(xi_red)
xi_red_shuf = np.array(xi_red_shuf)

N_vols = len(xi_real)
print(f"¡Éxito! Promediando {N_vols} volúmenes válidos...")

# 2. Matemáticas (Medias y Errores Estándar)
def calcular_stats(matriz):
    mean = np.mean(matriz, axis=0)
    err = np.std(matriz, axis=0) / np.sqrt(N_vols)
    return mean, err

mean_real, err_real = calcular_stats(xi_real)
mean_real_shuf, err_real_shuf = calcular_stats(xi_real_shuf)
mean_red, err_red = calcular_stats(xi_red)
mean_red_shuf, err_red_shuf = calcular_stats(xi_red_shuf)

# El Factor Kaiser es la división entre Redshift y Real
kaiser_ratio = mean_red / mean_real
# Propagación de errores básica para la división
kaiser_err = kaiser_ratio * np.sqrt((err_red/mean_red)**2 + (err_real/mean_real)**2)

# =========================================================
# GRÁFICA 1: ESPACIO REAL
# =========================================================
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

# =========================================================
# GRÁFICA 2: ESPACIO REDSHIFT
# =========================================================
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

# =========================================================
# GRÁFICA 3: DISTORSIÓN DE KAISER
# =========================================================
print("Generando Gráfica 3: Efecto Kaiser...")
plt.figure(figsize=(8, 6))
plt.errorbar(r_bins, kaiser_ratio, yerr=kaiser_err, fmt='-o', color='purple', capsize=3)
# Línea horizontal en 1.0 de referencia
plt.axhline(1.0, color='gray', linestyle='--')

plt.title("Efecto Kaiser (Espacio Redshift / Espacio Real)", fontsize=14)
plt.xlabel(r"Distancia \ $[h^{-1} \mathrm{Mpc}]$", fontsize=13)
plt.ylabel(r"$\xi(s) / \xi(r)$", fontsize=13)
plt.xscale('log')
plt.ylim(0.5, 2.0) # El factor de Kaiser suele estar cerca de 1.2 o 1.4
plt.grid(True, which="both", ls="--", alpha=0.4)
plt.savefig("Grafica_TFM_3_Kaiser_Ratio.png", dpi=300, bbox_inches='tight')
plt.close()

print("¡Proceso completado! Tienes las 3 gráficas listas en la carpeta.")
