import os
import h5py
import numpy as np
import matplotlib
# Esto es VITAL en Taurus para que no dé error por no tener pantalla
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

# ===================================================================
# 1. FUNCIÓN PARA LEER LOS ARCHIVOS .h5
# ===================================================================
def leer_h5(filename):
    # Asume que los archivos están en la misma carpeta desde donde ejecutas el script
    if not os.path.exists(filename):
        print(f"[Aviso] No se encontró {filename}")
        return None, None
        
    with h5py.File(filename, 'r') as f:
        edges = f['bin_edges'][:]
        phi = f['phi'][:]
        
    # Calculamos el centro matemático de cada cajón
    centros = (edges[:-1] + edges[1:]) / 2.0
    return centros, phi

# ===================================================================
# 2. PREPARACIÓN DE LA FIGURA
# ===================================================================
plt.figure(figsize=(10, 8))

# ===================================================================
# 3. CARGAR Y PINTAR LOS DATOS
# ===================================================================

# --- MATERIA OSCURA (ROCKSTAR) ---
x, y = leer_h5("HMF_Rockstar_Mvir.h5")
if x is not None: plt.plot(x[y>0], y[y>0], color='black', linestyle='-', linewidth=2.5, label="Materia Oscura (Mvir)")

x, y = leer_h5("HMF_Rockstar_M200C.h5")
if x is not None: plt.plot(x[y>0], y[y>0], color='gray', linestyle='--', linewidth=2.5, label="Materia Oscura (M200c)")

# --- SHARK ---
x, y = leer_h5("HMF_Shark_TOTAL.h5")
if x is not None: plt.plot(x[y>0], y[y>0], color='blue', linestyle='-', linewidth=1.5, label="Shark (Total)")

x, y = leer_h5("HMF_Shark_Centrales.h5")
if x is not None: plt.plot(x[y>0], y[y>0], color='blue', linestyle='--', linewidth=1.5, label="Shark (Centrales)")

x, y = leer_h5("HMF_Shark_Satelites.h5")
if x is not None: plt.plot(x[y>0], y[y>0], color='blue', linestyle=':', linewidth=1.5, label="Shark (Satélites)")

# --- GALFORM ---
x, y = leer_h5("HMF_Galform_TOTAL.h5")
if x is not None: plt.plot(x[y>0], y[y>0], color='red', linestyle='-', linewidth=1.5, label="Galform (Total)")

x, y = leer_h5("HMF_Galform_Centrales.h5")
if x is not None: plt.plot(x[y>0], y[y>0], color='red', linestyle='--', linewidth=1.5, label="Galform (Centrales)")

x, y = leer_h5("HMF_Galform_Satelites.h5")
if x is not None: plt.plot(x[y>0], y[y>0], color='red', linestyle=':', linewidth=1.5, label="Galform (Satélites)")

# ===================================================================
# 4. ESTÉTICA DE LA GRÁFICA Y GUARDADO
# ===================================================================
plt.yscale('log') # El eje Y debe ser logarítmico para la HMF
plt.xlabel(r'$\log_{10}(M_{halo} / M_\odot h^{-1})$', fontsize=14)
plt.ylabel(r'$\Phi \ [h^3 \ \rm{Mpc}^{-3} \ \rm{dex}^{-1}]$', fontsize=14)
plt.title('Comparativa HMF: Rockstar vs Shark vs Galform', fontsize=16)

# Ponemos la leyenda, rejilla y ajustamos los límites
plt.legend(fontsize=11, loc='lower left')
plt.grid(True, which="both", linestyle="--", alpha=0.3)
plt.ylim(1e-6, 1e0) # Ajusta estos límites si ves que la gráfica queda muy vacía o cortada
plt.xlim(10.5, 14.5)

# Guardar la imagen
output_name = "Grafica_HMF_Sencilla.png"
plt.savefig(output_name, dpi=300, bbox_inches='tight')
print(f"✅ ¡Éxito! Gráfica guardada como: {output_name}")
