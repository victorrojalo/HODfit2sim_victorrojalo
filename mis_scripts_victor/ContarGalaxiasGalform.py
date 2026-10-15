import os
import pandas as pd

# 1. Definimos la ruta de la carpeta (sin el salto de línea)
ruta_carpeta = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/Galaxias_Cortes/Galform/SU1/iz87/CortesPrueba"

# 2. Los cortes que quieres analizar
cortes = [5, 6, 7, 8]

print("--- CONTADOR DE GALAXIAS GALFORM ---")

for corte in cortes:
    # OJO AQUÍ: Modifica "Corte{corte}.txt" para que coincida exactamente 
    # con cómo se llaman tus archivos (ej. "Corte_5.dat", "corte5.csv", etc.)
    nombre_archivo = f"Corte{corte}.txt" 
    ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
    
    # Comprobamos si el archivo realmente existe en esa ruta
    if os.path.exists(ruta_completa):
        try:
            # Leemos el archivo. 
            # delim_whitespace=True asume que las columnas están separadas por espacios/tabulaciones (típico en astrofísica)
            # Si están separadas por comas, quita el delim_whitespace y pon sep=','
            df = pd.read_csv(ruta_completa, delim_whitespace=True, comment='#') 
            
            num_galaxias = len(df)
            print(f"✅ Corte {corte}: {num_galaxias} galaxias encontradas.")
            
        except Exception as e:
            print(f"❌ Error al intentar leer el archivo del Corte {corte}: {e}")
    else:
        print(f"⚠️ No se ha encontrado el archivo: {nombre_archivo} en la carpeta.")
