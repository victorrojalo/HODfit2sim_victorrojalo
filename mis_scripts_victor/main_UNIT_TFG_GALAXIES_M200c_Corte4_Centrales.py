#!/usr/bin/env python3
"""
===============================================================================
     GALAXY-HALO ANALYSIS PIPELINE: HOD CALIBRATION FROM SAM CATALOGUES
     (1 HALO GLOBAL, 64 VOLUMENES DE GALAXIAS SHARK)
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

# Cosmological parameters
OMEGA_M = 0.308900             # Matter density parameter
OMEGA_L = 0.691100             # Dark energy density parameter
h = 0.677400                   # Hubble constant (H0 = 100 * h km/s/Mpc)
Z_SNAP = 1.480159              # Snapshot redshift (Shark)

# Simulation parameters
BOXSIZE = 250.000000             # Box size in Mpc/h
val = 42.9
llim = 10**(val-40.)       # Minimum  for ELGs []
DO_FLUX_CUT = True  #         # If True, applies a flux cut to the galaxy sample

# Input and output file paths
BASE_DIR = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo"
RESULTS_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(RESULTS_DIR, exist_ok=True)

# --- CONFIGURACIÓN MULTI-VOLUMEN DE GALAXIAS Y 1 HALO FILE ---
DATA_DIR_HALOS = "/home2/vgonzalez/Data/Rockstar/SU1"
# NOTA: Asegúrate de que el archivo se llame out_87.list o outp_87.list según el ls
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

if INPUT_GALAXY_FORMAT == "txt":
    GALAXY_MAIN_ID_KEY = 1
    GALAXY_HOST_ID_KEY = 2
    GALAXY_MAIN_MASS_KEY = 3
    GALAXY_XPOS_KEY = 4
    GALAXY_YPOS_KEY = 5
    GALAXY_ZPOS_KEY = 6
    GALAXY_XVEL_KEY = 7
    GALAXY_YVEL_KEY = 8
    GALAXY_ZVEL_KEY = 9
    GALAXY_LOG_HALPHA_KEY = 10

# CENTRALFORMATS
CENTRALFORMATS = "galform"

# Halo file keys
if INPUT_HALO_FORMAT == "h5":
    HALO_XPOS_KEY = "Xpox"
    HALO_YPOS_KEY = "Ypos"
    HALO_ZPOS_KEY = "Zpos"
    HALO_MASS_KEY = "Mass"
    HALO_XVEL_KEY = "Xvel"
    HALO_YVEL_KEY = "Yvel"
    HALO_ZVEL_KEY = "Zvel"
    HALO_ID_KEY = "ID"
    HALO_PID_KEY = "PID"

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

# ===================================================================
# ========= 2. Two Point Correlation Function. Real Space ===========
# ===================================================================
DO_CORRELATION_FUNC_REAL_SPACE = False #
NBINS_2PCF_REAL = 80
RMAX_2PCF_REAL = 100.0
RMIN_2PCF_REAL = 1.4e-3
NTHREADS_2PCF_REAL = 4
DO_2PCF_REAL_RATIO = False #
XLIM_2PCF_RATIO = (0.01, 100.0)
YLIM_2PCF_RATIO = (0.5, 1.4)

# ====================================================================
# ======== 3. Two Point Correlation Function. Redshift Space =========
# ====================================================================
DO_CORRELATION_FUNC_REDSHIFT_SPACE = False #
NBINS_2PCF_REDSHIFT = 80
RMAX_2PCF_REDSHIFT = 100.0
RMIN_2PCF_REDSHIFT = 1.4e-3
NTHREADS_2PCF_REDSHIFT = 4
LOS_AXIS = 'z'

# ====================================================================
# ================= 4. Conformity Parameters =========================
# ====================================================================
DO_CONFORMITY = False #
M_MIN_CONFORMITY = 10.5
M_MAX_CONFORMITY = 14.5
N_BINS_CONFORMITY = 70
BIN_WIDTH_CONFORMITY = 0.057
DO_HMF_COMPARISON = True
BINNING_HMF= np.linspace(10.5, 14.5, 71)

# ====================================================================
# ===================== 5. Radial Profile ============================
# ====================================================================
DO_RADIAL_PROFILE = False #
BINNING_RADIAL = np.linspace(0, 1.5, 151)
DO_FIT_RADIAL_PROFILE = False #
INITAL_GUESS_RADIAL = None

# ====================================================================
# ================= 8. Radial Velocity Profile =======================
# ====================================================================
DO_VR_PROFILE = False #
BINNING_VR = np.linspace(-1000, 1000, 201)
DO_FIT_VR_PROFILE = False #
MANUAL_PARAMS_VR = None

# ====================================================================
# ================= 9. Tangential Velocity Profile ===================
# ===================================================================
DO_VTAN_PROFILE = False #
BINNING_VTAN = np.linspace(0, 1000, 201)
DO_FIT_VTAN_PROFILE = False #
MANUAL_PARAMS_VTAN = None

# ====================================================================
# ================= 10. Kaiser Analysis ==============================
# ====================================================================
DO_KAISER_ANALYSIS = False #
BIAS = 1.86
GAMMA = 0.55
DO_KAISER_RATIO = False #
XLIM_KAISER = (0.1,100)
YLIM_KAISER = (0.75,1.5)

# ====================================================================
# ===================== 11. Shuffling ================================
# ====================================================================
DO_SHUFFLING = False #
N_BINS_SHUFFLING = 70
M_MIN_SHUFFLING = 10.5
M_MAX_SHUFFLING = 14.5


def main():
    global GALAXY_MAIN_ID_KEY, GALAXY_HOST_ID_KEY, GALAXY_MAIN_MASS_KEY, \
           GALAXY_XPOS_KEY, GALAXY_YPOS_KEY, GALAXY_ZPOS_KEY, \
           GALAXY_XVEL_KEY, GALAXY_YVEL_KEY, GALAXY_ZVEL_KEY, \
           GALAXY_LOG_HALPHA_KEY

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

    # 1. ESCUDO ANTI-NOHUP (Limpia el archivo automáticamente si está corrupto)
    #os.system(f"sed -i '/nohup: ignoring input/d' {HALO_FILE}")

    # CARGA Y FILTRADO DE MASA
    from src.h2s_conformity2 import load_halos
    pid, mass = load_halos(HALO_FILE, INPUT_HALO_FORMAT, HALO_PID_KEY, HALO_MASS_KEY, testing=TESTING)
    mask_host = (pid == -1.0)
    host_masses = mass[mask_host]

    # HISTOGRAMA GLOBAL Y SUMA A LA HUCHA
   # log_m = np.log10(host_masses[host_masses > 0])
   # total_counts, bin_edges = np.histogram(log_m, bins=N_BINS, range=(M_MIN, M_MAX))
   # total_volume = BOXSIZE**3 # Volumen de una única caja grande de simulacion
   # INICIALIZAR LA HUCHA (VACÍA) PARA LAS GALAXIAS
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

        # ================== Apply flux cut =================
        if DO_FLUX_CUT:
            print(f"Applying flux cut to Galaxy Catalog ivol{ivol}...")
            from src.h2s_io_PRUEBA_NOPID import filter_log_flux
            FILTERED_GALAXIES = os.path.join(BASE_DIR, f"filtered_ELGs_{llim}_vol{ivol}.{INPUT_GALAXY_FORMAT}")
            filter_log_flux(infile=GALAXY_FILE, fmin=llim, outfile_name=FILTERED_GALAXIES,
                            output_format=INPUT_GALAXY_FORMAT, param_name=GALAXY_LOG_HALPHA_KEY, verbose=VERBOSE, testing=TESTING)
        else:
            FILTERED_GALAXIES = GALAXY_FILE
        # ====================================================================
        # NUEVO: EXTRAER MASAS DE HALOS DE LAS GALAXIAS Y SUMAR A LA HUCHA
        # ====================================================================
        try:
            with h5py.File(FILTERED_GALAXIES, 'r') as f_gal:
                # Sacamos los tipos y las masas de los halos de estas galaxias
                gal_types = f_gal[GALAXY_MAIN_ID_KEY][:]
                gal_masses = f_gal[GALAXY_MAIN_MASS_KEY][:]

            # COMO ESTE ES EL SCRIPT DE CENTRALES, NOS QUEDAMOS CON type == 0
            masas_interes = gal_masses[gal_types == 0]

            # Hacemos logaritmo y calculamos el histograma de ESTE volumen
            log_m_gal = np.log10(masas_interes[masas_interes > 0])
            counts, _ = np.histogram(log_m_gal, bins=bin_edges)

            # Sumamos las galaxias de este volumen a la hucha global
            total_counts += counts
            print(f"  -> Se sumaron {len(log_m_gal)} galaxias centrales al histograma global.")

        except Exception as e:
            print(f"  [ERROR] No se pudo hacer el histograma para el volumen {ivol}: {e}")
        # ====================================================================

        # ================= Galaxy Shuffling ================
        if DO_SHUFFLING:
            print(f"Splitting Halo Catalogue by mass (Vol {ivol})...")
            from src.h2s_io_PRUEBA_NOPID import split_halo_catalog_by_mass
            HALO_MASS_BINS = os.path.join(BASE_DIR, f"halo_mass_bins_vol{ivol}.h5")

            split_halo_catalog_by_mass(halo_file=HALO_FILE, mass_column=HALO_MASS_KEY, logmass=False,
                                       output_h5=HALO_MASS_BINS, min_logmass=M_MIN_SHUFFLING,
                                       max_logmass=M_MAX_SHUFFLING, n_bins=N_BINS_SHUFFLING,
                                       columns={"id": HALO_ID_KEY, "X": HALO_XPOS_KEY, "Y": HALO_YPOS_KEY,
                                                "Z": HALO_ZPOS_KEY,"vx": HALO_XVEL_KEY, "vy": HALO_YVEL_KEY,
                                                "vz": HALO_ZVEL_KEY, "pid": HALO_PID_KEY,"Mass": HALO_MASS_KEY},
                                       verbose=VERBOSE, testing=TESTING)

            print("Shuffling halo catalogue...")
            from src.h2s_shuffle2 import shuffle_parent_halos
            SHUFFLED_HALO_FILE = os.path.join(BASE_DIR, f"halo_mass_bins_vol{ivol}_shuffled.h5")
            shuffle_parent_halos(input_hdf5=HALO_MASS_BINS, output_hdf5=SHUFFLED_HALO_FILE, verbose=VERBOSE, rng_seed=None)

            print("Shuffling galaxy catalogue...")
            from src.h2s_shuffle2 import shuffle_galaxy_catalog_binned
            from src.h2s_profile_r import boundary_correction
            if DO_FLUX_CUT:
                SHUFFLED_GALAXY_FILE = os.path.join(BASE_DIR, f"filtered_ELGs_{llim}_shuffled_vol{ivol}.h5")
            else:
                SHUFFLED_GALAXY_FILE = os.path.join(BASE_DIR, f"filtered_ELGs_shuffled_vol{ivol}.h5")

            shuffle_galaxy_catalog_binned(galaxy_file=FILTERED_GALAXIES, halo_shuffled_file=SHUFFLED_HALO_FILE,
                                          output_file=SHUFFLED_GALAXY_FILE, boxsize=BOXSIZE, bins=N_BINS_SHUFFLING,
                                          galaxy_id_field=GALAXY_MAIN_ID_KEY , galaxy_host_field=GALAXY_HOST_ID_KEY ,
                                          boundary_correction=boundary_correction, verbose=VERBOSE)

        # =========== Calculate 2PCF. Real Space ============
        if DO_CORRELATION_FUNC_REAL_SPACE:
            print("Calculating correlation function in real space...")
            from src.h2s_corr import compute_correlation_corrfunc, export_positions

            if DO_FLUX_CUT:
                POSITIONS_GALAXIES = os.path.join(BASE_DIR, f"positions_vol{ivol}_{llim}.txt")
                GALAXY_2PCF_REAL = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_vol{ivol}_{llim}.txt")
                POSITIONS_GALAXIES_SHUFFLED = os.path.join(BASE_DIR, f"positions_shuffled_vol{ivol}_{llim}.txt")
                GALAXY_2PCF_REAL_SHUFFLED = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_shuffled_vol{ivol}_{llim}.txt")
            else:
                POSITIONS_GALAXIES = os.path.join(BASE_DIR, f"positions_vol{ivol}.txt")
                GALAXY_2PCF_REAL = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_vol{ivol}_.txt")
                POSITIONS_GALAXIES_SHUFFLED = os.path.join(BASE_DIR, f"positions_shuffled_vol{ivol}.txt")
                GALAXY_2PCF_REAL_SHUFFLED = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_shuffled_vol{ivol}.txt")

            if DO_SHUFFLING:
                export_positions(SHUFFLED_GALAXY_FILE, POSITIONS_GALAXIES_SHUFFLED,
                                 xkey=GALAXY_XPOS_KEY, ykey=GALAXY_YPOS_KEY, zkey=GALAXY_ZPOS_KEY, verbose=VERBOSE)
                compute_correlation_corrfunc(POSITIONS_GALAXIES_SHUFFLED, GALAXY_2PCF_REAL_SHUFFLED, boxsize=BOXSIZE,
                                             n_bins= NBINS_2PCF_REAL, rmax = RMAX_2PCF_REAL, rmin=RMIN_2PCF_REAL,
                                             n_threads=NTHREADS_2PCF_REAL, verbose=VERBOSE)

            export_positions(FILTERED_GALAXIES, POSITIONS_GALAXIES,
                             xkey=GALAXY_XPOS_KEY, ykey=GALAXY_YPOS_KEY, zkey=GALAXY_ZPOS_KEY, verbose=VERBOSE)
            compute_correlation_corrfunc(POSITIONS_GALAXIES, GALAXY_2PCF_REAL, boxsize=BOXSIZE, n_bins= NBINS_2PCF_REAL,
                                         rmax = RMAX_2PCF_REAL, rmin=RMIN_2PCF_REAL, n_threads=NTHREADS_2PCF_REAL, verbose=VERBOSE)

            if DO_PLOTS:
                from src.h2s_plots2 import plot_correlation_function, plot_2pcf_ratio
                if DO_FLUX_CUT:
                    PLOT_2PCF_REAL = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_vol{ivol}_{llim}.png")
                    PLOT_2PCF_REAL_SHUFFLED = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_shuffled_vol{ivol}_{llim}.png")
                else:
                    PLOT_2PCF_REAL = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_vol{ivol}_.png")
                    PLOT_2PCF_REAL_SHUFFLED = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_shuffled_vol{ivol}.png")
                plot_correlation_function(GALAXY_2PCF_REAL, PLOT_2PCF_REAL, loglog=True, show=False,
                                          r_index=0, xi_index=1, err_index=2)
                if DO_SHUFFLING:
                    plot_correlation_function(GALAXY_2PCF_REAL_SHUFFLED, PLOT_2PCF_REAL_SHUFFLED, loglog=True, show=False,
                                              r_index=0, xi_index=1, err_index=2)
                if DO_2PCF_REAL_RATIO:
                    PLOT_2PCF_RATIO = os.path.join(RESULTS_DIR, f"2PCF_ratio_vol{ivol}_{llim}.png" if DO_FLUX_CUT else f"2PCF_ratio_vol{ivol}.png")
                    plot_2pcf_ratio(file_normal=GALAXY_2PCF_REAL, file_shuffled=GALAXY_2PCF_REAL_SHUFFLED,
                                    output_png=PLOT_2PCF_RATIO, xlim=XLIM_2PCF_RATIO, ylim=YLIM_2PCF_RATIO, show=False)


        # ========= Calculate 2PCF. Redshift Space =========
        if DO_CORRELATION_FUNC_REDSHIFT_SPACE:
            print("Calculating correlation function in redshift space...")
            from src.h2s_corr import export_positions_redshift_space, compute_correlation_corrfunc

            if DO_FLUX_CUT:
                POSITIONS_GALAXIES_RS = os.path.join(BASE_DIR, f"positions_redshift_vol{ivol}_{llim}.txt")
                GALAXY_2PCF_REDSHIFT = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_redshift_vol{ivol}_{llim}.txt")
                POSITIONS_GALAXIES_RS_SHUFFLED = os.path.join(BASE_DIR, f"positions_redshift_shuffled_vol{ivol}_{llim}.txt")
                GALAXY_2PCF_REDSHIFT_SHUFFLED = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_redshift_shuffled_vol{ivol}_{llim}.txt")
            else:
                POSITIONS_GALAXIES_RS = os.path.join(BASE_DIR, f"positions_redshift_vol{ivol}.txt")
                GALAXY_2PCF_REDSHIFT = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_redshift_vol{ivol}.txt")
                POSITIONS_GALAXIES_RS_SHUFFLED = os.path.join(BASE_DIR, f"positions_redshift_shuffled_vol{ivol}.txt")
                GALAXY_2PCF_REDSHIFT_SHUFFLED = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_redshift_shuffled_vol{ivol}.txt")

            if DO_SHUFFLING:
                export_positions_redshift_space(infile=SHUFFLED_GALAXY_FILE, outfile= POSITIONS_GALAXIES_RS_SHUFFLED,
                                                z_snap=Z_SNAP, Omega_L=OMEGA_L, Omega_m=OMEGA_M, h=h,
                                                xkey=GALAXY_XPOS_KEY, ykey=GALAXY_YPOS_KEY, zkey=GALAXY_ZPOS_KEY,
                                                xvel_key=GALAXY_XVEL_KEY,yvel_key=GALAXY_YVEL_KEY, zvel_key=GALAXY_ZVEL_KEY,
                                                los_axis=LOS_AXIS, verbose=VERBOSE)
                compute_correlation_corrfunc(POSITIONS_GALAXIES_RS_SHUFFLED, GALAXY_2PCF_REDSHIFT_SHUFFLED, boxsize=BOXSIZE,
                                             n_bins= NBINS_2PCF_REDSHIFT,rmax = RMAX_2PCF_REDSHIFT, rmin=RMIN_2PCF_REDSHIFT,
                                             n_threads=NTHREADS_2PCF_REDSHIFT, verbose=VERBOSE)

            export_positions_redshift_space(infile=FILTERED_GALAXIES,
                                            outfile= POSITIONS_GALAXIES_RS, z_snap=Z_SNAP, Omega_L=OMEGA_L,
                                            Omega_m=OMEGA_M, h=h, xkey=GALAXY_XPOS_KEY, ykey=GALAXY_YPOS_KEY,
                                            zkey=GALAXY_ZPOS_KEY, xvel_key=GALAXY_XVEL_KEY,yvel_key=GALAXY_YVEL_KEY,
                                            zvel_key=GALAXY_ZVEL_KEY, los_axis=LOS_AXIS, verbose=VERBOSE)
            compute_correlation_corrfunc(POSITIONS_GALAXIES_RS, GALAXY_2PCF_REDSHIFT, boxsize=BOXSIZE,
                                         n_bins= NBINS_2PCF_REDSHIFT,rmax = RMAX_2PCF_REDSHIFT, rmin=RMIN_2PCF_REDSHIFT,
                                         n_threads=NTHREADS_2PCF_REDSHIFT, verbose=VERBOSE)

            if DO_PLOTS:
                from src.h2s_plots2 import plot_correlation_function
                PLOT_2PCF_REDSHIFT = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_redshift_vol{ivol}_{llim}.png" if DO_FLUX_CUT else f"2PCF_Corrfunc_redshift_vol{ivol}.png")
                PLOT_2PCF_REDSHIFT_SHUFFLED = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_redshift_shuffled_vol{ivol}_{llim}.png" if DO_FLUX_CUT else f"2PCF_Corrfunc_redshift_shuffled_vol{ivol}.png")

                plot_correlation_function(GALAXY_2PCF_REDSHIFT, PLOT_2PCF_REDSHIFT, loglog=True, show=False,
                                          r_index=0, xi_index=1, err_index=2)
                if DO_SHUFFLING:
                    plot_correlation_function(GALAXY_2PCF_REDSHIFT_SHUFFLED, PLOT_2PCF_REDSHIFT_SHUFFLED, loglog=True, show=False,
                                              r_index=0, xi_index=1, err_index=2)

        # ========= Calculate Conformity Parameters =========
        if DO_CONFORMITY:
            print("Calculating conformity parameters...")
            from src.h2s_conformity2 import compute_conformity_parameters, compute_conformity_parameters_shuffled

            CONFORMITY = os.path.join(RESULTS_DIR, f"conformity_vol{ivol}_{llim}.h5" if DO_FLUX_CUT else f"conformity_vol{ivol}.h5")
            CONFORMITY_SHUFFLED = os.path.join(RESULTS_DIR, f"conformity_shuffled_vol{ivol}_{llim}.h5" if DO_FLUX_CUT else f"conformity_shuffled_vol{ivol}.h5")

            compute_conformity_parameters(galaxy_file=FILTERED_GALAXIES,
                                          halo_file=HALO_FILE, M_min= M_MIN_CONFORMITY,
                                          M_max= M_MAX_CONFORMITY, N_bins=N_BINS_CONFORMITY,
                                          galaxy_format=INPUT_GALAXY_FORMAT, halo_format= INPUT_HALO_FORMAT,
                                          output_file=CONFORMITY, halo_pid=HALO_PID_KEY, halo_mass=HALO_MASS_KEY,
                                          verbose=VERBOSE,centralformats=CENTRALFORMATS, gal_host_id= GALAXY_HOST_ID_KEY,
                                          gal_main_id= GALAXY_MAIN_ID_KEY, gal_main_mass= GALAXY_MAIN_MASS_KEY, testing=TESTING)

            if DO_SHUFFLING:
                compute_conformity_parameters_shuffled(galaxy_file=SHUFFLED_GALAXY_FILE,
                                                       halo_file=HALO_FILE, M_min=M_MIN_CONFORMITY,
                                                       M_max=M_MAX_CONFORMITY, N_bins=N_BINS_CONFORMITY,
                                                       galaxy_format=INPUT_GALAXY_FORMAT, halo_format=INPUT_HALO_FORMAT,
                                                       output_file=CONFORMITY_SHUFFLED, halo_pid=HALO_PID_KEY, halo_mass=HALO_MASS_KEY,
                                                       verbose=VERBOSE, gal_is_central="is_central", centralformats=CENTRALFORMATS,
                                                       gal_main_id=GALAXY_MAIN_ID_KEY, gal_main_mass=GALAXY_MAIN_MASS_KEY, testing=TESTING)

            if DO_PLOTS:
                from src.h2s_plots2 import plot_hmf, plot_hod, plot_hmf_comparison
                PLOT_HMF = os.path.join(RESULTS_DIR, f"HMF_vol{ivol}_{llim}.png" if DO_FLUX_CUT else f"HMF_vol{ivol}.png")
                PLOT_HOD = os.path.join(RESULTS_DIR, f"HOD_Occupation_vol{ivol}_{llim}.png" if DO_FLUX_CUT else f"HOD_Occupation_vol{ivol}.png")

                plot_hmf(h5file=CONFORMITY, output_path=PLOT_HMF, box_size=BOXSIZE,
                         logM_min=M_MIN_CONFORMITY, logM_max=M_MAX_CONFORMITY, n_bins=N_BINS_CONFORMITY, show=False)
                plot_hod(h5file=CONFORMITY, output_path=PLOT_HOD, show=False)

                if DO_HMF_COMPARISON:
                    PLOT_HMF_COMPARISON = os.path.join(RESULTS_DIR, f"HMF_comparison_vol{ivol}_{llim}.png" if DO_FLUX_CUT else f"HMF_comparison_vol{ivol}.png")
                    # (Requiere Shuffling para funcionar correctamente con SHUFFLED_HALO_FILE)
                    if DO_SHUFFLING:
                        plot_hmf_comparison(conformity_file=CONFORMITY, halo_bins_file=SHUFFLED_HALO_FILE, bins=BINNING_HMF,
                                            output_png=PLOT_HMF_COMPARISON, boxsize=BOXSIZE, show=False, loglog=True)


        #=============== Calculate Radial Profile ===============
        if DO_RADIAL_PROFILE:
            print("Calculating radial profile...")
            from src.h2s_profile_r import compute_radial_profile, compute_radial_profile_shuffled, fit_radial_profile

            RADIAL_PROFILE = os.path.join(RESULTS_DIR, f"radial_profile_vol{ivol}_{llim}.h5" if DO_FLUX_CUT else f"radial_profile_vol{ivol}.h5")
            RADIAL_PROFILE_SHUFFLED = os.path.join(RESULTS_DIR, f"radial_profile_shuffled_vol{ivol}_{llim}.h5" if DO_FLUX_CUT else f"radial_profile_shuffled_vol{ivol}.h5")

            compute_radial_profile(galaxy_file=FILTERED_GALAXIES,
                                   halo_file=HALO_FILE, output_file=RADIAL_PROFILE, verbose=VERBOSE,
                                   boxsize=BOXSIZE, bins=BINNING_RADIAL, halo_format=INPUT_HALO_FORMAT,
                                   halo_id_key=HALO_ID_KEY, halo_pid_key=HALO_PID_KEY, halo_x_key=HALO_XPOS_KEY,
                                   halo_y_key=HALO_YPOS_KEY, halo_z_key=HALO_ZPOS_KEY, centralformats=CENTRALFORMATS,
                                   galaxy_host_key=GALAXY_HOST_ID_KEY, galaxy_id_key=GALAXY_MAIN_ID_KEY,
                                   galaxy_x_key=GALAXY_XPOS_KEY, galaxy_y_key=GALAXY_YPOS_KEY,
                                   galaxy_z_key=GALAXY_ZPOS_KEY, testing=TESTING)

            if DO_SHUFFLING:
                compute_radial_profile_shuffled(galaxy_file=SHUFFLED_GALAXY_FILE, halo_file=HALO_FILE,
                                                output_file=RADIAL_PROFILE_SHUFFLED, verbose=VERBOSE,
                                                boxsize=BOXSIZE, bins=BINNING_RADIAL, halo_format=INPUT_HALO_FORMAT,
                                                halo_id_key=HALO_ID_KEY, halo_pid_key=HALO_PID_KEY, halo_x_key=HALO_XPOS_KEY,
                                                halo_y_key=HALO_YPOS_KEY, halo_z_key=HALO_ZPOS_KEY,
                                                galaxy_is_central_key="is_central", centralformats=CENTRALFORMATS, galaxy_id_key=GALAXY_MAIN_ID_KEY,
                                                galaxy_x_key=GALAXY_XPOS_KEY, galaxy_y_key=GALAXY_YPOS_KEY,
                                                galaxy_z_key=GALAXY_ZPOS_KEY, testing=TESTING)

            if DO_PLOTS:
                from src.h2s_plots2 import plot_radial_profile
                PLOT_RADIAL_PROFILE = os.path.join(RESULTS_DIR, f"radial_profile_vol{ivol}_{llim}.png" if DO_FLUX_CUT else f"radial_profile_vol{ivol}.png")
                plot_radial_profile(profile_file=RADIAL_PROFILE, output_png=PLOT_RADIAL_PROFILE, loglog=True, show=False)

            if DO_FIT_RADIAL_PROFILE:
                FIT_RADIAL_PROFILE_PARAMS = os.path.join(RESULTS_DIR, f"radial_profile_fit_params_vol{ivol}_{llim}.txt" if DO_FLUX_CUT else f"radial_profile_fit_params_vol{ivol}.txt")
                FIT_RADIAL_PROFILE_PARAMS_SHUFFLED = os.path.join(RESULTS_DIR, f"radial_profile_fit_params_shuffled_vol{ivol}_{llim}.txt" if DO_FLUX_CUT else f"radial_profile_fit_params_shuffled_vol{ivol}.txt")

                fit_radial_profile(profile_file=RADIAL_PROFILE, output_params_file=FIT_RADIAL_PROFILE_PARAMS,
                                   initial_guess= INITAL_GUESS_RADIAL, bounds=None, verbose=VERBOSE)
                if DO_SHUFFLING:
                    fit_radial_profile(profile_file=RADIAL_PROFILE_SHUFFLED, output_params_file=FIT_RADIAL_PROFILE_PARAMS_SHUFFLED,
                                       initial_guess= INITAL_GUESS_RADIAL, bounds=None, verbose=VERBOSE)
                if DO_PLOTS:
                    from src.h2s_plots2 import plot_radial_profile_fit
                    FIT_RADIAL_PROFILE = os.path.join(RESULTS_DIR, f"radial_profile_fit_vol{ivol}_{llim}.png" if DO_FLUX_CUT else f"radial_profile_fit_vol{ivol}.png")
                    params_radial = np.loadtxt(FIT_RADIAL_PROFILE_PARAMS, delimiter=",", skiprows=1).flatten()
                    plot_radial_profile_fit(profile_file=RADIAL_PROFILE, output_png=FIT_RADIAL_PROFILE,
                                            params = params_radial, show=False, loglog=True)

        # ========== Calculate Radial Velocity Profile ===========
        if DO_VR_PROFILE:
            print("Calculating radial velocity profile...")
            from src.h2s_profile_vel import compute_vr_profile, compute_vr_profile_shuffled, fit_vr_profile

            VR_PROFILE = os.path.join(RESULTS_DIR, f"vr_profile_vol{ivol}_{llim}.h5" if DO_FLUX_CUT else f"vr_profile_vol{ivol}.h5")
            VR_PROFILE_SHUFFLED = os.path.join(RESULTS_DIR, f"vr_profile_shuffled_vol{ivol}_{llim}.h5" if DO_FLUX_CUT else f"vr_profile_shuffled_vol{ivol}.h5")

            compute_vr_profile(galaxy_file=FILTERED_GALAXIES,
                               halo_file=HALO_FILE, output_file=VR_PROFILE,verbose=VERBOSE, boxsize=BOXSIZE,
                               bins=BINNING_VR, halo_format=INPUT_HALO_FORMAT, halo_id_key=HALO_ID_KEY,
                               halo_pid_key=HALO_PID_KEY, halo_x_key=HALO_XPOS_KEY, halo_y_key=HALO_YPOS_KEY,
                               halo_z_key=HALO_ZPOS_KEY, halo_vx_key=HALO_XVEL_KEY, halo_vy_key=HALO_YVEL_KEY,
                               halo_vz_key=HALO_ZVEL_KEY, centralformats=CENTRALFORMATS, galaxy_host_id_key=GALAXY_HOST_ID_KEY,
                               galaxy_main_id_key=GALAXY_MAIN_ID_KEY, galaxy_x_key=GALAXY_XPOS_KEY,
                               galaxy_y_key=GALAXY_YPOS_KEY, galaxy_z_key=GALAXY_ZPOS_KEY,
                               galaxy_vx_key=GALAXY_XVEL_KEY, galaxy_vy_key=GALAXY_YVEL_KEY,
                               galaxy_vz_key=GALAXY_ZVEL_KEY,testing=TESTING)

            if DO_SHUFFLING:
                compute_vr_profile_shuffled(galaxy_file=SHUFFLED_GALAXY_FILE,
                                            halo_file=HALO_FILE, output_file=VR_PROFILE_SHUFFLED, verbose=VERBOSE,
                                            boxsize=BOXSIZE, bins=BINNING_VR, halo_format=INPUT_HALO_FORMAT,
                                            halo_id_key=HALO_ID_KEY, halo_pid_key=HALO_PID_KEY,
                                            halo_x_key=HALO_XPOS_KEY, halo_y_key=HALO_YPOS_KEY,
                                            halo_z_key=HALO_ZPOS_KEY, halo_vx_key=HALO_XVEL_KEY,
                                            halo_vy_key=HALO_YVEL_KEY, halo_vz_key=HALO_ZVEL_KEY,
                                            galaxy_is_central_key="is_central", centralformats=CENTRALFORMATS,
                                            galaxy_main_id_key=GALAXY_MAIN_ID_KEY, galaxy_x_key=GALAXY_XPOS_KEY,
                                            galaxy_y_key=GALAXY_YPOS_KEY, galaxy_z_key=GALAXY_ZPOS_KEY,
                                            galaxy_vx_key=GALAXY_XVEL_KEY, galaxy_vy_key=GALAXY_YVEL_KEY,
                                            galaxy_vz_key=GALAXY_ZVEL_KEY,testing=TESTING)

            if DO_PLOTS:
                from src.h2s_plots2 import plot_vr_distribution
                PLOT_VR_PROFILE = os.path.join(RESULTS_DIR, f"vr_profile_vol{ivol}_{llim}.png" if DO_FLUX_CUT else f"vr_profile_vol{ivol}.png")
                plot_vr_distribution(vr_profile_file=VR_PROFILE, output_png=PLOT_VR_PROFILE, loglog=False, show=False)

            if DO_FIT_VR_PROFILE:
                FIT_VR_PROFILE = os.path.join(RESULTS_DIR, f"vr_profile_fit_vol{ivol}_{llim}.png" if DO_FLUX_CUT else f"vr_profile_fit_vol{ivol}.png")
                FIT_VR_PROFILE_PARAMS = os.path.join(RESULTS_DIR, f"vr_profile_fit_params_vol{ivol}_{llim}.txt" if DO_FLUX_CUT else f"vr_profile_fit_params_vol{ivol}.txt")
                FIT_VR_PROFILE_SHUFFLED = os.path.join(RESULTS_DIR, f"vr_profile_fit_shuffled_vol{ivol}_{llim}.png" if DO_FLUX_CUT else f"vr_profile_fit_shuffled_vol{ivol}.png")
                FIT_VR_PROFILE_PARAMS_SHUFFLED = os.path.join(RESULTS_DIR, f"vr_profile_fit_params_shuffled_vol{ivol}_{llim}.txt" if DO_FLUX_CUT else f"vr_profile_fit_params_shuffled_vol{ivol}.txt")

                fit_vr_profile(vr_profile_file=VR_PROFILE, plot=True, output_png=FIT_VR_PROFILE,
                               loglog=False, manual_params=MANUAL_PARAMS_VR, output_params_file=FIT_VR_PROFILE_PARAMS)
                if DO_SHUFFLING:
                    fit_vr_profile(vr_profile_file=VR_PROFILE_SHUFFLED, plot=True, output_png=FIT_VR_PROFILE_SHUFFLED,
                                   loglog=False, manual_params=MANUAL_PARAMS_VR, output_params_file=FIT_VR_PROFILE_PARAMS_SHUFFLED)

        # ========== Calculate Tangential Velocity Profile ===========
        if DO_VTAN_PROFILE:
            print("Calculating tangential velocity profile...")
            from src.h2s_profile_vel import compute_vtan_profile, compute_vtan_profile_shuffled, fit_vtheta_profile

            VTAN_PROFILE = os.path.join(RESULTS_DIR, f"vtan_profile_vol{ivol}_{llim}.h5" if DO_FLUX_CUT else f"vtan_profile_vol{ivol}.h5")
            VTAN_PROFILE_SHUFFLED = os.path.join(RESULTS_DIR, f"vtan_profile_shuffled_vol{ivol}_{llim}.h5" if DO_FLUX_CUT else f"vtan_profile_shuffled_vol{ivol}.h5")

            compute_vtan_profile(galaxy_file=FILTERED_GALAXIES,
                                 halo_file=HALO_FILE, output_file=VTAN_PROFILE, verbose=VERBOSE, boxsize=BOXSIZE,
                                 bins=BINNING_VTAN, halo_format=INPUT_HALO_FORMAT, halo_id_key=HALO_ID_KEY,
                                 halo_pid_key=HALO_PID_KEY, halo_x_key=HALO_XPOS_KEY, halo_y_key=HALO_YPOS_KEY,
                                 halo_z_key=HALO_ZPOS_KEY, halo_vx_key=HALO_XVEL_KEY, halo_vy_key=HALO_YVEL_KEY,
                                 halo_vz_key=HALO_ZVEL_KEY, galaxy_host_id_key=GALAXY_HOST_ID_KEY,
                                 galaxy_main_id_key=GALAXY_MAIN_ID_KEY, galaxy_x_key=GALAXY_XPOS_KEY,
                                 galaxy_y_key=GALAXY_YPOS_KEY, galaxy_z_key=GALAXY_ZPOS_KEY,
                                 galaxy_vx_key=GALAXY_XVEL_KEY, galaxy_vy_key=GALAXY_YVEL_KEY,
                                 galaxy_vz_key=GALAXY_ZVEL_KEY, testing=TESTING)

            if DO_SHUFFLING:
                compute_vtan_profile_shuffled(galaxy_file=SHUFFLED_GALAXY_FILE,
                                              halo_file=HALO_FILE, output_file=VTAN_PROFILE_SHUFFLED, verbose=VERBOSE,
                                              boxsize=BOXSIZE, bins=BINNING_VTAN, halo_format=INPUT_HALO_FORMAT,
                                              halo_id_key=HALO_ID_KEY, halo_pid_key=HALO_PID_KEY,
                                              halo_x_key=HALO_XPOS_KEY, halo_y_key=HALO_YPOS_KEY,
                                              halo_z_key=HALO_ZPOS_KEY, halo_vx_key=HALO_XVEL_KEY,
                                              halo_vy_key=HALO_YVEL_KEY, halo_vz_key=HALO_ZVEL_KEY,
                                              galaxy_is_central_key="is_central",
                                              galaxy_main_id_key=GALAXY_MAIN_ID_KEY, galaxy_x_key=GALAXY_XPOS_KEY,
                                              galaxy_y_key=GALAXY_YPOS_KEY, galaxy_z_key=GALAXY_ZPOS_KEY,
                                              galaxy_vx_key=GALAXY_XVEL_KEY, galaxy_vy_key=GALAXY_YVEL_KEY,
                                              galaxy_vz_key=GALAXY_ZVEL_KEY,testing=TESTING)

            if DO_PLOTS:
                from src.h2s_plots2 import plot_vtan_distribution
                PLOT_VTAN_PROFILE = os.path.join(RESULTS_DIR, f"vtan_profile_vol{ivol}_{llim}.png" if DO_FLUX_CUT else f"vtan_profile_vol{ivol}.png")
                plot_vtan_distribution(vtan_profile_file=VTAN_PROFILE, output_png=PLOT_VTAN_PROFILE, loglog=False, show=False)

            if DO_FIT_VTAN_PROFILE:
                FIT_VTAN_PROFILE = os.path.join(RESULTS_DIR, f"vtan_profile_fit_vol{ivol}_{llim}.png" if DO_FLUX_CUT else f"vtan_profile_fit_vol{ivol}.png")
                FIT_VTAN_PROFILE_PARAMS = os.path.join(RESULTS_DIR, f"vtan_profile_fit_params_vol{ivol}_{llim}.txt" if DO_FLUX_CUT else f"vtan_profile_fit_params_vol{ivol}.txt")
                FIT_VTAN_PROFILE_SHUFFLED = os.path.join(RESULTS_DIR, f"vtan_profile_fit_shuffled_vol{ivol}_{llim}.png" if DO_FLUX_CUT else f"vtan_profile_fit_shuffled_vol{ivol}.png")
                FIT_VTAN_PROFILE_PARAMS_SHUFFLED = os.path.join(RESULTS_DIR, f"vtan_profile_fit_params_shuffled_vol{ivol}_{llim}.txt" if DO_FLUX_CUT else f"vtan_profile_fit_params_shuffled_vol{ivol}.txt")

                fit_vtheta_profile(vtheta_profile_file=VTAN_PROFILE, plot=True, output_png=FIT_VTAN_PROFILE, output_params_file= FIT_VTAN_PROFILE_PARAMS,
                                   loglog=False, manual_params= MANUAL_PARAMS_VTAN)
                if DO_SHUFFLING:
                    fit_vtheta_profile(vtheta_profile_file=VTAN_PROFILE_SHUFFLED, plot=True, output_png=FIT_VTAN_PROFILE_SHUFFLED,
                                       loglog=False, manual_params=MANUAL_PARAMS_VTAN, output_params_file=FIT_VTAN_PROFILE_PARAMS_SHUFFLED)

        # ================= Kaiser Analysis =================
        if DO_KAISER_ANALYSIS:
            print("Performing Kaiser analysis...")
            from src.h2s_plots2 import plot_kaiser_comparison, plot_kaiser_ratio
            from src.h2s_io_PRUEBA_NOPID import kaiser_factor

            fkaiser = kaiser_factor(omega_m=OMEGA_M, b=BIAS, gamma=GAMMA)
            print(f"Kaiser factor: {fkaiser:.4f}")

            if DO_PLOTS:
                REAL_FILE = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_vol{ivol}_{llim}.txt" if DO_FLUX_CUT else f"2PCF_Corrfunc_vol{ivol}_.txt")
                REDSHIFT_FILE = os.path.join(RESULTS_DIR, f"2PCF_Corrfunc_redshift_vol{ivol}_{llim}.txt" if DO_FLUX_CUT else f"2PCF_Corrfunc_redshift_vol{ivol}.txt")
                KAISER_PNG = os.path.join(RESULTS_DIR, f"kaiser_comparison_vol{ivol}_{llim}.png" if DO_FLUX_CUT else f"kaiser_comparison_vol{ivol}.png")

                plot_kaiser_comparison(real_file=REAL_FILE, redshift_file=REDSHIFT_FILE, omega_m=OMEGA_M, xlim = None, ylim=None,
                                       b=BIAS, gamma=GAMMA, output_png=KAISER_PNG, show=False, loglog=True)

            if DO_KAISER_RATIO:
                KAISER_RATIO = os.path.join(RESULTS_DIR, f"kaiser_ratio_vol{ivol}_{llim}.png" if DO_FLUX_CUT else f"kaiser_ratio_vol{ivol}.png")
                plot_kaiser_ratio(real_file=REAL_FILE, redshift_file=REDSHIFT_FILE, output_png=KAISER_RATIO,
                                  omega_m=OMEGA_M, bias=BIAS, gamma=GAMMA, show=False, xlim=XLIM_KAISER, ylim=YLIM_KAISER)

        # ============ Write master output file: h2s_output.h5 ============
        MASTER_OUTPUT = os.path.join(RESULTS_DIR, f"h2s_output_vol{ivol}.h5")
        try:
            with h5py.File(CONFORMITY, "r") as f_conf, \
                 h5py.File(RADIAL_PROFILE, "r") as f_radial, \
                 h5py.File(VR_PROFILE, "r") as f_vr, \
                 h5py.File(VTAN_PROFILE, "r") as f_vtan:

                k1_global = f_conf["data/global/k1_global"][()]
                k2_global = f_conf["data/global/k2_global"][()]

                params_vtan = np.loadtxt(FIT_VTAN_PROFILE_PARAMS, delimiter=",", skiprows=1).flatten() if DO_FIT_VTAN_PROFILE else np.zeros(4)
                params_vr = np.loadtxt(FIT_VR_PROFILE_PARAMS, delimiter=",", skiprows=1).flatten() if DO_FIT_VR_PROFILE else np.zeros(9)
                params_radial = np.loadtxt(FIT_RADIAL_PROFILE_PARAMS, delimiter=",", skiprows=1).flatten() if DO_FIT_RADIAL_PROFILE else np.zeros(5)

                alpha, beta, r0, N0, kappa = params_radial if len(params_radial)==5 else (0,0,0,0,0)
                vtan_y0, vtan_alpha, vtan_beta, vtan_kappa = params_vtan if len(params_vtan)==4 else (0,0,0,0)
                (vr_A1, vr_mu1, vr_sigma1, vr_A2, vr_mu2, vr_sigma2, vr_A3, vr_mu3, vr_sigma3) = params_vr if len(params_vr)==9 else (0,0,0,0,0,0,0,0,0)

                conf_bins = f_conf["data/bins"]
                M_min_data = conf_bins["M_min_bin"][:]
                M_max_data = conf_bins["M_max_bin"][:]
                N_halo = conf_bins["N_Halos"][:]
                k1 = conf_bins["k1"][:]
                k2 = conf_bins["k2"][:]
                Nsat = conf_bins["N_S"][:]
                Ncen = conf_bins["N_C"][:]

                r_centers = f_radial['radial_bins'][:]
                Nsat_r = f_radial['counts'][:]
                dr = np.diff(r_centers)
                edges = np.concatenate(([r_centers[0] - dr[0]/2], r_centers[:-1] + dr/2, [r_centers[-1] + dr[-1]/2]))
                r_min = edges[:-1]
                r_max = edges[1:]

                vr_centers = f_vr["velocity_bins"][:]
                dvr = np.diff(vr_centers)
                vr_edges = np.concatenate(([vr_centers[0] - dvr[0]/2], vr_centers[:-1] + dvr/2, [vr_centers[-1] + dvr[-1]/2]))
                Nsat_vr = f_vr["density"][:]
                vr_min = vr_edges[:-1]
                vr_max = vr_edges[1:]

                vtan_centers = f_vtan["velocity_bins"][:]
                dvtan = np.diff(vtan_centers)
                vtan_edges = np.concatenate(([vtan_centers[0] - dvtan[0]/2], vtan_centers[:-1] + dvtan/2, [vtan_centers[-1] + dvtan[-1]/2]))
                Nsat_vtan = f_vtan["density"][:]
                vtan_min = vtan_edges[:-1]
                vtan_max = vtan_edges[1:]

            with h5py.File(MASTER_OUTPUT, "w") as f:
                header = f.create_group("header")
                header.attrs["K1_global"] = k1_global
                header.attrs["K2_global"] = k2_global
                header.attrs["z_snap"] = Z_SNAP
                header.attrs["omega_m"] = OMEGA_M
                header.attrs["omega_l"] = OMEGA_L
                header.attrs["h"] = h
                header.attrs["boxsize"] = BOXSIZE
                header.attrs["alpha"] = alpha
                header.attrs["beta"] = beta
                header.attrs["kappa"] = kappa
                header.attrs["N0"] = N0
                header.attrs["r0"] = r0
                header.attrs["vtan_y0"] = vtan_y0
                header.attrs["vtan_alpha"] = vtan_alpha
                header.attrs["vtan_beta"] = vtan_beta
                header.attrs["vtan_kappa"] = vtan_kappa
                header.attrs["vr_A1"] = vr_A1
                header.attrs["vr_mu1"] = vr_mu1
                header.attrs["vr_sigma1"] = vr_sigma1
                header.attrs["vr_A2"] = vr_A2
                header.attrs["vr_mu2"] = vr_mu2
                header.attrs["vr_sigma2"] = vr_sigma2
                header.attrs["vr_A3"] = vr_A3
                header.attrs["vr_mu3"] = vr_mu3
                header.attrs["vr_sigma3"] = vr_sigma3

                data = f.create_group("data")
                data.create_dataset("M_min", data=M_min_data)
                data.create_dataset("M_max", data=M_max_data)
                data.create_dataset("N_halo", data=N_halo)
                data.create_dataset("k1", data=k1)
                data.create_dataset("k2", data=k2)
                data.create_dataset("Nsat", data=Nsat)
                data.create_dataset("Ncen", data=Ncen)
                data.create_dataset("r_min", data=r_min)
                data.create_dataset("r_max", data=r_max)
                data.create_dataset("Nsat_r", data=Nsat_r)
                data.create_dataset("vr_min", data=vr_min)
                data.create_dataset("vr_max", data=vr_max)
                data.create_dataset("Nsat_vr", data=Nsat_vr)
                data.create_dataset("vtan_min", data=vtan_min)
                data.create_dataset("vtan_max", data=vtan_max)
                data.create_dataset("Nsat_vtan", data=Nsat_vtan)

            print(f"\n[INFO] Master output file written: {MASTER_OUTPUT}\n")
        except Exception as e:
            print(f"[WARNING] No se pudo generar el MASTER_OUTPUT para vol {ivol}: (Asegúrate de tener en True Conformity, Radial y Vels para generarlo)")

        if DO_SHUFFLING:
            MASTER_OUTPUT_SHUFFLED = os.path.join(RESULTS_DIR, f"h2s_output_shuffled_vol{ivol}.h5")
            try:
                with h5py.File(CONFORMITY_SHUFFLED, "r") as f_conf, \
                     h5py.File(RADIAL_PROFILE_SHUFFLED, "r") as f_radial, \
                     h5py.File(VR_PROFILE_SHUFFLED, "r") as f_vr, \
                     h5py.File(VTAN_PROFILE_SHUFFLED, "r") as f_vtan:

                    k1_global = f_conf["data/global/k1_global"][()]
                    k2_global = f_conf["data/global/k2_global"][()]

                    params_vtan_shuffled = np.loadtxt(FIT_VTAN_PROFILE_PARAMS_SHUFFLED, delimiter=",", skiprows=1).flatten() if DO_FIT_VTAN_PROFILE else np.zeros(4)
                    params_vr_shuffled = np.loadtxt(FIT_VR_PROFILE_PARAMS_SHUFFLED, delimiter=",", skiprows=1).flatten() if DO_FIT_VR_PROFILE else np.zeros(9)
                    params_radial_shuffled = np.loadtxt(FIT_RADIAL_PROFILE_PARAMS_SHUFFLED, delimiter=",", skiprows=1).flatten() if DO_FIT_RADIAL_PROFILE else np.zeros(5)

                    alpha, beta, r0, N0, kappa = params_radial_shuffled if len(params_radial_shuffled)==5 else (0,0,0,0,0)
                    vtan_y0, vtan_alpha, vtan_beta, vtan_kappa = params_vtan_shuffled if len(params_vtan_shuffled)==4 else (0,0,0,0)
                    (vr_A1, vr_mu1, vr_sigma1, vr_A2, vr_mu2, vr_sigma2, vr_A3, vr_mu3, vr_sigma3) = params_vr_shuffled if len(params_vr_shuffled)==9 else (0,0,0,0,0,0,0,0,0)

                    conf_bins = f_conf["data/bins"]
                    M_min_data = conf_bins["M_min_bin"][:]
                    M_max_data = conf_bins["M_max_bin"][:]
                    N_halo = conf_bins["N_Halos"][:]
                    k1 = conf_bins["k1"][:]
                    k2 = conf_bins["k2"][:]
                    Nsat = conf_bins["N_S"][:]
                    Ncen = conf_bins["N_C"][:]

                    r_centers = f_radial['radial_bins'][:]
                    Nsat_r = f_radial['counts'][:]
                    dr = np.diff(r_centers)
                    edges = np.concatenate(([r_centers[0] - dr[0]/2], r_centers[:-1] + dr/2, [r_centers[-1] + dr[-1]/2]))
                    r_min = edges[:-1]
                    r_max = edges[1:]

                    vr_centers = f_vr["velocity_bins"][:]
                    dvr = np.diff(vr_centers)
                    vr_edges = np.concatenate(([vr_centers[0] - dvr[0]/2], vr_centers[:-1] + dvr/2, [vr_centers[-1] + dvr[-1]/2]))
                    Nsat_vr = f_vr["density"][:]
                    vr_min = vr_edges[:-1]
                    vr_max = vr_edges[1:]

                    vtan_centers = f_vtan["velocity_bins"][:]
                    dvtan = np.diff(vtan_centers)
                    vtan_edges = np.concatenate(([vtan_centers[0] - dvtan[0]/2], vtan_centers[:-1] + dvtan/2, [vtan_centers[-1] + dvtan[-1]/2]))
                    Nsat_vtan = f_vtan["density"][:]
                    vtan_min = vtan_edges[:-1]
                    vtan_max = vtan_edges[1:]

                with h5py.File(MASTER_OUTPUT_SHUFFLED, "w") as f:
                    header = f.create_group("header")
                    header.attrs["K1_global"] = k1_global
                    header.attrs["K2_global"] = k2_global
                    header.attrs["z_snap"] = Z_SNAP
                    header.attrs["omega_m"] = OMEGA_M
                    header.attrs["omega_l"] = OMEGA_L
                    header.attrs["h"] = h
                    header.attrs["boxsize"] = BOXSIZE
                    header.attrs["alpha"] = alpha
                    header.attrs["beta"] = beta
                    header.attrs["kappa"] = kappa
                    header.attrs["N0"] = N0
                    header.attrs["r0"] = r0
                    header.attrs["vtan_y0"] = vtan_y0
                    header.attrs["vtan_alpha"] = vtan_alpha
                    header.attrs["vtan_beta"] = vtan_beta
                    header.attrs["vtan_kappa"] = vtan_kappa
                    header.attrs["vr_A1"] = vr_A1
                    header.attrs["vr_mu1"] = vr_mu1
                    header.attrs["vr_sigma1"] = vr_sigma1
                    header.attrs["vr_A2"] = vr_A2
                    header.attrs["vr_mu2"] = vr_mu2
                    header.attrs["vr_sigma2"] = vr_sigma2
                    header.attrs["vr_A3"] = vr_A3
                    header.attrs["vr_mu3"] = vr_mu3
                    header.attrs["vr_sigma3"] = vr_sigma3

                    data = f.create_group("data")
                    data.create_dataset("M_min", data=M_min_data)
                    data.create_dataset("M_max", data=M_max_data)
                    data.create_dataset("N_halo", data=N_halo)
                    data.create_dataset("k1", data=k1)
                    data.create_dataset("k2", data=k2)
                    data.create_dataset("Nsat", data=Nsat)
                    data.create_dataset("Ncen", data=Ncen)
                    data.create_dataset("r_min", data=r_min)
                    data.create_dataset("r_max", data=r_max)
                    data.create_dataset("Nsat_r", data=Nsat_r)
                    data.create_dataset("vr_min", data=vr_min)
                    data.create_dataset("vr_max", data=vr_max)
                    data.create_dataset("Nsat_vr", data=Nsat_vr)
                    data.create_dataset("vtan_min", data=vtan_min)
                    data.create_dataset("vtan_max", data=vtan_max)
                    data.create_dataset("Nsat_vtan", data=Nsat_vtan)

                print(f"\n[INFO] Master output file for shuffled catalog written: {MASTER_OUTPUT_SHUFFLED}\n")
            except Exception as e:
                print(f"[WARNING] No se pudo generar el MASTER_OUTPUT_SHUFFLED para vol {ivol}: {e}")

    # <=============================================================================
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

        HMF_TOTAL_FILE = os.path.join(BASE_DIR, "HMF_TOTAL_Rockstar_out87_M200c_Corte4_Centrales.h5")
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
