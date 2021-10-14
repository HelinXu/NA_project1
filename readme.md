# NA project 1

## 01 bilinear interpolation

see 1_bilinear_interpolation.py

usage:

```shell
$ python 1_bilinear_interpolation.py
```

output png file is saved under `./img`.

## 02 trilinear interpolation

see 2_trilinear_interpolation.py

first, download `sdf.npy` from qr-code.png and put it under `.sdf/`:

```
└── sdf
    ├── readme.md
    └── sdf.npy
```

usage:
```shell
usage: 2_trilinear_interpolation.py [-h] [-x X] [-y Y] [-z Z]
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
$ python 2_trilinear_interpolation.py -x -1.34 -y 0.4 -z 2.94 # trilinear interpolation at arbitrary point (x, y, z)
sdf value at (-1.34, 0.4, 2.94) is:  -2.0801144991718887

$ python 2_trilinear_interpolation.py --save_path img --save_name point_cloud_5000.ply -n 5000 # sample 5000 points and save point cloud to ./img/point_cloud_5000.ply
sdf value at (0, 0, 0) is:  0.6956263619461209
point cloud saved to img/point_cloud_5000.ply
```