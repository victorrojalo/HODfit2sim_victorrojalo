import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import warnings

# Ignoramos avisos por si alguna caja lejana no tiene galaxias y da división por cero
warnings.filterwarnings("ignore")

RESULTS_DIR = "output"

ratios_real = []
ratios_red = []
r_bins = None

print("Calculando la señal de Conformidad Galáctica (Normal / Shuffled)...")

for i in range(64):
    f_real = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_vol{i}_.txt")
    f_real_shuf = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_shuffled_vol{i}.txt")
    f_red = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_redshift_vol{i}.txt")
    f_red_shuf = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_redshift_shuffled_vol{i}.txt")
    
    if os.path.exists(f_real) and os.path.exists(f_real_shuf) and os.path.exists(f_red) and os.path.exists(f_red_shuf):
        try:
            d_real = np.loadtxt(f_real, comments='#', delimiter=',')
            d_real_shuf = np.loadtxt(f_real_shuf, comments='#', delimiter=',')
            d_red = np.loadtxt(f_red, comments='#', delimiter=',')
            d_red_shuf = np.loadtxt(f_red_shuf, comments='#', delimiter=',')
            
            if r_bins is None:
                r_bins = d_real[:, 0]
            
            # Calculamos el ratio de ESTE volumen directamente
            # (Sumamos 1e-10 al denominador para evitar que Python colapse si hay un 0 absoluto)
            ratio_vol_real = d_real[:, 1] / (d_real_shuf[:, 1] + 1e-10)
            ratio_vol_red = d_red[:, 1] / (d_red_shuf[:, 1] + 1e-10)
            
            ratios_real.append(ratio_vol_real)
            ratios_red.append(ratio_vol_red)
            
        except Exception as e:
            print(f"  [!] Error en volumen {i}: {e}")

ratios_real = np.array(ratios_real)
ratios_red = np.array(ratios_red)

N_vols = len(ratios_real)
if N_vols == 0:
    print("🚨 Error: No se encontraron datos.")
    sys.exit()

print(f"¡Éxito! Promediando los ratios de {N_vols} volúmenes...")

# --- ESTADÍSTICA ---
mean_ratio_real = np.mean(ratios_real, axis=0)
err_ratio_real = np.std(ratios_real, axis=0) / np.sqrt(N_vols)

mean_ratio_red = np.mean(ratios_red, axis=0)
err_ratio_red = np.std(ratios_red, axis=0) / np.sqrt(N_vols)


# --- GRÁFICA DE DOS PANELES ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# Panel 1: Espacio Real
ax1.errorbar(r_bins, mean_ratio_real, yerr=err_ratio_real, fmt='-o', color='blue', capsize=4)
# Línea de referencia del 1.0 (No conformidad)
ax1.axhline(1.0, color='black', linestyle='--', linewidth=2)
ax1.set_title("Conformidad en Espacio Real", fontsize=14)
ax1.set_xlabel(r"$r \ [h^{-1} \mathrm{Mpc}]$", fontsize=13)
ax1.set_ylabel(r"$\xi_{\rm Normal} \ / \ \xi_{\rm Shuffled}$", fontsize=15)
ax1.set_xscale('log')
ax1.grid(True, which="both", ls="--", alpha=0.4)

# Panel 2: Espacio Redshift
ax2.errorbar(r_bins, mean_ratio_red, yerr=err_ratio_red, fmt='-s', color='red', capsize=4)
# Línea de referencia
ax2.axhline(1.0, color='black', linestyle='--', linewidth=2)
ax2.set_title("Conformidad en Espacio Redshift", fontsize=14)
ax2.set_xlabel(r"$s \ [h^{-1} \mathrm{Mpc}]$", fontsize=13)
ax2.set_xscale('log')
ax2.grid(True, which="both", ls="--", alpha=0.4)

plt.suptitle("Señal de Conformidad Galáctica (Galaxias Centrales)", fontsize=16, y=1.02)
plt.tight_layout()

# Ajustamos límites de Y para que se vea bien alrededor del 1 (puedes cambiarlos si tu señal es muy grande)
plt.ylim(0.5, 1.5) 

GRAFICA_SALIDA = "Grafica_TFM_4_Conformidad_Ratio.png"
plt.savefig(GRAFICA_SALIDA, dpi=300, bbox_inches='tight')
print(f"¡Gráfica guardada como: {GRAFICA_SALIDA}!")
