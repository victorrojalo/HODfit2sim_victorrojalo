import os
import h5py
import numpy as np
from src.h2s_io_PRUEBA_NOPID import filter_log_flux

# --- CONFIGURACIÓN ---
GALAXY_BASE_DIR = "/home2/vgonzalez/Data/Shark/SU1/iz87"
# Aquí es donde se guardarán todos los .h5 juntos
BASE_OUTPUT = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/Galaxias_Cortes/Shark/SU1/iz87/CortesPrueba"

os.makedirs(BASE_OUTPUT, exist_ok=True)

galaxy_subvols = list(range(64))
val = 45.5
llim = 10**(val)
GALAXY_LOG_HALPHA_KEY = "data/bolometric_luminosity_agn"

print(f"🚀 Iniciando pre-procesado: Archivos 'galaxias_Corte1_Shark_volX.h5' con estructura /data/...")

for ivol in galaxy_subvols:
    INPUT_FILE = os.path.join(GALAXY_BASE_DIR, f"ivol{ivol}", "gne_input.hdf5")
    # EL NOMBRE QUE TÚ QUIERES:
    OUT_FILE = os.path.join(BASE_OUTPUT, f"galaxias_Corte8_Shark_vol{ivol}.h5")

    if os.path.exists(INPUT_FILE):
        print(f"Procesando {OUT_FILE}...")
        
        filter_log_flux(
            infile=INPUT_FILE,
            fmin=llim,
            outfile_name=OUT_FILE,
            output_format="h5",
            param_name=GALAXY_LOG_HALPHA_KEY,
            verbose=False
        )
        
        # --- SEGURO DE VIDA: Forzar estructura /data/ ---
        with h5py.File(OUT_FILE, 'a') as f:
            if 'data' not in f:
                g = f.create_group('data')
                for key in list(f.keys()):
                    if key != 'data':
                        f.move(key, f'data/{key}')
    else:
        print(f"⚠️ Saltando ivol{ivol}: No encontrado.")

print(f"✅ ¡Listo! Los archivos están en: {BASE_OUTPUT}")
