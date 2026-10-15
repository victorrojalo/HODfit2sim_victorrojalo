import os
import h5py
import numpy as np


TESTING = False
# Cosmological parameters
OMEGA_M = 0.308900             # Matter density parameter
OMEGA_L = 0.691100             # Dark energy density parameter
h = 0.677400                   # Hubble constant (H0 = 100 * h km/\ s/Mpc)
Z_SNAP = 1.480159              # Snapshot redshift (Shark)

# Simulation parameters
BOXSIZE = 250.000000             # Box size in Mpc/h
val = 45.5
llim = 10**(val-40.)       # Minimum  for ELGs []
DO_FLUX_CUT = False  #         # If True, applies a flux cut to the galaxy sample
# Input and output file paths
BASE_DIR = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo"
RESULTS_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(RESULTS_DIR, exist_ok=True)

# --- CONFIGURACIÓN MULTI-VOLUMEN DE GALAXIAS Y 1 HALO FILE ---
DATA_DIR_HALOS = "/home2/vgonzalez/Data/Rockstar/SU1"
# NOTA: Asegúrate de que el archivo se llame out_87.list o outp_87\.list según el ls
HALO_FILE = os.path.join(DATA_DIR_HALOS, "outp_87.list")
GALAXY_BASE_DIR = "/home2/vgonzalez/Data/Shark/SU1/iz87"
galaxy_subvols = list(range(64)) # Iteramos sobre 64 volúmenes (0 al 63)

# Parámetros globales para el histograma de masa
N_BINS = 70
M_MIN = 10.5
M_MAX = 14.5
# Input file formats
INPUT_GALAXY_FORMAT = "h5"
INPUT_HALO_FORMAT = "txt"

# Galaxy file keys
if INPUT_GALAXY_FORMAT == "h5":
    GALAXY_MAIN_ID_KEY = "data/type"
    GALAXY_HOST_ID_KEY = "data/id_halo"
    GALAXY_MAIN_MASS_KEY = "data/mvir_hosthalo"
    GALAXY_XPOS_KEY = "data/position_x"
    GALAXY_YPOS_KEY = "data/position_y"
    GALAXY_ZPOS_KEY = "data/position_z"
    GALAXY_XVEL_KEY = "data/velocity_x"
    GALAXY_YVEL_KEY = "data/velocity_y"
    GALAXY_ZVEL_KEY = "data/velocity_z"
    GALAXY_LOG_HALPHA_KEY = "data/bolometric_luminosity_agn"
    DATA_GALAXY = True

# CENTRALFORMATS
CENTRALFORMATS = "galform"
ROCKSTAR_FORMAT = True

if INPUT_HALO_FORMAT == "txt":
    HALO_XPOS_KEY = 8
    HALO_YPOS_KEY = 9
    HALO_ZPOS_KEY = 10
    HALO_MASS_KEY = 21
    HALO_XVEL_KEY = 11
    HALO_YVEL_KEY = 12
    HALO_ZVEL_KEY = 13
    HALO_ID_KEY = 0
    HALO_PID_KEY = 40   # PID Actualizado
    HALO_MVIR_KEY = 2
    HALO_RVIR_KEY = 5



