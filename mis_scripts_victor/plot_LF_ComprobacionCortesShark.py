import os
import h5py
import numpy as np
import matplotlib
matplotlib.use('Agg') # Escudo anti-errores de pantalla en taurus
import matplotlib.pyplot as plt

# Rutas
BASE_DIR = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo"
RESULTS_DIR = os.path.join(BASE_DIR, "output/Shark/Validacion_Cortes")
PLOT_FILE = os.path.join(RESULTS_DIR, "LF_Cortes_ComparacionShark.png")

cortes = [5, 6, 7, 8]
colores = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728'] # Azul, Verde, Naranja, Rojo

print("\n" + "="*50)
print("DIBUJANDO FUNCIÓN DE LUMINOSIDAD DE LOS CORTES")
print("="*50)

# Preparamos el lienzo
plt.figure(figsize=(10, 7))
archivos_leidos = 0

for corte, color in zip(cortes, colores):
    archivo = os.path.join(RESULTS_DIR, f"LF_Validacion_Corte{corte}.h5")

    if os.path.exists(archivo):
        with h5py.File(archivo, 'r') as f:
            bin_edges = f['bin_edges'][:]
            phi = f['phi'][:]

            # El eje X son los límites de las cajas.
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0

            # Máscara de seguridad
            mask = phi > 0
            puntos_validos = np.sum(mask)

            if puntos_validos > 0:
                plt.plot(bin_centers[mask], phi[mask], marker='o', markersize=6,
                         linewidth=2, linestyle='-', color=color, label=f'Corte {corte}')
                print(f"✅ Añadido Corte {corte}: dibujando {puntos_validos} puntos.")
                archivos_leidos += 1
            else:
                print(f"⚠️ Corte {corte} encontrado, pero todos sus valores Phi son cero.")
    else:
        print(f"❌ ARCHIVO NO ENCONTRADO: {archivo}")

# Configuración estética y física de la gráfica
plt.yscale('log') 

# --- AQUI ESTA LA MAGIA DEL ENCUADRE ---
# Forzamos los límites exactos de la gráfica que quieres de referencia
plt.xlim(41.5, 47)
plt.ylim(5e-7, 4e-3)

plt.xlabel(r'$\log_{10}(L_{\rm bol} \, / \, {\rm erg \, s^{-1}})$', fontsize=14)
plt.ylabel(r'$\Phi \, [{\rm h^3 \, Mpc^{-3} \, mag^{-1}}]$', fontsize=14)
plt.title('Función de Luminosidad Bolométrica por Cortes (Shark)', fontsize=16, pad=15)

# Añadimos la leyenda y una cuadrícula
if archivos_leidos > 0:
    plt.legend(fontsize=12, loc='upper right')
plt.grid(True, which="both", ls="--", alpha=0.4)

# Ajustamos márgenes y guardamos
plt.tight_layout()
plt.savefig(PLOT_FILE, dpi=300, bbox_inches='tight')

if archivos_leidos == 0:
    print(f"\n[!] ALERTA CRÍTICA: La gráfica saldrá en blanco porque no se leyó ningún dato.")
    print(f"    ¿Te aseguraste de ejecutar primero 'main_HISTOGRAMA_Comprobacion_Cortes.py'?")
else:
    print(f"\n🎉 Gráfica guardada exitosamente en: {PLOT_FILE}")
