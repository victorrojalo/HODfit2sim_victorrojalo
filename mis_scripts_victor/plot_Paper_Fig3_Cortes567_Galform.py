import numpy as np
import matplotlib.pyplot as plt
import os
import mpl_style

# --- 1. ESTILO PAPER ---
plt.style.use(mpl_style.style1)

CORTES_A_PROCESAR = [5, 6, 7, 8]

for CORTE in CORTES_A_PROCESAR:
    print(f"\n" + "="*50)
    print(f"🚀 Generando Figura 3 (Original vs Shuffled) para el Corte {CORTE}...")
    print("="*50)

    BASE_DIR = f"/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/output/Mvir/Corte{CORTE}/Centrales"

    # ¡IMPORTANTE! Vaciamos las listas en cada vuelta del bucle
    xi_orig_lista = []
    xi_shuff_lista = []
    r_bins = None
    vols_leidos = 0

    # --- 2. RECOLECTAR DATOS ---
    for i in range(64):
        file_orig = os.path.join(BASE_DIR, f"2PCF_Corrfunc_vol{i}_.txt")
        file_shuff = os.path.join(BASE_DIR, f"2PCF_Corrfunc_shuffled_vol{i}.txt")

        if os.path.exists(file_orig) and os.path.exists(file_shuff):
            try:
                # Leer Original
                try:
                    d_orig = np.loadtxt(file_orig, delimiter=',')
                except ValueError:
                    d_orig = np.loadtxt(file_orig, delimiter=',', skiprows=1)

                # Leer Shuffled
                try:
                    d_shuff = np.loadtxt(file_shuff, delimiter=',')
                except ValueError:
                    d_shuff = np.loadtxt(file_shuff, delimiter=',', skiprows=1)

                if r_bins is None:
                    r_bins = d_orig[:, 0]

                xi_orig_lista.append(d_orig[:, 1])
                xi_shuff_lista.append(d_shuff[:, 1])
                vols_leidos += 1

            except Exception as e:
                if i == 0: print(f"  [❌] Error leyendo vol {i}: {e}")

    if vols_leidos == 0:
        print(f"❌ Fracaso total: No se encontraron los archivos para el Corte {CORTE}. Saltando...")
        continue  # Salta al siguiente corte en lugar de romper el programa

    print(f"✅ Promediados {vols_leidos} volúmenes.")

    # --- 3. CÁLCULO DE MEDIAS Y ERRORES ---
    xi_orig_arr = np.array(xi_orig_lista)
    xi_shuff_arr = np.array(xi_shuff_lista)

    mean_orig = np.mean(xi_orig_arr, axis=0)
    err_orig = np.std(xi_orig_arr, axis=0) / np.sqrt(vols_leidos)

    mean_shuff = np.mean(xi_shuff_arr, axis=0)
    err_shuff = np.std(xi_shuff_arr, axis=0) / np.sqrt(vols_leidos)

    # --- 4. DIBUJAR LA GRÁFICA (2 PANELES VERTICALES) ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10), sharex=True, gridspec_kw={'height_ratios': [2, 1]})
    fig.subplots_adjust(hspace=0.05)

    mask = (mean_orig > 0) & (mean_shuff > 0)

    # ==========================================
    # PANEL SUPERIOR: La 2PCF
    # ==========================================
    ax1.errorbar(r_bins[mask], mean_orig[mask], yerr=err_orig[mask],
                 fmt='-o', color='#1f77b4', markersize=5, label='Shark (Original)')

    ax1.errorbar(r_bins[mask], mean_shuff[mask], yerr=err_shuff[mask],
                 fmt='--s', color='#d62728', markersize=5, label=r'Shark$_{\rm sh}$ (Shuffled)')

    ax1.set_yscale('log')
    ax1.set_xscale('log')
    ax1.set_ylabel(r'$\xi(r)$', fontsize=15)
    ax1.legend(loc='upper right', fontsize=12)
    ax1.grid(True, which="both", linestyle="--", alpha=0.3)

    # ==========================================
    # PANEL INFERIOR: El Ratio (Impacto del Assembly Bias)
    # ==========================================
    ratio = mean_orig[mask] / mean_shuff[mask]
    err_ratio = ratio * np.sqrt((err_orig[mask]/mean_orig[mask])**2 + (err_shuff[mask]/mean_shuff[mask])**2)

    ax2.errorbar(r_bins[mask], ratio, yerr=err_ratio, fmt='-o', color='black', markersize=5)
    ax2.axhline(1.0, color='gray', linestyle='--', linewidth=2)

    ax2.set_xlabel(r'$r \ [h^{-1} \mathrm{Mpc}]$', fontsize=15)
    ax2.set_ylabel(r'$\xi_{\rm Orig} \ / \ \xi_{\rm Shuff}$', fontsize=15)
    ax2.grid(True, which="both", linestyle="--", alpha=0.3)
    ax2.set_ylim(0.5, 1.5)  

    plt.tight_layout()
    SALIDA = os.path.join(BASE_DIR, f"Grafica_TFM_Paper_Fig3_Original_vs_Shuffled_Corte{CORTE}.png")
    plt.savefig(SALIDA, dpi=300, bbox_inches='tight')
    
    # ¡VITAL! Cerramos la figura para que no se superpongan en la siguiente vuelta
    plt.close(fig) 
    
    print(f"🎉 ¡Figura 3 del Corte {CORTE} guardada con éxito!")

print("\n¡PROCESO COMPLETADO PARA TODOS LOS CORTES! 🚀")
