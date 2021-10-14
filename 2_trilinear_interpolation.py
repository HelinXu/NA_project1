# NA project 12
# Auther: Helin Xu

import numpy as np
import math
import argparse

D = 0.06 # division value of original sample

def read_npy():
    sdf = np.load('./sdf/sdf.npy')
    return sdf


def is_valid_point(x, y, z):
    '''Check if point coordinate is valid'''
    return (x >= -3 and x < 3) and (y >= -3 and y < 3) and (z >= -3 and z < 3)


def get_floor_index(x):
    '''
    round x to floor, with division value = D, x starting from -3.
    Output: index
    '''
    return math.floor((x + 3.) / D)


def l(x):
    '''
    input:
        x: coordinate
    output:
        distance between x and nearest lower sampling coordinate.
    '''
    return x - math.floor(x / D) * D


def u(x):
    '''
    input:
        x: coordinate
    output:
        distance between x and nearest upper sampling coordinate.
    '''
    return math.floor(x / D) * D + D - x


def trilinear_interpolate(sdf, x, y, z):
    '''
    Input:
        - sdf: numpy array.
        - x, y, z: coordinate to be interpolated.
    Output:
        - interpolated sdf value.
    '''
    assert is_valid_point(x, y, z), "Invalid interpolation point!"
    x_idx = get_floor_index(x)
    y_idx = get_floor_index(y)
    z_idx = get_floor_index(z)
    assert abs(sdf[x_idx][y_idx][z_idx][0] - math.floor((x) / D) * D) < 1e-6, 'Wrong index! Check again.'

    sdf_inter = (
        sdf[x_idx  ][y_idx  ][z_idx  ][3] * u(x) * u(y) * u(z) +
        sdf[x_idx  ][y_idx  ][z_idx+1][3] * u(x) * u(y) * l(z) +
        sdf[x_idx  ][y_idx+1][z_idx  ][3] * u(x) * l(y) * u(z) +
        sdf[x_idx  ][y_idx+1][z_idx+1][3] * u(x) * l(y) * l(z) +
        sdf[x_idx+1][y_idx  ][z_idx  ][3] * l(x) * u(y) * u(z) +
        sdf[x_idx+1][y_idx  ][z_idx+1][3] * l(x) * u(y) * l(z) +
        sdf[x_idx+1][y_idx+1][z_idx  ][3] * l(x) * l(y) * u(z) +
        sdf[x_idx+1][y_idx+1][z_idx+1][3] * l(x) * l(y) * l(z)
        ) / (D * D * D)
    
    return sdf_inter


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', help='x coordinate to be interpolated', default=0, type=float)
    parser.add_argument('-y', help='y coordinate to be interpolated', default=0, type=float)
    parser.add_argument('-z', help='z coordinate to be interpolated', default=0, type=float)
    opt = parser.parse_args()
    sdf = read_npy()
    sdf_inter = trilinear_interpolate(sdf, opt.x, opt.y, opt.z) # enter a random coordinate!
    print(f'sdf value at ({opt.x}, {opt.y}, {opt.z}) is: ', sdf_inter)