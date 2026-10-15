import os
import h5py

base_dir = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/Galaxias_Cortes/Shark/SU1/iz87/CortesMal"
cortes = [5, 6, 7, 8]
vol = 0

print("🕵️‍♀️ Investigando los archivos de la semana pasada en 'CortesMal'...")

for c in cortes:
    archivo = os.path.join(base_dir, f"galaxias_Corte{c}_Shark_vol{vol}.h5")
    if os.path.exists(archivo):
        try:
            with h5py.File(archivo, 'r') as f:
                n_gals = len(f['data/mvir_hosthalo'][:])
                print(f" -> Corte {c} (Volumen 0): {n_gals} galaxias.")
        except Exception as e:
            print(f" -> Error leyendo Corte {c}: {e}")
    else:
        print(f" -> ⚠️ No se encontró el archivo para el Corte {c}.")
