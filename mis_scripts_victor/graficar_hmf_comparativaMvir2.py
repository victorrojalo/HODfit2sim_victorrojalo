def leer_hmf(archivo):
    with h5py.File(archivo, 'r') as f:
        # 1. ¿Habla el "idioma" de Rockstar?
        if "bin_edges" in f and "total_counts" in f:
            edges = f["bin_edges"][:]
            # Como nos da los bordes, calculamos el punto medio exacto de la caja
            mass = (edges[:-1] + edges[1:]) / 2.0
            counts = f["total_counts"][:]
            
        # 2. ¿Habla el "idioma" de Shark/Galform (nuestro código)?
        elif "data/M_min_bin" in f:
            mass = f["data/M_min_bin"][:]
            # Buscamos las centrales (o los halos si no hay centrales)
            if "data/N_Cen" in f:
                counts = f["data/N_Cen"][:]
            elif "data/N_Halos" in f:
                counts = f["data/N_Halos"][:]
            else:
                counts = f["data"][list(f["data"].keys())[1]][:]
                
        else:
            raise ValueError(f"¡Estructura desconocida en el archivo {archivo}!")
            
    return mass, counts
