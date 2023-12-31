import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import sys
import matplotlib as mpl

from skimage import exposure

import numpy as np
def histogram_equalize(img):
    img_cdf, bin_centers = exposure.cumulative_distribution(img)
    return np.interp(img, bin_centers, img_cdf)

img = sys.argv[1]
# img = "ImageBand4.tif"

#im1 = np.array(Image.open(img), dtype=int)
#plt.imshow(im1,cmap="gray")
#plt.show()

#im1 = np.array(Image.open(img+"/ImageBand4.tif"), dtype=int)
im1 = np.array(Image.open(img), dtype=int)

im1 = im1[::20, ::20]
im2 = histogram_equalize(im1)
# im2 = im2[:2000]

sz = np.shape(im1)
print(sz)

plt.figure()
plt.imshow(im1)

plt.figure()
plt.imshow(im2)

mpl.image.imsave("half.tiff",im1)
mpl.image.imsave("equal.tiff",im2)

plt.show()
