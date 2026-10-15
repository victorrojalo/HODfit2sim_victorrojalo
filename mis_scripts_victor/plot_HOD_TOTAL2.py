import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 1. APLICAR TU ESTILO PRO ---
import mpl_style
plt.style.use(mpl_style.style1)

# --- 2. ARCHIVOS DE DATOS ---
# Pon aquí los nombres reales que te ha generado tu código para cada población
FILE_CENTRALES = "HOD_Centrales_Shark_Corte1.h5"  # <-- CAMBIAR por tu archivo real
FILE_SATELITES = "HOD_Satelites_Shark_Corte1.h5"  # <-- CAMBIAR por tu archivo real

plt.figure(figsize=(8, 7))

# Variables para guardar los datos y sumarlos después
mass_bins = None
N_cen = None
N_sat = None

# --- 3. CARGAR Y PINTAR CENTRALES ---
if os.path.exists(FILE_CENTRALES):
    print("Leyendo Centrales...")
    with h5py.File(FILE_CENTRALES, 'r') as f:
        # Ajusta estas claves ('mass', 'N_mean') según cómo las guardaste en tu script
        mass_bins = f['mass'][:] 
        N_cen = f['N_mean'][:]
    
    # Pintamos centrales (suele usarse línea punteada o discontinua para distinguirlas)
    plt.plot(mass_bins, N_cen, '--', color='#1f77b4', linewidth=2.5, label='Centrales')

# --- 4. CARGAR Y PINTAR SATÉLITES ---
if os.path.exists(FILE_SATELITES):
    print("Leyendo Satélites...")
    with h5py.File(FILE_SATELITES, 'r') as f:
        mass_bins = f['mass'][:]
        N_sat = f['N_mean'][:]
        
    # Pintamos satélites
    plt.plot(mass_bins, N_sat, '-.', color='#ff7f0e', linewidth=2.5, label='Satélites')

# --- 5. CALCULAR Y PINTAR EL TOTAL ---
if N_cen is not None and N_sat is not None:
    print("Calculando HOD Total...")
    N_total = N_cen + N_sat
    # El total suele ir en línea continua y color negro o un color fuerte
    plt.plot(mass_bins, N_total, '-', color='black', linewidth=3, label='Total')

# --- 6. CONFIGURACIÓN DE LA GRÁFICA ---
plt.title("Halo Occupation Distribution (HOD) - ELGs")

# Eje X en logaritmo (Masa del halo)
plt.xscale('log')
plt.xlabel(r"$M_{\rm halo} \ [M_{\odot} h^{-1}]$")
# Límites típicos de masa para HOD
plt.xlim(1e11, 1e15)

# Eje Y en logaritmo (Número medio de galaxias)
plt.yscale('log')
plt.ylabel(r"$\langle N_{\rm gal} \rangle$")
# Límites típicos de N (desde fracciones muy pequeñas hasta cientos)
plt.ylim(1e-3, 1e2)

# Añadir una línea horizontal en N=1 de referencia (muy útil visualmente)
plt.axhline(1, color='gray', linestyle=':', alpha=0.7)

plt.legend(loc='lower right') # Abajo a la derecha suele estar vacío en las gráficas HOD

GRAFICA_SALIDA = "Grafica_TFM_7_HOD_Completa.png"
plt.savefig(GRAFICA_SALIDA, dpi=300)
print(f"¡HOD generada con éxito! Guardada en: {GRAFICA_SALIDA}")
