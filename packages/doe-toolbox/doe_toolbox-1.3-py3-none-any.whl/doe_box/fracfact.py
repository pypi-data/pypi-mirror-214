"""
This module implements the fracfact function that generates fractional 
factorial designs.
"""

from .parser import parse
from .fullfact import fullfact
from typing import Tuple
import numpy as np
import re

def _getByName(name: str, list_: list) -> dict:
    """ Retrieves a dictionary with the factor's data given the factor's 
        name. 
        Inputs:
            name: String with the factor's name
            list_: List of dictionaries containing the data extracted
                   when the generator string was parsed (output of the 
                   parse() function)
        Outputs:
            d: Dictionary containing the parsed information for the given factor name
        NOTE: Raises KeyError if the factor is not found in the list
    """
    for d in list_:
        if d['name'].strip('-') == name:
            return d
    
    raise KeyError(f'Factor with name {name} does not exist.')


def _splitFactors(factors: list) -> Tuple[list, list]:
    """ Splits factor list in base and generated factors. 
        Inputs:
            factors: List of parsed factors (output of the parse function)
        Outputs:
            baseFactors: List of base factors
            genFactors : List containing the generated (non-base) factors
    """

    baseFactors, genFactors = [], []
    for f in factors:
        if f['isBase']: baseFactors.append(f)
        else:           genFactors.append(f)
    
    return baseFactors, genFactors


def _addBaseLevels(baseFactors: list) -> list:
    """ Generates the levels of the DoE matrix only for the base factors.
        Inputs:
            baseFactors: List of dictionaries containing the parsed data for the 
                         base factors (output of the parse function)
        Outputs:
            baseFactors: Input dictionary with the levels of the base factors (
                         numpy array of integer dtype) added as a new field, 
                         with key name: 'levels'
    """
    
    # Make a full factorial DoE matrix for the base factors.
    fullfactorial = fullfact(levels = [2] * len(baseFactors)).astype(int)

    # Loop over the base factors and add the corresponding levels from the yates matrix
    for idx, dict_ in enumerate(baseFactors):
        
        levels = fullfactorial[:, idx]        # Grab the column from the Yates matrix
        if '-' in dict_['name']: levels *= -1 # Flip sign if needed
        dict_['levels'] = levels              # Add yates column to dict

    return baseFactors


def _addGeneratedLevels(genFactors: list, baseFactors : list, numRuns: int) -> list:
    """ Generates the levels of the DoE matrix only for the generated factors. 
        Inputs:
            genFactors : List of dictionaries for the generated factors
            baseFactors: List of dictionaries for the base factors
            numRuns    : Number of runs of the fractional factorial design
        Outputs:
            genFactors: The corresponding input list of dictionaries with the
            levels of the generated factors (numpy array of integer dtype) added 
            as a new field, with key name: 'levels'

    """

    for gDict in genFactors:

        # Start with a column filled with 1s and iteratively 
        # multiply it with the Yates columns of the base factors  
        levels = np.ones(shape = numRuns, dtype = int) 

        for baseName in gDict['baseNames']:

            # Get the current base factor dictionary
            bDict = _getByName(baseName, baseFactors)

            # Multiply them with the current levels of the generated factor
            # while accounting for the base factor's sign.
            if '-' in bDict['name']: levels *= -bDict['levels']
            else                   : levels *= bDict['levels']

        # Flip sign if needed
        if '-' in gDict['name']: levels *= -1
        
        gDict['levels'] = levels

    return genFactors


def fracfact(gen: str) -> np.array:
    """ Creates the two-level fractional factorial design defined by the generator gen.
        Input: 
            gen: Generator string
        Output: 
            out: DoE matrix with dimensions: Number of samples (runs) x Number of factors
    """
    
    # Make base & generated factors from the generator string
    factors             = parse(gen)
    bFactors, gFactors  = _splitFactors(factors)
    bFactors            = _addBaseLevels(bFactors)
    numRuns, numFactors = 2 ** len(bFactors), len(bFactors) + len(gFactors)
    _addGeneratedLevels(gFactors, bFactors, numRuns)

    # Make output matrix with levels for each factor from the gen. string
    out = np.empty(shape = (numRuns, numFactors), dtype = int)
    for i, f in enumerate(factors): out[:, i] = f['levels']

    return out
