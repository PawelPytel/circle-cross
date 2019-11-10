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


def photo_div_ver(photo):
    for p in range(len(photo)):
        if 0 not in photo[p]:
            new_img1 = photo[:p, :]
            new_img2 = photo[p:, :]
            new_img1 = cut(new_img1, 'allp', 255)
            new_img2 = cut(new_img2, 'allp', 255)
            final_list.append(new_img1)
            photo_div_ver(new_img2)
            break
    else:
        final_list.append(photo)


def photo_div_hor(photo):
    iloczyn = 1
    for p in range(len(photo[0])):
        for q in range(len(photo)):
            iloczyn *= photo[q][p]
        if iloczyn != 0:
            new_img1 = photo[:, :p]
            new_img2 = photo[:, p:]
            new_img1 = cut(new_img1, 'allp', 255)
            new_img2 = cut(new_img2, 'allp', 255)
            final_list2.append(new_img1)
            photo_div_hor(new_img2)
            break
        iloczyn = 1
    else:
        final_list2.append(photo)


def split_photo(photo):
    result = rgb2gray(io.imread(photo)) ** 2
    result = mp.erosion(result)
    x = thresh(0.2, result)
    x = cut(x, 'allp', 255)
    photo_div_hor(x)
    for g in final_list2:
        photo_div_ver(g)


final_list = []
final_list2 = []
img = 'photo02.jpg'
split_photo(img)
print(len(final_list))
for a in final_list:
    io.imshow(a, cmap=plt.cm.gray)
    io.show()

