import h5py

archivo = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/Galaxias_Cortes/Galform/SU1/iz87/CortesPrueba/galaxias_Corte5_Galform_vol0.h5"

print(f"Abriendo: {archivo}\n")

with h5py.File(archivo, 'r') as f:
    for llave in f.keys():
        tipo = type(f[llave])
        print(f"▶️ Elemento: '{llave}'")
        
        # Si es un conjunto de datos, vemos cuántos hay
        if isinstance(f[llave], h5py.Dataset):
            print(f"   - Es una matriz de datos con tamaño: {f[llave].shape}")
            
        # Si es un grupo (como una subcarpeta), miramos qué hay dentro
        elif isinstance(f[llave], h5py.Group):
            print(f"   - Es un subgrupo que contiene: {list(f[llave].keys())}")
