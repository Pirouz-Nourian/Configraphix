# -*- coding: utf-8 -*-
""" 
Python Script
Created on  Thursday September 2020 09:25:19 
@author:  shervinazadi 
"""

import numpy as np
import topogenesis as tg

lattices = []
# normalization loop
for values in lattice_values:
    # convert to numpy array
    a_values = np.array(values)

    # normalization of values
    max_values = np.max(a_values)
    min_values = np.min(a_values)
    normalized_values = (a_values - min_values) / (max_values - min_values)

    # convert to lattice
    norm_shaped_values = normalized_values.reshape(lattice_shape)
    lattice = tg.to_lattice(norm_shaped_values, np.array([0, 0, 0]))

    lattices.append(lattice)

# normalize weights
weights = np.array(lattice_weights)
weights /= np.sum(weights)
'''
 The aggregation algorithm is based on Fuzzy Logics framework that is introduced, and generalized in Pirouz Nourian dissertation: section 5.7.3, pp. 201-208, eq. 57
you can refer to it like this:

P. Nourian, “Configraphics: Graph Theoretical Methods for Design and Analysis of Spatial Configurations,” Doi.Org, vol. 6, no. 14. pp. 1–348, 2016, url. ISBN-13 15) 978-94-6186-720-9

'''
# initialize the aggregated lattice
agg_lattice = lattices[0] * 0 + 1
# aggregation loop
for lat, w in zip(lattices, weights.tolist()):
    agg_lattice *= np.power(lat, w)

lattice_values = agg_lattice.flatten().tolist()
