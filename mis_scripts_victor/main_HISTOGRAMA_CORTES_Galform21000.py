import os
import h5py
import numpy as np

# Parámetros cosmológicos y de simulación
BOXSIZE = 1000.000000             # Box size in Mpc/h

# Rutas de archivos
BASE_DIR = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo"
RESULTS_DIR = os.path.join(BASE_DIR, "output/Galform")
os.makedirs(RESULTS_DIR, exist_ok=True)

GALAXY_BASE_DIR = "/home2/vgonzalez/Data/Galform/UNIT1GPC_fnl0/iz87"
galaxy_subvols = list(range(64)) # Iteramos sobre 64 volúmenes (0 al 63)

# Parámetros globales para el histograma de luminosidad
N_BINS = 100
L_MIN = 38
L_MAX = 48

# Galaxy file keys
GALAXY_LOG_HALPHA_KEY = "data/Lbol_AGN"

def main():
    global GALAXY_LOG_HALPHA_KEY
    GALAXY_LOG_HALPHA_KEY = GALAXY_LOG_HALPHA_KEY.split("/")[-1]

    # Preparamos las cajas del histograma
    total_counts = np.zeros(N_BINS)
    bin_edges = np.linspace(L_MIN, L_MAX, N_BINS + 1)
    total_volume = BOXSIZE**3 # Volumen de una única caja grande de simulacion

    print(f"\n" + "="*50)
    print(f"INICIANDO CÁLCULO DE FUNCIÓN DE LUMINOSIDAD (TOTAL)")
    print("="*50)

    # ==============================================================================
    # ========================== EL GRAN BUCLE DE 64 GALAXIAS ======================
    # ==============================================================================

    for ivol in galaxy_subvols:
        GALAXY_FILE = os.path.join(GALAXY_BASE_DIR, f"ivol{ivol}", "gne_input.hdf5")

        if not os.path.exists(GALAXY_FILE):
            print(f"[WARNING] No se encontró el archivo: {GALAXY_FILE}")
            continue

        print(f"Procesando subvolumen de galaxias ivol{ivol}/63...")

        try:
            with h5py.File(GALAXY_FILE, 'r') as f_gal:
                # Sacamos SOLO las luminosidades (ya no filtramos por tipo)
                gal_lums = f_gal['data'][GALAXY_LOG_HALPHA_KEY][:]

                # Nos quedamos con TODAS las galaxias cuya luminosidad sea > 0
                lums_validas = gal_lums[gal_lums > 0]
                lums_validas2 = lums_validas/((0.6774)**2)
                
                # Aplicamos la transformación matemática
                log_L_bol = np.log10(lums_validas2) + 40.0
                
                # Calculamos el histograma de ESTE volumen
                counts, _ = np.histogram(log_L_bol, bins=bin_edges)

                # Sumamos las galaxias de este volumen a la hucha global
                total_counts += counts
                print(f"  -> Se sumaron {len(lums_validas)} galaxias (centrales y satélites).")

        except Exception as e:
            print(f"  [ERROR] No se pudo hacer el histograma para el volumen {ivol}: {e}")

    # ==============================================================================
    # 3. GUARDADO DE LA FUNCIÓN DE LUMINOSIDAD (LF) GLOBAL
    # ==============================================================================
    print("\n" + "="*50)
    print("GUARDANDO FUNCIÓN DE LUMINOSIDAD (LF) GLOBAL")
    print("="*50)
    
    bin_width = bin_edges[1] - bin_edges[0]
    phi_total = total_counts / (bin_width * total_volume)

    # Guardamos con un nombre distinto para diferenciarlo de las centrales
    LF_TOTAL_FILE = os.path.join(BASE_DIR, "LF_Galform_TotalBIEN1000.h5")
    
    with h5py.File(LF_TOTAL_FILE, 'w') as f:
        f.create_dataset('bin_edges', data=bin_edges)
        f.create_dataset('phi', data=phi_total)
        f.create_dataset('total_counts', data=total_counts)

    print(f"✅ LF total guardada exitosamente en: {LF_TOTAL_FILE}")
    print("\n¡PROCESO MULTI-VOLUMEN DE GALAXIAS COMPLETADO!")

if __name__ == "__main__":
     main()
