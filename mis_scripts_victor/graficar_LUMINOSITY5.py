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

    # Para dibujar, necesitamos el punto medio de cada "caja" (bin)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0

    # 🕵️‍♀️ CHIVATOS DE DEBUGGING:
    print(f"🔎 DEBUG - Centros de los bins: {bin_centers}")
    print(f"🔎 DEBUG - Total de Phi sumado: {np.sum(phi)}")

    # --- 3. DIBUJAR GRÁFICA ---
    plt.figure(figsize=(8, 6))

    # Filtramos los ceros porque en escala logarítmica dan error matemático
    mask = phi > 0

    if np.sum(mask) == 0:
        print("⚠️ ADVERTENCIA: ¡Todos los valores de Phi son 0! La gráfica saldrá vacía.")
    else:
        plt.plot(bin_centers[mask], phi[mask], marker='o', linestyle='-', color='blue', linewidth=2, label='Centrales Shark (Sin Corte)')

    # =================================================================
    # ✂️ AÑADIR LÍNEAS VERTICALES DE LOS CORTES
    # =================================================================
    umbrales_log = {
        5: 42.0, 
        6: 43.0, 
        7: 45.0, 
        8: 45.5  
    }
    
    colores_cortes = {5: '#1f77b4', 6: '#ff7f0e', 7: '#2ca02c', 8: '#d62728'} # Colores a juego con Fig1

    for corte, val_log in umbrales_log.items():
        plt.axvline(x=val_log, color=colores_cortes[corte], linestyle='--', alpha=0.7, label=f'Umbral Corte {corte}')
    # =================================================================

    # --- 4. MAQUILLAJE Y FORZADO DE EJES ---
    plt.yscale('log')

    # FORZAMOS LOS EJES PARA QUE SIEMPRE TENGAN TAMAÑO ASTROFÍSICO:
    plt.xlim(41.0, 47.0)      # Luminosidades típicas AGN
    plt.ylim(1e-3, 1e-2)      # Densidades típicas (ajusta esto si tus datos caen fuera)

    # TEXTOS EN FORMATO LATEX PARA QUE QUEDE DE PAPER
    plt.xlabel(r'$\log_{10}(L_{\rm bol} \ / \ \rm{erg \ s}^{-1})$', fontsize=14)
    plt.ylabel(r'$\Phi \ [h^3 \mathrm{Mpc}^{-3} \mathrm{dex}^{-1}]$', fontsize=14)
    plt.title('Función de Luminosidad AGN y Umbrales de Corte', fontsize=16)

    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    
    # Ajustamos la leyenda para que no pise la curva (opcional, prueba con 'best')
    plt.legend(fontsize=10, loc='lower left') 
    plt.tight_layout()

    # --- 5. GUARDAR ---
    plt.savefig(PLOT_OUT, dpi=300)
    print(f"✅ ¡Éxito! Gráfica guardada en: {PLOT_OUT}")

if __name__ == "__main__":
    plot_luminosity_function()
