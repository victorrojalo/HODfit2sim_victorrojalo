import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
import mpl_style

# --- 1. ESTILO PAPER ---
plt.style.use(mpl_style.style1)

BASE_DIR = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/output/Mvir"
CORTES = [5, 6, 7, 8]
COLORES = {5: '#1f77b4', 6: '#ff7f0e', 7: '#2ca02c', 8: '#d62728'}
LABELS_LUM = {
    5: r'$L > 10^{42.0}$ erg/s',
    6: r'$L > 10^{43.0}$ erg/s',
    7: r'$L > 10^{45.0}$ erg/s',
    8: r'$L > 10^{45.5}$ erg/s',
}

print("🚀 Generando HOD Súper-Cortes con la lógica de la Fig 1...")

plt.figure(figsize=(9, 8))

for corte in CORTES:
    DIR_CONF = os.path.join(BASE_DIR, f"Corte{corte}", "Centrales")
    cen_list, sat_list = [], []
    mass_bins = None

    for i in range(64):
        archivo = os.path.join(DIR_CONF, f"conformity_vol{i}.h5")
        if os.path.exists(archivo):
            try:
                with h5py.File(archivo, 'r') as f:
                    if mass_bins is None:
                        # Usamos el punto medio de los bins como en la Fig 1
                        mass_bins = (f['data/bins/M_min_bin'][:] + f['data/bins/M_max_bin'][:]) / 2.0
                    
                    n_h = f['data/bins/N_Halos'][:]
                    with np.errstate(divide='ignore', invalid='ignore'):
                        # Guardamos las fracciones por volumen
                        cen_list.append(np.where(n_h > 0, f['data/bins/N_C'][:] / n_h, 0.0))
                        sat_list.append(np.where(n_h > 0, f['data/bins/N_S'][:] / n_h, 0.0))
            except: pass

    if cen_list:
        # APLICAMOS LA LÓGICA DE LA FIGURA 1: SUMAR EN LUGAR DE PROMEDIAR
        mean_cen = np.sum(cen_list, axis=0)
        mean_sat = np.sum(sat_list, axis=0)
        mean_tot = mean_cen + mean_sat

        color = COLORES[corte]
        label = LABELS_LUM[corte]

        # Línea TOTAL (Sólida —)
        plt.plot(mass_bins[mean_tot>0], mean_tot[mean_tot>0], 
                 '-', color=color, linewidth=2.5, label=label)
        
        # Línea CENTRALES (Discontinua ---)
        plt.plot(mass_bins[mean_cen>0], mean_cen[mean_cen>0], 
                 '--', color=color, linewidth=1.5, alpha=0.7)
        
        # Línea SATÉLITES (Punteada ···)
        plt.plot(mass_bins[mean_sat>0], mean_sat[mean_sat>0], 
                 ':', color=color, linewidth=1.5, alpha=0.7)

# --- MAQUILLAJE ---
plt.axhline(1.0, color='gray', linestyle='-', alpha=0.3) # Techo físico
plt.yscale('log')
plt.ylim(1e-3, 10)
plt.xlim(10.5, 14.5)

plt.xlabel(r'$\log_{10}(M_{\rm halo} \ / \ M_{\odot} h^{-1})$', fontsize=18)
plt.ylabel(r'$\langle N(M) \rangle$', fontsize=18)
plt.title("HOD Shark: Total (—), Centrales (---) y Satélites (···)")

# Leyenda elegante
plt.legend(loc='upper left', fontsize=10, ncol=1, frameon=True)
plt.grid(True, linestyle='--', alpha=0.3)
# NUEVO: Aumentamos el tamaño de los números en los ejes (ticks)
plt.tick_params(axis='both', which='major', labelsize=14)
plt.tick_params(axis='both', which='minor', labelsize=12) # Opcional para los ticks menores del log
plt.tight_layout()
SALIDA = "Grafica_HOD_SUPER_CORREGIDA_TOTAL.png"
plt.savefig(SALIDA, dpi=500)
print(f"✅ ¡GRÁFICA PERFECTA GUARDADA EN: {SALIDA}!")
