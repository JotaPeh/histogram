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

# ACS half
data = (np.fromfile("half_C.bin", dtype=np.uint16)).reshape(int(height/20), int(width/20) + 1)

mpl.image.imsave("half_C.tiff",data)
os.remove('half_C.bin')

if compare_images('half_C.tiff', 'half.tiff'):
    print("Half:  As imagens são idênticas!")
else:
    print("Half:  As imagens são diferentes.")

# Equal
data = (np.fromfile("equal_C.bin", dtype=np.float32)).reshape(int(height/20), int(width/20) + 1)

mpl.image.imsave("equal_C.tiff",data)
os.remove('equal_C.bin')

if compare_images('equal_C.tiff', 'equal.tiff'):
    print("Equal: As imagens são idênticas!")
else:
    print("Equal: As imagens são diferentes.")