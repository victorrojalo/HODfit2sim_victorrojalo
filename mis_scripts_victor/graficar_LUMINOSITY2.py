import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 1. RUTAS ---
# Ajusta este nombre si al final le pusiste LF_Shark_Centrales.h5
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

    # Para dibujar, necesitamos el punto medio de cada "caja" (bin)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0

    # --- 3. DIBUJAR GRÁFICA ---
    plt.figure(figsize=(8, 6))

    # Filtramos los ceros porque en escala logarítmica dan error matemático
    mask = phi > 0 
    
    plt.plot(bin_centers[mask], phi[mask], marker='o', linestyle='-', color='blue', linewidth=2, label='Centrales Shark (Sin Corte)')

    # --- 4. MAQUILLAJE DE LA GRÁFICA ---
    plt.yscale('log') # La densidad SIEMPRE se pone en escala logarítmica
    
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
