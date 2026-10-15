import h5py
import numpy as np

archivo_original = "/home2/vgonzalez/Data/Shark/SU1/iz87/ivol0/gne_input.hdf5"
with h5py.File(archivo_original, 'r') as f:
    L_agn = f['data/bolometric_luminosity_agn'][:]
    print(f"Total galaxias en el archivo en bruto: {len(L_agn)}")
    print(f"Valor MÍNIMO en el array: {np.min(L_agn)}")
    print(f"Valor MÁXIMO en el array: {np.max(L_agn)}")
    print(f"Valor MEDIO en el array: {np.mean(L_agn)}")
