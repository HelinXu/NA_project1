# NA project 1_3
# Auther: Helin Xu

from trilinear_interpolation import point_cloud_sampling, read_npy, D
import argparse
from math import pow as pow
import numpy as np


def phi0_array(x, y, z):
    return np.power(x, 2) * np.power(z, 3)


def phi1_array(x, y, z):
    return np.power(y, 2) * np.power(z, 3)


def y_bar_array(x, y, z):
    return -np.power((2 * np.power(x, 2) + np.power(y, 2) + np.power(z, 2) - 1), 3)


def solve_least_square(x, y, z):
    y_bar = y_bar_array(x, y, z)
    phi0 = phi0_array(x, y, z)
    phi1 = phi1_array(x, y, z)

    a = np.inner(phi0, phi0)
    b = np.inner(phi0, phi1)
    c = np.inner(phi1, phi1)
    d = np.inner(phi0, y_bar)
    e = np.inner(phi1, y_bar)
    B = (b * d - e * a) / (b * b - a * c)
    A = (b * e - c * d) / (b * b - a * c)
    return A, B


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', help='Number of points to be sampled', default=5000, type=int)
    parser.add_argument('-e', help='epsilon', default=D/10, type=float)
    opt = parser.parse_args()

    # point cloud sampling
    points = point_cloud_sampling(sdf=read_npy(), N=opt.n, save_name=None, n=200)
    points = np.array(points).T

    a, b = solve_least_square(points[0], points[1], points[2])
    print(f'a = {a}, b = {b}')
    