import os
import glob
import h5py

ruta_carpeta = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/Galaxias_Cortes/Galform/SU1/iz87/CortesPrueba"
cortes = [5, 6, 7, 8]

print("--- CONTADOR REAL DE GALAXIAS GALFORM ---")

for corte in cortes:
    # Busca todos los volúmenes del corte actual
    patron = os.path.join(ruta_carpeta, f"galaxias_Corte{corte}_Galform_vol*.h5")
    archivos_corte = glob.glob(patron)
    
    if len(archivos_corte) == 0:
        print(f"⚠️ No se encontraron archivos para el Corte {corte}")
        continue
        
    total_galaxias = 0
    archivos_leidos = 0
    
    for archivo in archivos_corte:
        try:
            with h5py.File(archivo, 'r') as f:
                # Entramos en 'data' y medimos cuántas filas tiene la columna 'xgal'
                num_galaxias_vol = len(f['data']['xgal'])
                total_galaxias += num_galaxias_vol
                archivos_leidos += 1
        except Exception as e:
            print(f"Error leyendo {archivo}: {e}")
            pass
            
    print(f"✅ Corte {corte}: {total_galaxias} galaxias (en {archivos_leidos} volúmenes leídos).")
