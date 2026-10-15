import os.path
import sys
import h5py
import numpy as np
import src.h2s_const as const

def get_mask(pid, rockstar_format=True):
    return (pid == -1)

def get_central(gal_host_id, gal_main_id, centralformats='sage'):
    if centralformats == 'sage':
        return (gal_host_id == gal_main_id)
    elif centralformats == 'galform':
        return (gal_main_id == 0)
    else:
        print(f'{centralformats} Central format not recognized')
        sys.exit()

def stop_if_no_file(infile):
    if (not os.path.isfile(infile)):
        print('STOP: no input file {}'.format(infile))
        sys.exit()

def check_file(infile, verbose=False):
    file_fine = os.path.isfile(infile)
    if (not file_fine) and verbose:
        print('WARNING (io.check_file): file not found {}'.format(infile))
    return file_fine

def create_dir(dirout):
    if not os.path.exists(dirout):
        try:
            os.makedirs(dirout)
        except:
            print('WARNING (h2s_io.create_dir): problem creating directory ', dirout)
            return False
    return True

def filter_log_flux(infile, fmin, outfile_name, output_format="h5", param_name="logFHalpha_att", verbose=True, testing=False, **kwargs):
    log_fmin = fmin 
    with h5py.File(infile, "r") as f:
        # SAGE logic: read from root
        p_name = param_name.replace("data/", "")
        if p_name not in f:
            raise KeyError(f"Column {p_name} not found in SAGE file.")

        flux_data = f[p_name][:]
        mask = flux_data >= log_fmin

        if testing:
            idx = np.where(mask)[0]
            if len(idx) > const.testlimit_galaxies:
                mask[idx[const.testlimit_galaxies:]] = False

        if verbose:
            print(f"SAGE Galaxies selected: {np.sum(mask)}")

        with h5py.File(outfile_name, "w") as fout:
            g_out = fout.create_group("data")
            for key in f.keys():
                if isinstance(f[key], h5py.Dataset):
                    g_out.create_dataset(key, data=f[key][mask])
    return outfile_name

def split_halo_catalog_by_mass(halo_file, mass_column=17, logmass=False, n_bins=70, min_logmass=10.5, max_logmass=14.5, output_h5="data/halo_mass_bins.h5", columns=None, testing=False, verbose=True):
    if columns is None:
        columns = {"id": 1, "X": 3, "Y": 4, "Z": 5, "vx": 6, "vy": 7, "vz": 8, "pid": 13, "Mass": 17}
    
    os.makedirs(os.path.dirname(output_h5), exist_ok=True)
    halos = np.loadtxt(halo_file, skiprows=1)
    halos = halos[~np.isnan(halos).any(axis=1)]

    if testing:
        halos = halos[:const.testlimit_halos]

    pids = halos[:, columns['pid']]
    mask_host = (pids == -1)
    halos = halos[mask_host]

    masses = halos[:, mass_column]
    valid_mass = masses > 0
    halos, masses = halos[valid_mass], masses[valid_mass]
    
    if not logmass:
        masses = np.log10(masses)

    bin_edges = np.linspace(min_logmass, max_logmass, n_bins + 1)

    with h5py.File(output_h5, "w") as h5f:
        for i in range(n_bins):
            lo, hi = bin_edges[i], bin_edges[i + 1]
            m_mask = (masses >= lo) & (masses < hi)
            h_bin = halos[m_mask]
            grp = h5f.create_group(f"bin_{i:02d}")
            for dset_name, col_idx in columns.items():
                d = h_bin[:, col_idx] if len(h_bin) > 0 else np.array([])
                grp.create_dataset(dset_name, data=d, dtype='f8')
    return bin_edges

def kaiser_factor(omega_m, b, gamma=0.55):
    growth_rate = omega_m**gamma
    ratio = growth_rate / b
    return 1 + (2/3) * ratio + (1/5) * ratio**2
