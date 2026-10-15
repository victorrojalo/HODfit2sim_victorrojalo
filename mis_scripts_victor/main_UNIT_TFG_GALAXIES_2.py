#!/usr/bin/env python3
"""
===============================================================================
     GALAXY-HALO ANALYSIS PIPELINE: HOD CALIBRATION FROM SAM CATALOGUES
     (VERSIÓN COMPLETA: 1 CATÁLOGO DE HALOS GLOBAL, 64 SUBVOLÚMENES SHARK)
===============================================================================
"""

import os
import h5py
import numpy as np

# ===================================================================
# ============== 1. PARAMETER DEFINITION SECTION ====================
# ===================================================================

# Control parameters
TESTING = False              # If True, runs in testing mode (faster, less data)
VERBOSE = True               # If True, prints detailed information during execution
DO_PLOTS = True              # If True, generates plots for the results

# Cosmological parameters (Ajustados según el header de tus h5 de Shark)
OMEGA_M = 0.308900             # Matter density parameter
OMEGA_L = 0.691100             # Dark energy density parameter
h = 0.677400                   # Hubble constant (H0 = 100 * h km/s/Mpc)
Z_SNAP = 1.480159              # Snapshot redshift

# Simulation parameters
BOXSIZE = 250.000000           # Box size in Mpc/h
val = 45.5
llim = 10**(val-40.)           # Minimum flux for ELGs
DO_FLUX_CUT = True             # If True, applies a flux cut to the galaxy sample

# Input and output file paths
BASE_DIR = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo"
RESULTS_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(RESULTS_DIR, exist_ok=True)

# --- CONFIGURACIÓN RUTAS ---
DATA_DIR_HALOS = "/data8/adrian/MN5/SEP_UNI/N2048_L250_fid/ROCKSTAR/outputs"
# REVISA ESTE NOMBRE: He quitado la 'p' de 'outp_87' porque suele ser 'out_87'
HALO_FILE = os.path.join(DATA_DIR_HALOS, "out_87.list")

GALAXY_BASE_DIR = "/home2/vgonzalez/Data/Shark/SU1/iz87" 
galaxy_subvols = list(range(64)) # Bucle de ivol0 a ivol63

# Formatos
INPUT_GALAXY_FORMAT = "h5"
INPUT_HALO_FORMAT = "txt"

# Galaxy file keys (Shark structure)
if INPUT_GALAXY_FORMAT == "h5":
    GALAXY_MAIN_ID_KEY = "data/type"
    GALAXY_HOST_ID_KEY = "data/index"
    GALAXY_MAIN_MASS_KEY = "data/mhhalo"
    GALAXY_XPOS_KEY = "data/xgal"
    GALAXY_YPOS_KEY = "data/ygal"
    GALAXY_ZPOS_KEY = "data/zgal"
    GALAXY_XVEL_KEY = "data/vxgal"
    GALAXY_YVEL_KEY = "data/vygal"
    GALAXY_ZVEL_KEY = "data/vzgal"
    GALAXY_LOG_HALPHA_KEY = "data/Lbol_AGN"
    DATA_GALAXY = True

# Halo file keys (Rockstar outp_87.list)
if INPUT_HALO_FORMAT == "txt":
    HALO_ID_KEY = 0
    HALO_MASS_KEY = 2
    HALO_RVIR_KEY = 5
    HALO_XPOS_KEY = 8
    HALO_YPOS_KEY = 9
    HALO_ZPOS_KEY = 10
    HALO_XVEL_KEY = 11
    HALO_YVEL_KEY = 12
    HALO_ZVEL_KEY = 13
    HALO_PID_KEY = 40   # Tu nueva columna de PID
    HALO_MVIR_KEY = 2

# Configuración de análisis
DO_CONFORMITY = True
M_MIN_CONFORMITY = 10.5
M_MAX_CONFORMITY = 14.5
N_BINS_CONFORMITY = 70

DO_RADIAL_PROFILE = True
BINNING_RADIAL = np.linspace(0, 1.5, 151)

# Parámetros HMF
N_BINS = 70
M_MIN = 10.5
M_MAX = 14.5
CENTRALFORMATS = "sage"

# ===================================================================
# ======================== MAIN FUNCTION ============================
# ===================================================================

