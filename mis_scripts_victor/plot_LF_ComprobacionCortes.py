import os
import h5py
import numpy as np
import matplotlib
matplotlib.use('Agg') # Escudo anti-errores de pantalla en taurus
import matplotlib.pyplot as plt

# Rutas
BASE_DIR = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo"
RESULTS_DIR = os.path.join(BASE_DIR, "output/Galform/Validacion_Cortes")
PLOT_FILE = os.path.join(RESULTS_DIR, "LF_Cortes_Comparacion.png")

cortes = [5, 6, 7, 8]
colores = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728'] # Azul, Verde, Naranja, Rojo

print("\n" + "="*50)
print("DIBUJANDO FUNCIÓN DE LUMINOSIDAD DE LOS CORTES")
print("="*50)

# Preparamos el lienzo
plt.figure(figsize=(10, 7))

for corte, color in zip(cortes, colores):
    archivo = os.path.join(RESULTS_DIR, f"LF_Validacion_Corte{corte}.h5")
    
    if os.path.exists(archivo):
        with h5py.File(archivo, 'r') as f:
            bin_edges = f['bin_edges'][:]
            phi = f['phi'][:]
            
            # El eje X son los límites de las cajas. Para dibujar el punto, 
            # calculamos el centro exacto de cada caja.
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0
            
            # Máscara de seguridad: solo dibujamos donde haya galaxias reales (phi > 0)
            # Esto evita que el logaritmo explote hacia infinito negativo
            mask = phi > 0
            
            plt.plot(bin_centers[mask], phi[mask], marker='o', markersize=6, 
                     linewidth=2, linestyle='-', color=color, label=f'Corte {corte}')
            print(f"✅ Añadido Corte {corte} a la gráfica.")
    else:
        print(f"⚠️ Archivo no encontrado para el Corte {corte}")

# Configuración estética y física de la gráfica
plt.yscale('log') # La Función de Luminosidad SIEMPRE va en escala logarítmica en el eje Y
plt.xlabel(r'$\log_{10}(L_{\rm bol} \, / \, {\rm erg \, s^{-1}})$', fontsize=14)
plt.ylabel(r'$\Phi \, [{\rm h^3 \, Mpc^{-3} \, mag^{-1}}]$', fontsize=14)
plt.title('Función de Luminosidad Bolométrica por Cortes (Galform)', fontsize=16, pad=15)

# Añadimos la leyenda y una cuadrícula para que se lea mejor
plt.legend(fontsize=12, loc='upper right')
plt.grid(True, which="both", ls="--", alpha=0.4)

# Ajustamos márgenes y guardamos
plt.tight_layout()
plt.savefig(PLOT_FILE, dpi=300, bbox_inches='tight')
print(f"\n🎉 Gráfica guardada exitosamente en: {PLOT_FILE}")
