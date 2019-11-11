from __future__ import division
import skimage
from skimage import io, filters
import skimage.morphology as mp
from skimage.color import rgb2gray
from matplotlib import pylab as plt, gridspec
import numpy as np
from ipykernel.pylab.backend_inline import flush_figures
import warnings


def thresh(t, photo):
    warnings.simplefilter("ignore")
    binary = (photo > t) * 255
    binary = np.uint8(binary)
    flush_figures()
    return binary


def cut(img, tag, color):
    if tag == 'allp':
        while all(img[0, :] == color):
            img = np.delete(img, 0, 0)
        while all(img[:, 0] == color):
            img = np.delete(img, 0, 1)
        while all(img[-1, :] == color):
            img = np.delete(img, -1, 0)
        while all(img[:, -1] == color):
            img = np.delete(img, -1, 1)
    elif tag == 'anyp':
        while any(img[0, :] == color):
            img = np.delete(img, 0, 0)
        while any(img[:, 0] == color):
            img = np.delete(img, 0, 1)
        while any(img[-1, :] == color):
            img = np.delete(img, -1, 0)
        while any(img[:, -1] == color):
            img = np.delete(img, -1, 1)
    return img


def photo_div(photo):
    for p in range(len(photo)):
        if 0 not in photo[p]:
            new_img1 = photo[:p, :]
            new_img2 = photo[p:, :]
            new_img1 = cut(new_img1, 'allp', 255)
            new_img2 = cut(new_img2, 'allp', 255)
            photo_div(new_img1)
            photo_div(new_img2)
            break
    else:
        iloczyn = 1
        for p in range(len(photo[0])):
            for q in range(len(photo)):
                iloczyn *= photo[q][p]
            if iloczyn != 0:
                photo1 = photo[:, :p]
                photo2 = photo[:, p:]
                photo1 = cut(photo1, 'allp', 255)
                photo2 = cut(photo2, 'allp', 255)
                photo_div(photo1)
                photo_div(photo2)
                break
            iloczyn = 1
        else:
            final_list.append(photo)


final_list = []
photo_div(x)
print(len(final_list))


for a in final_list:
    io.imshow(a, cmap=plt.cm.gray)
    io.show()
