import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# --- ARCHIVOS ---
FILE_M200C = "HMF_TOTAL_M200c_Shark_Corte1_Centrales_COMPLETO.h5" 
FILE_MVIR = "HMF_TOTAL_Mvir_Shark_Corte1_Centrales_COMPLETO.h5"
ROCKSTAR_FILE = "/home2/vgonzalez/Data/Rockstar/SU1/outp_87.list"

# Parámetros de la simulación (Extraídos de tu log de Rockstar)
BOX_SIZE = 250.0  # Mpc/h
VOLUMEN = BOX_SIZE**3

print("Iniciando la comparativa completa de HMFs...")
plt.figure(figsize=(10, 7))

# 1. --- Cargar y pintar ELGs (M200c) ---
if os.path.exists(FILE_M200C):
    print(" -> Leyendo ELGs (M200c)...")
    with h5py.File(FILE_M200C, 'r') as f:
        edges_m200c = f['bin_edges'][:]
        mass_200c = (edges_m200c[:-1] + edges_m200c[1:]) / 2.0
        phi_200c = f['phi'][:]
    
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
    
    mask_mvir = phi_mvir > 0
    plt.plot(mass_mvir[mask_mvir], np.log10(phi_mvir[mask_mvir]), '-s', color='darkviolet',
             linewidth=2.5, markersize=5, label=r'ELGs Centrales ($M_{\rm vir}$)')

# 3. --- Cargar y pintar TODOS LOS HALOS (Fondo de Materia Oscura) ---
print(" -> Calculando HMF total de Rockstar (Esto tomará ~1 minuto)...")
try:
    # usecols=(2, 40) lee SOLO la masa virial (col 2) y el PID (col 40). Es muchísimo más rápido.
    rockstar_data = np.loadtxt(ROCKSTAR_FILE, skiprows=1, comments='#', usecols=(2, 40))
    mvir_todos = rockstar_data[:, 0]
    pid_todos = rockstar_data[:, 1]
    
    # Nos quedamos solo con los halos principales (PID == -1)
    mask_principales = (pid_todos == -1)
    mvir_principales = mvir_todos[mask_principales]
    
    # Hacemos el histograma usando los mismos bines que los archivos h5
    # (Asumimos que edges_mvir está en escala logarítmica)
    log_mvir_principales = np.log10(mvir_principales)
    hist_total, _ = np.histogram(log_mvir_principales, bins=edges_mvir)
    
    # Convertimos los conteos a la función de masa Phi (densidad por unidad de volumen y bin de masa)
    dlogM = edges_mvir[1] - edges_mvir[0]
    phi_total = hist_total / (VOLUMEN * dlogM)
    
    mask_total = phi_total > 0
    
    # Lo pintamos como una línea gris punteada o sombreada por encima de las otras
    plt.plot(mass_mvir[mask_total], np.log10(phi_total[mask_total]), '--', color='dimgray',
             linewidth=2.5, alpha=0.8, label=r'Todos los Halos Principales Rockstar ($M_{\rm vir}$)')
    
except Exception as e:
    print(f"⚠️ Error al procesar Rockstar: {e}")

# --- Configuración visual ---
plt.title("Función de Masa (HMF): Materia Oscura vs Galaxias ELG", fontsize=15)
plt.xlabel(r"$\log_{10}(M_{\rm halo} \ / \ M_{\odot} h^{-1})$", fontsize=14)
plt.ylabel(r"$\log_{10}(\Phi)$", fontsize=14)

plt.xlim(10.5, 14.5)

# Opcional: ajustar el eje Y para asegurar que se ve la línea gris (que estará más arriba)
# plt.ylim(-5, -1) 

plt.grid(True, which="both", ls="--", alpha=0.4)
plt.legend(fontsize=11, loc='upper right')

GRAFICA_SALIDA = "Grafica_TFM_6_HMF_Completa.png"
plt.savefig(GRAFICA_SALIDA, dpi=300, bbox_inches='tight')
print(f"\n¡Éxito! Gráfica definitiva guardada como: {GRAFICA_SALIDA}")
