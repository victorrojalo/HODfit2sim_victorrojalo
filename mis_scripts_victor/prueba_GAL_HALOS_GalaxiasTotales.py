import h5py
import numpy as np
import os

# --- CONFIGURACIÓN ---
n_vols = 64
# El archivo maestro de halos (Rockstar)
DATA_DIR_HALOS = "/home2/vgonzalez/Data/Rockstar/SU1/outp_87.list"
HALO_ID_KEY = 0  # El ID está en la primera columna (Dataset 0 del TXT)

# Contadores globales para el reporte
total_galaxias = 0
total_type0 = 0
total_idhalo_en_rockstar = 0
total_galidx_en_rockstar = 0

print(f"1. Cargando IDs del catálogo maestro de Rockstar (Dataset {HALO_ID_KEY})...")
try:
    # Cargamos solo la columna 0 para que sea ultra rápido
    halos_maestros = np.loadtxt(DATA_DIR_HALOS, usecols=(HALO_ID_KEY,), skiprows=1, comments='#')
    # Convertimos a 'set' porque buscar un número en un set es instantáneo (O(1))
    halos_set = set(halos_maestros) #hace que busque conjunto de datos (asi es más rápido)
    print(f"   ¡Listo! {len(halos_set)} IDs de halos cargados.\n")
except Exception as e:
    print(f"Error al leer el archivo de halos: {e}")
    exit()

print(f"2. Escaneando {n_vols} volúmenes de galaxias (HDF5)...")

for i in range(n_vols):
    file_path = f"/home2/vgonzalez/Data/Shark/SU1/iz87/ivol{i}/gne_input.hdf5"

    if not os.path.exists(file_path):
        continue

    with h5py.File(file_path, 'r') as f:
        d = f['data']
        g_type = d['type'][:]
        # Aquí usamos los nombres que tú ya has modificado en tu archivo
        id_halo_gal = d['id_halo'][:]   
        gal_idx_gal = d['gal_index'][:]
        
        # Nos centramos en las centrales (Type 0), ya que si es una galaxia central si ID será el del halo obligatoriamente
        #mask_type0 = (g_type == 0)
        centrales_id_halo = id_halo_gal
        centrales_gal_index = gal_idx_gal

        # ¿Existen estos IDs en el set de Rockstar?
        # Comprobamos uno a uno de forma eficiente, ME DICE TRUE OR FALSE uno a uno
        idhalo_ok = np.array([val in halos_set for val in centrales_id_halo])
        galidx_ok = np.array([val in halos_set for val in centrales_gal_index])

        # Actualizamos estadísticas
        total_galaxias += len(g_type)
        total_type0 += len(centrales_id_halo)
        total_idhalo_en_rockstar += np.sum(idhalo_ok)
        total_galidx_en_rockstar += np.sum(galidx_ok)

    if i % 10 == 0:
        print(f"   Procesando volumen {i}...")

# --- REPORTE FINAL ---
print("\n" + "="*60)
print("REPORTE DE CONSISTENCIA: GALAXIAS H5 vs HALOS ROCKSTAR")
print("="*60)
print(f"Total galaxias (todos los volúmenes): {total_galaxias}")
print(f"Total centrales reales (Type 0):       {total_type0}")
print("-" * 60)
print(f"Centrales cuyo 'id_halo' ESTÁ en Rockstar:   {total_idhalo_en_rockstar} / {total_type0}")
print(f"Centrales cuyo 'gal_index' ESTÁ en Rockstar: {total_galidx_en_rockstar} / {total_type0}")
print("-" * 60)

# Veredicto
if total_idhalo_en_rockstar == total_type0:
    print("✅ VERDICTO: El campo 'id_halo' es 100% consistente con Rockstar.")
elif total_galidx_en_rockstar == total_type0:
    print("✅ VERDICTO: El campo 'gal_index' es 100% consistente con Rockstar.")
else:
    print("⚠️  ATENCIÓN: Algunos IDs no se encuentran en el catálogo de halos.")
    print("    Esto podría indicar que estás usando versiones distintas de los catálogos.")
