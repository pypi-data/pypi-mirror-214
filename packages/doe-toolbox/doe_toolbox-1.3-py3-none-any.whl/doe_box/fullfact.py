""" This module implements full factorial design-related functions.
"""

import numpy as np
from itertools import product

def fullfact(levels: list) -> np.array:
    """ Full factorial design of experiments
        It provides factor settings for a full factorial design with n = len(levels) factors, where the number of levels for 
        all factors is given by the vector levels of length n.

        Inputs:
            levels: Vector of the number of levels for each factor
        Outputs:
            outProd: Full factorial DoE matrix
    """

    arrays  = [np.linspace(-1, 1, level) for level in levels]
    outProd = list( product(*arrays) )
    outProd = np.array(outProd)
    return outProd


def ff2n(numFactors: int) -> np.array:
    """ Two-level full factorial design with <numFactors> factors. Convenience wrapper around fullfact().
        Inputs:
            numFactor: Number of factors in the DoE
        Outputs:
            DoE matrix
    """
    return fullfact(levels = [2] * numFactors).astype(int)

