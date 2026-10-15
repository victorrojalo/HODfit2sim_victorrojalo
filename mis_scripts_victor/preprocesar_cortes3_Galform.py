import os
import numpy as np
from src.h2s_io_PRUEBA_NOPID import filter_log_flux

# --- CONFIGURACIÓN ---
GALAXY_BASE_DIR = "/home2/vgonzalez/Data/Galform/SU1/iz87"
BASE_DIR = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/Galaxias_Cortes/Galform/SU1/iz87"
galaxy_subvols = list(range(64))
val = 46.1
llim = 10**(val-40.)  # El corte de flujo
GALAXY_LOG_HALPHA_KEY = "Lbol_AGN" # La clave dentro del h5

print(f"🚀 Iniciando pre-procesado para Corte {val} (llim={llim})...")

for ivol in galaxy_subvols:
    GALAXY_FILE = os.path.join(GALAXY_BASE_DIR, f"ivol{ivol}", "gne_input.hdf5")
    OUT_FILE = os.path.join(BASE_DIR, f"galaxias_Corte3_Galform_vol{ivol}.h5")

    if os.path.exists(GALAXY_FILE):
        print(f"Filtrando vol {ivol}/63...")
        filter_log_flux(
            infile=GALAXY_FILE, 
            fmin=llim, 
            outfile_name=OUT_FILE,
            output_format="h5", 
            param_name=GALAXY_LOG_HALPHA_KEY, 
            verbose=False
        )
    else:
        print(f"⚠️ Saltando vol {ivol}: No existe.")

print("✅ ¡Pre-procesado completado! Ya tienes los 64 archivos filtrados.")
