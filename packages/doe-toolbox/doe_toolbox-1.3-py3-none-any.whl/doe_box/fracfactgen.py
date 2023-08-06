""" This module implements the fracfactgen function that makes appropriate
    generator strings for fractional factorial designs.
"""

from .parser import parse
import numpy as np
from itertools import combinations
from typing import Tuple
import warnings

def _makeInelligible(terms: list) -> list:
    """ Generates the ineligible effects set from the factors in the requirements set. 
        Inputs:
            terms: List containing the names of the factors in the DoE
        Outputs:
            Inelligible effects set

    """

    interactions = [_getInteraction(t1, t2) for t1, t2 in combinations(terms, 2)]
    iEffects     = terms + interactions

    return sorted(set(iEffects))


def _getInteraction(t1: str, t2: str) -> str: 
    """ Computes the generalised interaction between the two terms. 
        Inputs:
            t1: First term
            t2: Second term
        Outputs:
            Generalised interaction of the two terms
        Example: t1 = 'abc', t2 = 'bce' -> 'ae'
    """

    if t1 == t2: return '1' # Mean effect
    
    # Grab unique elements from the two terms
    l = set(t1).symmetric_difference(set(t2))

    # Sort and join
    return "".join(sorted(l))


def _getMinSampleSize(terms: list, resolution: int) -> int:
    """ Computes the minimum required sample size for the 
        given term list and resolution number (Step 2).
        Inputs:
            terms     : List of factor names
            resolution: Resolution of the design
        Outputs:
            Minimum required sample size to achieve the needed resolution.
    """

    # Get highest interaction number in the requirements set
    termSize = [len(e) for e in terms]
    minSize  = max(np.ceil( np.log2(len(terms) + 1) ), max(termSize)) # Valid for a resolution 3 design
    n        = _getNumBase(terms)

    # For resolution 5 find all terms up to 2-factor interactions
    if resolution >= 5:   minSize = max(np.ceil(np.log2(1 + n + n * (n - 1) / 2)), minSize)

    # For resolution 4, the number of terms should at least equal to a resolution 3 design
    elif resolution == 4: minSize = max(np.ceil(np.log2(2 * n)), minSize)

    return minSize.astype(int)


def _getNumBase(terms: list) -> int:
    """ Returns the number of base factors in the model. 
        Inputs:
            terms: List of factor names in the design
        Outputs:
            Number of base factors in the terms list
    """
    return sum([len(t) == 1 for t in terms])


def _getBase(terms: list) -> list:
    """ Returns base factors in the model. 
        Inputs:
            terms: List of factor names in the design
        Outputs:
            Base factors in the terms list
    
    """
    return [t for t in terms if len(t) == 1]


def _makeSampleSize(terms: list, resolution: int) -> np.array:
    """ Computes the sample size (number of runs) required for the design, given
        a list of factors, and the required resolution.

        Inputs:
            terms     : List of factor names in the design
            resolution: Required resolution of the design
        Outputs:
            sampleSizeVec: Vector of sample sizes

        NOTE: Raises ValueError for invalid specified sample sizes, or invalid resolution.

    """
    
    numFactors    = _getNumBase(terms)
    minSampleSize = _getMinSampleSize(terms, resolution)
    sampleSizeVec = np.arange(minSampleSize, numFactors)

    # Check if a valid sample size vector has been obtained.
    if sampleSizeVec.size == 0:
        msg = f'Resolution must be an integer lower than {resolution}.'
        raise ValueError(msg);

    return sampleSizeVec


def _makeBasicTerms(terms: list, base: list, sampleSize: int) -> list:
    """ Selects the basic factors of the model from the list of terms. 
        Inputs:
            terms: List of factor names in the design
            base : List of base factors in the design
            sampleSize: Number of runs for the design
        Outputs:
            List of basic factors for the design
    """

    # Get the term with the highest level of interaction (i.e. highest character count)
    termSize = [len(t) for t in terms]
    maxInter = terms[np.argmax(termSize)]

    # Make base terms
    idx, n = 0, len(base)
    basic  = list(maxInter)

    while len(basic) < sampleSize and idx < (n - 1):
        b = base[idx]
        if b not in basic: basic.append(b)
        idx +=1

    return sorted(basic)


def _makeAddedTerms(base: list, basic: list) -> list:
    """ Returns the added factors of the model given its base and basic terms. 
        Inputs:
            terms: List of factor names in the design
            base : List of base factors in the design
            sampleSize: Number of runs for the design
        Outputs:
            List of basic factors for the design
    """

    added = list(set(base).difference(set(basic)))
    return sorted(added)


