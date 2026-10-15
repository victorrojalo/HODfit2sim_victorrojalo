import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 1. ESTILO ---
import mpl_style
plt.style.use(mpl_style.style1)

BASE_DIR = "output/Mvir"
CORTES = [5, 6, 7, 8]
colores = {5: '#1f77b4', 6: '#ff7f0e', 7: '#2ca02c', 8: '#d62728'}

plt.figure(figsize=(10, 8))

for corte in CORTES:
    DIR_DATOS = os.path.join(BASE_DIR, f"Corte{corte}", "Centrales")
    
    # INICIALIZAMOS HUCHAS A CERO
    sum_n_halos = None
    sum_n_cen = None
    sum_n_sat = None
    mass_bins = None

    for i in range(64):
        archivo = os.path.join(DIR_DATOS, f"conformity_vol{i}.h5")
        if os.path.exists(archivo):
            with h5py.File(archivo, 'r') as f:
                n_h = f['data/bins/N_Halos'][:]
                n_c = f['data/bins/N_C'][:]
                n_s = f['data/bins/N_S'][:]
                
                if sum_n_halos is None:
                    mass_bins = f['data/bins/M_min_bin'][:]
                    sum_n_halos = np.zeros_like(n_h, dtype=float)
                    sum_n_cen = np.zeros_like(n_h, dtype=float)
                    sum_n_sat = np.zeros_like(n_h, dtype=float)
                
                # ¡SUMAMOS TODO EL UNIVERSO!
                sum_n_halos += n_h
                sum_n_cen += n_c
                sum_n_sat += n_s

    # AHORA DIVIDIMOS UNA SOLA VEZ AL FINAL
    with np.errstate(divide='ignore', invalid='ignore'):
        mean_cen = np.where(sum_n_halos > 0, sum_n_cen / sum_n_halos, 0.0)
        mean_sat = np.where(sum_n_halos > 0, sum_n_sat / sum_n_halos, 0.0)
        mean_tot = mean_cen + mean_sat

    mask = sum_n_halos > 0
    plt.plot(mass_bins[mask], mean_tot[mask], '-', color=colores[corte], label=f'Total Corte {corte}')
    plt.plot(mass_bins[mask], mean_cen[mask], '--', color=colores[corte], alpha=0.5)
    plt.plot(mass_bins[mask], mean_sat[mask], ':', color=colores[corte], alpha=0.5)

plt.axhline(1.0, color='black', linewidth=1, alpha=0.3)
plt.yscale('log')
plt.ylim(1e-3, 10)
plt.xlim(10.5, 14.5)
plt.xlabel(r"$\log_{10}(M_{\rm halo} \ / \ M_{\odot} h^{-1})$")
plt.ylabel(r"$\langle N \rangle$")
plt.legend(ncol=2, fontsize=9)
plt.savefig("HOD_Super_Cortes_CORREGIDA.png", dpi=300)
