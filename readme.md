# NA project 1

Auther: Helin Xu (xhl19@mails.tsinghua.edu.cn)

## Installation

- python 3.7
- numpy
- opencv 3.4
- math

This repository should look like this:

```
.
├── bilinear_interpolation.py       # 01 bilinear interpolation
├── compute_a_b.sh                  # 03 for computing a and b
├── img                             # my outputs
│   ├── mesh_screen_shot.png        # 02 result: snapshot
│   ├── point_cloud_5000.ply        # 02 result: point cloud
│   ├── qr-code.png                 # 01 result: qr code
│   ├── qr-code_large.png           # 01 result: qr code, high resolution
│   ├── qr-polar.png
│   └── reconstructed_mesh.ply      # 02 result: reconstructed mesh
├── least_square.py                 # 03 least square
├── readme.md
├── sdf
│   ├── readme.md
│   └── sdf.npy
└── trilinear_interpolation.py      # 02 trilinear interpolation
```

## 01 bilinear interpolation

see bilinear_interpolation.py

usage:

```shell
$ python bilinear_interpolation.py
```

output png file is saved under `./img`.

## 02 trilinear interpolation

see trilinear_interpolation.py

first, download `sdf.npy` from qr-code.png and put it under `.sdf/`:

```
└── sdf
    ├── readme.md
    └── sdf.npy
```

usage:
```shell
usage: trilinear_interpolation.py [-h] [-x X] [-y Y] [-z Z]
                                    [--save_name SAVE_NAME]
                                    [--save_path SAVE_PATH] [-n N]

optional arguments:
  -h, --help            show this help message and exit
  -x X                  x coordinate to be interpolated
  -y Y                  y coordinate to be interpolated
  -z Z                  z coordinate to be interpolated
  --save_name SAVE_NAME
                        name for saving the sampled pointcloud. e.g.
                        point_cloud.ply Default=None, do not save.
  --save_path SAVE_PATH
                        where to save the sampled pointcloud. e.g. ./img
  -n N                  Number of points to be sampled
```

examples:

```shell
$ python trilinear_interpolation.py -x -1.34 -y 0.4 -z 2.94 # trilinear interpolation at arbitrary point (x, y, z)
sdf value at (-1.34, 0.4, 2.94) is:  -2.0801144991718887

$ python trilinear_interpolation.py --save_path img --save_name point_cloud_5000.ply -n 5000 # sample 5000 points and save point cloud to ./img/point_cloud_5000.ply
sdf value at (0, 0, 0) is:  0.6956263619461209
point cloud saved to img/point_cloud_5000.ply
```

## 03 least square

see least_square.py

usage: trilinear_interpolation

```shell
$ python least_square.py -h
usage: least_square.py [-h] [-n N] [-e E]

optional arguments:
  -h, --help  show this help message and exit
  -n N        Number of points to be sampled
  -e E        epsilon
```

You can directly run this command:

```shell
$ zsh compute_a_b.sh
a = -0.09247355384143766, b = -0.9969486721355191
```