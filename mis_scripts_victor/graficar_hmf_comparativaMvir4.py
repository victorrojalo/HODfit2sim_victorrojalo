import h5py
import numpy as np
import matplotlib.pyplot as plt

# 1. Archivos de entrada
F_ROCKSTAR_MVIR = "HMF_Rockstar_Mvir.h5"
F_ROCKSTAR_M200C = "HMF_Rockstar_M200C.h5"
F_SHARK = "HMF_Shark_Centrales.h5"
F_GALFORM = "HMF_Galform_Centrales.h5"

# Nombres de las dos imágenes que se van a generar
GRAFICA_SALIDA_MVIR = "Grafica_HMF_Solo_Mvir.png"
GRAFICA_SALIDA_M200C = "Grafica_HMF_Solo_M200c.png"

# Función bilingüe (Mantenemos la que arregla el error de Rockstar)
def leer_hmf(archivo):
    with h5py.File(archivo, 'r') as f:
        if "bin_edges" in f and "total_counts" in f:
            edges = f["bin_edges"][:]
            mass = (edges[:-1] + edges[1:]) / 2.0
            counts = f["total_counts"][:]
        elif "data" in f:
            if "M_min_bin" in f["data"]: mass = f["data"]["M_min_bin"][:]
            elif "M_min" in f["data"]: mass = f["data"]["M_min"][:]
            else: raise KeyError(f"No masa en {archivo}")
                
            if "N_Cen" in f["data"]: counts = f["data"]["N_Cen"][:]
            elif "N_Halos" in f["data"]: counts = f["data"]["N_Halos"][:]
            else: counts = f["data"][list(f["data"].keys())[1]][:]
        else:
            raise ValueError(f"Estructura desconocida en {archivo}")
    return mass, counts

print("Cargando los datos...")
m_rk_vir, n_rk_vir = leer_hmf(F_ROCKSTAR_MVIR)
m_rk_200, n_rk_200 = leer_hmf(F_ROCKSTAR_M200C)
m_sh, n_sh = leer_hmf(F_SHARK)
m_gf, n_gf = leer_hmf(F_GALFORM)


# ==========================================
# GRÁFICA 1: EJE X = MVIR
# ==========================================
print("Generando Gráfica 1 (Mvir)...")
plt.figure(figsize=(8, 6))

plt.plot(m_rk_vir, np.log10(n_rk_vir + 1e-5), label='Rockstar (DM Halos)', color='black', linewidth=2.5)
plt.plot(m_sh, np.log10(n_sh + 1e-5), label='Shark (Centrales)', color='blue', linestyle='--', linewidth=2)
plt.plot(m_gf, np.log10(n_gf + 1e-5), label='Galform (Centrales)', color='red', linestyle='-.', linewidth=2)

plt.title("HMF: Galaxias Centrales vs Rockstar (Mvir)", fontsize=14)
# ¡AQUÍ PONEMOS Mvir EN EL EJE X!
plt.xlabel(r"$\log_{10}(M_{\rm vir} / M_{\odot} h^{-
