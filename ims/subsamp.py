# import matplotlib.pyplot as plt
# import numpy as np
# import os
# from PIL import Image
# import sys
# import matplotlib as mpl

# from skimage import exposure

# import numpy as np
# def histogram_equalize(img):
#     img_cdf, bin_centers = exposure.cumulative_distribution(img)
#     return np.interp(img, bin_centers, img_cdf)

# def tem_elemento_diferente_de_zero(imagem):
#     for matriz in imagem:
#         for linha in matriz:
#             for elemento in linha:
#                 if elemento != 0:
#                     return True
#     return False

# img = "acs_full.tiff" # sys.argv[1]

# #im1 = np.array(Image.open(img), dtype=int)
# #plt.imshow(im1,cmap="gray")
# #plt.show()

# #im1 = np.array(Image.open(img+"/ImageBand4.tif"), dtype=int)
# im1 = np.array(Image.open(img), dtype=int)

# # print(im1[0][:25])
# # print(os.path.getsize(img)-206)
# # print(os.path.getsize('im2.bin'))
# # print((os.path.getsize(img)-206-os.path.getsize('im2.bin'))/(4*4096))

# im1 = histogram_equalize(im1)
# im1 = im1[:2000]

# sz = np.shape(im1)
# # print(sz)

# # plt.figure()
# # plt.imshow(im1)

# im2 = im1[::20, ::20]
# # plt.figure()
# # plt.imshow(im2)

# mpl.image.imsave("acs_full_equal.tiff",im1)
# mpl.image.imsave("acs_half.tiff",im2)
# print(im1[:1][:1]*255)
# # plt.show()

# imm1 = np.array(Image.open("acs_full_equal.tiff"), dtype=int)

# print(imm1[:1][:1])

# im1 = np.floor(im1*255).astype(np.uint8)
# print(im1[:1][:1])
# mpl.image.imsave("acs_full_equal1.tiff",im1)
# imm2 = np.array(Image.open("acs_full_equal1.tiff"), dtype=int)
# print(np.all(imm1 == imm2))
# # print(os.path.getsize("acs_full_equal.tiff")-206)
# # print(os.path.getsize("acs_half.tiff"))

# # im1 = np.array(Image.open('acs_half.tiff'), dtype=int)
# # im2 = np.array(Image.open('im2.tiff'), dtype=int)
# # print("OK" if not tem_elemento_diferente_de_zero(im1 - im2) else "Deu ruim")






import numpy as np
from PIL import Image
import matplotlib.pyplot
import matplotlib as mpl
from skimage import exposure

def histogram_equalize(img):
    hist, bc = np.histogram(img, 255)
    img_cdf = hist.cumsum()
    img_cdf = img_cdf/ img_cdf[-1]
    bin_centers = [i for i in range(1,256)]
    u = np.interp(img, bin_centers, img_cdf)
    return u, img_cdf

imp = np.array(Image.open("acs_full.tiff"), dtype=int)

im1, cdf2 = histogram_equalize(imp)

# bins= [i for i in range(1,256)]
histo = np.array([0]*256)
for i in range(2000):
    for j in range(4096):
        for k in range(4):
           histo[imp[i][j][k]] += 1
           


cdf = histo.cumsum()
cdf = cdf/ cdf[-1]
cdf = (cdf[1:]*255).astype(np.uint8)

v = np.zeros_like(imp, dtype=float)

for i in range(2000): 
    for j in range(4096):
        for k in range(4):
           v[i][j][k] = cdf[imp[i][j][k]-1]
           if i < 2 and j < 2:
               print(v[i][j][k])


# print(v - im1)
# print(imp[0][0], v[0][0])
# print('\n')
# print(imp[0][0][0], imp[0][0][1], imp[0][0][2], imp[0][0][3])
# print('\n')
# print(cdf[imp[0][0][0]-1], cdf[imp[0][0][1]-1], cdf[imp[0][0][2]-1], cdf[imp[0][0][3]-1])
# # print(list(zip([i for i in range(1,256)], cdf)))