import h5py
import numpy as np
import matplotlib.pyplot as plt

# 1. Definimos los nombres exactos de tus 4 archivos
F_ROCKSTAR_MVIR = "HMF_Rockstar_Mvir.h5"
F_ROCKSTAR_M200C = "HMF_Rockstar_M200C.h5"
F_SHARK = "HMF_Shark_Centrales.h5"
F_GALFORM = "HMF_Galform_Centrales.h5"

GRAFICA_SALIDA = "Comparativa_HMF_Modelos_vs_DM.png"

# Función auxiliar para leer los datos de cualquier archivo .h5
def leer_hmf(archivo):
    with h5py.File(archivo, 'r') as f:
        # Extraer los bines de masa
        if "data/M_min_bin" in f:
            mass = f["data/M_min_bin"][:]
        elif "data/M_min" in f:
            mass = f["data/M_min"][:]
        else:
            # Por si están guardados directamente en la raíz
            mass = f["M_min_bin"][:]
            
        # Extraer las cuentas (Halos o Galaxias)
        if "data/N_Cen" in f:
            counts = f["data/N_Cen"][:]
        elif "data/N_Halos" in f:
            counts = f["data/N_Halos"][:]
        elif "N_Halos" in f:
             counts = f["N_Halos"][:]
        else:
            # Si no encuentra ninguna, asume que es la primera key de datos
            counts = f["data"][list(f["data"].keys())[1]][:]
            
    return mass, counts

print("Cargando los 4 catálogos de HMF...")
# 2. Leemos los 4 catálogos
m_rk_vir, n_rk_vir = leer_hmf(F_ROCKSTAR_MVIR)
m_rk_200, n_rk_200 = leer_hmf(F_ROCKSTAR_M200C)
m_sh, n_sh = leer_hmf(F_SHARK)
m_gf, n_gf = leer_hmf(F_GALFORM)

print("Generando la gráfica de doble panel...")
# 3. Creamos la figura con 2 paneles (1 fila, 2 columnas)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# --- PANEL IZQUIERDO: Referencia Mvir ---
# Rockstar en negro continuo, Modelos en discontinua
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
