from PIL import Image
import os

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
bytespp = 4

# Equal
with open('acs_full_equal_C.bin', 'rb') as file:
    data = file.read()

image = Image.frombytes('RGBA', (width, height), data)
image.save('acs_full_equal_C.tiff')
os.remove('acs_full_equal_C.bin')

# ACS half
with open('acs_half_C.bin', 'rb') as file:
    data = file.read()

image = Image.frombytes('RGBA', (int(width/20) + 1, int(height/20)), data)
image.save('acs_half_C.tiff')
os.remove('acs_half_C.bin')

if compare_images('acs_full_equal_C.tiff', 'acs_full_equal.tiff'):
    print("1: As imagens são idênticas!")
else:
    print("1: As imagens são diferentes.")

if compare_images('acs_half_C.tiff', 'acs_half.tiff'):
    print("1: As imagens são idênticas!")
else:
    print("1: As imagens são diferentes.")