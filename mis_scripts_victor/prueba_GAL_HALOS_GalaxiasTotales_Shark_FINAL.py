import h5py
import numpy as np
import os

DATA_DIR_HALOS = "/home2/vgonzalez/Data/Rockstar/SU1/outp_87.list"
HALO_ID_KEY = 0  # El ID está en la primera columna
n_vols = 64

print("1. Cargando IDs del catálogo maestro de Rockstar...")
try:
    halos_maestros = np.loadtxt(DATA_DIR_HALOS, usecols=(HALO_ID_KEY,), skiprows=1)
    
    # Aplicamos la magia: unique quita duplicados y ordena
    halos_unicos_rockstar = np.unique(halos_maestros)
    print(f"   ¡Listo! {len(halos_unicos_rockstar)} IDs únicos de Rockstar cargados.\n")
except Exception as e:
    print(f"Error al leer el archivo de halos: {e}")
    exit()

print(f"2. Extrayendo IDs de los {n_vols} volúmenes de galaxias...")
todos_id_halo_gal = []
todos_gal_index_gal = []

for i in range(n_vols):
    file_path = f"/home2/vgonzalez/Data/Shark/SU1/iz87/ivol{i}/gne_input.hdf5"
    if not os.path.exists(file_path):
        continue
        
    with h5py.File(file_path, 'r') as f:
        d = f['data']
        # Metemos todos los IDs en listas
        todos_id_halo_gal.append(d['id_halo'][:])
        todos_gal_index_gal.append(d['gal_index'][:])

    if i % 10 == 0:
        print(f"   Leído volumen {i}...")

# Unimos todas las cajitas en una sola lista gigante
id_halo_gal_total = np.concatenate(todos_id_halo_gal)
gal_index_gal_total = np.concatenate(todos_gal_index_gal)

print("\n3. Aplicando np.unique() sugerido por tu profesora...")
# Quitamos duplicados y ordenamos los IDs de las galaxias
id_halo_unicos_gal = np.unique(id_halo_gal_total)
gal_index_unicos_gal = np.unique(gal_index_gal_total)

print(f"   -> Encontramos {len(id_halo_gal_total)} galaxias en total.")
print(f"   -> Que habitan en {len(id_halo_unicos_gal)} halos únicos según 'id_halo'.")

print("\n4. Cruzando los datos para ver coincidencias exactas...")
# Comparamos listas limpias y ordenadas
idhalo_ok = np.isin(id_halo_unicos_gal, halos_unicos_rockstar)
galidx_ok = np.isin(gal_index_unicos_gal, halos_unicos_rockstar)

total_idhalo_en_rockstar = np.sum(idhalo_ok)
total_galidx_en_rockstar = np.sum(galidx_ok)

# --- REPORTE FINAL ---
print("\n" + "="*65)
print("REPORTE DE CONSISTENCIA: GALAXIAS H5 vs HALOS ROCKSTAR")
print("="*65)
print(f"Halos únicos usando 'id_halo':        {len(id_halo_unicos_gal)}")
print(f"De esos, ¿cuántos ESTÁN en Rockstar?: {total_idhalo_en_rockstar}")
print("-" * 65)
print(f"Halos únicos usando 'gal_index':      {len(gal_index_unicos_gal)}")
print(f"De esos, ¿cuántos ESTÁN en Rockstar?: {total_galidx_en_rockstar}")
print("="*65)

if total_idhalo_en_rockstar == len(id_halo_unicos_gal):
    print("✅ VERDICTO: ¡Éxito total! Todos los 'id_halo' están en Rockstar.")
else:
    print("⚠️ ATENCIÓN: Faltan IDs. Revisa las variablees.") 
