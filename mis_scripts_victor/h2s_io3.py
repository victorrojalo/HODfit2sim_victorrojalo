import os.path
import sys
import h5py
import numpy as np
import src.h2s_const as const

def get_mask(pid, rockstar_format=True):
    """
    Para Rockstar: -1 es Host, lo demás es subhalo.
    """
    return (pid == -1)

def get_central(gal_host_id, gal_main_id):
    """
    En SAGE: Si HostID == MainID, la galaxia es central.
    """
    return (gal_host_id == gal_main_id)

def stop_if_no_file(infile):
    if not os.path.isfile(infile):
        print(f'STOP: no hay archivo {infile}')
        sys.exit()

def check_file(infile, verbose=False):
    exists = os.path.isfile(infile)
    if not exists and verbose:
        print(f'WARNING: Archivo no encontrado {infile}')
    return exists

def create_dir(dirout):
    if not os.path.exists(dirout):
        os.makedirs(dirout, exist_ok=True)
    return True

def get_nheader(infile):
    ih = 0
    with open(infile, 'r') as ff:
        for line in ff:
            if not line.strip() or not line.strip()[0].isdigit() and line.strip()[0] != '-':
                ih += 1
            else:
                return ih
    return ih

def filter_log_flux(infile, fmin, outfile_name, output_format="h5", param_name="logFHalpha_att", verbose=True, testing=False, **kwargs):
    """
    FILTRO ESPECÍFICO PARA SAGE (Acepta argumentos extra para evitar TypeErrors).
    Lee archivos planos y guarda con grupo /data para el resto del pipeline.
    """
    # fmin ya debe ser logaritmo (ej: -15.87)
    log_fmin = fmin 

    with h5py.File(infile, "r") as f:
        # SAGE no tiene grupo 'data', leemos directo de la raíz
        # Si por casualidad param_name trae el prefijo 'data/', lo limpiamos
        p_name = param_name.replace("data/", "")
        
        if p_name not in f:
            raise KeyError(f"No encuentro la columna '{p_name}' en el archivo SAGE.")

        flux_array = f[p_name][:]
        mask = flux_array >= log_fmin

        if testing:
            idx = np.where(mask)[0]
            if len(idx) > const.testlimit_galaxies:
                mask[idx[const.testlimit_galaxies:]] = False

        n_selected = np.sum(mask)
        if verbose:
            print(f"SAGE Galaxies selected: {n_selected}")

        # Guardamos el archivo filtrado
        with h5py.File(outfile_name, "w") as fout:
            g_out = fout.create_group("data")
            for key in f.keys():
                if isinstance(f[key], h5py.Dataset):
                    g_out.create_dataset(key, data=f[key][mask])

    if verbose:
        print(f"Filtered SAGE data saved to {outfile_name}")
    return outfile_name

def split_halo_catalog_by_mass(halo_file, mass_column=17, logmass=False, n_bins=70, min_logmass=10.5, max_logmass=14.5, output_h5="halo_mass_bins.h5", columns=None, testing=False, verbose=True):
    """
    Procesa el TXT de halos de Rockstar.
    """
    if columns is None:
        columns = {"id": 1, "X": 3, "Y": 4, "Z": 5, "vx": 6, "vy": 7, "vz": 8, "pid": 13, "Mass": 17}
    
    halos = np.loadtxt(halo_file, skiprows=1)
    halos = halos[~np.isnan(halos).any(axis=1)]

    if testing:
        halos = halos[:const.testlimit_halos]

    # Quedarse solo con Host Halos (PID == -1)
    pids = halos[:, columns['pid']]
    mask_host = (pids == -1)
    halos = halos[mask_host]

    masses = halos[:, mass_column]
    if not logmass:
        masses = np.log10(masses)

    bin_edges = np.linspace(min_logmass, max_logmass, n_bins + 1)

    with h5py.File(output_h5, "w") as h5f:
        for i in range(n_bins):
            lo, hi = bin_edges[i], bin_edges[i + 1]
            m_mask = (masses >= lo) & (masses < hi)
            halos_bin = halos[m_mask]
            grp = h5f.create_group(f"bin_{i:02d}")
            for dset_name, col_idx in columns.items():
                d = halos_bin[:, col_idx] if len(halos_bin) > 0 else np.array([])
                grp.create_dataset(dset_name, data=d, dtype='f8')
            if verbose:
                print(f"Bin {i:02d}: {len(halos_bin)} halos.")

    return bin_edges

def kaiser_factor(omega_m, b, gamma=0.55):
    f = omega_m**gamma
    beta = f / b
    return 1 + (2/3) * beta + (1/5) * beta**2
