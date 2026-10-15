import os
import glob
import pandas as pd
import h5py

ruta_carpeta = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/Galaxias_Cortes/Galform/SU1/iz87/CortesPrueba"
cortes = [5, 6, 7, 8]

print("--- CONTADOR DE GALAXIAS GALFORM (HDF5) ---")

for corte in cortes:
    # El asterisco (*) le dice que coja todos los volúmenes de ese corte
    patron = os.path.join(ruta_carpeta, f"galaxias_Corte{corte}_Galform_vol*.h5")
    archivos_corte = glob.glob(patron)
    
    if len(archivos_corte) == 0:
        print(f"⚠️ No se encontraron archivos para el Corte {corte}")
        continue
        
    total_galaxias = 0
    archivos_leidos = 0
    
    for archivo in archivos_corte:
        try:
            # PLAN A: Intentar leerlo como un DataFrame de Pandas
            df = pd.read_hdf(archivo)
            total_galaxias += len(df)
            archivos_leidos += 1
        except:
            try:
                # PLAN B: Si no es de Pandas, leerlo en bruto con h5py
                with h5py.File(archivo, 'r') as f:
                    llave = list(f.keys())[0] # Cogemos la primera matriz de datos
                    total_galaxias += len(f[llave])
                    archivos_leidos += 1
            except Exception as e:
                pass # Si un archivo está corrupto, lo salta en silencio
                
    print(f"✅ Corte {corte}: {total_galaxias} galaxias encontradas (en {archivos_leidos} volúmenes leídos).")
