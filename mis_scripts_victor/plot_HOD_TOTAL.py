import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# --- 1. ESTILO PAPER ---
import mpl_style
plt.style.use(mpl_style.style1)

# --- 2. CARPETAS DE DATOS ---
# Pon aquí el nombre de las carpetas donde tienes los 64 archivos de cada ejecución
DIR_CEN = "output/Mvir/Corte1/Centrales" 
DIR_SAT = "output/Mvir/Corte1/Satelites"

hod_cen_lista = []
hod_sat_lista = []
#hod_tot_lista = []
mass_bins = None

print("Recolectando datos de HOD de los 64 subvolúmenes...")

for i in range(64):
    archivo_cen = os.path.join(DIR_CEN, f"conformity_vol{i}.h5")
    archivo_sat = os.path.join(DIR_SAT, f"conformity_vol{i}.h5")

    if os.path.exists(archivo_cen) and os.path.exists(archivo_sat):
        try:
            # Leer Centrales
            with h5py.File(archivo_cen, 'r') as f_cen:
                m_min = f_cen['data/bins/M_min_bin'][:]
                n_cen = f_cen['data/bins/N_C'][:]
                n_halos_cen = f_cen['data/bins/N_Halos'][:]
                
                if mass_bins is None:
                    mass_bins = m_min

            # Leer Satélites (suponiendo que la variable internamente se sigue llamando N_C)
            with h5py.File(archivo_sat, 'r') as f_sat:
                n_sat = f_sat['data/bins/N_C'][:]
                n_halos_sat = f_sat['data/bins/N_Halos'][:]

            # Calcular HOD por volumen evitando división por cero
            with np.errstate(divide='ignore', invalid='ignore'):
                hod_vol_cen = np.where(n_halos_cen > 0, n_cen / n_halos_cen, 0.0)
                hod_vol_sat = np.where(n_halos_sat > 0, n_sat / n_halos_sat, 0.0)
                #hod_vol_tot = hod_vol_cen + hod_vol_sat

            hod_cen_lista.append(hod_vol_cen)
            hod_sat_lista.append(hod_vol_sat)
            #hod_tot_lista.append(hod_vol_tot)

        except Exception as e:
            print(f" [!] Error en volumen {i}: {e}")
    else:
        print(f" [!] Faltan archivos del volumen {i} en alguna de las carpetas.")

# --- ESTADÍSTICA (Media y Error) ---
n_vols = len(hod_cen_lista)
if n_vols == 0:
    print("🚨 Error crítico: No se encontraron datos para promediar.")
    sys.exit()

print(f"¡Éxito! Promediando HOD de {n_vols} volúmenes para Centrales y Satélites...")

# Convertir a matrices
hod_cen_lista = np.array(hod_cen_lista)
hod_sat_lista = np.array(hod_sat_lista)
#hod_tot_lista = np.array(hod_tot_lista)

# Calcular medias
mean_cen = np.mean(hod_cen_lista, axis=0)
mean_sat = np.mean(hod_sat_lista, axis=0)
#mean_tot = np.mean(hod_tot_lista, axis=0)

# Calcular errores estándar de la media
err_cen = np.std(hod_cen_lista, axis=0) / np.sqrt(n_vols)
err_sat = np.std(hod_sat_lista, axis=0) / np.sqrt(n_vols)
#err_tot = np.std(hod_tot_lista, axis=0) / np.sqrt(n_vols)

# --- CREACIÓN DE LA GRÁFICA ---
plt.figure() # El tamaño ya viene dictado por mpl_style.style1

# Enmascaramos los ceros para que la escala logarítmica no dé problemas
mask_cen = mean_cen > 0
mask_sat = mean_sat > 0
#mask_tot = mean_tot > 0

# Pintamos Centrales
plt.errorbar(mass_bins[mask_cen], mean_cen[mask_cen], yerr=err_cen[mask_cen], 
             fmt='--o', color='#1f77b4', markersize=5, label='Centrales')

# Pintamos Satélites
plt.errorbar(mass_bins[mask_sat], mean_sat[mask_sat], yerr=err_sat[mask_sat], 
             fmt='-.s', color='#ff7f0e', markersize=5, label='Satélites')

# Pintamos Total
#plt.errorbar(mass_bins[mask_tot], mean_tot[mask_tot], yerr=err_tot[mask_
             #fmt='-D', color='black', markersize=4, label='Total')

plt.title("Halo Occupation Distribution (HOD) - ELGs")
# Como m_min ya es log10(M), no usamos plt.xscale('log')
plt.xlabel(r"$\log_{10}(M_{\rm halo} \ / \ M_{\odot} h^{-1})$")

# El eje Y sí debe ir en logaritmo para ver bien las satélites
plt.yscale('log')
plt.ylabel(r"$\langle N_{\rm gal} \rangle$")

# Límites típicos para HOD de ELGs. Ajusta el Y según veas tus datos
plt.xlim(10.5, 14.5)
plt.ylim(1e-3, 5) 

plt.axhline(1.0, color='gray', linestyle=':', alpha=0.7)

plt.legend(loc='lower right')

GRAFICA_SALIDA = "Grafica_TFM_8_HOD_Promedio_Completa.png"
plt.savefig(GRAFICA_SALIDA)
print(f"¡Gráfica guardada como: {GRAFICA_SALIDA}!")
