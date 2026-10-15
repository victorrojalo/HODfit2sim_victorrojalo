import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
import mpl_style

# --- 1. ESTILO PAPER ---
plt.style.use(mpl_style.style1)

CORTES = [5, 6, 7]
COLORES = {5: '#1f77b4', 6: '#ff7f0e', 7: '#2ca02c'} 
#NUEVO DICCIONARIO DE ETIQUETAS CON CORTES
LABELS_LUM = {
    5: r'$L > 10^{42.0}$ erg/s',
    6: r'$L > 10^{43.0}$ erg/s',
    7: r'$L > 10^{45.0}$ erg/s',
}

BASE_DIR = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/output/Galform/Mvir"
ROCKSTAR_FILE = "/home2/vgonzalez/Data/Rockstar/SU1/outp_87.list"
VOLUMEN = 250.0**3

print("🚀 Clonando la Figura 1 del paper (HMF + HOD)...")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10), sharex=True)
fig.subplots_adjust(hspace=0.05) # Pegamos los paneles

# ==========================================
# PANEL 1: HMF (Función de Masa)
# ==========================================
print(" -> Procesando Materia Oscura para el Panel 1...")
try:
    rockstar_data = np.loadtxt(ROCKSTAR_FILE, skiprows=1, comments='#', usecols=(2, 40))
    mvir_principales = rockstar_data[:, 0][rockstar_data[:, 1] == -1]
    
    edges_mvir = np.linspace(10.5, 14.5, 71)
    mass_mvir = (edges_mvir[:-1] + edges_mvir[1:]) / 2.0
    dlogM = edges_mvir[1] - edges_mvir[0]
    
    hist_total, _ = np.histogram(np.log10(mvir_principales), bins=edges_mvir)
    phi_total = hist_total / (VOLUMEN * dlogM)
    mask_tot = phi_total > 0
    
    ax1.plot(mass_mvir[mask_tot], phi_total[mask_tot], '-', color='black', linewidth=2, label='DM Halos (Rockstar)')
except Exception as e:
    print(f"  [⚠️] Error Rockstar: {e}")

print(" -> Procesando HMF de Cortes...")
for corte in CORTES:
    # Centrales
    file_cen = os.path.join(BASE_DIR, f"Corte{corte}", "Centrales", f"HMF_TOTAL_Mvir_Galform_Corte{corte}_Centrales_COMPLETO.h5")
    if os.path.exists(file_cen):
        with h5py.File(file_cen, 'r') as f:
            mass = (f['bin_edges'][:-1] + f['bin_edges'][1:]) / 2.0
            phi = f['phi'][:]
        ax1.plot(mass[phi>0], phi[phi>0], '-', color=COLORES[corte], linewidth=2, label=LABELS_LUM[corte]) #NOMBRES LEYENDA
    
    # Satélites
    file_sat = os.path.join(BASE_DIR, f"Corte{corte}", "Satelites", f"HMF_TOTAL_Mvir_Galform_Corte{corte}_Satelites_COMPLETO.h5")
    if os.path.exists(file_sat):
        with h5py.File(file_sat, 'r') as f:
            phi_s = f['phi'][:]
        ax1.plot(mass[phi_s>0], phi_s[phi_s>0], '--', color=COLORES[corte], linewidth=2)

ax1.set_yscale('log')
ax1.set_ylabel(r'$dn / d\log_{10}M \ [h^3 \mathrm{Mpc}^{-3}]$', fontsize=18)
ax1.set_ylim(1e-6, 1) # Límites parecidos al paper
ax1.legend(loc='upper right', fontsize=10, ncol=2)
ax1.grid(True, linestyle='--', alpha=0.4)
# NUEVO: Aumentamos el tamaño de los números en los ejes (ticks)
plt.tick_params(axis='both', which='major', labelsize=14)
plt.tick_params(axis='both', which='minor', labelsize=12) # Opcional para los ticks menores del log
# ==========================================
# PANEL 2: HOD (Función de Ocupación)
# ==========================================
print(" -> Procesando HOD para el Panel 2...")
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
                        mass_bins = (f['data/bins/M_min_bin'][:] + f['data/bins/M_max_bin'][:]) / 2.0
                    n_h = f['data/bins/N_Halos'][:]
                    with np.errstate(divide='ignore', invalid='ignore'):
                        cen_list.append(np.where(n_h > 0, f['data/bins/N_C'][:] / n_h, 0.0))
                        sat_list.append(np.where(n_h > 0, f['data/bins/N_S'][:] / n_h, 0.0))
            except: pass

    if cen_list:
        mean_cen = np.sum(cen_list, axis=0)
        mean_sat = np.sum(sat_list, axis=0)
        
        ax2.plot(mass_bins[mean_cen>0], mean_cen[mean_cen>0], '-', color=COLORES[corte], linewidth=2)
        ax2.plot(mass_bins[mean_sat>0], mean_sat[mean_sat>0], '--', color=COLORES[corte], linewidth=2)

ax2.set_yscale('log')
ax2.set_xlabel(r'$\log_{10}(M_{\rm halo} \ / \ M_{\odot} h^{-1})$', fontsize=18)
ax2.set_ylabel(r'$\langle N(M) \rangle$', fontsize=18)
ax2.set_xlim(10.5, 14.5)
ax2.set_ylim(1e-4, 5)
ax2.grid(True, linestyle='--', alpha=0.4)

# Pequeña leyenda manual para el panel 2 (Centrales vs Satélites)
ax2.plot([], [], 'k-', label='Centrales')
ax2.plot([], [], 'k--', label='Satélites')
ax2.legend(loc='lower right', fontsize=11)
# NUEVO: Aumentamos el tamaño de los números en los ejes (ticks)
plt.tick_params(axis='both', which='major', labelsize=14)
plt.tick_params(axis='both', which='minor', labelsize=12) # Opcional para los ticks menores del log
plt.tight_layout()
SALIDA = os.path.join(BASE_DIR, "Grafica_TFM_Paper_Fig1_Completa_Galform.png")
plt.savefig(SALIDA, dpi=600, bbox_inches='tight')
print(f"🎉 ¡Figura 1 replicada y guardada en: {SALIDA}!")
