import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# --- ARCHIVOS ---
FILE_M200C = "HMF_TOTAL_M200c_Shark_Corte1_Centrales_COMPLETO.h5" 
FILE_MVIR = "HMF_TOTAL_Mvir_Shark_Corte1_Centrales_COMPLETO.h5"
ROCKSTAR_FILE = "/home2/vgonzalez/Data/Rockstar/SU1/outp_87.list"

# Parámetros de la simulación
BOX_SIZE = 250.0  # Mpc/h
VOLUMEN = BOX_SIZE**3

print("Iniciando la comparativa cuádruple de HMFs...")
plt.figure(figsize=(10, 7))

# 1. --- Cargar y pintar ELGs (M200c) ---
if os.path.exists(FILE_M200C):
    print(" -> Leyendo ELGs (M200c)...")
    with h5py.File(FILE_M200C, 'r') as f:
        edges_m200c = f['bin_edges'][:]
        mass_200c = (edges_m200c[:-1] + edges_m200c[1:]) / 2.0
        phi_200c = f['phi'][:]
        dlogM_200c = edges_m200c[1] - edges_m200c[0] # Ancho del bin
    
    mask_200c = phi_200c > 0
    plt.plot(mass_200c[mask_200c], np.log10(phi_200c[mask_200c]), '-o', color='darkorange',
             linewidth=2.5, markersize=5, label=r'ELGs Centrales ($M_{\rm 200c}$)')

# 2. --- Cargar y pintar ELGs (Mvir) ---
if os.path.exists(FILE_MVIR):
    print(" -> Leyendo ELGs (Mvir)...")
    with h5py.File(FILE_MVIR, 'r') as f:
        edges_mvir = f['bin_edges'][:]
        mass_mvir = (edges_mvir[:-1] + edges_mvir[1:]) / 2.0
        phi_mvir = f['phi'][:]
        dlogM_mvir = edges_mvir[1] - edges_mvir[0]
    
    mask_mvir = phi_mvir > 0
    plt.plot(mass_mvir[mask_mvir], np.log10(phi_mvir[mask_mvir]), '-s', color='darkviolet',
             linewidth=2.5, markersize=5, label=r'ELGs Centrales ($M_{\rm vir}$)')

# 3. --- Cargar y pintar TODOS LOS HALOS (Mvir y M200c) ---
print(" -> Calculando HMF total de Rockstar (Esto tomará ~1 minuto)...")
try:
    # usecols=(2, 21, 40) lee Mvir (col 2), M200c (col 21) y PID (col 40).
    rockstar_data = np.loadtxt(ROCKSTAR_FILE, skiprows=1, comments='#', usecols=(2, 21, 40))
    mvir_todos = rockstar_data[:, 0]
    m200c_todos = rockstar_data[:, 1]
    pid_todos = rockstar_data[:, 2]
    
    # Nos quedamos solo con los halos principales (PID == -1)
    mask_principales = (pid_todos == -1)
    mvir_principales = mvir_todos[mask_principales]
    m200c_principales = m200c_todos[mask_principales]
    
    # --- Histograma de Todos los Halos Mvir ---
    log_mvir_principales = np.log10(mvir_principales)
    hist_total_mvir, _ = np.histogram(log_mvir_principales, bins=edges_mvir)
    phi_total_mvir = hist_total_mvir / (VOLUMEN * dlogM_mvir)
    
    mask_total_mvir = phi_total_mvir > 0
    plt.plot(mass_mvir[mask_total_mvir], np.log10(phi_total_mvir[mask_total_mvir]), '--', color='mediumorchid',
             linewidth=2.5, alpha=0.8, label=r'Todos los Halos Rockstar ($M_{\rm vir}$)')

    # --- Histograma de Todos los Halos M200c ---
    # Evitamos logaritmos de 0 o negativos si los hubiera en la columna M200c
    valid_m200c = m200c_principales > 0
    log_m200c_principales = np.log10(m200c_principales[valid_m200c])
    
    hist_total_m200c, _ = np.histogram(log_m200c_principales, bins=edges_m200c)
    phi_total_m200c = hist_total_m200c / (VOLUMEN * dlogM_200c)
    
    mask_total_m200c = phi_total_m200c > 0
    plt.plot(mass_200c[mask_total_m200c], np.log10(phi_total_m200c[mask_total_m200c]), '--', color='sandybrown',
             linewidth=2.5, alpha=0.8, label=r'Todos los Halos Rockstar ($M_{\rm 200c}$)')
    
except Exception as e:
    print(f"⚠️ Error al procesar Rockstar: {e}")

# --- Configuración visual ---
plt.title("Función de Masa (HMF): Materia Oscura vs Galaxias ELG", fontsize=15)
plt.xlabel(r"$\log_{10}(M_{\rm halo} \ / \ M_{\odot} h^{-1})$", fontsize=14)
plt.ylabel(r"$\log_{10}(\Phi)$", fontsize=14)

plt.xlim(10.5, 14.5)

plt.grid(True, which="both", ls="--", alpha=0.4)
plt.legend(fontsize=11, loc='upper right')

GRAFICA_SALIDA = "Grafica_TFM_6_HMF_Completa_Cuadruple.png"
plt.savefig(GRAFICA_SALIDA, dpi=300, bbox_inches='tight')
print(f"\n¡Éxito! Gráfica cuádruple guardada como: {GRAFICA_SALIDA}")