def _makeBasicEffectsGroup(terms: list, basic: list, resolution: int) -> list:
    """ Generates the basic effects of the model, i.e. all combinations of the basic 
        terms according to the given resolution and the model.
        Inputs:
            terms     : List of factor names of the design
            basic     : List of basic factors in the design
            resolution: Required resolution of the design
        Outputs:
            basicEffects: Basig effects group
    """

    basicEffects = []
    for term in basic:

        if not basicEffects: # Empty list
            # Add the new term in the basicEffects list
            basicEffects.append(term)
        else:
            # Evaluate all interactions between the new term and 
            # all terms in the basicEffects list
            interactions = [_getInteraction(e, term) for e in basicEffects]

            # Add the new term in the basic effects, and then all interactions
            basicEffects.append(term)
            basicEffects.extend(interactions)
    
    # Remove model terms
    for t in terms:
        if t in basicEffects: basicEffects.remove(t)

    # Remove irrelevant (for the required resolution) terms
    basicEffects = [t for t in basicEffects if len(t) >= resolution - 1]

    return basicEffects


def _makeBasic(terms: list, sampleSize: int, resolution: int) -> Tuple[list, list]:
    """ Step 3: Selects a set of basic factors and forms the basic effects group.
        Inputs:
            terms: List of factor names in the design
            sampleSize: Number of runs of the design
            resolution: Required design resolution
        Outputs:
            baseTerms   : Base factors of the design
            addedTerms  : Added factors of the design
            basicEffects: Basic effects group
     """

    baseTerms    = _getBase(terms)
    basicTerms   = _makeBasicTerms(terms, baseTerms, sampleSize)
    addedTerms   = _makeAddedTerms(baseTerms, basicTerms)
    basicEffects = _makeBasicEffectsGroup(terms, basicTerms, resolution)
    
    return baseTerms, addedTerms, basicEffects


def _makeTab(basicEffects: list, addedTerms: list, inelligible: list) -> np.array:
    """ Step 4: Generates table of eligible effects. 
        Inputs:
            basicEffects: Basic effects group
            addedTerms  : Added factors in the design
            inelligible : Inelligible effects set
        Outputs:
            Matrix containing the eligible effects
    """

    tab = np.empty(shape = (len(basicEffects), len(addedTerms)), dtype = 'U52')

    for i, effect in enumerate(basicEffects):
        for j, term in enumerate(addedTerms):
            interaction = _getInteraction(effect, term)
            if interaction in inelligible: interaction = ''
            tab[i, j] = interaction

    return tab


def _getInteractions(
    generator: str, contrasts: list, inelligibleSet: list) -> Tuple[bool, list]:
    """ Step 8: Checks whether all generalized interactions between the 
        current generator and the defining contrasts group are eligible.
        Inputs:
            generator     : Generator string of the design
            contrasts     : Set of defining contrasts found so far
            inelligibleSet: Set of inelligible effects
        Outputs:
            eligible   : Indicator whether the current generator is an eligible effect
            interaction: Generalised interactions
    """
    
    empty        = all([c is None for c in contrasts])
    eligible     = True
    interactions = []

    if not empty: # If contrasts list is empty, the generator is eligible.
        for c in contrasts:
            if c is not None:
                interaction = _getInteraction(c, generator)
                interactions.append(interaction)
                if interaction in inelligibleSet: 
                    eligible = False
                    break
            else:
                interactions.append(None)
    
    return eligible, interactions


def _getResolution(contrasts: list) -> int:
    """ Computes the resolution of a design. 
        Inputs:
            contrasts: Set of defining contrasts
        Outputs:
            resolution of the design
    """
    return min([len(c) for c in contrasts])


def _addGenerator(gens: list, col: int, curSelection: list, 
    addedTerms: list, baseTerms:list, basicEffects: list) -> list:
    """ Adds a generator to the appropriate place (index) in 
        the list of the design's generators.
        Inputs:
            gens        : List of generators, one for each column of the contrasts table
            col         : Current column being evaluated
            curSelection: Generators selected in this iteration of the algorithm
            addedTerms  : Added factors of the design
            baseTerms   : Base factors of the design
            basicEffects: Basic effects group
        Outputs:
            gens        : Updated list of generators
    """
    
    idx = baseTerms.index(addedTerms[col])
    val = basicEffects[curSelection[col]]
    gens[idx] = val

    return gens


def _addContrast(generator: str, colNum: int, interactions: list, contrasts: list) -> list:
    """ Adds a contrast to the appropriate place (index) in the list of the design's contrasts.
        Inputs:
            generator   : Generator string
            colNum      : Current column being evaluated
            interactions: Interactions between the currently selected generator and the 
                          defining contrasts group
            contrasts   : Set of defining contrasts
        Outputs:
            contrasts   : Updated set of defining contrasts
    """

    index = 2 ** colNum - 1
    contrasts[index] = generator
    for j in range(index): contrasts[index + j + 1] = interactions[j]
    
    return contrasts


