#python -m unittest tests/test_shuffle.py 
import shutil
import unittest
import tempfile, os
import numpy as np
import h5py
from numpy.testing import assert_allclose
import numpy as np
import h5py
import src.h2s_shuffle as shu
                                            


class test_h2s_shuffle(unittest.TestCase):
    def test_shuffle_galaxy_catalog_binned(self):
        galaxy_file='/home2/vgonzalez/Data/Galform/SU1/iz87/ivol0/gne_input.hdf5'
        halo_shuffled_file='dkaskjdpo'
        output_file='ksdjjposjo'
        shu.shuffle_galaxy_catalog_binned(galaxy_file, halo_shuffled_file, output_file)
        
       

if __name__ == "__main__":
    unittest.main()
                                                      
