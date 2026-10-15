import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 1. RUTAS ---
FILE_PATH = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/LF_Shark_TotalBIEN.h5"
PLOT_OUT = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/LF_Shark_Total.png"

def plot_luminosity_function():
    if not os.path.exists(FILE_PATH):
        print(f"❌ Error: No encuentro el archivo {FILE_PATH}")
        return

    # --- 2. LEER DATOS ---
    with h5py.File(FILE_PATH, 'r') as f:
        bin_edges = f['bin_edges'][:]
        phi = f['phi'][:]

    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0

    # --- 3. EXTENDER LOS DATOS PARA TODO EL EJE X ---
    # Creamos un eje X completo desde 41 a 47
    full_x = np.linspace(41.0, 47.0, 100)
    # Interpolamos los datos de Phi sobre este nuevo eje X. 
    # Lo que esté fuera del rango original se rellena con 1e-10 (un valor casi cero)
    full_phi = np.interp(full_x, bin_centers, phi, left=1e-10, right=1e-10)

    # --- 4. DIBUJAR GRÁFICA ---
    plt.figure(figsize=(10, 7))

    # Dibujamos la línea azul usando el eje extendido
    plt.plot(full_x, full_phi, marker='o', markersize=4, linestyle='-', 
             color='blue', linewidth=2, label='Galaxias Shark (Censo Total)')

    # --- 5. LÍNEAS DE CORTES ---
    umbrales_log = {5: 42.0, 6: 43.0, 7: 45.0, 8: 45.5}
    colores_cortes = {5: '#1f77b4', 6: '#ff7f0e', 7: '#2ca02c', 8: '#d62728'}

    # Nuevo diccionario con las etiquetas matemáticas para la leyenda
    etiquetas_cortes = {
        5: r'$L > 10^{42.0}$ erg/s',
        6: r'$L > 10^{43.0}$ erg/s',
        7: r'$L > 10^{45.0}$ erg/s',
        8: r'$L > 10^{45.5}$ erg/s'
    }
    for corte, val_log in umbrales_log.items():
        plt.axvline(x=val_log, color=colores_cortes[corte], linestyle='--', alpha=0.8, label=etiquetas_cortes[corte])

    # --- 6. MAQUILLAJE ---
    plt.yscale('log')
    plt.xlim(41.0, 47.0)
    # Ajustamos el límite inferior para que se vea la caída pero no el "suelo" de 1e-10
    plt.ylim(1e-4, 1e-2) 

    plt.xlabel(r'$\log_{10}(L_{\rm bol} \ / \ \rm{erg \ s}^{-1})$', fontsize=18)
    plt.ylabel(r'$\Phi \ [h^3 \mathrm{Mpc}^{-3} \mathrm{dex}^{-1}]$', fontsize=18)
    plt.title('Función de Luminosidad AGN - Rango Completo', fontsize=20)
    # NUEVO: Aumentamos el tamaño de los números en los ejes (ticks)
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.tick_params(axis='both', which='minor', labelsize=12) # Opcional para los ticks menores del log
    
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend(fontsize=10, loc='lower left')
    plt.tight_layout()

    plt.savefig(PLOT_OUT, dpi=600)
    print(f"✅ ¡Éxito! Gráfica extendida guardada en: {PLOT_OUT}")

if __name__ == "__main__":
    plot_luminosity_function()
