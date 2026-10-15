#!/usr/bin/env python3
import h5py
import numpy as np

# 1. Pedir al usuario los datasets a comparar
# Se puede introducir como nombres separados por comas, ej: M_min,M_max,N_halo
datasets_input = input("Introduce los nombres de los datasets a comparar (separados por comas): ")
names = [name.strip() for name in datasets_input.split(",")]

# 2. Abrir los archivos HDF5
file1 = "output/h2s_output.h5"
file2 = "output-DatosBase/h2s_output.h5"

f1 = h5py.File(file1, "r")
f2 = h5py.File(file2, "r")

# 3. Recorrer los datasets seleccionados
for name in names:
        # 3a. Leer el dataset del primer archivo
        d1 = f1[f"data/{name}"][:]
        # 3b. Leer el dataset del segundo archivo
        d2 = f2[f"data/{name}"][:]

        # 3c. Calcular la diferencia absoluta
        diff = np.abs(d1 - d2)

        # 3d. Mostrar resultados
        print(f"\nDataset: {name}")
        print("  Máxima diferencia:", diff.max())
        print("  Número de valores distintos (>1e-6):", np.sum(diff > 1e-6))


# 4. Cerrar los archivos
f1.close()
f2.close()
                                        
