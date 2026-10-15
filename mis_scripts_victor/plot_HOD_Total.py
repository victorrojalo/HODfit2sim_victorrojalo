import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

RESULTS_DIR = "output"

hod_lista = []
mass_bins = None

print("Recolectando datos de HOD de los 64 archivos de Conformidad...")

for i in range(64):
    archivo = os.path.join(RESULTS_DIR, f"conformity_vol{i}.h5")
    
    if os.path.exists(archivo):
        try:
            with h5py.File(archivo, 'r') as f:
                # Extraemos los datos de los bines
                m_min = f['data/bins/M_min_bin'][:]
                n_cen = f['data/bins/N_C'][:]
                n_halos = f['data/bins/N_Halos'][:]
                
                if mass_bins is None:
                    # Guardamos el eje X (las masas en escala logarítmica)
                    mass_bins = m_min
                
                # Calculamos el HOD (N_Cen / N_Halos). 
                # np.where evita que dividamos por cero si N_Halos es 0.
                with np.errstate(divide='ignore', invalid='ignore'):
                    hod_vol = np.where(n_halos > 0, n_cen / n_halos, 0.0)
                    
                hod_lista.append(hod_vol)
        except Exception as e:
            print(f" [!] Error en volumen {i}: {e}")

# Convertimos a matriz para la estadística
hod_lista = np.array(hod_lista)
n_vols = len(hod_lista)

if n_vols == 0:
    print("🚨 Error crítico: No se encontraron datos para el HOD.")
    sys.exit()

print(f"¡Éxito! Promediando HOD de {n_vols} volúmenes...")

# --- ESTADÍSTICA (Media y Error) ---
mean_hod = np.mean(hod_lista, axis=0)
err_hod = np.std(hod_lista, axis=0) / np.sqrt(n_vols)

# --- CREACIÓN DE LA GRÁFICA ---
plt.figure(figsize=(9, 6))

# Pintamos la curva con barras de error
plt.errorbar(mass_bins, mean_hod, yerr=err_hod, fmt='-o', color='forestgreen', 
             capsize=4, linewidth=2, markersize=5, label='Media de 64 Volúmenes')

plt.title("Halo Occupation Distribution (HOD) - Galaxias Centrales", fontsize=15)
plt.xlabel(r"$\log_{10}(M_{\rm halo} \ / \ M_{\odot} h^{-1})$", fontsize=14)
plt.ylabel(r"$\langle N_{\rm cen} \rangle$", fontsize=15)

# Líneas grises punteadas de referencia en el 0 y en el 1 (Probabilidad máxima)
plt.axhline(1.0, color='gray', linestyle='--', alpha=0.7)
plt.axhline(0.0, color='gray', linestyle='--', alpha=0.7)

# Limites del eje Y (un poco por debajo de 0 y por encima de 1 para que "respire")
plt.ylim(-0.05, 0.11)

plt.grid(True, which="both", ls="--", alpha=0.4)
plt.legend(fontsize=12, loc='lower right')

GRAFICA_SALIDA = "Grafica_TFM_5_HOD_Promedio.png"
plt.savefig(GRAFICA_SALIDA, dpi=300, bbox_inches='tight')
print(f"¡Gráfica guardada como: {GRAFICA_SALIDA}!")
