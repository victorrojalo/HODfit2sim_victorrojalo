import h5py
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')

# ===================================================================
# 1. CONFIGURACIÓN DE ARCHIVOS Y COLORES (MVIR + M200C)
# ===================================================================
BASE_DIR = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo"

# Archivos de Materia Oscura Total
ARCHIVO_DM_MVIR = os.path.join(BASE_DIR, "HMF_TOTAL_Rockstar_out87.h5")
ARCHIVO_DM_M200C = os.path.join(BASE_DIR, "HMF_TOTAL_Rockstar_out87_M200c.h5")

# Diccionario maestro con todos los cortes
cortes = {
    "C1 (45.5)": {"color": "gold",  
                  "mvir_cen": "HMF_TOTAL_Rockstar_out87_Mvir_Corte1_Centrales.h5", 
                  "mvir_sat": "HMF_TOTAL_Rockstar_out87_Mvir_Corte1_Satelites.h5",
                  "m200c_cen": "HMF_TOTAL_Rockstar_out87_M200c_Corte1_Centrales.h5",
                  "m200c_sat": "HMF_TOTAL_Rockstar_out87_M200c_Corte1_Satelites.h5"},
                  
    "C2 (45.3)": {"color": "green", 
                  "mvir_cen": "HMF_TOTAL_Rockstar_out87_Mvir_Corte2_Centrales.h5", 
                  "mvir_sat": "HMF_TOTAL_Rockstar_out87_Mvir_Corte2_Satelites.h5",
                  "m200c_cen": "HMF_TOTAL_Rockstar_out87_M200c_Corte2_Centrales.h5",
                  "m200c_sat": "HMF_TOTAL_Rockstar_out87_M200c_Corte2_Satelites.h5"},
                  
    "C3 (46.1)": {"color": "red",   
                  "mvir_cen": "HMF_TOTAL_Rockstar_out87_Mvir_Corte3_Centrales.h5", 
                  "mvir_sat": "HMF_TOTAL_Rockstar_out87_Mvir_Corte3_Satelites.h5",
                  "m200c_cen": "HMF_TOTAL_Rockstar_out87_M200c_Corte3_Centrales.h5",
                  "m200c_sat": "HMF_TOTAL_Rockstar_out87_M200c_Corte3_Satelites.h5"},
                  
    "C4 (42.9)": {"color": "blue",  
                  "mvir_cen": "HMF_TOTAL_Rockstar_out87_Mvir_Corte4_Centrales.h5", 
                  "mvir_sat": "HMF_TOTAL_Rockstar_out87_Mvir_Corte4_Satelites.h5",
                  "m200c_cen": "HMF_TOTAL_Rockstar_out87_M200c_Corte4_Centrales.h5",
                  "m200c_sat": "HMF_TOTAL_Rockstar_out87_M200c_Corte4_Satelites.h5"}
}

# ===================================================================
# 2. PREPARACIÓN DE LA FIGURA
# ===================================================================
# Hacemos la figura un poco más ancha para que quepa la leyenda a la derecha
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), sharex=True, gridspec_kw={'height_ratios': [2, 1]})
fig.subplots_adjust(hspace=0.05, right=0.75) # Dejamos margen derecho del 25% para la leyenda

def leer_h5(filepath):
    if not os.path.exists(filepath):
        return None, None
    with h5py.File(filepath, 'r') as f:
        edges = f['bin_edges'][:]
        phi = f['phi'][:]
    bin_centers = (edges[:-1] + edges[1:]) / 2.0
    return bin_centers, phi

# ===================================================================
# 3. GRAFICAR MATERIA OSCURA (Base para el HOD)
# ===================================================================
x_dm_mvir, phi_dm_mvir = leer_h5(ARCHIVO_DM_MVIR)
if phi_dm_mvir is not None:
    mask = phi_dm_mvir > 0
    ax1.plot(x_dm_mvir[mask], phi_dm_mvir[mask], color='black', lw=2.5, ls='-', label='DM (Mvir)')

x_dm_m200c, phi_dm_m200c = leer_h5(ARCHIVO_DM_M200C)
if phi_dm_m200c is not None:
    mask = phi_dm_m200c > 0
    ax1.plot(x_dm_m200c[mask], phi_dm_m200c[mask], color='gray', lw=2.5, ls='-.', label='DM (M200c)', alpha=0.8)

