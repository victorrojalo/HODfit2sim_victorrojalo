import numpy as np
import matplotlib.pyplot as plt
import os
import mpl_style

# --- 1. ESTILO ---
plt.style.use(mpl_style.style1)

CORTES = [5, 6, 7, 8]
COLORES = {5: '#1f77b4', 6: '#ff7f0e', 7: '#2ca02c', 8: '#d62728'}
MARCADORES = {5: 'o', 6: 's', 7: '^', 8: 'D'}

BASE_DIR = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/output/Mvir"

print("🚀 Iniciando Súper-Script de Correlación y Kaiser (Modo Detective 🕵️‍♀️)...")

resultados = {}

# --- 2. RECOLECTAR Y PROMEDIAR DATOS ---
for corte in CORTES:
    DIR_DATOS = os.path.join(BASE_DIR, f"Corte{corte}", "Centrales")
    print(f"\nBuscando datos en: {DIR_DATOS}")
    
    xi_real_lista = []
    xi_red_lista = []
    r_bins = None
    archivos_faltantes = 0

    for i in range(64):
        file_real = os.path.join(DIR_DATOS, f"2PCF_Corrfunc_vol{i}_.txt")
        file_red = os.path.join(DIR_DATOS, f"2PCF_Corrfunc_redshift_vol{i}.txt")

        if os.path.exists(file_real) and os.path.exists(file_red):
            try:
                # Intentamos leer normal
                try:
                    data_real = np.loadtxt(file_real)
                except ValueError:
                    # Si falla por culpa de una cabecera de texto, nos la saltamos
                    data_real = np.loadtxt(file_real, skiprows=1)
                
                try:
                    data_red = np.loadtxt(file_red)
                except ValueError:
                    data_red = np.loadtxt(file_red, skiprows=1)

                # Guardamos el eje X (las distancias r)
                if r_bins is None:
                    r_bins = data_real[:, 0]

                # Añadimos la columna 1 (xi) a nuestra olla
                xi_real_lista.append(data_real[:, 1])
                xi_red_lista.append(data_red[:, 1])
                
            except Exception as e:
                # Si sigue fallando, ¡que nos diga por qué!
                if i == 0: # Imprimimos solo el primero para no saturar la pantalla
                    print(f"  [❌] ¡Archivos encontrados pero NO se pueden leer! Error vol {i}: {e}")
        else:
            archivos_faltantes += 1

    if archivos_faltantes > 0:
        print(f"  [⚠️] Faltan {archivos_faltantes} pares de archivos de texto en este corte.")

    if len(xi_real_lista) > 0:
        print(f"  [✅] Corte {corte}: Promediados con éxito {len(xi_real_lista)} volúmenes.")
        xi_real_lista = np.array(xi_real_lista)
        xi_red_lista = np.array(xi_red_lista)
        
        resultados[corte] = {
            'r': r_bins,
            'xi_real_mean': np.mean(xi_real_lista, axis=0),
            'xi_real_err': np.std(xi_real_lista, axis=0) / np.sqrt(len(xi_real_lista)),
            'xi_red_mean': np.mean(xi_red_lista, axis=0),
            'xi_red_err': np.std(xi_red_lista, axis=0) / np.sqrt(len(xi_red_lista))
        }
    else:
        print(f"  [❌] Fracaso total para el Corte {corte}: 0 volúmenes leídos.")

# --- 3. DIBUJAR LA SÚPER GRÁFICA (2 PANELES) ---
if len(resultados) > 0:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    for corte in CORTES:
        if corte not in resultados:
            continue
            
        res = resultados[corte]
        r = res['r']
        
        # Máscara para evitar logaritmos de números negativos o ceros
        mask_real = res['xi_real_mean'] > 0
        mask_red = res['xi_red_mean'] > 0
        mask_kaiser = mask_real & mask_red 

        # PANEL IZQUIERDO: Agrupamiento Espacio Real
        ax1.errorbar(r[mask_real], res['xi_real_mean'][mask_real], yerr=res['xi_real_err'][mask_real],
                     fmt=f'-{MARCADORES[corte]}', color=COLORES[corte], markersize=4, 
                     label=f'Corte {corte}')

        # PANEL DERECHO: Ratio de Kaiser (Redshift / Real)
        ratio = res['xi_red_mean'][mask_kaiser] / res['xi_real_mean'][mask_kaiser]
        err_ratio = ratio * np.sqrt((res['xi_red_err'][mask_kaiser] / res['xi_red_mean'][mask_kaiser])**2 + 
                                    (res['xi_real_err'][mask_kaiser] / res['xi_real_mean'][mask_kaiser])**2)
        
        ax2.errorbar(r[mask_kaiser], ratio, yerr=err_ratio,
                     fmt=f'--{MARCADORES[corte]}', color=COLORES[corte], markersize=4, 
                     label=f'Corte {corte}')

    # --- 4. MAQUILLAJE DEL PANEL IZQUIERDO (REAL) ---
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel(r'$r \ [h^{-1} \mathrm{Mpc}]$', fontsize=14)
    ax1.set_ylabel(r'$\xi(r)$', fontsize=14)
    ax1.set_title('Función de Correlación (Espacio Real)', fontsize=15)
    ax1.grid(True, which="both", linestyle="--", alpha=0.3)
    ax1.legend(loc='lower left', fontsize=11)

    # --- 5. MAQUILLAJE DEL PANEL DERECHO (KAISER) ---
    ax2.set_xscale('log')
    ax2.set_xlabel(r'$s \ [h^{-1} \mathrm{Mpc}]$', fontsize=14)
    ax2.set_ylabel(r'$\xi(s) \ / \ \xi(r)$', fontsize=14)
    ax2.set_title('Efecto Kaiser (Redshift / Real)', fontsize=15)
    ax2.axhline(1.0, color='black', linestyle='-', linewidth=2) 
    ax2.grid(True, which="both", linestyle="--", alpha=0.3)
    ax2.set_ylim(0.5, 1.6)

    plt.tight_layout()

    GRAFICA_SALIDA = os.path.join(BASE_DIR, "Grafica_TFM_SUPER_2PCF_Kaiser_Completa.png")
    plt.savefig(GRAFICA_SALIDA, dpi=300)
    print(f"\n🎉 ¡Súper Gráfica 2PCF guardada en: {GRAFICA_SALIDA}!")
else:
    print("\n[!] No se generó la gráfica porque no se pudo leer ningún corte.")
