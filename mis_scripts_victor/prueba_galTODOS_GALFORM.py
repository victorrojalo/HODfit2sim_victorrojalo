import h5py
import numpy as np
import os

# Definimos cuántos volúmenes hay (normalmente 64, del 0 al 63)
n_vols = 64

# Contadores globales para sumar lo de todos los volúmenes
total_galaxias = 0
total_type0 = 0
total_coincidencias = 0
total_fallos = 0

print(f"Iniciando el escaneo de {n_vols} volúmenes en iz87...\n")

for i in range(n_vols):
    # Construimos la ruta dinámica usando f-strings (cambiando ivol0 por ivol{i})
    file_path = f"/home2/vgonzalez/Data/Galform/SU1/iz87/ivol{i}/gne_input.hdf5"
    
    # Comprobamos que el archivo existe antes de abrirlo
    if not os.path.exists(file_path):
        print(f"[Aviso] El archivo no existe: {file_path}")
        continue
        
    with h5py.File(file_path, 'r') as f:
        d = f['data']
        g_type = d['type'][:]
        id_halo = d['index'][:]
        gal_idx = d['gal_index'][:]
        
        # 1. Máscaras
        mask_type0 = (g_type == 0)
        mask_id_match = (id_halo == gal_idx)
        
        # 2. Sumas locales (de este volumen)
        vol_galaxias = len(g_type)
        vol_type0 = np.sum(mask_type0)
        vol_match = np.sum(mask_id_match)
        vol_fallos = np.sum(mask_type0 & ~mask_id_match)
        
        # 3. Añadimos a los contadores globales
        total_galaxias += vol_galaxias
        total_type0 += vol_type0
        total_coincidencias += vol_match
        total_fallos += vol_fallos
        
        # (Opcional) Imprimir el progreso cada 10 volúmenes para ver que avanza
        if i % 10 == 0:
            print(f"Procesado hasta ivol{i}...")

# --- RESULTADOS FINALES ---
print("\n" + "="*40)
print("RESUMEN GLOBAL (Todos los volúmenes)")
print("="*40)
print(f"Total galaxias en la caja: {total_galaxias}")
print(f"Total galaxias type == 0 (Centrales reales): {total_type0}")
print(f"Total donde id_halo == gal_index: {total_coincidencias}")
print(f"Total FALLOS (type=0 pero IDs distintos): {total_fallos}")

coincidencia_total = (total_fallos == 0)
print(f"\n¿Coinciden ambos métodos al 100% en toda la caja?: {coincidencia_total}")
