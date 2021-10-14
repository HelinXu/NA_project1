# NA project 1_1
# Auther: Helin Xu

import cv2
import numpy as np
import math
from math import pi as PI


def read_img():
    img = cv2.imread('./img/qr-polar.png')
    return img


def bilinear_interpolate_v1(img, length):
    '''
    version 1
    length must be aligned to the original image.
    '''
    output_img = np.zeros((length, length, 3))
    for y in range(length):
        for x in range(length):
            _x = x * math.cos(y * 2 * PI / length) + length
            _y = -x * math.sin(y * 2 * PI / length) + length
            x1 = int(_x) # lower bound for float x
            y1 = int(_y) # lower bound for float y
            x2 = int(_x) + 1 # upper bound for float x
            y2 = int(_y) + 1 # upper bound for float y

            rgb11 = img[y1][x1]
            rgb12 = img[y1][x2]
            rgb21 = img[y2][x1]
            rgb22 = img[y2][x2]

            rgb = rgb11 * (x2 - _x) * (y2 - _y) +\
                  rgb12 * (x2 - _x) * (_y - y1) +\
                  rgb21 * (_x - x1) * (y2 - _y) +\
                  rgb22 * (_x - x1) * (_y - y1)

            output_img[y][x] = rgb

    return output_img


def bilinear_interpolate(img, N):
    '''
    version 2
    output lenght can be arbitrary number N.
    Input:
        - img: original image
        - N: output width & height
    Output:
        - output_img: numpy array (N*N*3)
    '''
    output_img = np.zeros((N, N, 3))
    length = img.shape[0]
    for x in range(N):
        x_norm = x / N * 2 * PI
        for y in range(N):
            y_norm = y / N * 2 * PI
            _x = length * (x_norm * math.cos(y_norm) + 2 * PI) / (4 * PI)
            _y = length * (-x_norm * math.sin(y_norm) + 2 * PI) / (4 * PI)
            x1 = int(_x) # lower bound for float x
            y1 = int(_y) # lower bound for float y
            x2 = int(_x) + 1 # upper bound for float x
            y2 = int(_y) + 1 # upper bound for float y

            rgb11 = img[y1][x1]
            rgb12 = img[y1][x2]
            rgb21 = img[y2][x1]
            rgb22 = img[y2][x2]

            rgb = rgb11 * (x2 - _x) * (y2 - _y) +\
                  rgb12 * (x2 - _x) * (_y - y1) +\
                  rgb21 * (_x - x1) * (y2 - _y) +\
                  rgb22 * (_x - x1) * (_y - y1)

            output_img[y][x] = rgb

    return output_img


if __name__ == '__main__':
    polar_img = read_img()
    output_img = bilinear_interpolate(polar_img, 200)
    cv2.imwrite('./img/qr-code.png', output_img)
