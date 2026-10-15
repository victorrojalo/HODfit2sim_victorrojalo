import numpy as np
import matplotlib.pyplot as plt
import os

RESULTS_DIR = "output" # Asegúrate de que esta es la carpeta donde están tus txt
GRAFICA_SALIDA = "Grafica_2PCF_Media_Real.png"

# Listas para guardar las curvas de cada volumen
xi_real_normal = []
xi_real_shuffled = []
r_bins = None

print("Recolectando archivos 2PCF de los 64 volúmenes...")

for i in range(64):
    # Ojo a los nombres de los txt que vimos en tus logs
    f_normal = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_vol{i}_.txt")
    f_shuf = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_shuffled_vol{i}.txt")
    
    if os.path.exists(f_normal) and os.path.exists(f_shuf):
        d_norm = np.loadtxt(f_normal)
        d_shuf = np.loadtxt(f_shuf)
        
        # Guardamos el eje X (las distancias 'r') solo la primera vez
        if r_bins is None:
            r_bins = d_norm[:, 0]
            
        xi_real_normal.append(d_norm[:, 1])
        xi_real_shuffled.append(d_shuf[:, 1])

# Convertimos a matrices para la estadística
xi_real_normal = np.array(xi_real_normal)
xi_real_shuffled = np.array(xi_real_shuffled)
N_vols = len(xi_real_normal)

print(f"¡Éxito! Promediando {N_vols} volúmenes válidos...")

# Cálculos estadísticos: Media y Error Estándar (std / sqrt(N))
mean_norm = np.mean(xi_real_normal, axis=0)
err_norm = np.std(xi_real_normal, axis=0) / np.sqrt(N_vols)

mean_shuf = np.mean(xi_real_shuffled, axis=0)
err_shuf = np.std(xi_real_shuffled, axis=0) / np.sqrt(N_vols)

# --- CREACIÓN DE LA GRÁFICA ---
plt.figure(figsize=(9, 7))

# Dibujamos las curvas con barras de error
plt.errorbar(r_bins, mean_norm, yerr=err_norm, fmt='-o', color='black', label='Shark (Normal)', capsize=4)
plt.errorbar(r_bins, mean_shuf, yerr=err_shuf, fmt='--s', color='red', label='Shark (Shuffled)', capsize=4)

plt.title("Función de Correlación Espacial (Galaxias Centrales)", fontsize=15)
plt.xlabel(r"$r \ [h^{-1} \mathrm{Mpc}]$", fontsize=14)
plt.ylabel(r"$\xi(r)$", fontsize=14)

# Escala logarítmica para ver bien el clustering
plt.xscale('log')
plt.yscale('log')

plt.grid(True, which="both", ls="--", alpha=0.4)
plt.legend(fontsize=12)

plt.savefig(GRAFICA_SALIDA, dpi=300, bbox_inches='tight')
print(f"Gráfica terminada y guardada como: {GRAFICA_SALIDA}")
