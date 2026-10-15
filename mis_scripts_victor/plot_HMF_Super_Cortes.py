import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
import mpl_style

plt.style.use(mpl_style.style1)

CORTES = [5, 6, 7, 8]
COLORES = {5: '#1f77b4', 6: '#ff7f0e', 7: '#2ca02c', 8: '#d62728'} 

BASE_DIR = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/output/Mvir"
ROCKSTAR_FILE = "/home2/vgonzalez/Data/Rockstar/SU1/outp_87.list"
VOLUMEN = 250.0**3

plt.figure(figsize=(10, 7))
print("🚀 Iniciando Súper-Script HMF...")

# 1. --- PINTAR MATERIA OSCURA (ROCKSTAR) DE FONDO ---
print("Cargando Rockstar (puede tardar unos segundos)...")
try:
    rockstar_data = np.loadtxt(ROCKSTAR_FILE, skiprows=1, comments='#', usecols=(2, 40))
    mvir_todos = rockstar_data[:, 0]
    pid_todos = rockstar_data[:, 1]
    mvir_principales = mvir_todos[pid_todos == -1]
    log_mvir = np.log10(mvir_principales)
    
    # Usamos bins genéricos del 10.5 al 14.5
    edges_mvir = np.linspace(10.5, 14.5, 71)
    mass_mvir = (edges_mvir[:-1] + edges_mvir[1:]) / 2.0
    dlogM = edges_mvir[1] - edges_mvir[0]
    
    hist_total, _ = np.histogram(log_mvir, bins=edges_mvir)
    phi_total = hist_total / (VOLUMEN * dlogM)
    mask_tot = phi_total > 0
    
    plt.plot(mass_mvir[mask_tot], np.log10(phi_total[mask_tot]), '--', color='black',
             linewidth=2, alpha=0.6, label=r'Halos Anfitriones (Rockstar)')
except Exception as e:
    print(f"⚠️ Error cargando Rockstar: {e}")

# 2. --- BUCLE PARA CENTRALES Y SATÉLITES DE CADA CORTE ---
for corte in CORTES:
    # --- CENTRALES ---
    FILE_CEN = os.path.join(BASE_DIR, f"Corte{corte}", "Centrales", f"HMF_TOTAL_Mvir_Shark_Corte{corte}_Centrales_COMPLETO.h5")
    if os.path.exists(FILE_CEN):
        with h5py.File(FILE_CEN, 'r') as f:
            edges = f['bin_edges'][:]
            mass = (edges[:-1] + edges[1:]) / 2.0
            phi = f['phi'][:]
        mask = phi > 0
        plt.plot(mass[mask], np.log10(phi[mask]), linestyle='-', color=COLORES[corte], 
                 linewidth=2, label=f'Centrales Corte {corte}')
    
    # --- SATÉLITES ---
    FILE_SAT = os.path.join(BASE_DIR, f"Corte{corte}", "Satelites", f"HMF_TOTAL_Mvir_Shark_Corte{corte}_Satelites_COMPLETO.h5")
    if os.path.exists(FILE_SAT):
        with h5py.File(FILE_SAT, 'r') as f:
            edges = f['bin_edges'][:]
            mass = (edges[:-1] + edges[1:]) / 2.0
            phi = f['phi'][:]
        mask = phi > 0
        plt.plot(mass[mask], np.log10(phi[mask]), linestyle=':', color=COLORES[corte], 
                 linewidth=2, marker='x', markersize=4, label=f'Satélites Corte {corte}')
    else:
        print(f"  -> (Sin datos de Satélites para el Corte {corte} aún)")

# --- MAQUILLAJE ---
plt.title("HMF: Halos vs ELGs Centrales y Satélites")
plt.xlabel(r"$\log_{10}(M_{\rm halo} \ / \ M_{\odot} h^{-1})$")
plt.ylabel(r"$\log_{10}(\Phi)$")
plt.xlim(10.5, 14.5)
# Ajustamos los límites de la Y para que quepa bien todo
plt.ylim(-6.5, -1.0) 

# Ponemos la leyenda en 2 columnas para que no ocupe toda la gráfica
plt.legend(loc='upper right', fontsize=9, ncol=2)

GRAFICA_SALIDA = os.path.join(BASE_DIR, "Grafica_TFM_SUPER_HMF_Completa.png")
plt.savefig(GRAFICA_SALIDA, dpi=300)
print(f"🎉 ¡Súper Gráfica HMF guardada en: {GRAFICA_SALIDA}!")
