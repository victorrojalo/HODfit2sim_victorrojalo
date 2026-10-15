import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# --- 1. ESTILO PAPER ---
import mpl_style
plt.style.use(mpl_style.style1)

# --- 2. CARPETA DE DATOS ---
# 🚨 CAMBIO: Solo necesitamos leer de UNA carpeta, porque cada archivo 
# ya contiene las Centrales (N_C) y las Satélites (N_S).
DIR_DATOS = "output/Mvir/Corte6/Centrales"

hod_cen_lista = []
hod_sat_lista = []
hod_tot_lista = [] # <-- Descomentado para la línea Total
mass_bins = None

print("Recolectando datos de HOD de los 64 subvolúmenes...")

for i in range(64):
    archivo = os.path.join(DIR_DATOS, f"conformity_vol{i}.h5")

    if os.path.exists(archivo):
        try:
            # Leer el ÚNICO archivo
            with h5py.File(archivo, 'r') as f:
                m_min = f['data/bins/M_min_bin'][:]
                n_halos = f['data/bins/N_Halos'][:]
                
                # 🚨 CAMBIO CLAVE: Extraemos ambas poblaciones del mismo sitio
                n_cen = f['data/bins/N_C'][:]  # Centrales
                n_sat = f['data/bins/N_S'][:]  # Satélites

                if mass_bins is None:
                    mass_bins = m_min

            # Calcular HOD por volumen evitando división por cero
            with np.errstate(divide='ignore', invalid='ignore'):
                hod_vol_cen = np.where(n_halos > 0, n_cen / n_halos, 0.0)
                hod_vol_sat = np.where(n_halos > 0, n_sat / n_halos, 0.0)
                hod_vol_tot = hod_vol_cen + hod_vol_sat # <-- Descomentado

            hod_cen_lista.append(hod_vol_cen)
            hod_sat_lista.append(hod_vol_sat)
            hod_tot_lista.append(hod_vol_tot) # <-- Descomentado

        except Exception as e:
            print(f" [!] Error en volumen {i}: {e}")
    else:
        print(f" [!] Falta archivo del volumen {i} en la carpeta {DIR_DATOS}.")

# --- ESTADÍSTICA (Media y Error) ---
n_vols = len(hod_cen_lista)
if n_vols == 0:
    print("🚨 Error crítico: No se encontraron datos para promediar.")
    sys.exit()

print(f"¡Éxito! Promediando HOD de {n_vols} volúmenes para Centrales, Satélites y Total...")

# Convertir a matrices
hod_cen_lista = np.array(hod_cen_lista)
hod_sat_lista = np.array(hod_sat_lista)
hod_tot_lista = np.array(hod_tot_lista) # <-- Descomentado

# Calcular medias
mean_cen = np.mean(hod_cen_lista, axis=0)
mean_sat = np.mean(hod_sat_lista, axis=0)
mean_tot = np.mean(hod_tot_lista, axis=0) # <-- Descomentado

# Calcular errores estándar de la media
err_cen = np.std(hod_cen_lista, axis=0) / np.sqrt(n_vols)
err_sat = np.std(hod_sat_lista, axis=0) / np.sqrt(n_vols)
err_tot = np.std(hod_tot_lista, axis=0) / np.sqrt(n_vols) # <-- Descomentado

# --- CREACIÓN DE LA GRÁFICA ---
plt.figure() # El tamaño ya viene dictado por mpl_style.style1

# Enmascaramos los ceros para que la escala logarítmica no dé problemas
mask_cen = mean_cen > 0
mask_sat = mean_sat > 0
mask_tot = mean_tot > 0 # <-- Descomentado

# Pintamos Centrales
plt.errorbar(mass_bins[mask_cen], mean_cen[mask_cen], yerr=err_cen[mask_cen],
             fmt='--o', color='#1f77b4', markersize=5, label='Centrales')

# Pintamos Satélites
plt.errorbar(mass_bins[mask_sat], mean_sat[mask_sat], yerr=err_sat[mask_sat],
             fmt='-.s', color='#ff7f0e', markersize=5, label='Satélites')

# Pintamos Total
plt.errorbar(mass_bins[mask_tot], mean_tot[mask_tot], yerr=err_tot[mask_tot],
             fmt='-D', color='black', markersize=4, label='Total')

plt.title("Halo Occupation Distribution (HOD) - ELGs")
# Como m_min ya es log10(M), no usamos plt.xscale('log')
plt.xlabel(r"$\log_{10}(M_{\rm halo} \ / \ M_{\odot} h^{-1})$")

# El eje Y sí debe ir en logaritmo para ver bien las satélites
plt.yscale('log')
plt.ylabel(r"$\langle N_{\rm gal} \rangle$")

# Límites típicos para HOD de ELGs. Ajusta el Y según veas tus datos
plt.xlim(10.5, 14.5)
plt.ylim(1e-3, 5)

plt.axhline(1.0, color='gray', linestyle=':', alpha=0.7) #marca límite para las centrales

plt.legend(loc='lower right')

GRAFICA_SALIDA = "Grafica_TFM_8_HOD_Promedio_Completa_Corte6.png"
plt.savefig(GRAFICA_SALIDA)
print(f"¡Gráfica guardada como: {GRAFICA_SALIDA}!")
