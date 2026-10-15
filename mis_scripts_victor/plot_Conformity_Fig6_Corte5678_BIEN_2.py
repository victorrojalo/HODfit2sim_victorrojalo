import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
import mpl_style
from scipy.optimize import curve_fit

# --- 1. ESTILO PAPER ---
plt.style.use(mpl_style.style1)

# Lista de los cortes que nos faltan
CORTES_A_PROCESAR = [5, 6, 7, 8]

# Función constante para el ajuste
def funcion_constante(x, c):
    return np.full_like(x, c)

for CORTE in CORTES_A_PROCESAR:
    print(f"\n" + "="*50)
    print(f"🚀 Iniciando corrección y clonación de la Figura 6 para el CORTE {CORTE}...")
    print("="*50)

    BASE_DIR = f"/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/output/Mvir/Corte{CORTE}/Centrales"

    mass_bins = None
    vols_leidos = 0

    # HUCHAS GLOBALES PARA LOS CONTEOS CRUDOS (Para evitar el bug de dividir por 64)
    SUM_N_H = None
    SUM_N_C = None
    SUM_N_S = None
    SUM_N_SWC = None
    SUM_N_SWNC = None

    # --- 2. RECOLECTAR DATOS CRUDOS ---
    for i in range(64):
        archivo = os.path.join(BASE_DIR, f"conformity_vol{i}.h5")

        if os.path.exists(archivo):
            try:
                with h5py.File(archivo, 'r') as f:
                    # Si es el primer archivo, inicializamos las huchas
                    if mass_bins is None:
                        m_min = f['data/bins/M_min_bin'][:]
                        m_max = f['data/bins/M_max_bin'][:]
                        mass_bins = (m_min + m_max) / 2.0

                        SUM_N_H = f['data/bins/N_Halos'][:]
                        SUM_N_C = np.zeros_like(SUM_N_H, dtype=float)
                        SUM_N_S = np.zeros_like(SUM_N_H, dtype=float)
                        SUM_N_SWC = np.zeros_like(SUM_N_H, dtype=float)
                        SUM_N_SWNC = np.zeros_like(SUM_N_H, dtype=float)

                    # Sacamos los conteos de este volumen
                    n_c = f['data/bins/N_C'][:]
                    n_s = f['data/bins/N_S'][:]

                    # Intentamos sacar N_swc directo, si no existe, lo reconstruimos
                    try:
                        n_swc = f['data/bins/N_swc'][:]
                        n_swnc = f['data/bins/N_swnc'][:]
                    except KeyError:
                        k1 = f['data/bins/k1'][:]
                        k2 = f['data/bins/k2'][:]
                        with np.errstate(divide='ignore', invalid='ignore'):
                            n_swc = np.where(SUM_N_H > 0, k1 * n_c * n_s / SUM_N_H, 0)
                            n_swnc = np.where(SUM_N_H > 0, k2 * (SUM_N_H - n_c) * n_s / SUM_N_H, 0)

                            # Limpiamos NaNs
                            n_swc = np.nan_to_num(n_swc, 0)
                            n_swnc = np.nan_to_num(n_swnc, 0)

                    # Sumamos a las huchas globales \N_H NO HAGO SUM PQ SON LAS TOTALES
                    SUM_N_C += n_c
                    SUM_N_S += n_s
                    SUM_N_SWC += n_swc
                    SUM_N_SWNC += n_swnc

                    vols_leidos += 1
            except Exception as e:
                print(f"⚠️ Error leyendo {archivo}: {e}")

    if vols_leidos == 0:
        print(f"❌ Error: No se encontraron datos para el Corte {CORTE}. Saltando...")
        continue

    print(f"✅ Reconstruyendo matemática global a partir de {vols_leidos} volúmenes...")

    # --- 3. CÁLCULO FÍSICO GLOBAL (AQUÍ SUCEDE LA MAGIA) ---
    with np.errstate(divide='ignore', invalid='ignore'):
        # Ocupaciones medias reales
        mean_nsat_tot = np.where(SUM_N_H > 0, SUM_N_S / SUM_N_H, np.nan)
        mean_nsat_c1 = np.where(SUM_N_C > 0, SUM_N_SWC / SUM_N_C, np.nan)
        mean_nsat_c0 = np.where((SUM_N_H - SUM_N_C) > 0, SUM_N_SWNC / (SUM_N_H - SUM_N_C), np.nan)

        # Valores reales de Conformidad K1 y K2 bin a bin
        mean_k1 = np.where(mean_nsat_tot > 0, mean_nsat_c1 / mean_nsat_tot, np.nan)
        mean_k2 = np.where(mean_nsat_tot > 0, mean_nsat_c0 / mean_nsat_tot, np.nan)

        # --- AJUSTE CON CURVE_FIT ---
        # Filtramos los NaNs e Infinitos para poder hacer el ajuste
        mask_valid_k1 = ~np.isnan(mean_k1) & np.isfinite(mean_k1)
        mask_valid_k2 = ~np.isnan(mean_k2) & np.isfinite(mean_k2)

        k1_glob_avg = np.nan
        err_k1_glob = np.nan
        k2_glob_avg = np.nan
        err_k2_glob = np.nan

        if np.sum(mask_valid_k1) > 2: # Necesitamos algunos puntos para ajustar
            xdata_k1 = mass_bins[mask_valid_k1]
            ydata_k1 = mean_k1[mask_valid_k1]
            try:
                popt_k1, pcov_k1 = curve_fit(funcion_constante, xdata_k1, ydata_k1)
                k1_glob_avg = popt_k1[0]
                err_k1_glob = np.sqrt(np.diag(pcov_k1))[0]
            except Exception as e:
                print(f"⚠️ No se pudo ajustar K1 para el Corte {CORTE}: {e}")
                k1_glob_avg = np.nanmean(ydata_k1) # Fallback al promedio si falla

        if np.sum(mask_valid_k2) > 2:
            xdata_k2 = mass_bins[mask_valid_k2]
            ydata_k2 = mean_k2[mask_valid_k2]
            try:
                popt_k2, pcov_k2 = curve_fit(funcion_constante, xdata_k2, ydata_k2)
                k2_glob_avg = popt_k2[0]
                err_k2_glob = np.sqrt(np.diag(pcov_k2))[0]
            except Exception as e:
                print(f"⚠️ No se pudo ajustar K2 para el Corte {CORTE}: {e}")
                k2_glob_avg = np.nanmean(ydata_k2) # Fallback al promedio si falla

    # --- 4. DIBUJAR LA GRÁFICA (3 PANELES) ---
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 10), sharex=True)
    fig.subplots_adjust(hspace=0.05)

    # --- PANEL 1: Ocupación de Satélites ---
    mask1 = mean_nsat_tot > 0
    ax1.plot(mass_bins[mask1], mean_nsat_tot[mask1], '-', color='#ff7f0e', label=r'$\langle N_{\rm sat} \rangle$')
    ax1.plot(mass_bins[mask1], mean_nsat_c1[mask1], '-.', color='#1f77b4', label=r'$\langle N_{\rm sat} | N_{\rm cen}=1 \rangle$')
    ax1.plot(mass_bins[mask1], mean_nsat_c0[mask1], '--', color='#2ca02c', label=r'$\langle N_{\rm sat} | N_{\rm cen}=0 \rangle$')

    ax1.set_yscale('log')
    ax1.set_ylabel(r'$\langle N_{\rm sat} \rangle$', fontsize=18)
    ax1.legend(loc='lower right', fontsize=11)
    ax1.grid(True, linestyle='--', alpha=0.5)

    if np.any(~np.isnan(mean_nsat_c1[mask1])):
        ax1.set_ylim(1e-4, np.nanmax(mean_nsat_c1[mask1]) * 2.0)

    # --- PANEL 2: Factor de Conformidad K1 ---
    ax2.plot(mass_bins, mean_k1, '-.', color='#1f77b4', label=r'$K_1(M)$')
    if not np.isnan(k1_glob_avg):
        label_k1 = r'$K_{1, {\rm glob}} = %.2f \pm %.2f$' % (k1_glob_avg, err_k1_glob) if not np.isnan(err_k1_glob) else r'$K_{1, {\rm glob}}$'
        ax2.axhline(k1_glob_avg, color='#d62728', linestyle='-.', label=label_k1)
        if not np.isnan(err_k1_glob):
            # Dibujamos una banda de error (1 sigma)
            ax2.fill_between(mass_bins, k1_glob_avg - err_k1_glob, k1_glob_avg + err_k1_glob, color='#d62728', alpha=0.2)
    
    ax2.axhline(1.0, color='black', linestyle=':', alpha=0.7) # Línea de referencia en 1

    ax2.set_ylabel(r'$K_1$', fontsize=18)
    ax2.legend(loc='upper left', fontsize=11)
    ax2.grid(True, linestyle='--', alpha=0.5)

    if not np.isnan(k1_glob_avg):
        k1_validos = mean_k1[~np.isnan(mean_k1) & np.isfinite(mean_k1)]
        if len(k1_validos) > 0:
            techo_k1 = max(1.5, k1_glob_avg * 1.5, np.percentile(k1_validos, 95) * 1.2)
            ax2.set_ylim(0.0, techo_k1)

    # --- PANEL 3: Factor de Conformidad K2 ---
    ax3.plot(mass_bins, mean_k2, '--', color='#2ca02c', label=r'$K_2(M)$')
    if not np.isnan(k2_glob_avg):
        label_k2 = r'$K_{2, {\rm glob}} = %.2f \pm %.2f$' % (k2_glob_avg, err_k2_glob) if not np.isnan(err_k2_glob) else r'$K_{2, {\rm glob}}$'
        ax3.axhline(k2_glob_avg, color='#d62728', linestyle='--', label=label_k2)
        if not np.isnan(err_k2_glob):
            # Dibujamos una banda de error (1 sigma)
            ax3.fill_between(mass_bins, k2_glob_avg - err_k2_glob, k2_glob_avg + err_k2_glob, color='#d62728', alpha=0.2)

    ax3.axhline(1.0, color='black', linestyle=':', alpha=0.7) # Línea de referencia en 1

    ax3.set_ylabel(r'$K_2$', fontsize=18)
    ax3.set_xlabel(r"$\log_{10}(M_{\rm halo} \ / \ M_{\odot} h^{-1})$", fontsize=18)
    ax3.legend(loc='lower left', fontsize=11)
    ax3.grid(True, linestyle='--', alpha=0.5)
    ax3.set_xlim(10.5, 14.5)

    if not np.isnan(k2_glob_avg):
        k2_validos = mean_k2[~np.isnan(mean_k2) & np.isfinite(mean_k2)]
        if len(k2_validos) > 0:
            techo_k2 = max(1.5, k2_glob_avg * 1.5, np.percentile(k2_validos, 95) * 1.2)
            ax3.set_ylim(0.0, techo_k2)

    plt.tight_layout()

    GRAFICA_SALIDA = os.path.join(BASE_DIR, f"Grafica_TFM_Fig6_Conformidad_Corte{CORTE}.png")
    plt.savefig(GRAFICA_SALIDA, dpi=600, bbox_inches='tight')
    plt.close(fig)

    print(f"🎉 ¡Gráfica del Corte {CORTE} guardada con éxito!")
    print(f"   -> Valor K1_glob: {k1_glob_avg:.3f} +/- {err_k1_glob:.3f}")
    print(f"   -> Valor K2_glob: {k2_glob_avg:.3f} +/- {err_k2_glob:.3f}")

print("\n¡PROCESO COMPLETADO! Revisa las nuevas gráficas. 🚀")
