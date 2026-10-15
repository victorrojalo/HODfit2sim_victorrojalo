import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 1. RUTAS ---
FILE_PATH = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/LF_Shark_Centrales.h5"
PLOT_OUT = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/LF_Shark_Centrales.png"

def plot_luminosity_function():
    if not os.path.exists(FILE_PATH):
        print(f"❌ Error: No encuentro el archivo {FILE_PATH}")
        return

    print(f"📂 Abriendo datos desde: {FILE_PATH}")

    # --- 2. LEER DATOS ---
    with h5py.File(FILE_PATH, 'r') as f:
        bin_edges = f['bin_edges'][:]
        phi = f['phi'][:]

    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0

    # 🕵️‍♀️ CHIVATOS DE DEBUGGING:
    print(f"🔎 DEBUG - Centros de los bins: {bin_centers}")
    print(f"🔎 DEBUG - Valores de Phi: {phi}")
    print(f"🔎 DEBUG - Total de Phi sumado: {np.sum(phi)}")

    # --- 3. DIBUJAR GRÁFICA ---
    plt.figure(figsize=(8, 6))

    mask = phi > 0

    if np.sum(mask) == 0:
        print("⚠️ ADVERTENCIA: ¡Todos los valores de Phi son 0! La gráfica saldrá vacía.")
    else:
        plt.plot(bin_centers[mask], phi[mask], marker='o', linestyle='-', color='blue', linewidth=2, label='Centrales Shark (Sin Corte)')

    # --- 4. MAQUILLAJE Y FORZADO DE EJES ---
    plt.yscale('log')
    
    # FORZAMOS LOS EJES PARA QUE SIEMPRE TENGAN TAMAÑO ASTROFÍSICO:
    plt.xlim(41, 49)          # Luminosidades entre 10^41 y 10^49
    plt.ylim(1e-8, 1e-1)      # Densidades típicas (ajusta esto si tus datos caen fuera)

    plt.xlabel('log10( L_bol )', fontsize=14)
    plt.ylabel('Densidad Numérica  Phi', fontsize=14)
    plt.title('Función de Luminosidad de Galaxias', fontsize=16)

    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend(fontsize=12)
    plt.tight_layout()

    # --- 5. GUARDAR ---
    plt.savefig(PLOT_OUT, dpi=300)
    print(f"✅ ¡Éxito! Gráfica guardada en: {PLOT_OUT}")

if __name__ == "__main__":
    plot_luminosity_function()