def main():
    global GALAXY_MAIN_ID_KEY, GALAXY_HOST_ID_KEY, GALAXY_MAIN_MASS_KEY, \
           GALAXY_XPOS_KEY, GALAXY_YPOS_KEY, GALAXY_ZPOS_KEY, \
           GALAXY_XVEL_KEY, GALAXY_YVEL_KEY, GALAXY_ZVEL_KEY, \
           GALAXY_LOG_HALPHA_KEY

    # Limpieza de nombres de keys (quitar el 'data/')
    if DATA_GALAXY:
        keys_to_clean = [
            'GALAXY_MAIN_ID_KEY', 'GALAXY_HOST_ID_KEY', 'GALAXY_MAIN_MASS_KEY',
            'GALAXY_XPOS_KEY', 'GALAXY_YPOS_KEY', 'GALAXY_ZPOS_KEY',
            'GALAXY_XVEL_KEY', 'GALAXY_YVEL_KEY', 'GALAXY_ZVEL_KEY',
            'GALAXY_LOG_HALPHA_KEY'
        ]
        for key in keys_to_clean:
            globals()[key] = globals()[key].split("/")[-1]

    # ---------------------------------------------------------------
    # 1. CARGA DE HALOS Y HMF GLOBAL
    # ---------------------------------------------------------------
    print("\n" + "="*50)
    print("CARGANDO CATÁLOGO DE HALOS Y CALCULANDO HMF GLOBAL")
    print(f"Archivo: {HALO_FILE}")
    print("="*50)

    from src.h2s_conformity2 import load_halos
    try:
        pid, mass = load_halos(HALO_FILE, INPUT_HALO_FORMAT, HALO_PID_KEY, HALO_MASS_KEY, testing=TESTING)
    except FileNotFoundError:
        print(f"\n[ERROR FATAL]: No se encuentra el archivo {HALO_FILE}")
        print("Por favor, verifica el nombre con 'ls' y edita la línea 48 del script.")
        return

    mask_host = (pid == -1.0)
    host_masses = mass[mask_host]

    log_m = np.log10(host_masses[host_masses > 0])
    counts, bin_edges = np.histogram(log_m, bins=N_BINS, range=(M_MIN, M_MAX))
    bin_width = bin_edges[1] - bin_edges[0]
    phi = counts / (bin_width * (BOXSIZE**3))

    # Guardar HMF Global
    HMF_FILE = os.path.join(BASE_DIR, "HMF_TOTAL_Rockstar_outp87.h5")
    with h5py.File(HMF_FILE, 'w') as f:
        f.create_dataset('bin_edges', data=bin_edges)
        f.create_dataset('phi', data=phi)
        f.create_dataset('total_counts', data=counts)
    print(f"✅ HMF Global guardada en: {HMF_FILE}")

    # ---------------------------------------------------------------
    # 2. BUCLE SOBRE VOLÚMENES DE GALAXIAS
    # ---------------------------------------------------------------
    for ivol in galaxy_subvols:
        GALAXY_FILE = os.path.join(GALAXY_BASE_DIR, f"ivol{ivol}", "gne_input.hdf5")

        if not os.path.exists(GALAXY_FILE):
            print(f"\n[SKIP] No existe: {GALAXY_FILE}")
            continue

        print(f"\n>>> PROCESANDO IVOL {ivol} / 63")

        # Filtro de flujo
        FILTERED_GAL = GALAXY_FILE
        if DO_FLUX_CUT:
            from src.h2s_io_PRUEBA_NOPID import filter_log_flux
            FILTERED_GAL = os.path.join(BASE_DIR, f"filtered_ELGs_vol{ivol}.h5")
            filter_log_flux(infile=GALAXY_FILE, fmin=llim, outfile_name=FILTERED_GAL,
                            output_format="h5", param_name=GALAXY_LOG_HALPHA_KEY, 
                            verbose=False, testing=TESTING)

        # Conformidad (HOD)
        if DO_CONFORMITY:
            from src.h2s_conformity2 import compute_conformity_parameters
            OUT_CONF = os.path.join(RESULTS_DIR, f"conformity_vol{ivol}.h5")
            compute_conformity_parameters(galaxy_file=FILTERED_GAL, halo_file=HALO_FILE,
                                          M_min=M_MIN_CONFORMITY, M_max=M_MAX_CONFORMITY,
                                          N_bins=N_BINS_CONFORMITY, galaxy_format="h5",
                                          halo_format="txt", output_file=OUT_CONF,
                                          halo_pid=HALO_PID_KEY, halo_mass=HALO_MASS_KEY,
                                          verbose=False, centralformats=CENTRALFORMATS,
                                          gal_host_id=GALAXY_HOST_ID_KEY, 
                                          gal_main_id=GALAXY_MAIN_ID_KEY,
                                          gal_main_mass=GALAXY_MAIN_MASS_KEY, testing=TESTING)

        # Perfil Radial
        if DO_RADIAL_PROFILE:
            from src.h2s_profile_r import compute_radial_profile
            OUT_RAD = os.path.join(RESULTS_DIR, f"radial_profile_vol{ivol}.h5")
            compute_radial_profile(galaxy_file=FILTERED_GAL, halo_file=HALO_FILE,
                                   output_file=OUT_RAD, verbose=False, boxsize=BOXSIZE,
                                   bins=BINNING_RADIAL, halo_format="txt",
                                   halo_id_key=HALO_ID_KEY, halo_pid_key=HALO_PID_KEY,
                                   halo_x_key=HALO_XPOS_KEY, halo_y_key=HALO_YPOS_KEY,
                                   halo_z_key=HALO_ZPOS_KEY, centralformats=CENTRALFORMATS,
                                   galaxy_host_key=GALAXY_HOST_ID_KEY, 
                                   galaxy_id_key=GALAXY_MAIN_ID_KEY,
                                   galaxy_x_key=GALAXY_XPOS_KEY, galaxy_y_key=GALAXY_YPOS_KEY,
                                   galaxy_z_key=GALAXY_ZPOS_KEY, testing=TESTING)

    print("\n" + "="*50)
    print("¡FINALIZADO! Todos los volúmenes procesados.")
    print("="*50)

if __name__ == "__main__":
    main()

