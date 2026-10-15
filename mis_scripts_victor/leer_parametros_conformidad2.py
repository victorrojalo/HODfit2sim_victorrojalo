import h5py
import numpy as np
import os

RESULTS_DIR = "output"

k1_lista = []
k2_lista = []

print("Extrayendo parámetros de Conformidad de los 64 volúmenes...")

for i in range(64):
    archivo = os.path.join(RESULTS_DIR, f"conformity_vol{i}.h5")
    
    if os.path.exists(archivo):
        try:
            with h5py.File(archivo, 'r') as f:
                # Vamos directos a la ruta que hemos descubierto
                if "data/global/k1_global" in f:
                    k1 = f["data/global/k1_global"][()]
                    k2 = f["data/global/k2_global"][()]
                    
                    # np.atleast_1d nos asegura de que si es un número suelto o una lista [numero], 
                    # siempre coja el número limpio para hacer la media bien.
                    k1_lista.append(float(np.atleast_1d(k1)[0]))
                    k2_lista.append(float(np.atleast_1d(k2)[0]))
        except Exception as e:
            print(f" [!] Error leyendo el volumen {i}: {e}")

# Convertimos a matrices y calculamos la media y el error
k1_lista = np.array(k1_lista)
k2_lista = np.array(k2_lista)

n_validos = len(k1_lista)

if n_validos > 0:
    k1_media = np.mean(k1_lista)
    k1_error = np.std(k1_lista) / np.sqrt(n_validos)
    
    k2_media = np.mean(k2_lista)
    k2_error = np.std(k2_lista) / np.sqrt(n_validos)
    
    print("\n" + "="*50)
    print(f"📊 RESULTADOS GLOBALES (Promedio de {n_validos} volúmenes)")
    print("="*50)
    print(f"Parámetro k1_global (Media ± Error): {k1_media:.4f} ± {k1_error:.4f}")
    print(f"Parámetro k2_global (Media ± Error): {k2_media:.4f} ± {k2_error:.4f}")
    print("="*50)
else:
    print("No se encontraron datos de k1 y k2.")
