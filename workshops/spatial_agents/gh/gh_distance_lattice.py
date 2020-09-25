
__author__ = "shervinazadi"
__version__ = "2020.09.24"

import Rhino.Geometry as rg

values = []
for cell in lattice_cell_centroids:
    dist = cell.DistanceTo(interest_point)
    values.append(dist)

lattice_values = values
