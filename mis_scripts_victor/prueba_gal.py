import h5py
import numpy as np

file_path = "/home2/vgonzalez/Data/Shark/SU1/iz87/ivol0/gne_input.hdf5"

with h5py.File(file_path, 'r') as f:
    d = f['data']
    g_type = d['type'][:]
    id_halo = d['id_halo'][:]
    gal_idx = d['gal_index'][:]

    # 1. ¿Cuántas son type 0?
    mask_type0 = (g_type == 0)
    
    # 2. ¿En cuántas coincide el ID del halo con el ID de la galaxia?
    mask_id_match = (id_halo == gal_idx)

    print(f"Total galaxias en vol0: {len(g_type)}")
    print(f"Galaxias con type == 0 (Centrales por etiqueta): {np.sum(mask_type0)}")
    print(f"Galaxias donde id_halo == gal_index (Centrales por ID): {np.sum(mask_id_match)}")
    
    # 3. La prueba de fuego: ¿Son las mismas?
    coincidencia_total = np.array_equal(mask_type0, mask_id_match)
    print(f"¿Coinciden ambos métodos al 100%?: {coincidencia_total}")

    if not coincidencia_total:
        # Ver si hay alguna type=0 que NO tenga IDs iguales
        fallos = np.sum(mask_type0 & ~mask_id_match)
        print(f"¡OJO! Hay {fallos} galaxias que son type=0 pero sus IDs NO coinciden.")
