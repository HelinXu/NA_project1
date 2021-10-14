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
$ python 2_trilinear_interpolation.py -x -1.34 -y 0.4 -z 2.94 # trilinear interpolation at arbitrary point (x, y, z)
sdf value at (-1.34, 0.4, 2.94) is:  -2.0801144991718887
```