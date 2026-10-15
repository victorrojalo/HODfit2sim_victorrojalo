import os.path
import sys
import h5py

class nf(float):
    '''
    Define a class that forces representation of float to look a certain way
    This removes trailing zero so '1.0' becomes '1'
    '''
    def __repr__(self):
        str = '%.1f' % (self.__float__(),)
        if str[-1] == '0':
            return '%.0f' % self.__float__() 
        else:
            return '%.1f' % self.__float__()
    

def stop_if_no_file(infile):
    '''
    Stop if the file does not exist
    '''
    if (not os.path.isfile(infile)):
        print('STOP: no input file {}'.format(infile)) 
        sys.exit()
    return


def check_file(infile,verbose=False):
    '''
    Return True if the file exists
    '''
    file_fine = True  
    if (not os.path.isfile(infile)):
        file_fine = False
        if verbose:
            print('WARNING (io.check_file): file not found {}'.format(infile))

    return file_fine


def create_dir(outdir):
    '''
    Return True if directory already exists or it has been created
    '''
    if not os.path.exists(outdir):
        try:
            os.makedirs(outdir)
        except:
            print('WARNING (iotools.create_dir): problem creating directory ',outdir)
            return False
    return True


def is_sorted(a):
    '''
    Return True if the array is sorted
    '''
    for i in range(len(a)-1): 
        if a[i+1] < a[i] : 
            return False
    return True


def print_h5attr(infile,inhead='Header'):
    """
    Print out the group attributes of a hdf5 file

    Parameters
    ----------
    infile : string
      Name of input file (this should be a hdf5 file)
    inhead : string
      Name of the group to read the attributes from

    Example
    -------
    >>> import iotools as io
    >>> infile = '/hpcdata0/simulations/BAHAMAS/AGN_TUNED_nu0_L100N256_WMAP9/Data/Snapshots/snapshot_026/snap_026.27.hdf5'
    >>> io.print_header5(infile)
    """

    filefine = check_file(infile) #print(filefine)
    if (not filefine):
        print('WARNING (iotools.printh5attr): Check that the file provided is correct')
        return ' '
    
    f = h5py.File(infile, 'r')
    header = f[inhead]
    for hitem in list(header.attrs.items()): 
        print(hitem)
    f.close()

    return ' '


def print_info_h5dataset(name, obj):
   if isinstance(obj, h5py.Dataset):
       print(f"\nDataset: {name}")
       print(f"  Shape: {obj.shape}")
       print(f"  Dtype: {obj.dtype}")
       
       # Print attributes if any
       if obj.attrs:
           print("  Attributes:")
           for attr_name, attr_value in obj.attrs.items():
               print(f"    {attr_name}: {attr_value}")
       
       # Print min/max if dataset contains numeric data
       try:
           if obj.size > 0:  # Check if dataset is not empty
               data = obj[()]
               if data.dtype.kind in 'biufc':  # numeric types
                   print(f"  Min value: {data.min()}")
                   print(f"  Max value: {data.max()}")
           else:
               print("  Dataset is empty")
       except Exception as e:
           print(f"  Could not compute min/max: {e}")

           
def explore_h5group(grp, prefix=""):
    """Recursively explore groups and datasets"""
    for key in grp.keys():
        item = grp[key]
        full_path = f"{prefix}/{key}" if prefix else key
        
        if isinstance(item, h5py.Group):
            print(f"\nGroup: {full_path}")
            if item.attrs:
                print("  Attributes:")
                for attr_name, attr_value in item.attrs.items():
                    print(f"    {attr_name}: {attr_value}")
            explore_h5group(item, full_path)
        elif isinstance(item, h5py.Dataset):
            print_info_h5dataset(full_path, item)

            
def explore_h5file(infile,group=None,dataset=None):
    """
    Print out the minimum and maximum of each data set
    in an hdf5 file

    Parameters
    ----------
    infile : string
      Name of input file (this should be a hdf5 file)
    group : string
      Name of the group to explore, if any
    dataset : string
      Name of the specific dataset to explore

    Example
    -------
    >>> import iotools as io
    >>> infile = 'ex.hdf5'
    >>> io.explore_h5file(infile,group='data',dataset='index')   
    """

    filefine = check_file(infile) ; print(filefine)
    if (not filefine):
        print('WARNING (iotools.explore_h5file): Check that the file provided is correct')
        return ' '

    f = h5py.File(infile, 'r')
    if dataset:
        if group:
            path = f"{group}/{dataset}"
        else:
            path = dataset
        
        try:
            obj = f[path]
            print(f"\nExploring dataset: {path}")
            print_info_h5dataset(path, obj)
        except KeyError:
            print(f"WARNING: Dataset '{path}' not found in file")
            print("Available items in file:")
            f.visit(lambda name: print(f"  {name}"))
    elif group:
        try:
            grp = f[group]
            print(f"\nExploring group: {group}")
            if grp.attrs:
                print("  Attributes:")
                for attr_name, attr_value in grp.attrs.items():
                    print(f"    {attr_name}: {attr_value}")
            explore_h5group(grp, group)
        except KeyError:
            print(f"WARNING: Group '{group}' not found in file")
            print("Available items in file:")
            f.visit(lambda name: print(f"  {name}"))
    else:
        print(f"\nExploring file: {infile}")
        # Print file-level attributes if any
        if f.attrs:
            print("\nFile attributes:")
            for attr_name, attr_value in f.attrs.items():
                print(f"  {attr_name}: {attr_value}")
        
        # Explore all groups and datasets
        explore_h5group(f)
          
    f.close()
    return 


def count_symbol(infile,sym):
    fileok = check_file(infile)
    if fileok:
        total = 0
        with  open(infile, "r") as f:
            count = sum(line.count(sym) for line in f)
            total += count
        print('There are {} {} in {}'.format(count,sym,infile))
    else:
        print('File {} not found'.format(infile))
    return ' '


if __name__== "__main__":
    infile = 'blu'
    outdir = 'remove_dir/blu'
    #print(nf('4.0'))
    #print(is_sorted([1,3,6]))
    #print(is_sorted([1,9,6]))
    #print(stop_if_no_file(infile))
    #print('Create dir {}: {}'.format(outdir,create_dir(outdir)))
    #print('Check file {}: {}'.format(infile,check_file(infile)))
    
    # Below: useful to find postion in author list
    #print(count_symbol('/home/violeta/Downloads/blu',';'))

    # Below: useful to explore quantities in hdf5 file
    infile = '/data2/users/olivia/shark_output/SU1_UNIT_250/N2048_L250_fid_np_corrected/87/22/galaxies.hdf5'
    print(explore_h5file(infile,group='galaxies',dataset='id_subhalo'))

