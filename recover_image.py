import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib as mpl

# Dimensions
width = 4096
height = 2000
bytespp = 1

# ACS half
data = (np.fromfile("half_C.bin", dtype=np.uint16)).reshape(int(height/20), int(width/20) + 1)

mpl.image.imsave("half_C.tiff",data)
os.remove('half_C.bin')

# Equal
data = (np.fromfile("equal_C.bin", dtype=np.float32)).reshape(int(height/20), int(width/20) + 1)

mpl.image.imsave("equal_C.tiff",data)
os.remove('equal_C.bin')