def _removeContrast(contrasts: list, colNum: int) -> list:
    """ Removes a contrast from the list of the design's contrasts. 
        Inputs:
            constrasts: Set of defining contrasts
            colNum: Current column of the constrasts table being operated upon
        Outputs:
            constrasts: Updated list with the defining contrasts    
    """

    index = 2 ** colNum - 1
    contrasts[index] = None
    for j in range(index): contrasts[index + j + 1] = None
    
    return contrasts


def _addBaseToGenerators(terms: list, gens: list) -> list:
    """ Adds base term to its corresponding location in the generators. 
        Inputs:
            terms: List of factor names in the design
            gens:  List of generators from each column of the contrasts table
        Outputs:
            gens: Updated list of generators from each column of the contrasts table
    """

    n = _getNumBase(terms)
    for i, t in enumerate(terms):
        if i >= n: break
        if gens[i] is None: gens[i] = terms[i]
    
    return gens


def _searchContrasts(terms: list, inelligible: list, resolution: int, k: int) -> Tuple[list, int]:
    """ Steps 3 - 10: Algorithm to search for the defining contrasts. 
        Inputs:
            terms       : Names of the factors in the design
            inelligible : Inelligible effects set
            resolution  : Required resolution of the design
            k           : Sample size (number of runs) of the design
        Outputs:
            gens        : List of generators (one from each column of the defining contrasts table)
            curRes      : Resolution of the current design
    """
    
    base, added, effects = _makeBasic(terms, k, resolution)       # Step 3
    contrastsTab         = _makeTab(effects, added, inelligible)  # Step 4
    
    # Initialize search
    numRows, numCols = contrastsTab.shape
    numBase     = _getNumBase(terms)
    m           = numBase - k
    curGens     = [numRows] * m         # Current selection of generators from table
    gens        = [None] * numBase      # Generator from each column
    contrasts   = [None] * (2 ** m-1)   # Defining contrasts group
    stop        = False                 # Exit criterion (see Step 10)
    col, curRes = 0, 0                  # Current column and best resolution so far
    gen         = lambda j: contrastsTab[curGens[j]][j] # Step 7

    # Search contrasts
    while curRes < resolution and not stop:
        curGens[col] -= 1

        if curGens[col] >= 0 and gen(col) != '':
            eligible, interactions = _getInteractions(gen(col), contrasts, inelligible) # Step 8
            
            if eligible: # Step 9
                contrasts = _addContrast(gen(col), col, interactions, contrasts)
                gens      = _addGenerator(gens, col, curGens, added, base, effects)

                if col == numCols - 1:
                    curRes    = _getResolution(contrasts)
                    contrasts = _removeContrast(contrasts, col)
                else:
                    col += 1
                    curGens[col] = numRows
        
        elif curGens[col] == -1 and col == 0: # Step 11
            stop = True
        elif curGens[col] == -1 and col > 0: # Step 10
            col -= 1
            contrasts = _removeContrast(contrasts, col)
    
    gens = _addBaseToGenerators(terms, gens)

    return gens, curRes


def fracfactgen(terms: str, resolution: int = 3) -> str:
    """ Finds generators of the smallest two-level fractional factorial design for the model specified
        by the term string, using the Franklin-Bailey algorithm [1, 2].

        Inputs:
            terms:      String scalar consisting of words formed from the 52 case-sensitive letters a-Z, 
                        separated by spaces. Use 'a'-'z' for the first 26 factors, and, if necessary, 
                        'A'-'Z' for the remaining factors. For example, terms = 'a b c ab ac'. Single-letter 
                        words indicate main effects to be estimated; multiple-letter words indicate interactions. 
            resolution: Required resolution of the design, defaults to 3
        
        Outputs: 
            The generator string for the smallest possible fractional factorial design.

        References:
        [1] Selection of Defining Contrasts and Confounded Effects in Two-level Experiments. Franklin M.F., 
            and Bailey R.A., Applied Statistics 26, No. 3, pp 321-326, 1977.
        [2] Box, G. E. P., W. G. Hunter, and J. S. Hunter. Statistics for Experimenters. Hoboken, NJ: Wiley-Interscience, 1978.
    """

    if not isinstance(terms, str):
        raise ValueError('Generator should be a string.')

    if not isinstance(resolution, int) or resolution < 3: 
        raise ValueError('Resolution must be an integer higher than or equal to 3.')

    tParsed     = parse(terms)                     # Step 0
    terms       = [t['name'] for t in tParsed]
    inelligible = _makeInelligible(terms)            # Step 1
    kVec        = _makeSampleSize(terms, resolution) # Step 2
    numBase     = _getNumBase(terms)

    for k in kVec: # Step 11
        gens, curRes = _searchContrasts(terms, inelligible, resolution, k) # Steps 3-10
        if curRes >= resolution or numBase - k == 1: break
    
    if curRes == 0: raise RuntimeError('No design was found.')

    return " ".join(gens)
