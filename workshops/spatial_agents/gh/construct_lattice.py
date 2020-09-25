# -*- coding: utf-8 -*-
""" 
Python Script
Created on  Thursday September 2020 09:25:19 
@author:  shervinazadi 
"""

import numpy as np
import topogenesis as tg

lattices = []
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
