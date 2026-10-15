import h5py
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
matplotlib.use('Agg') # Fundamental para que Taurus no se queje por no tener pantalla

# ===================================================================
# 1. CONFIGURACIÓN DE ARCHIVOS Y COLORES
# ===================================================================
BASE_DIR = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo"

# Archivo de la Materia Oscura Total (Ajusta el nombre si es distinto)
ARCHIVO_DM = os.path.join(BASE_DIR, "HMF_TOTAL_Rockstar_out87.h5")

# Definimos los cortes que has ejecutado (Ajusta los nombres si hace falta)
cortes = {
    "Corte 1 (val=45.5)": {"color": "gold",  "cen": "HMF_TOTAL_Rockstar_out87_Mvir_Corte1_Centrales.h5", "sat": "HMF_TOTAL_Rockstar_out87_Mvir_Corte1_Satelites.h5"},
    "Corte 2 (val=45.3)": {"color": "green", "cen": "HMF_TOTAL_Rockstar_out87_Mvir_Corte2_Centrales.h5", "sat": "HMF_TOTAL_Rockstar_out87_Mvir_Corte2_Satelites.h5"},
    "Corte 3 (val=46.1)": {"color": "red",   "cen": "HMF_TOTAL_Rockstar_out87_Mvir_Corte3_Centrales.h5", "sat": "HMF_TOTAL_Rockstar_out87_Mvir_Corte3_Satelites.h5"},
    "Corte 4 (val=42.9)": {"color": "blue",  "cen": "HMF_TOTAL_Rockstar_out87_Mvir_Corte4_Centrales.h5", "sat": "HMF_TOTAL_Rockstar_out87_Mvir_Corte4_Satelites.h5"}
}

# ===================================================================
# 2. PREPARACIÓN DE LA FIGURA (2 PANELES)
# ===================================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12), sharex=True, gridspec_kw={'height_ratios': [2, 1]})
fig.subplots_adjust(hspace=0.05) # Juntamos los paneles

# Función auxiliar para leer los H5 con seguridad
def leer_h5(filepath):
    if not os.path.exists(filepath):
        print(f"⚠️ Aviso: No se encuentra {filepath}")
        return None, None
    with h5py.File(filepath, 'r') as f:
        edges = f['bin_edges'][:]
        phi = f['phi'][:]
    bin_centers = (edges[:-1] + edges[1:]) / 2.0
    return bin_centers, phi

# ===================================================================
# 3. CARGAR Y GRAFICAR MATERIA OSCURA (Línea Negra)
# ===================================================================
bin_centers_dm, phi_dm = leer_h5(ARCHIVO_DM)
if phi_dm is not None:
    mask_dm = phi_dm > 0
    ax1.plot(bin_centers_dm[mask_dm], phi_dm[mask_dm], color='black', lw=2.5, label='Dark Matter Halos')
else:
    print("❌ ERROR CRÍTICO: No se encontró el archivo de Materia Oscura Total.")
    exit()

# ===================================================================
# 4. BUCLE PARA CARGAR Y GRAFICAR CADA CORTE (Galaxias)
# ===================================================================
for nombre, datos in cortes.items():
    color = datos["color"]
    
    # --- CENTRALES ---
    x_cen, phi_cen = leer_h5(os.path.join(BASE_DIR, datos["cen"]))
    if phi_cen is not None:
        mask_c = phi_cen > 0
        # Panel Superior: Función de masa
        ax1.plot(x_cen[mask_c], phi_cen[mask_c], color=color, ls='-', lw=2, label=f'{nombre} (Cen)')
        
        # Panel Inferior: HOD = Phi_Galaxias / Phi_DM
        # Aseguramos no dividir por cero
        hod_cen = np.zeros_like(phi_cen)
        valid = (phi_dm > 0)
        hod_cen[valid] = phi_cen[valid] / phi_dm[valid]
        mask_hod_c = hod_cen > 0
        ax2.plot(x_cen[mask_hod_c], hod_cen[mask_hod_c], color=color, ls='-', lw=2)

    # --- SATÉLITES ---
    x_sat, phi_sat = leer_h5(os.path.join(BASE_DIR, datos["sat"]))
    if phi_sat is not None:
        mask_s = phi_sat > 0
        # Panel Superior: Función de masa
        ax1.plot(x_sat[mask_s], phi_sat[mask_s], color=color, ls='--', lw=2, label=f'{nombre} (Sat)')
        
        # Panel Inferior: HOD = Phi_Galaxias / Phi_DM
        hod_sat = np.zeros_like(phi_sat)
        valid = (phi_dm > 0)
        hod_sat[valid] = phi_sat[valid] / phi_dm[valid]
        mask_hod_s = hod_sat > 0
        ax2.plot(x_sat[mask_hod_s], hod_sat[mask_hod_s], color=color, ls='--', lw=2)

# ===================================================================
# 5. ESTILOS, LÍMITES Y ETIQUETAS (Estilo Paper)
# ===================================================================
# Panel Superior (HMF)
ax1.set_yscale('log')
ax1.set_ylabel(r'$\Phi = \frac{dn}{d\log_{10}M_{halo}} \ [h^3 \ \rm{Mpc}^{-3}]$', fontsize=16)
ax1.grid(True, which="both", ls="--", alpha=0.3)
ax1.legend(fontsize=11, loc='lower left')
ax1.set_ylim(1e-7, 1e0) # Ajusta estos límites si ves que se corta la gráfica

# Panel Inferior (HOD)
ax2.set_yscale('log')
ax2.set_xlabel(r'$\log_{10}(M_{halo} / M_\odot h^{-1})$', fontsize=16)
ax2.set_ylabel(r'$\langle N \rangle = \frac{\Phi_{gal}}{\Phi_{halo}}$', fontsize=16)
ax2.grid(True, which="both", ls="--", alpha=0.3)
ax2.set_ylim(1e-3, 1e2) # Límites típicos para HOD

# Guardar la joya de la corona
output_name = os.path.join(BASE_DIR, 'RESULTADO_FINAL_HOD_Mvir.png')
plt.savefig(output_name, dpi=300, bbox_inches='tight')
print(f"✅ ¡Gráfica espectacular generada con éxito! Descárgala: {output_name}")
