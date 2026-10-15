import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# --- 1. ESTILO PAPER ---
import mpl_style
plt.style.use(mpl_style.style1)

# --- 2. CARPETA DE DATOS ---
DIR_DATOS = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/output/Mvir/Corte5/Centrales"

hod_cen_lista = []
hod_sat_lista = []
hod_tot_lista = [] 
mass_bins = None

print("Recolectando datos de HOD de los 64 subvolúmenes...")

for i in range(64):
    archivo = os.path.join(DIR_DATOS, f"conformity_vol{i}.h5")

    if os.path.exists(archivo):
        try:
            with h5py.File(archivo, 'r') as f:
                m_min = f['data/bins/M_min_bin'][:]
                n_halos = f['data/bins/N_Halos'][:]

                n_cen = f['data/bins/N_C'][:]  # Centrales
                n_sat = f['data/bins/N_S'][:]  # Satélites

                if mass_bins is None:
                    mass_bins = m_min

            # Calcular HOD por volumen evitando división por cero
            with np.errstate(divide='ignore', invalid='ignore'):
                hod_vol_cen = np.where(n_halos > 0, n_cen / n_halos, 0.0)
                hod_vol_sat = np.where(n_halos > 0, n_sat / n_halos, 0.0)
                hod_vol_tot = hod_vol_cen + hod_vol_sat 

            hod_cen_lista.append(hod_vol_cen)
            hod_sat_lista.append(hod_vol_sat)
            hod_tot_lista.append(hod_vol_tot) 

        except Exception as e:
            print(f" [!] Error en volumen {i}: {e}")
    # else:
    #     print(f" [!] Falta archivo del volumen {i} (Normal si no lo corriste).")

# --- ESTADÍSTICA (Media y Error) ---
n_vols = len(hod_cen_lista)
if n_vols == 0:
    print("🚨 Error crítico: No se encontraron datos para promediar.")
    sys.exit()

print(f"¡Éxito! Promediando HOD de {n_vols} volúmenes...")

hod_cen_lista = np.array(hod_cen_lista)
hod_sat_lista = np.array(hod_sat_lista)
hod_tot_lista = np.array(hod_tot_lista) 

mean_cen = np.mean(hod_cen_lista, axis=0)
mean_sat = np.mean(hod_sat_lista, axis=0)
mean_tot = np.mean(hod_tot_lista, axis=0) 

err_cen = np.std(hod_cen_lista, axis=0) / np.sqrt(n_vols)
err_sat = np.std(hod_sat_lista, axis=0) / np.sqrt(n_vols)
err_tot = np.std(hod_tot_lista, axis=0) / np.sqrt(n_vols) 

# --- CREACIÓN DE LA GRÁFICA ---
plt.figure()

mask_cen = mean_cen > 0
mask_sat = mean_sat > 0
mask_tot = mean_tot > 0 

# Centrales
plt.errorbar(mass_bins[mask_cen], mean_cen[mask_cen], yerr=err_cen[mask_cen],
             fmt='--o', color='#1f77b4', markersize=5, label='Centrales')

# Satélites (No te asustes si no sale, ¡es porque los datos actuales solo tienen centrales!)
if np.any(mask_sat):
    plt.errorbar(mass_bins[mask_sat], mean_sat[mask_sat], yerr=err_sat[mask_sat],
                 fmt='-.s', color='#ff7f0e', markersize=5, label='Satélites')

# Total
plt.errorbar(mass_bins[mask_tot], mean_tot[mask_tot], yerr=err_tot[mask_tot],
             fmt='-D', color='black', markersize=4, label='Total')

plt.title("Halo Occupation Distribution (HOD) - Corte 5")
plt.xlabel(r"$\log_{10}(M_{\rm halo} \ / \ M_{\odot} h^{-1})$")
plt.yscale('log')
plt.ylabel(r"$\langle N_{\rm gal} \rangle$")

plt.xlim(10.5, 14.5)
plt.ylim(1e-3, 5)

plt.axhline(1.0, color='gray', linestyle=':', alpha=0.7) 

plt.legend(loc='lower right')

GRAFICA_SALIDA = os.path.join(DIR_DATOS, "Grafica_TFG_HOD_Promedio_Corte5_FINAL.png")
plt.savefig(GRAFICA_SALIDA)
print(f"¡Gráfica guardada como: {GRAFICA_SALIDA}!")
