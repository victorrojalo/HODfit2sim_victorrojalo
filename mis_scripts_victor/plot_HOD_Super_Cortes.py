import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import mpl_style

plt.style.use(mpl_style.style1)

# Configuramos los cortes que queremos iterar y sus colores para que quede visual
CORTES = [5, 6, 7, 8]
COLORES = {5: '#1f77b4', 6: '#ff7f0e', 7: '#2ca02c', 8: '#d62728'} # Azul, Naranja, Verde, Rojo
MARCADORES = {5: 'o', 6: 's', 7: '^', 8: 'D'}

BASE_DIR = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/output/Mvir"

plt.figure(figsize=(8, 6))
print("🚀 Iniciando Súper-Script HOD...")

for corte in CORTES:
    DIR_DATOS = os.path.join(BASE_DIR, f"Corte{corte}", "Centrales")
    
    hod_cen_lista = []
    mass_bins = None

    # Recolectamos los 64 volúmenes de este corte
    for i in range(64):
        archivo = os.path.join(DIR_DATOS, f"conformity_vol{i}.h5")
        if os.path.exists(archivo):
            with h5py.File(archivo, 'r') as f:
                if mass_bins is None:
                    mass_bins = f['data/bins/M_min_bin'][:]
                n_halos = f['data/bins/N_Halos'][:]
                n_cen = f['data/bins/N_C'][:]  
                
                with np.errstate(divide='ignore', invalid='ignore'):
                    hod_vol_cen = np.where(n_halos > 0, n_cen / n_halos, 0.0)
                hod_cen_lista.append(hod_vol_cen)

    # Si ha encontrado datos, calculamos la media y dibujamos
    if len(hod_cen_lista) > 0:
        print(f"✅ Corte {corte}: Promediados {len(hod_cen_lista)} volúmenes.")
        hod_cen_lista = np.array(hod_cen_lista)
        mean_cen = np.mean(hod_cen_lista, axis=0)
        err_cen = np.std(hod_cen_lista, axis=0) / np.sqrt(len(hod_cen_lista))
        
        mask = mean_cen > 0
        plt.errorbar(mass_bins[mask], mean_cen[mask], yerr=err_cen[mask],
                     fmt=f'--{MARCADORES[corte]}', color=COLORES[corte], 
                     markersize=5, label=r'$log_{10}(L_{\rm bol})=$')
    else:
        print(f"⚠️ Aviso: No se encontraron datos para el Corte {corte}")

# --- MAQUILLAJE ---
plt.title("Evolución de la HOD (Centrales) según Corte Límite")
plt.xlabel(r"$\log_{10}(M_{\rm halo} \ / \ M_{\odot} h^{-1})$")
plt.yscale('log')
plt.ylabel(r"$\langle N_{\rm gal} \rangle$")
plt.xlim(10.5, 14.5)
plt.ylim(1e-3, 5)
plt.axhline(1.0, color='gray', linestyle=':', alpha=0.7) 
plt.legend(loc='lower right', fontsize=10)

GRAFICA_SALIDA = os.path.join(BASE_DIR, "Grafica_TFM_SUPER_HOD_Cortes_5678.png")
plt.savefig(GRAFICA_SALIDA, dpi=300)
print(f"🎉 ¡Súper Gráfica HOD guardada en: {GRAFICA_SALIDA}!")