# ===================================================================
# 4. BUCLE PARA CARGAR Y GRAFICAR (MVIR Y M200C)
# ===================================================================
for nombre, datos in cortes.items():
    color = datos["color"]
    
    # ---------------- MVIR (Trazos continuos/discontinuos) ----------------
    x_mc, phi_mc = leer_h5(os.path.join(BASE_DIR, datos["mvir_cen"]))
    if phi_mc is not None and phi_dm_mvir is not None:
        mask = phi_mc > 0
        ax1.plot(x_mc[mask], phi_mc[mask], color=color, ls='-', lw=2, label=f'{nombre} Mvir (Cen)')
        hod = np.zeros_like(phi_mc)
        valid = phi_dm_mvir > 0
        hod[valid] = phi_mc[valid] / phi_dm_mvir[valid]
        ax2.plot(x_mc[hod>0], hod[hod>0], color=color, ls='-', lw=2)

    x_ms, phi_ms = leer_h5(os.path.join(BASE_DIR, datos["mvir_sat"]))
    if phi_ms is not None and phi_dm_mvir is not None:
        mask = phi_ms > 0
        ax1.plot(x_ms[mask], phi_ms[mask], color=color, ls='--', lw=2, label=f'{nombre} Mvir (Sat)')
        hod = np.zeros_like(phi_ms)
        valid = phi_dm_mvir > 0
        hod[valid] = phi_ms[valid] / phi_dm_mvir[valid]
        ax2.plot(x_ms[hod>0], hod[hod>0], color=color, ls='--', lw=2)

    # ---------------- M200C (Trazos punto-raya/punteados) ----------------
    x_2c, phi_2c = leer_h5(os.path.join(BASE_DIR, datos["m200c_cen"]))
    if phi_2c is not None and phi_dm_m200c is not None:
        mask = phi_2c > 0
        ax1.plot(x_2c[mask], phi_2c[mask], color=color, ls='-.', lw=2, alpha=0.8, label=f'{nombre} M200c (Cen)')
        hod = np.zeros_like(phi_2c)
        valid = phi_dm_m200c > 0
        hod[valid] = phi_2c[valid] / phi_dm_m200c[valid]
        ax2.plot(x_2c[hod>0], hod[hod>0], color=color, ls='-.', lw=2, alpha=0.8)

    x_2s, phi_2s = leer_h5(os.path.join(BASE_DIR, datos["m200c_sat"]))
    if phi_2s is not None and phi_dm_m200c is not None:
        mask = phi_2s > 0
        ax1.plot(x_2s[mask], phi_2s[mask], color=color, ls=':', lw=2, alpha=0.8, label=f'{nombre} M200c (Sat)')
        hod = np.zeros_like(phi_2s)
        valid = phi_dm_m200c > 0
        hod[valid] = phi_2s[valid] / phi_dm_m200c[valid]
        ax2.plot(x_2s[hod>0], hod[hod>0], color=color, ls=':', lw=2, alpha=0.8)

# ===================================================================
# 5. ESTILOS, LÍMITES Y LEYENDA EXTERNA
# ===================================================================
# Eje Y (Panel HMF)
ax1.set_yscale('log')
ax1.set_ylabel(r'$\Phi = \frac{dn}{d\log_{10}M_{halo}} \ [h^3 \ \rm{Mpc}^{-3}]$', fontsize=16)
ax1.grid(True, which="both", ls="--", alpha=0.3)
ax1.set_ylim(1e-7, 1e0)

# Sacamos la leyenda gigante fuera del cuadro, a la derecha
ax1.legend(fontsize=9, loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0.)

# Eje Y (Panel HOD)
ax2.set_yscale('log')
ax2.set_xlabel(r'$\log_{10}(M_{halo} / M_\odot h^{-1})$', fontsize=16)
ax2.set_ylabel(r'$\langle N \rangle = \frac{\Phi_{gal}}{\Phi_{halo}}$', fontsize=16)
ax2.grid(True, which="both", ls="--", alpha=0.3)
ax2.set_ylim(1e-3, 1e2)

# Guardar
output_name = os.path.join(BASE_DIR, 'RESULTADO_COMPARATIVA_TOTAL.png')
plt.savefig(output_name, dpi=300, bbox_inches='tight')
print(f"✅ ¡Gráfica de comparativa total generada! Descárgala: {output_name}")
