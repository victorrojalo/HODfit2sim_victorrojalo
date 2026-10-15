import os
import h5py
import numpy as np

# Parámetros cosmológicos y de simulación
BOXSIZE = 250.000000             # Box size in Mpc/h

# Rutas de archivos de salida
BASE_DIR = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo"
RESULTS_DIR = os.path.join(BASE_DIR, "output/Shark")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ⚠️ OJO AQUÍ: Pon la ruta correcta donde están tus 64 volúmenes de Shark
GALAXY_BASE_DIR = "/home2/vgonzalez/Data/Shark/SU1/iz87" 
galaxy_subvols = list(range(64))

# Parámetros globales para el histograma de luminosidad
N_BINS = 20
L_MIN = 38
L_MAX = 48

# ⚠️ OJO AQUÍ: Pon el nombre exacto de la variable de luminosidad en Shark
# (En Galform era "data/Lbol_AGN", pero Shark suele usar nombres como "galaxies/Lbol" o parecidos)
GALAXY_LOG_HALPHA_KEY = "bolometric_luminosity_agn" 

def main():
    # Preparamos las cajas del histograma
    total_counts = np.zeros(N_BINS)
    bin_edges = np.linspace(L_MIN, L_MAX, N_BINS + 1)
    total_volume = BOXSIZE**3 

    print(f"\n" + "="*50)
    print(f"INICIANDO CÁLCULO DE FUNCIÓN DE LUMINOSIDAD SHARK (TOTAL)")
    print("="*50)

    for ivol in galaxy_subvols:
        # ⚠️ OJO AQUÍ: Asegúrate de que Shark también use carpetas "ivol0", "ivol1"... y "gne_input.hdf5"
        # Si Shark guarda los archivos directamente como "shark_vol0.h5", tendrás que cambiar esta línea:
        GALAXY_FILE = os.path.join(GALAXY_BASE_DIR, f"ivol{ivol}", "gne_input.hdf5")

        if not os.path.exists(GALAXY_FILE):
            print(f"[WARNING] No se encontró el archivo: {GALAXY_FILE}")
            continue

        print(f"Procesando subvolumen de galaxias Shark ivol{ivol}/63...")

        try:
            with h5py.File(GALAXY_FILE, 'r') as f_gal:
                # Extraemos la luminosidad
                gal_lums = f_gal[GALAXY_LOG_HALPHA_KEY][:]

                # Nos quedamos con TODAS las galaxias cuya luminosidad sea > 0
                lums_validas = gal_lums[gal_lums > 0]

                # Aplicamos la misma transformación matemática que en Galform
                log_L_bol = np.log10(lums_validas) + 40.0
                
                # Calculamos el histograma
                counts, _ = np.histogram(log_L_bol, bins=bin_edges)

                # Sumamos a la hucha global
                total_counts += counts
                print(f"  -> Se sumaron {len(lums_validas)} galaxias a la HMF de Shark.")

        except Exception as e:
            print(f"  [ERROR] No se pudo hacer el histograma para el volumen {ivol}: {e}")

    # ==============================================================================
    # GUARDADO DE LA FUNCIÓN DE LUMINOSIDAD GLOBAL DE SHARK
    # ==============================================================================
    print("\n" + "="*50)
    print("GUARDANDO FUNCIÓN DE LUMINOSIDAD (LF) GLOBAL SHARK")
    print("="*50)
    
    bin_width = bin_edges[1] - bin_edges[0]
    phi_total = total_counts / (bin_width * total_volume)

    LF_TOTAL_FILE = os.path.join(BASE_DIR, "LF_Shark_Total.h5")
    
    with h5py.File(LF_TOTAL_FILE, 'w') as f:
        f.create_dataset('bin_edges', data=bin_edges)
        f.create_dataset('phi', data=phi_total)
        f.create_dataset('total_counts', data=total_counts)

    print(f"✅ LF total de Shark guardada exitosamente en: {LF_TOTAL_FILE}")
    print("\n¡PROCESO MULTI-VOLUMEN DE SHARK COMPLETADO!")

if __name__ == "__main__":
     main()
