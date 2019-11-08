import skimage as ski
from matplotlib import pyplot as plt
from skimage import data, io, filters, exposure
from skimage.color import rgb2hsv, hsv2rgb, rgb2gray
from skimage.feature import canny
import warnings
import skimage.morphology as mp
from skimage import measure
from skimage.transform import resize
import numpy as np

img = io.imread('images/img0.jpg')
result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
img = rgb2gray(img)
img **= 3
img[img >= 0.1] = 1
for i in range(10):
    img = mp.erosion(img)
img = (img == 1) * 255


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


img = cut(img, 'allp', 0)
img = cut(img, 'anyp', 0)
img = cut(img, 'allp', 255)

spots = []
spot2 = []
square_range = 40
for i in range(0, img.shape[0] - square_range):
    for j in range(0, img.shape[1] - square_range):
        square = np.array(img[i:i + square_range, j:j + square_range])
        if (square[0, 0] == 255
                and square[0, -1] == 255
                and square[-1, 0] == 255
                and square[-1, -1] == 255
                and not all(square[0, :] == 255)
                and not all(square[-1, :] == 255)
                and not all(square[:, 0] == 255)
                and not all(square[:, -1] == 255)):
            spots.append([i + square_range // 2, j + square_range // 2])

top_right = []
top_left = []
bottom_right = []
bottom_left = []

for i in spots:
    if i[0] < img.shape[0] // 2 and i[1] < img.shape[1] // 2:
        top_left = i
        break
for i in spots:
    if i[0] > img.shape[0] // 2 and i[1] < img.shape[1] // 2:
        bottom_left = i
        break
for i in spots:
    if i[0] < img.shape[0] // 2 and i[1] > img.shape[1] // 2:
        top_right = i
        break
for i in spots:
    if i[0] > img.shape[0] // 2 and i[1] > img.shape[1] // 2:
        bottom_right = i
        break
# spot_sums=[sum(i) for i in spots]
# min_sum=min(spot_sums)
# max_sum=max(spot_sums)
# for i,j in zip(spot_sums,spots):
#     if i ==  min_sum:
#         top_left=j
#     if i == max_sum:
#         top_right=j
# for i in spots:
#     for j in [-1,0,1]:
#         for k in [-1,0,1]:
#             if not (k==j and j==0):
#                 if i not in to_remove:
#                     if [i[0]+k, i[1] + j] in spots:
#                         #img[i[0]+k, i[1] + j] = 0
#                         to_remove.append([i[0]+k, i[1] + j])
# for i in to_remove:
#     try:
#         if i in spots:
#             spots.remove(i)
#     except ValueError:
#         print(i)
img = ski.segmentation.flood_fill(img, (top_right[0], top_right[1]), 125)
for i in range(0, img.shape[0] - square_range):
    for j in range(0, img.shape[1] - square_range):
        square = np.array(img[i:i + square_range, j:j + square_range])
        if (square[0, 0] == 0
                and square[0, -1] == 0
                and square[-1, 0] == 0
                and square[-1, -1] == 0
                and not all(square[0, :] == 0)
                and not all(square[-1, :] == 0)
                and not all(square[:, 0] == 0)
                and not all(square[:, -1] == 0)):
            spot2.append([i + square_range // 2, j + square_range // 2])
for i in spot2:
    img[i[0], i[1]] = 50
print(top_left,top_right)
print(bottom_left,bottom_right)
print((img[:top_left[0], :top_left[1]]==50).all())
if (img[ 0:top_left[0],0:top_left[1]] == 50).any():
    result[0][0] = 'X'
elif (img[0:top_left[0], 0:top_left[1]] == 0).any():
    result[0][0] = 'O'
else:
    result[0][0] = ' '
if (img[ 0:min(top_left[0], top_right[0]),top_left[1]:top_right[1]] == 50).any():
    result[0][1] = 'X'
elif (img[ 0:min(top_left[0], top_right[0]),top_left[1]:top_right[1]] == 0).any():
    result[0][1] = 'O'
else:
    result[0][1] = ' '
if (img[ :top_right[0],top_right[1]:] == 50).any():
    result[0][2] = 'X'
elif (img[ :top_right[0],top_right[1]:] == 0).any():
    result[0][2] = 'O'
else:
    result[0][2] = ' '
if (img[ top_left[0]:bottom_left[0],0:top_left[1]] == 50).any():
    result[1][0] = 'X'
elif (img[ top_left[0]:bottom_left[0],0:top_left[1]] == 0).any():
    result[1][0] = 'O'
else:
    result[1][0] = ' '
if ((img[max(top_left[0], top_right[0]):min(bottom_left[0], bottom_right[0]),
     max(top_left[1], bottom_left[1]):min(top_right[1], bottom_right[1])] == 50).any()):
    result[1][1] = 'X'
elif ((img[max(top_left[0], top_right[0]):min(bottom_left[0], bottom_right[0]),
     max(top_left[1], bottom_left[1]):min(top_right[1], bottom_right[1])] == 0).any()):
    result[1][1] = 'O'
else:
    result[1][1] = ' '
if (img[ top_right[0]:bottom_right[0],max(bottom_right[1],top_right[1]):] == 50).any():
    result[1][2] = 'X'
elif (img[ top_right[0]:bottom_right[0],max(bottom_right[1],top_right[1]):] == 0).any():
    result[1][2] = 'O'
else:
    result[1][2] = ' '
if (img[ bottom_left[0]:,0:bottom_left[1]] == 50).any():
    result[2][0] = 'X'
elif (img[ bottom_left[0]:,0:bottom_left[1]] == 0).any():
    result[2][0] = 'O'
else:
    result[2][0] = ' '
if (img[max(bottom_left[0],bottom_right[0]):, bottom_left[1]:bottom_right[1]] == 50).any():
    result[2][1] = 'X'
elif (img[max(bottom_left[0],bottom_right[0]):, bottom_left[1]:bottom_right[1]] == 0).any():
    result[2][1] = 'O'
else:
    result[2][1] = ' '
if (img[ bottom_right[0]:,bottom_right[1]:] == 50).any():
    result[2][2] = 'X'
elif (img[ bottom_right[0]:,bottom_right[1]:] == 0).any():
    result[2][2] = 'O'
else:
    result[2][2] = ' '
for i in result:
    print(''.join(i))
plt.grid(True)
io.imshow(img, cmap=plt.cm.gray)
io.show()
