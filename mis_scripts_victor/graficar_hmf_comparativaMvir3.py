import h5py
import numpy as np
import matplotlib.pyplot as plt

# 1. Definimos los nombres exactos de tus 4 archivos
F_ROCKSTAR_MVIR = "HMF_Rockstar_Mvir.h5"
F_ROCKSTAR_M200C = "HMF_Rockstar_M200C.h5"
F_SHARK = "HMF_Shark_Centrales.h5"
F_GALFORM = "HMF_Galform_Centrales.h5"

GRAFICA_SALIDA = "Comparativa_HMF_Modelos_vs_DM.png"

# Función bilingüe: Entiende los archivos de Rockstar y los tuyos propios
def leer_hmf(archivo):
    with h5py.File(archivo, 'r') as f:
        
        # CASO A: Es un archivo original de Rockstar (tiene "bin_edges" en la raíz)
        if "bin_edges" in f and "total_counts" in f:
            edges = f["bin_edges"][:]
            # Calculamos el centro exacto de la caja de masa sumando los bordes y dividiendo por 2
            mass = (edges[:-1] + edges[1:]) / 2.0
            counts = f["total_counts"][:]
            
        # CASO B: Es tu archivo de Shark o Galform (tiene carpeta "data")
        elif "data" in f:
            # Buscamos la variable de masa
            if "M_min_bin" in f["data"]:
                mass = f["data"]["M_min_bin"][:]
            elif "M_min" in f["data"]:
                mass = f["data"]["M_min"][:]
            else:
                raise KeyError(f"No se encontró la variable de masa en {archivo}")
                
            # Buscamos la variable de cuentas (Prioridad: Galaxias Centrales)
            if "N_Cen" in f["data"]:
                counts = f["data"]["N_Cen"][:]
            elif "N_Halos" in f["data"]:
                counts = f["data"]["N_Halos"][:]
            else:
                # Si no encuentra el nombre exacto, coge la segunda columna de datos por defecto
                claves = list(f["data"].keys())
                counts = f["data"][claves[1]][:]
                
        else:
            raise ValueError(f"¡Estructura totalmente desconocida en el archivo {archivo}!")
            
    return mass, counts

print("Cargando los 4 catálogos de HMF...")
# 2. Leemos los 4 catálogos usando nuestra súper función
m_rk_vir, n_rk_vir = leer_hmf(F_ROCKSTAR_MVIR)
m_rk_200, n_rk_200 = leer_hmf(F_ROCKSTAR_M200C)
m_sh, n_sh = leer_hmf(F_SHARK)
m_gf, n_gf = leer_hmf(F_GALFORM)

print("Generando la gráfica de doble panel...")
# 3. Creamos la figura con 2 paneles (1 fila, 2 columnas)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# --- PANEL IZQUIERDO: Referencia Mvir ---
ax1.plot(m_rk_vir, np.log10(n_rk_vir + 1e-5), label='Rockstar (Mvir)', color='black', linewidth=2.5)
ax1.plot(m_sh, np.log10(n_sh + 1e-5), label='Shark (Centrales)', color='blue', linestyle='--', linewidth=2)
ax1.plot(m_gf, np.log10(n_gf + 1e-5), label='Galform (Centrales)', color='red', linestyle='-.', linewidth=2)

ax1.set_title("A. Referencia: Masa Virial (Mvir)", fontsize=14)
ax1.set_xlabel(r"$\log_{10}(M_{\rm halo} / M_{\odot} h^{-1})$", fontsize=12)
ax1.set_ylabel(r"$\log_{10}(N)$", fontsize=12)
ax1.set_xlim(10.5, 14.5)
ax1.set_ylim(0, 7) # Ajusta este valor si se te cortan por arriba
ax1.grid(True, which='both', ls='--', alpha=0.5)
ax1.legend(fontsize=11)

# --- PANEL DERECHO: Referencia M200c ---
ax2.plot(m_rk_200, np.log10(n_rk_200 + 1e-5), label='Rockstar (M200c)', color='gray', linewidth=2.5)
ax2.plot(m_sh, np.log10(n_sh + 1e-5), label='Shark (Centrales)', color='blue', linestyle='--', linewidth=2)
ax2.plot(m_gf, np.log10(n_gf + 1e-5), label='Galform (Centrales)', color='red', linestyle='-.', linewidth=2)

ax2.set_title("B. Referencia: Masa 200c (M200c)", fontsize=14)
ax2.set_xlabel(r"$\log_{10}(M_{\rm halo} / M_{\odot} h^{-1})$", fontsize=12)
ax2.set_xlim(10.5, 14.5)
ax2.grid(True, which='both', ls='--', alpha=0.5)
ax2.legend(fontsize=11)

# 4. Ajustes finales y guardar
plt.suptitle("Comparativa HMF: Galaxias Centrales vs Referencia de Materia Oscura", fontsize=16, y=1.02)
plt.tight_layout()

plt.savefig(GRAFICA_SALIDA, dpi=300, bbox_inches='tight')
print(f"¡Éxito! Gráfica guardada como: {GRAFICA_SALIDA}")
