import h5py
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
matplotlib.use('Agg') # Para que Taurus no pida pantalla

# ===================================================================
# 1. CONFIGURACIÓN DE ARCHIVOS
# ===================================================================
BASE_DIR = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo"

# Archivo de la Materia Oscura Total
ARCHIVO_DM = os.path.join(BASE_DIR, "HMF_TOTAL_Rockstar_out87.h5")

# Archivo ÚNICO de Centrales (Corte 1)
NOMBRE_CORTE = "Corte 1 (val=45.5)"
COLOR_CORTE  = "blue" 
ARCHIVO_CEN = os.path.join(BASE_DIR, "HMF_TOTAL_Rockstar_out87_Mvir_Corte1_Centrales_COMPLETO.h5")

# ===================================================================
# 2. PREPARACIÓN DE LA FIGURA Y LECTURA
# ===================================================================
fig, ax1 = plt.subplots(figsize=(10, 8))

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
# 3. GRAFICAR MATERIA OSCURA
# ===================================================================
bin_centers_dm, phi_dm = leer_h5(ARCHIVO_DM)
if phi_dm is not None:
    mask_dm = phi_dm > 0
    ax1.plot(bin_centers_dm[mask_dm], phi_dm[mask_dm], color='black', lw=2.5, label='Dark Matter Halos')
else:
    print("❌ ERROR CRÍTICO: No se encontró el archivo de Materia Oscura.")
    exit()

# ===================================================================
# 4. GRAFICAR SOLO CENTRALES
# ===================================================================
x_cen, phi_cen = leer_h5(ARCHIVO_CEN)
if phi_cen is not None:
    mask_c = phi_cen > 0
    ax1.plot(x_cen[mask_c], phi_cen[mask_c], color=COLOR_CORTE, ls='-', lw=2.5, label=f'{NOMBRE_CORTE} (Solo Centrales)')

# ===================================================================
# 5. ESTILOS FINALES
# ===================================================================
ax1.set_yscale('log')
ax1.set_xlabel(r'$\log_{10}(M_{halo} / M_\odot h^{-1})$', fontsize=16)
ax1.set_ylabel(r'$\Phi = \frac{dn}{d\log_{10}M_{halo}} \ [h^3 \ \rm{Mpc}^{-3}]$', fontsize=16)

ax1.grid(True, which="both", ls="--", alpha=0.3)
ax1.legend(fontsize=14, loc='lower left')
ax1.set_ylim(1e-7, 1e0)
ax1.set_xlim(10.5, 14.5)

output_name = os.path.join(BASE_DIR, 'RESULTADO_HMF_Corte1_Centrales_COMPLETO3.png')
plt.savefig(output_name, dpi=300, bbox_inches='tight')
print(f"✅ ¡Gráfica lista! Solo DM y Centrales. Descárgala: {output_name}")
