import h5py

cortes = [5, 6, 7, 8]
vol = 0
base_dir = "/home/tfm-violeta/Victor/HODfit2sim_victorrojalo/Galaxias_Cortes/Shark/SU1/iz87/CortesPrueba"

print("🔍 Comprobando número de galaxias en el Volumen 0...")

for c in cortes:
    archivo = f"{base_dir}/galaxias_Corte{c}_Shark_vol{vol}.h5"
    try:
        with h5py.File(archivo, 'r') as f:
            # Leemos cualquier columna para ver su longitud
            n_gals = len(f['data/mvir_hosthalo'][:])
            print(f"Corte {c} (L > 10^{f['data/bolometric_luminosity_agn'].name[-1]}... bueno, tu 'val'): {n_gals} galaxias.")
    except Exception as e:
        print(f"Error en Corte {c}: {e}")
