import os
import h5py
import numpy as np

# Parámetros cosmológicos y de simulación
BOXSIZE = 250.000000             # Box size in Mpc/h
total_volume = BOXSIZE**3        # Volumen de una única caja de simulación

# Rutas de archivos
BASE_DIR = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo"
# Carpeta donde guardaste los cortes ya procesados
CORTES_DIR = os.path.join(BASE_DIR, "Galaxias_Cortes/Shark/SU1/iz87/CortesPrueba")
# Carpeta para guardar estos nuevos resultados
RESULTS_DIR = os.path.join(BASE_DIR, "output/Shark/Validacion_Cortes")
os.makedirs(RESULTS_DIR, exist_ok=True)

# Los cortes y volúmenes a analizar
cortes_a_evaluar = [5, 6, 7, 8]
galaxy_subvols = list(range(64)) # Volúmenes del 0 al 63

# Parámetros globales para el histograma de luminosidad
N_BINS = 20
L_MIN = 38
L_MAX = 48
bin_edges = np.linspace(L_MIN, L_MAX, N_BINS + 1)
bin_width = bin_edges[1] - bin_edges[0]

def main():
    print(f"\n" + "="*60)
    print(f"INICIANDO VALIDACIÓN DE FUNCIÓN DE LUMINOSIDAD POR CORTES")
    print("="*60)

    # Bucle externo: Iteramos sobre cada uno de tus cortes
    for corte in cortes_a_evaluar:
        print(f"\n---> PROCESANDO CORTE {corte} <---")
        total_counts = np.zeros(N_BINS)
        galaxias_totales_corte = 0

        # Bucle interno: Iteramos sobre los 64 volúmenes de ese corte
        for ivol in galaxy_subvols:
            # Reconstruimos el nombre exacto que tienen tus archivos preprocesados
            nombre_archivo = f"galaxias_Corte{corte}_Galform_vol{ivol}.h5"
            GALAXY_FILE = os.path.join(CORTES_DIR, nombre_archivo)

            if not os.path.exists(GALAXY_FILE):
                # Es normal que en el Corte 8 falten archivos si estaban vacíos y no se crearon
                # print(f"  [INFO] Archivo no encontrado/vacío: {nombre_archivo}")
                continue

            try:
                with h5py.File(GALAXY_FILE, 'r') as f_gal:
                    # Accedemos directamente a los datos
                    if 'data' in f_gal and 'bolometric_luminosity_agn' in f_gal['data']:
                        gal_lums = f_gal['data']['bolometric_luminosity_agn'][:]
                        
                        # Nos quedamos con TODAS las galaxias (centrales y satélites)
                        lums_validas = gal_lums[gal_lums > 0]
                        
                        if len(lums_validas) > 0:
                            # Transformación de unidades de Galform (log10 + 40)
                            log_L_bol = np.log10(lums_validas) + 40.0
                            
                            # Calculamos el histograma
                            counts, _ = np.histogram(log_L_bol, bins=bin_edges)
                            total_counts += counts
                            galaxias_totales_corte += len(lums_validas)
            except Exception as e:
                print(f"  [ERROR] Fallo al leer {nombre_archivo}: {e}")

        # Guardado de la LF específica de este corte
        if galaxias_totales_corte > 0:
            phi_total = total_counts / (bin_width * total_volume)
            archivo_salida = os.path.join(RESULTS_DIR, f"LF_Validacion_Corte{corte}.h5")
            
            with h5py.File(archivo_salida, 'w') as f:
                f.create_dataset('bin_edges', data=bin_edges)
                f.create_dataset('phi', data=phi_total)
                f.create_dataset('total_counts', data=total_counts)
            
            print(f"✅ Corte {corte} completado: {galaxias_totales_corte} galaxias.")
            print(f"💾 Guardado en: {archivo_salida}")
        else:
            print(f"⚠️ Corte {corte}: No se encontraron galaxias válidas.")

    print("\n¡PROCESO DE VALIDACIÓN COMPLETADO!")

if __name__ == "__main__":
     main()
