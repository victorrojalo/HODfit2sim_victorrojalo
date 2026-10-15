import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
import mpl_style

# --- 1. ESTILO PAPER ---
plt.style.use(mpl_style.style1)

# Lista de los cortes que nos faltan (puedes añadir el 5 si quieres regenerarlo)
CORTES_A_PROCESAR = [5, 6, 7, 8]

for CORTE in CORTES_A_PROCESAR:
    print(f"\n" + "="*50)
    print(f"🚀 Iniciando clonación de la Figura 5 para el CORTE {CORTE}...")
    print("="*50)

    BASE_DIR = f"/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/output/Mvir/Corte{CORTE}/Centrales"

    # Vaciamos las listas para que no se mezclen los datos de un corte con el anterior
    k1_lista, k2_lista = [], []
    k1_glob_lista, k2_glob_lista = [], []
    nsat_tot_lista, nsat_c1_lista, nsat_c0_lista = [], [] , []
    mass_bins = None
    vols_leidos = 0

    # --- 2. RECOLECTAR DATOS ---
    for i in range(64):
        archivo = os.path.join(BASE_DIR, f"conformity_vol{i}.h5")
        
        if os.path.exists(archivo):
            try:
                with h5py.File(archivo, 'r') as f:
                    if mass_bins is None:
                        m_min = f['data/bins/M_min_bin'][:]
                        m_max = f['data/bins/M_max_bin'][:]
                        mass_bins = (m_min + m_max) / 2.0
                    
                    n_h = f['data/bins/N_Halos'][:]
                    n_s = f['data/bins/N_S'][:]
                    k1 = f['data/bins/k1'][:]
                    k2 = f['data/bins/k2'][:]
                    k1_g = f['data/global/k1_global'][()]
                    k2_g = f['data/global/k2_global'][()]
                    
                    with np.errstate(divide='ignore', invalid='ignore'):
                        nsat_tot = np.where(n_h > 0, n_s / n_h, np.nan)
                        nsat_c1 = k1 * nsat_tot
                        nsat_c0 = k2 * nsat_tot
                        
                        k1_clean = np.where(n_h > 0, k1, np.nan)
                        k2_clean = np.where(n_h > 0, k2, np.nan)

                    k1_lista.append(k1_clean)
                    k2_lista.append(k2_clean)
                    k1_glob_lista.append(k1_g)
                    k2_glob_lista.append(k2_g)
                    nsat_tot_lista.append(nsat_tot)
                    nsat_c1_lista.append(nsat_c1)
                    nsat_c0_lista.append(nsat_c0)
                    
                    vols_leidos += 1
            except Exception as e:
                pass

    if vols_leidos == 0:
        print(f"❌ Error: No se encontraron datos para el Corte {CORTE}. Saltando al siguiente...")
        continue

    print(f"✅ Promediando datos de {vols_leidos} volúmenes...")

    # --- 3. PROMEDIAR ---
    with np.errstate(invalid='ignore'):
        mean_k1 = np.nanmean(k1_lista, axis=0)
        mean_k2 = np.nanmean(k2_lista, axis=0)
        mean_nsat_tot = np.nanmean(nsat_tot_lista, axis=0)
        mean_nsat_c1 = np.nanmean(nsat_c1_lista, axis=0)
        mean_nsat_c0 = np.nanmean(nsat_c0_lista, axis=0)
        
        k1_glob_avg = np.nanmean(k1_glob_lista)
        k2_glob_avg = np.nanmean(k2_glob_lista)

    # --- 4. DIBUJAR LA GRÁFICA (3 PANELES) ---
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 10), sharex=True)
    fig.subplots_adjust(hspace=0.05)

    # --- PANEL 1: Ocupación de Satélites ---
    mask1 = mean_nsat_tot > 0
    ax1.plot(mass_bins[mask1], mean_nsat_tot[mask1], '-', color='#ff7f0e', label=r'$\langle N_{\rm sat} \rangle$')
    ax1.plot(mass_bins[mask1], mean_nsat_c1[mask1], '-.', color='#1f77b4', label=r'$\langle N_{\rm sat} | N_{\rm cen}=1 \rangle$')
    ax1.plot(mass_bins[mask1], mean_nsat_c0[mask1], '--', color='#2ca02c', label=r'$\langle N_{\rm sat} | N_{\rm cen}=0 \rangle$')

    ax1.set_yscale('log')
    ax1.set_ylabel(r'$\langle N_{\rm sat} \rangle$', fontsize=14)
    ax1.legend(loc='lower right', fontsize=11)
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    if np.any(~np.isnan(mean_nsat_c1[mask1])):
        ax1.set_ylim(1e-4, np.nanmax(mean_nsat_c1[mask1]) * 2.0)

    # --- PANEL 2: Factor de Conformidad K1 ---
    ax2.plot(mass_bins, mean_k1, '-.', color='#1f77b4', label=r'$K_1(M)$')
    ax2.axhline(k1_glob_avg, color='#d62728', linestyle='-.', label=r'$K_{1, {\rm glob}}$')

    ax2.set_ylabel(r'$K_1$', fontsize=14)
    ax2.legend(loc='upper left', fontsize=11)
    ax2.grid(True, linestyle='--', alpha=0.5)

    if not np.isnan(k1_glob_avg):
        k1_validos = mean_k1[~np.isnan(mean_k1)]
        if len(k1_validos) > 0:
            techo_k1 = max(k1_glob_avg * 1.5, np.percentile(k1_validos, 95) * 1.2)
            ax2.set_ylim(0.0, techo_k1)

    # --- PANEL 3: Factor de Conformidad K2 ---
    ax3.plot(mass_bins, mean_k2, '--', color='#2ca02c', label=r'$K_2(M)$')
    ax3.axhline(k2_glob_avg, color='#d62728', linestyle='--', label=r'$K_{2, {\rm glob}}$')

    ax3.set_ylabel(r'$K_2$', fontsize=14)
    ax3.set_xlabel(r"$\log_{10}(M_{\rm halo} \ / \ M_{\odot} h^{-1})$", fontsize=14)
    ax3.legend(loc='lower left', fontsize=11)
    ax3.grid(True, linestyle='--', alpha=0.5)
    ax3.set_xlim(10.5, 14.5)

    if not np.isnan(k2_glob_avg):
        k2_validos = mean_k2[~np.isnan(mean_k2)]
        if len(k2_validos) > 0:
            techo_k2 = max(0.3, k2_glob_avg * 2.0, np.percentile(k2_validos, 95) * 1.2)
            ax3.set_ylim(0.0, techo_k2)

    plt.tight_layout()

    GRAFICA_SALIDA = os.path.join(BASE_DIR, f"Grafica_TFM_Fig6_Conformidad_Corte{CORTE}.png")
    plt.savefig(GRAFICA_SALIDA, dpi=300, bbox_inches='tight')
    
    # Cerramos la figura actual para que no se superponga con la del siguiente corte
    plt.close(fig)
    
    print(f"🎉 ¡Gráfica del Corte {CORTE} guardada con éxito en su carpeta!")
    print(f"   -> Valor medio K1_glob: {k1_glob_avg:.3f}")
    print(f"   -> Valor medio K2_glob: {k2_glob_avg:.3f}")

print("\n¡PROCESO COMPLETADO! Revisa las carpetas de tus cortes. 🚀")