def main():
    global GALAXY_MAIN_ID_KEY, GALAXY_HOST_ID_KEY, GALAXY_MAIN_MASS_KEY, GALAXY_XPOS_KEY, GALAXY_YPOS_KEY, GALAXY_ZPOS_KEY, GALAXY_XVEL_KEY, GALAXY_YVEL_KEY, GALAXY_ZVEL_KEY, GALAXY_LOG_HALPHA_KEY
    if DATA_GALAXY:
        GALAXY_MAIN_ID_KEY = GALAXY_MAIN_ID_KEY.split("/")[-1]
        GALAXY_HOST_ID_KEY = GALAXY_HOST_ID_KEY.split("/")[-1]
        GALAXY_MAIN_MASS_KEY = GALAXY_MAIN_MASS_KEY.split("/")[-1]
        GALAXY_XPOS_KEY = GALAXY_XPOS_KEY.split("/")[-1]
        GALAXY_YPOS_KEY = GALAXY_YPOS_KEY.split("/")[-1]
        GALAXY_ZPOS_KEY = GALAXY_ZPOS_KEY.split("/")[-1]
        GALAXY_XVEL_KEY = GALAXY_XVEL_KEY.split("/")[-1]
        GALAXY_YVEL_KEY = GALAXY_YVEL_KEY.split("/")[-1]
        GALAXY_ZVEL_KEY = GALAXY_ZVEL_KEY.split("/")[-1]
        GALAXY_LOG_HALPHA_KEY = GALAXY_LOG_HALPHA_KEY.split("/")[-1]


    # ==============================================================================
    # 1. CARGA DE HALOS MAESTROS Y CÁLCULO DE HMF (FUERA DEL BUCLE)
    # ==============================================================================
    print(f"\n" + "="*50)
    print(f"Cargando Catálogo Maestro de Halos: {HALO_FILE}...")
    print("="*50)

    # CARGA Y FILTRADO DE MASA
    from src.h2s_conformity2 import load_halos
    from src.h2s_io_PRUEBA_NOPID import get_mask
    pid, mass = load_halos(HALO_FILE, INPUT_HALO_FORMAT, HALO_PID_KEY, HALO_MASS_KEY, testing=TESTING)
    mask_host = get_mask(pid, rockstar_format=ROCKSTAR_FORMAT)             #(pid == -1.0)
    host_masses = mass[mask_host]
    total_counts = np.zeros(N_BINS)
    bin_edges = np.linspace(M_MIN, M_MAX, N_BINS + 1)
    total_volume = BOXSIZE**3 # Volumen de una única caja grande de simulacion



    # ==============================================================================
    # ========================== EL GRAN BUCLE DE 64 GALAXIAS ======================
    # ==============================================================================
 
    for ivol in galaxy_subvols:
        GALAXY_FILE = os.path.join(GALAXY_BASE_DIR, f"ivol{ivol}", "gne_input.hdf5")

        if not os.path.exists(GALAXY_FILE):
            print(f"[WARNING] No se encontró el archivo: {GALAXY_FILE}")
            continue

        print(f"\n" + "="*50)
        print(f"Procesando subvolumen de galaxias ivol{ivol}/63...")
        print("="*50)

        FILTERED_GALAXIES = GALAXY_FILE
        # ====================================================================
        # NUEVO: EXTRAER MASAS DE HALOS DE LAS GALAXIAS Y SUMAR A LA HUCHA
        # ====================================================================
        try:
            with h5py.File(FILTERED_GALAXIES, 'r') as f_gal:
                # Sacamos los tipos y las masas de los halos de estas galaxias
                gal_main_id = f_gal['data'][GALAXY_MAIN_ID_KEY][:]
                gal_host_id = f_gal['data'][GALAXY_HOST_ID_KEY][:]
                gal_masses = f_gal['data'][GALAXY_MAIN_MASS_KEY][:]
   
                # COMO ESTE ES EL SCRIPT DE SATELITES, NOS QUEDAMOS CON galaxias satelites
                if CENTRALFORMATS == 'sage':
                    masas_interes = gal_masses[gal_main_id != gal_host_id] #con != le digo que iguale lo que sea contrario
                elif CENTRALFORMATS == 'galform':
                    masas_interes = gal_masses[gal_main_id != 0]
                
                #masas_interes = gal_masses[gal_types == 0]
                
                # Hacemos logaritmo y calculamos el histograma de ESTE volumen
                log_m_gal = np.log10(masas_interes[masas_interes > 0])
                counts, _ = np.histogram(log_m_gal, bins=bin_edges)
 
                # Sumamos las galaxias de este volumen a la hucha global
                total_counts += counts
                print(f"  -> Se sumaron {len(log_m_gal)} galaxias centrales al histograma global.")

        except Exception as e:
            print(f"  [ERROR] No se pudo hacer el histograma para el volumen {ivol}: {e}")

    # <============================================================================
    # <========================= FIN DEL BUCLE DE 64 CAJAS =========================
    # <=============================================================================
 
    # ==============================================================================
    # 3. GUARDADO DE LA FUNCIÓN DE MASA (HMF) GLOBAL
    # ==============================================================================
    if bin_edges is not None:
        print("\n" + "="*50)
        print("GUARDANDO NORMALIZACIÓN GLOBAL DE LA HMF")
        print("="*50)
        bin_width = bin_edges[1] - bin_edges[0]
        phi_total = total_counts / (bin_width * total_volume)
    
        HMF_TOTAL_FILE = os.path.join(BASE_DIR, "HMF_Shark_Satelites.h5")
        with h5py.File(HMF_TOTAL_FILE, 'w') as f:
            f.create_dataset('bin_edges', data=bin_edges)
            f.create_dataset('phi', data=phi_total)
            f.create_dataset('total_counts', data=total_counts)
 
            print(f"✅ HMF total guardada exitosamente en: {HMF_TOTAL_FILE}")
            print("\n¡PROCESO MULTI-VOLUMEN DE GALAXIAS COMPLETADO!")
    else:
        print("\n[ERROR] No se procesó ningún archivo, no hay datos para la HMF.")
 
if __name__ == "__main__":
     main()
























