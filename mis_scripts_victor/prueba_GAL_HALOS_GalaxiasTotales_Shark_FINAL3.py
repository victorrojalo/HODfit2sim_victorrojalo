import h5py
import numpy as np
import os

DATA_DIR_HALOS = "/home2/vgonzalez/Data/Rockstar/SU1/outp_87.list"
HALO_ID_KEY = 0  
n_vols = 64

print("1. Cargando IDs de Rockstar...")
try:
    halos_maestros = np.loadtxt(DATA_DIR_HALOS, usecols=(HALO_ID_KEY,), skiprows=1)
    halos_unicos_rockstar = np.unique(halos_maestros)
    print(f"   ¡Listo! {len(halos_unicos_rockstar)} IDs de Rockstar cargados.\n")
except Exception as e:
    print(f"Error: {e}")
    exit()

print("2. Extrayendo IDs de los volúmenes de galaxias...")
todos_id_halo_gal = []

for i in range(n_vols):
    file_path = f"/home2/vgonzalez/Data/Shark/SU1/iz87/ivol{i}/gne_input.hdf5"
    if os.path.exists(file_path):
        with h5py.File(file_path, 'r') as f:
            todos_id_halo_gal.append(f['data']['id_halo'][:])

id_halo_gal_total = np.concatenate(todos_id_halo_gal)

print("3. Aplicando np.unique() (limpia duplicados y ORDENA)...")
# Al usar unique, esta lista ya queda perfectamente ordenada de menor a mayor
id_halo_unicos_gal = np.unique(id_halo_gal_total)
print(f"   -> Tenemos {len(id_halo_unicos_gal)} halos únicos en nuestro catálogo H5.")

print("\n4. Calculando la intersección matemática...")
# intersect1d saca los números en común, y también los devuelve ORDENADOS
coincidencias_idhalo = np.intersect1d(id_halo_unicos_gal, halos_unicos_rockstar)
print(f"   -> De ellos, {len(coincidencias_idhalo)} han hecho 'match' con Rockstar.")

print("\n" + "="*65)
print("VEREDICTO FINAL CON numpy.array_equal")
print("="*65)

# ¡AQUÍ ESTÁ LA MAGIA DE ARRAY_EQUAL!
# Comprobamos si la lista de nuestras galaxias es EXACTAMENTE IGUAL a la lista de coincidencias
es_consistente = np.array_equal(id_halo_unicos_gal, coincidencias_idhalo)

if es_consistente:
    print("✅ np.array_equal() devuelve TRUE.")
    print("   Significa que el 100% de los 'id_halo' están en Rockstar.")
    print("   (Las matrices coinciden término a término).")
else:
    print("⚠️ np.array_equal() devuelve FALSE.")
    print("   Hay IDs en las galaxias que NO existen en Rockstar.")
