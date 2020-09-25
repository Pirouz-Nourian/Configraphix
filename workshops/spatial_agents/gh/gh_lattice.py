__author__ = "shervinazadi"
__version__ = "2020.09.24"

import Rhino.Geometry as rg

centroids = []
indices = []
for zi in range(z+1):
    for yi in range(y+1):
        for xi in range(x+1):
            point = rg.Point3d(xi*x_unit, yi*y_unit, zi*z_unit)
            centroids.append(point)
            indices.append((xi, yi, zi))


lattice_unit = (x_unit, y_unit, z_unit)
lattice_shape = (x+1, y+1, z+1)
lattice_bounds = [(0, 0, 0), (x, y, z)]
lattice_cell_indices = indices
lattice_cell_centroids = centroids
