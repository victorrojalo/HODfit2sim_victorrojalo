import h5py
import numpy as np
import os

# --- CONFIGURACIÓN ---
n_vols = 64
# Ruta del catálogo único de halos (Rockstar)
DATA_DIR_HALOS = "/home2/vgonzalez/Data/Rockstar/SU1/outp_87.list"

# Contadores globales
total_galaxias = 0
total_type0 = 0
total_idx_en_rockstar = 0
total_galidx_en_rockstar = 0

print(f"1. Cargando IDs del catálogo único de Rockstar...")
# Cargamos solo la columna 0 (ID) y saltamos la cabecera
# Rockstar suele usar '#' para comentarios, np.loadtxt lo ignora bien.
try:
    halo_ids_txt = np.loadtxt(DATA_DIR_HALOS, usecols=(0,), skiprows=1, comments='#')
    halo_ids_set = set(halo_ids_txt) # El SET es clave para que la búsqueda sea instantánea
    print(f"   Done! {len(halo_ids_set)} halos cargados en memoria.\n")
except Exception as e:
    print(f"Error cargando el archivo de halos: {e}")
    exit()

print(f"2. Iniciando el escaneo de {n_vols} volúmenes de galaxias...")

for i in range(n_vols):
    file_path = f"/home2/vgonzalez/Data/Galform/SU1/iz87/ivol{i}/gne_input.hdf5"

    if not os.path.exists(file_path):
        continue

    with h5py.File(file_path, 'r') as f:
        d = f['data']
        g_type = d['type'][:]
        id_halo_gal = d['id_halo'][:]    # Columna 'index'
        gal_idx_gal = d['gal_index'][:] # Columna 'gal_index'

        # Filtramos solo las centrales (Type 0)
        mask_type0 = (g_type == 0)
        idx_type0 = id_halo_gal[mask_type0]
        galidx_type0 = gal_idx_gal[mask_type0]

        # Comprobamos existencia en el set de Rockstar
        # Esto genera un array de True/False para cada galaxia central
        idx_exists = np.array([val in halo_ids_set for val in idx_type0])
        galidx_exists = np.array([val in halo_ids_set for val in galidx_type0])

        # Sumamos a los totales
        total_galaxias += len(g_type)
        total_type0 += len(idx_type0)
        total_idx_en_rockstar += np.sum(idx_exists)
        total_galidx_en_rockstar += np.sum(galidx_exists)

    if i % 10 == 0:
        print(f"   Procesado hasta ivol{i}...")

# --- RESULTADOS FINALES ---
print("\n" + "="*55)
print("RESUMEN DE VALIDACIÓN: Galaxias (HDF5) vs Rockstar (.list)")
print("="*55)
print(f"Total galaxias en los 64 volúmenes:   {total_galaxias}")
print(f"Total centrales (Type 0):             {total_type0}")
print("-" * 55)
print(f"Centrales con 'index' en Rockstar:     {total_idx_en_rockstar} / {total_type0}")
print(f"Centrales con 'gal_index' en Rockstar: {total_galidx_en_rockstar} / {total_type0}")

# Diagnóstico final
if total_idx_en_rockstar == total_type0:
    print("\n✅ CONCLUSIÓN: El campo 'index' mapea perfectamente con Rockstar.")
elif total_galidx_en_rockstar == total_type0:
    print("\n✅ CONCLUSIÓN: El campo 'gal_index' mapea perfectamente con Rockstar.")
else:
    print("\n❌ ALERTA: Ninguno de los dos campos coincide al 100% con Rockstar.")
