# NA project 1_2
# Auther: Helin Xu

import numpy as np
import math
import argparse
import random
import os

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


def point_cloud_sampling(sdf, N, epsilon=D/10, save_name='./point_cloud.ply', n=25):
    '''
    Input:
        - sdf: numpy array.
        - N: number of points to sample.
        - epsilon: threshold for sampling points that are within epsilone to surface.
        - save_name: name of the file. None for not saving.
        - n: number of points in each cube to sample.
    
    Output:
        - points_downsampled: list of N points
    '''
    def near_surface(x_idx, y_idx, z_idx):
        '''judge if point is near the surface.'''
        return abs(sdf[x_idx][y_idx][z_idx][3]) < D
    
    def down_sampling(points, N):
        '''down sampling point cloud to N points.'''
        assert len(points) > N, 'N is larger than number of points.'
        return random.sample(points, N)
   
    def sample_in_cube(x_idx, y_idx, z_idx, epsilon=epsilon, n=n):
        '''
        Do random sampling in selected cube. Return a list of points that are within epsilone to surface.
        '''
        point_in_cube = []
        for _ in range(n):
            x = random.uniform(x_idx * D - 3.06, x_idx * D - 2.94)
            y = random.uniform(y_idx * D - 3.06, y_idx * D - 2.94)
            z = random.uniform(z_idx * D - 3.06, z_idx * D - 2.94)
            if abs(trilinear_interpolate(sdf, x, y, z)) < epsilon:
                point_in_cube.append([x, y, z])
        return point_in_cube

    def save_point_cloud_to_ply(points, save_name=save_name):
        '''Save point cloud to ply file'''
        PLY_HEAD = f"ply\nformat ascii 1.0\nelement vertex {len(points)}\nproperty float x\nproperty float y\nproperty float z\nproperty uchar red\nproperty uchar green\nproperty uchar blue\nend_header\n"
        file_sting = PLY_HEAD
        for i in range(len(points)):
            file_sting += f'{points[i][0]} {points[i][1]} {points[i][2]} 255 0 0\n'
        f = open(save_name, 'w')
        f.write(file_sting)
        f.close()
        print(f'point cloud saved to {save_name}')
    
    points = []
    for x_idx in range(1, 100):
        for y_idx in range(1, 100):
            for z_idx in range(1, 100):
                if near_surface(x_idx, y_idx, z_idx):
                    points += sample_in_cube(x_idx, y_idx, z_idx)
    points_downsampled = down_sampling(points, N)
    if save_name != None:
        save_point_cloud_to_ply(points_downsampled)
    return points_downsampled


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', help='x coordinate to be interpolated', default=0, type=float)
    parser.add_argument('-y', help='y coordinate to be interpolated', default=0, type=float)
    parser.add_argument('-z', help='z coordinate to be interpolated', default=0, type=float)
    parser.add_argument('--save_name', help='name for saving the sampled pointcloud. e.g. point_cloud.ply\nDefault=None, do not save.', default=None)
    parser.add_argument('--save_path', help='where to save the sampled pointcloud. e.g. ./img', default='./img')
    parser.add_argument('-n', help='Number of points to be sampled', default=5000, type=int)
    opt = parser.parse_args()
    sdf = read_npy()

    # trilinear interpolation
    sdf_inter = trilinear_interpolate(sdf, opt.x, opt.y, opt.z) # enter a random coordinate!
    print(f'sdf value at ({opt.x}, {opt.y}, {opt.z}) is: ', sdf_inter)

    # point cloud sampling
    if opt.save_name != None:
        assert os.path.exists(opt.save_path)
        point_cloud_sampling(sdf=sdf, N=opt.n, save_name=os.path.join(opt.save_path, opt.save_name))