import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
import mpl_style
plt.style.use(mpl_style.style1)


# Rutas de tus archivos (Ajusta si los nombres varían)
F_ROCKSTAR_MVIR = "HMF_Rockstar_Mvir.h5"
F_ROCKSTAR_M200C = "HMF_Rockstar_M200c.h5"
F_SHARK = "HMF_Shark_Centrales.h5"
F_GALFORM = "HMF_Galform_Centrales.h5"

def leer_datos(archivo):
    if not os.path.exists(archivo):
        print(f"⚠️ Archivo no encontrado: {archivo}")
        return None, None
    with h5py.File(archivo, 'r') as f:
        # Usamos los nombres de datasets que vimos en tu código anterior
        edges = f['bin_edges'][:]
        mass_centers = (edges[:-1] + edges[1:]) / 2.0
        counts = f['total_counts'][:]
        return mass_centers, counts

print("Cargando datos...")
m_rvir, n_rvir = leer_datos(F_ROCKSTAR_MVIR)
m_r200, n_r200 = leer_datos(F_ROCKSTAR_M200C)
m_sh, n_sh = leer_datos(F_SHARK)
m_gf, n_gf = leer_datos(F_GALFORM)

# Función auxiliar para graficar y no repetir código
def generar_grafica_ratio(m_halo, n_halo, m_sh, n_sh, m_gf, n_gf, nombre_materia, nombre_salida):
    plt.figure(figsize=(9, 6))
    
    # Calculamos ratios (añadimos epsilon para evitar division por cero)
    #eps = 1e-10
    #ratio_sh = n_sh / (n_halo + eps)
    #ratio_gf = n_gf / (n_halo + eps)
    
    plt.plot(m_rvir, m_sh, label=f'Shark / {nombre_materia}', color='blue', linewidth=2.5)
    plt.plot(m_rvir, m_gf, label=f'Galform / {nombre_materia}', color='red', linestyle='--', linewidth=2.5)
    
    #plt.axhline(1.0, color='black', linestyle=':', alpha=0.5, label='100% Ocupación')
    
    plt.title(f"Fracción de Ocupación: Modelos vs {nombre_materia}", fontsize=14)
    plt.xlabel(r"$\log_{10}(M \ / \ M_{\odot} h^{-1})$", fontsize=13)
    plt.ylabel("Ratio (N_gal / N_halo)", fontsize=13)
    
    plt.ylim(10, 16)
    plt.xlim(10, 16)
    plt.grid(True, which="both", ls="--", alpha=0.4)
    plt.legend()
    
    plt.savefig(nombre_salida, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfica guardada: {nombre_salida}")

# --- EJECUCIÓN ---

if n_rvir is not None:
    generar_grafica_ratio(m_rvir, n_rvir, m_sh, n_sh, m_gf, n_gf, "Shark Mvir", "Ratio_HMF_Mvir_Shark_Estilo.png")

if n_r200 is not None:
    generar_grafica_ratio(m_r200, n_rvir, m_sh, n_sh, m_gf, n_gf, "Galform M200c", "Ratio_HMF_Mvir_Galform_Estilo.png")

print("\n¡Proceso finalizado!")
