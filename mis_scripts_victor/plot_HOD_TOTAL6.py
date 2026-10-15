import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 1. ESTILO PAPER ---
import mpl_style
plt.style.use(mpl_style.style1)

BASE_DIR = "output/Mvir"
CORTES = [5, 6, 7, 8]
COLORES = {5: '#1f77b4', 6: '#ff7f0e', 7: '#2ca02c', 8: '#d62728'}
LABELS = {5: '42.0', 6: '43.0', 7: '45.0', 8: '45.5'}

plt.figure(figsize=(10, 8))

for corte in CORTES:
    DIR_DATOS = os.path.join(BASE_DIR, f"Corte{corte}", "Centrales")
    
    # --- ESTO ES LA HUCHA GLOBAL ---
    # Inicializamos a None para capturar el tamaño del array en el primer archivo
    sum_halos = None
    sum_cen = None
    sum_sat = None
    mass_bins = None

    print(f"📦 Procesando Corte {corte} (Sumando 64 subvolúmenes)...")

    for i in range(64):
        archivo = os.path.join(DIR_DATOS, f"conformity_vol{i}.h5")
        if os.path.exists(archivo):
            try:
                with h5py.File(archivo, 'r') as f:
                    n_h = f['data/bins/N_Halos'][:]
                    n_c = f['data/bins/N_C'][:]
                    n_s = f['data/bins/N_S'][:]
                    
                    if sum_halos is None:
                        mass_bins = f['data/bins/M_min_bin'][:]
                        sum_halos = np.zeros_like(n_h, dtype=float)
                        sum_cen = np.zeros_like(n_h, dtype=float)
                        sum_sat = np.zeros_like(n_h, dtype=float)
                    
                    # AQUÍ SUMAMOS LOS CONTEOS BRUTOS
                    sum_halos += n_h
                    sum_cen += n_c
                    sum_sat += n_s
            except:
                continue

    # --- LA DIVISIÓN SE HACE AQUÍ, UNA SOLA VEZ AL FINAL ---
    if sum_halos is not None:
        with np.errstate(divide='ignore', invalid='ignore'):
            # Ocupación = (Suma total de galaxias) / (Suma total de halos)
            mean_cen = np.where(sum_halos > 0, sum_cen / sum_halos, 0.0)
            mean_sat = np.where(sum_halos > 0, sum_sat / sum_halos, 0.0)
            mean_tot = mean_cen + mean_sat

        mask = sum_halos > 0
        color = COLORES[corte]
        l_val = LABELS[corte]

        # Dibujamos las tres componentes por corte
        plt.plot(mass_bins[mask], mean_tot[mask], '-', color=color, label=f'Total log L > {l_val}', linewidth=2)
        plt.plot(mass_bins[mask], mean_cen[mask], '--', color=color, alpha=0.6)
        plt.plot(mass_bins[mask], mean_sat[mask], ':', color=color, alpha=0.6)

# --- MAQUILLAJE FINAL ---
plt.axhline(1.0, color='gray', linestyle='-', alpha=0.5, label='Límite físico ($N_{cen}=1$)')
plt.yscale('log')
plt.ylim(1e-3, 10)
plt.xlim(10.5, 14.5)
plt.xlabel(r"$\log_{10}(M_{\rm halo} \ / \ M_{\odot} h^{-1})$")
plt.ylabel(r"$\langle N \rangle$")
plt.title("HOD Multi-Corte Corregida (Suma Global)")
plt.legend(ncol=1, fontsize=9, loc='upper left', bbox_to_anchor=(1.0, 1.0))
plt.grid(True, which="both", linestyle="--", alpha=0.3)
plt.tight_layout()

plt.savefig("HOD_Super_Cortes_5678_Corregida.png", dpi=300)
print("🚀 ¡Gráfica con Hucha Global guardada!")
