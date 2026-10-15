import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 1. IMPORTAR Y APLICAR EL ESTILO MAESTRO ---
import mpl_style
plt.style.use(mpl_style.style1)

# --- ARCHIVOS ---
RESULTS_DIR = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/output/Mvir/Corte5/Centrales"
FILE_MVIR = os.path.join(RESULTS_DIR, "HMF_TOTAL_Mvir_Shark_Corte5_Centrales_COMPLETO.h5")
ROCKSTAR_FILE = "/home2/vgonzalez/Data/Rockstar/SU1/outp_87.list"

BOX_SIZE = 250.0 
VOLUMEN = BOX_SIZE**3

print("Iniciando la comparativa de HMFs con estilo paper...")
plt.figure(figsize=(10, 7))

# --- Cargar y pintar ELGs (Mvir) ---
if os.path.exists(FILE_MVIR):
    print(" -> Leyendo ELGs (Mvir) del Corte 5...")
    with h5py.File(FILE_MVIR, 'r') as f:
        edges_mvir = f['bin_edges'][:]
        mass_mvir = (edges_mvir[:-1] + edges_mvir[1:]) / 2.0
        phi_mvir = f['phi'][:]
        dlogM_mvir = edges_mvir[1] - edges_mvir[0]

    mask_mvir = phi_mvir > 0
    plt.plot(mass_mvir[mask_mvir], np.log10(phi_mvir[mask_mvir]), '-s', color='darkviolet',
             markersize=6, label=r'ELGs Centrales Corte 5 ($M_{\rm vir}$)')
else:
    print(f"❌ Error: No encuentro el archivo {FILE_MVIR}")

# --- Cargar y pintar TODOS LOS HALOS ---
print(" -> Calculando HMF total de Rockstar (Esto tomará ~1 minuto)...")
try:
    rockstar_data = np.loadtxt(ROCKSTAR_FILE, skiprows=1, comments='#', usecols=(2, 21, 40))
    mvir_todos = rockstar_data[:, 0]
    pid_todos = rockstar_data[:, 2]

    mask_principales = (pid_todos == -1)
    mvir_principales = mvir_todos[mask_principales]

    log_mvir_principales = np.log10(mvir_principales)
    hist_total_mvir, _ = np.histogram(log_mvir_principales, bins=edges_mvir)
    phi_total_mvir = hist_total_mvir / (VOLUMEN * dlogM_mvir)

    mask_total_mvir = phi_total_mvir > 0
    plt.plot(mass_mvir[mask_total_mvir], np.log10(phi_total_mvir[mask_total_mvir]), '--', color='mediumorchid',
             alpha=0.8, label=r'Todos los Halos Rockstar ($M_{\rm vir}$)')

except Exception as e:
    print(f"⚠️ Error al procesar Rockstar: {e}")

# --- Configuración visual final ---
plt.title("Función de Masa (HMF): Materia Oscura vs Galaxias ELG Corte 5")
plt.xlabel(r"$\log_{10}(M_{\rm halo} \ / \ M_{\odot} h^{-1})$")
plt.ylabel(r"$\log_{10}(\Phi)$")

plt.xlim(10.5, 14.5)
plt.legend(loc='upper right')

GRAFICA_SALIDA = os.path.join(RESULTS_DIR, "Grafica_TFG_HMF_Comparativa_Corte5_FINAL.png")
plt.savefig(GRAFICA_SALIDA, dpi=300)
print(f"\n¡Éxito! Gráfica guardada como: {GRAFICA_SALIDA}")
