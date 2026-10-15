import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# 1. Definimos los nombres de los dos archivos
FILE_M200C = "HMF_TOTAL_M200c_Shark_Corte1_Centrales_COMPLETO.h5" 
FILE_MVIR = "HMF_TOTAL_Mvir_Shark_Corte1_Centrales_COMPLETO.h5"

print("Iniciando la comparación de HMFs...")
plt.figure(figsize=(9, 6))

# --- Cargar y pintar M200c ---
if os.path.exists(FILE_M200C):
    print(f" -> Leyendo datos de M200c...")
    with h5py.File(FILE_M200C, 'r') as f:
        edges = f['bin_edges'][:]
        mass_200c = (edges[:-1] + edges[1:]) / 2.0
        phi_200c = f['phi'][:]
    
    mask_200c = phi_200c > 0
    plt.plot(mass_200c[mask_200c], np.log10(phi_200c[mask_200c]), '-o', color='darkorange',
             linewidth=2.5, markersize=6, label=r'ELGs Centrales ($M_{\rm 200c}$)')
else:
    print(f"⚠️ Aviso: No se encontró {FILE_M200C}. Revisa el nombre exacto.")

# --- Cargar y pintar Mvir ---
if os.path.exists(FILE_MVIR):
    print(f" -> Leyendo datos de Mvir...")
    with h5py.File(FILE_MVIR, 'r') as f:
        edges = f['bin_edges'][:]
        mass_mvir = (edges[:-1] + edges[1:]) / 2.0
        phi_mvir = f['phi'][:]
    
    mask_mvir = phi_mvir > 0
    # Usamos '-s' (cuadrados) para distinguir mejor los puntos de Mvir de los círculos de M200c
    plt.plot(mass_mvir[mask_mvir], np.log10(phi_mvir[mask_mvir]), '-s', color='darkviolet',
             linewidth=2.5, markersize=6, label=r'ELGs Centrales ($M_{\rm vir}$)')
else:
    print(f"⚠️ Aviso: No se encontró {FILE_MVIR}. Revisa el nombre exacto.")

# --- Configuración de la gráfica ---
plt.title("Comparación de Función de Masa Global (HMF)", fontsize=15)

# Ponemos M_halo genérico en el eje X porque estamos representando dos definiciones de masa
plt.xlabel(r"$\log_{10}(M_{\rm halo} \ / \ M_{\odot} h^{-1})$", fontsize=14)
plt.ylabel(r"$\log_{10}(\Phi)$", fontsize=14)

# Límites típicos para que se vea bonita
plt.xlim(10.5, 14.5)

plt.grid(True, which="both", ls="--", alpha=0.4)
plt.legend(fontsize=12)

# Guardamos el resultado final
GRAFICA_SALIDA = "Grafica_TFM_6_HMF_Comparacion_Masas.png"
plt.savefig(GRAFICA_SALIDA, dpi=300, bbox_inches='tight')
print(f"\n¡Éxito! Gráfica comparativa guardada como: {GRAFICA_SALIDA}")
