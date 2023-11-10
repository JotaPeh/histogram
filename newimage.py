from PIL import Image
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib as mpl

def compare_images(image_path1, image_path2):
    img1 = Image.open(image_path1)
    img2 = Image.open(image_path2)

    # Verifica se as dimensões são iguais
    if img1.size != img2.size:
        return False

    # Compara os pixels
    pixel_data1 = list(img1.getdata())
    pixel_data2 = list(img2.getdata())

    return pixel_data1 == pixel_data2

# Dimensions
width = 4096
height = 2000
bytespp = 1

# Equal
data = (np.fromfile("acs_full_equal_C.bin", dtype=np.float32)).reshape((height, width))

mpl.image.imsave("acs_full_equal_C.tiff",data)
os.remove('acs_full_equal_C.bin')

# ACS half
data = (np.fromfile("acs_half_C.bin", dtype=np.float32)).reshape(int(height/20), int(width/20) + 1)

mpl.image.imsave("acs_half_C.tiff",data)
os.remove('acs_half_C.bin')

if compare_images('acs_full_equal_C.tiff', 'acs_full_equal.tiff'):
    print("1: As imagens são idênticas!")
else:
    print("1: As imagens são diferentes.")

if compare_images('acs_half_C.tiff', 'acs_half.tiff'):
    print("1: As imagens são idênticas!")
else:
    print("1: As imagens são diferentes.")