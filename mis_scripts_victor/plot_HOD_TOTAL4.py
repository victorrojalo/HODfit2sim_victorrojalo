import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# --- 1. ESTILO PAPER ---
import mpl_style
plt.style.use(mpl_style.style1)

# --- 2. CONFIGURACIÓN ---
BASE_DIR = "output/Mvir"
CORTES = [5, 6, 7, 8]

# Valores reales de los cortes para la leyenda
labels_cortes = {
    5: r"$\log L > 42.0$",
    6: r"$\log L > 43.0$",
    7: r"$\log L > 45.0$",
    8: r"$\log L > 45.5$"
}

colores = {5: '#1f77b4', 6: '#ff7f0e', 7: '#2ca02c', 8: '#d62728'}
estilos = {'Cen': '--', 'Sat': ':', 'Tot': '-'}

plt.figure(figsize=(10, 8))

# --- 3. BUCLE SOBRE CORTES ---
for corte in CORTES:
    DIR_DATOS = os.path.join(BASE_DIR, f"Corte{corte}", "Centrales")
    
    SUM_N_H = None
    SUM_N_C = None
    SUM_N_S = None
    mass_bins = None

    print(f"Procesando Corte {corte}...")

    for i in range(64):
        archivo = os.path.join(DIR_DATOS, f"conformity_vol{i}.h5")
        if os.path.exists(archivo):
            try:
                with h5py.File(archivo, 'r') as f:
                    n_h = f['data/bins/N_Halos'][:]
                    n_c = f['data/bins/N_C'][:]
                    n_s = f['data/bins/N_S'][:]
                    m_b = f['data/bins/M_min_bin'][:]

                    if SUM_N_H is None:
                        mass_bins = m_b
                        SUM_N_H = np.zeros_like(n_h, dtype=float)
                        SUM_N_C = np.zeros_like(n_h, dtype=float)
                        SUM_N_S = np.zeros_like(n_h, dtype=float)

                    SUM_N_H += n_h
                    SUM_N_C += n_c
                    SUM_N_S += n_s
            except: continue

    if SUM_N_H is not None:
        # Normalización Global
        with np.errstate(divide='ignore', invalid='ignore'):
            mean_cen = np.where(SUM_N_H > 0, SUM_N_C / SUM_N_H, 0.0)
            mean_sat = np.where(SUM_N_H > 0, SUM_N_S / SUM_N_H, 0.0)
            mean_tot = mean_cen + mean_sat

        mask = mean_tot > 0
        color = colores[corte]
        label_base = labels_cortes[corte]

        # 4. AÑADIR LÍNEAS (Total, Cen, Sat)
        # Solo ponemos label en la TOTAL para no saturar la leyenda, o una combinada
        plt.plot(mass_bins[mask], mean_tot[mask], linestyle=estilos['Tot'], 
                 color=color, linewidth=2, label=f'Total {label_base}')
        plt.plot(mass_bins[mask], mean_cen[mask], linestyle=estilos['Cen'], 
                 color=color, alpha=0.6)
        plt.plot(mass_bins[mask], mean_sat[mask], linestyle=estilos['Sat'], 
                 color=color, alpha=0.6)

# --- 5. MAQUILLAJE ---
plt.axhline(1.0, color='black', linestyle='-', alpha=0.2)
plt.yscale('log')
plt.xlim(10.5, 14.5)
plt.ylim(1e-3, 10)

plt.xlabel(r"$\log_{10}(M_{\rm halo} \ / \ M_{\odot} h^{-1})$")
plt.ylabel(r"$\langle N_{\rm gal} \rangle$")
plt.title("HOD Multi-Corte: Centrales (---), Satélites (···) y Total (—)")

# Leyenda organizada
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
plt.grid(True, which="both", linestyle="--", alpha=0.3)
plt.tight_layout()

GRAFICA_SALIDA = "HOD_Super_Cortes_5678_Completa.png"
plt.savefig(GRAFICA_SALIDA, dpi=300)
print(f"✅ ¡Súper HOD guardada! Archivo: {GRAFICA_SALIDA}")
