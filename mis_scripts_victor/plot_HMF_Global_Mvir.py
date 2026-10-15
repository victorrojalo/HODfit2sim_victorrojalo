import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# El archivo que tu main_UNIT_... ya calculó por ti
HMF_FILE = "HMF_TOTAL_Mvir_Shark_Corte1_Centrales_COMPLETO.h5"

if not os.path.exists(HMF_FILE):
    print(f"🚨 ¡No encuentro el archivo {HMF_FILE}! Asegúrate de estar en la carpeta correcta.")
else:
    print(f"Leyendo la HMF Global desde {HMF_FILE}...")
    
    with h5py.File(HMF_FILE, 'r') as f:
        edges = f['bin_edges'][:]
        # Calculamos el centro de cada cajón de masa
        mass = (edges[:-1] + edges[1:]) / 2.0
        phi = f['phi'][:]
        
    print("Generando la gráfica...")
    plt.figure(figsize=(8, 6))
    
    # Filtramos los ceros absolutos para que el logaritmo no explote
    mask = phi > 0
    
    plt.plot(mass[mask], np.log10(phi[mask]), '-o', color='darkorange', 
             linewidth=2.5, markersize=6, label='Catálogo Filtrado (ELGs Centrales)')
    
    plt.title("Función de Masa Global (HMF) - Galaxias ELG", fontsize=15)
    plt.xlabel(r"$\log_{10}(M_{\rm vir} \ / \ M_{\odot} h^{-1})$", fontsize=14)
    plt.ylabel(r"$\log_{10}(\Phi)$", fontsize=14)
    
    # Límites típicos para que se vea bonita
    plt.xlim(10.5, 14.5)
    
    plt.grid(True, which="both", ls="--", alpha=0.4)
    plt.legend(fontsize=12)
    
    GRAFICA_SALIDA = "Grafica_TFM_6_HMF_Mvir.png"
    plt.savefig(GRAFICA_SALIDA, dpi=300, bbox_inches='tight')
    print(f"¡Éxito! Gráfica guardada como: {GRAFICA_SALIDA}")
