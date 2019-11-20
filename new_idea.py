import skimage as ski
from matplotlib import pyplot as plt
from skimage import data, io, filters, exposure
from skimage.color import rgb2hsv, hsv2rgb, rgb2gray
import skimage.morphology as mp
from skimage.transform import resize
from skimage.segmentation import flood_fill
import numpy as np
import photo_spliting as ps
import math
import warnings
import circle_cross as cc
from numpy import *
def perp( a ) :
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# return
def seg_intersect(a1,a2, b1,b2) :
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = dot( dap, db)
    num = dot( dap, dp )
    return (num / denom.astype(float))*db + b1
top_right = []
top_left = []
bottom_right = []
bottom_left = []
images = []
result = []
img = cc.load_file('images/photo01.jpg')
img = cc.black_white(img)
img = cc.cut_min(img)
images = ps.photo_division(img)
top=()
left=()
right=()
bottom=()

i=images[0]
i = cc.rotate(i)
contours = ski.measure.find_contours(i, 0.5)


color=20
# for contour in contours:
#     for j in contour:
#         i[int(round(j[0])),int(round(j[1]))]=color
#
#     color+=10
#def find_board2(i):
corners = ski.transform.probabilistic_hough_line(i,line_length=int(2/3*min(i.shape[0],i.shape[1])),line_gap=1)
done=False
while not done:
    try:
        for line in corners:
            if abs(line[0][0]-line[1][0])<i.shape[1]//3 and line[0][0]<i.shape[1]//2:
                left=np.float32(np.array((line)))

                break
        for line in corners:
            if abs(line[0][0]-line[1][0])<i.shape[1]//3 and line[0][0]>i.shape[1]//2:
                right=np.float32(np.array((line)))

                break

        for line in corners:
            if abs(line[0][1]-line[1][1])<i.shape[0]//3 and line[0][0]<i.shape[0]//2:
                top=np.float32(np.array((line)))

                break
        for line in corners:
            if abs(line[0][1]-line[1][1])<i.shape[0]//3 and line[0][0]>i.shape[0]//2:
                bottom=np.float32(np.array((line)))

                break
        done=True
    except IndexError:
        done=False
top_left=np.uint16(seg_intersect(left[0],left[1],top[0],top[1]))
bottom_left=np.uint16(seg_intersect(left[0],left[1],bottom[0],bottom[1]))
top_right=np.uint16(seg_intersect(right[0],right[1],top[0],top[1]))
bottom_right=np.uint16(seg_intersect(right[0],right[1],bottom[0],bottom[1]))
for j in range(top_left[0]-i.shape[1]//12,top_left[0]+i.shape[1]//12):
    for k in range(i.shape[0]):
        i[k][j]=0
for j in range(top_right[0]-i.shape[1]//12,top_right[0]+i.shape[1]//12):
    for k in range(i.shape[0]):
        i[k][j]=0
for j in range(top_left[1]-i.shape[0]//12,top_left[1]+i.shape[0]//12):
    for k in range(i.shape[1]):
        i[j][k]=0
for j in range(bottom_right[1]-i.shape[0]//12,bottom_right[1]+i.shape[0]//12):
    for k in range(i.shape[1]):
        i[j][k ]= 0
# i[top_left[1],top_left[0]]=125
# i[top_right[1],top_right[0]]=125
# i[bottom_right[1],bottom_right[0]]=125
# i[bottom_left[1],bottom_left[0]]=125
# i=cc.fill_board(i,top_right,0)

# for j in range(5):
#     i=mp.dilation(i)
ax = cc.show_img(i)
plt.show()

