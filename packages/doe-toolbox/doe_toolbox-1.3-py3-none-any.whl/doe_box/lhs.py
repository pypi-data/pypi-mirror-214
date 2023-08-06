import numpy as np
from typing import Literal
from scipy.spatial.distance import pdist

MAX_ITER = 10 # Max. number of iterations to imporce the criterion

def _makeSample(numSamples: int, numVars: int, smooth: bool) -> np.array:
    """ Generates a uniform random sample.
        Inputs:
            numSamples : Number of samples for the design
            numVars    : Number of variables in the design
            smooth     : Indicates whether a continuous or discrete sample is needed
        Outputs:
            x: Array containing <numSamples> uniform samples for <numVars> variables.
    """

    x = np.random.rand(numSamples, numVars)

    for i in range(numVars): 
        x[:, i] = _rank(x[:, i]) + 1

    if smooth: x -= np.random.rand(*x.shape)
    else     : x -= 0.5
    
    x /= numSamples

    return x


def _rank(x: np.array) -> np.array:
    """ Computes the rank of each element in the input array x. 
        Inputs:
            x: Vector whose rank needs to be computed
        Outputs:
            r: Rank of each element in x
    """
    n     = x.shape[0]
    ix    = np.argsort(x)
    r     = np.empty(n, dtype = int)
    r[ix] = np.arange(0, n)
    r     = r.reshape(1, -1)

    return r


def _getScore(x: np.array, criterion: str) -> float:
    """ Computes the score achieved by the current design.
        Inputs:
            x        : Current sample matrix. Dimensions: numSamples x numVariables
            criterion: Criterion that is being optimized
        Outputs:
            score: Score achieved by the current matrix
    """
    if criterion == 'maxdist':
        score = pdist(x).min() # min distance between two points

    else:
        corr  = np.corrcoef(x, rowvar = False) 
        score = -np.sum(np.triu(corr, k = 1) ** 2) # sum of between-column squared correlations

    return score


def lhs(
    numSamples: int, numVariables: int, 
    criterion : Literal['maxdist', 'mincorr', None] = 'maxdist',
    smooth    : bool = True
    ) -> np.array:
    """ Latin hypercube sampling (LHS) design of experiments [1].
        Inputs: 
            numSamples  : Number of samples to be generated
            numVariables: Number of variables in the design
            criterion   : Criterion to be used to evaluate design improvement
                Can be one of:
                * maxdist: Maximizes the point-to-point distance
                * mincorr: Minimizes the correlation
            smooth      : Indicator whether the points that will be produced 
                should be randomly distributed, with one point from each of the
                intervals: (0, 1/numSamples), (1/numSamples , 2/numSamples),
                (1-1/numSamples, 1), with a subsequent random permutation,
                or
                if they should be produced only at the midpoints of the intervals:  
                .5/numSamples, 1.5/numSamples, ..., 1-.5/numSamples.
        
        Outputs:
            bestDesign: LHS matrix
        
        References:
        [1] M. Stein, "Large sample properties of simulations using Latin
            hypercube sampling." Technometrics 29, no. 2: 143-151, 1987.
    """

    if not isinstance(numSamples, int) or numSamples <= 1:
        raise ValueError('Number of samples should be an integer higher than 1.')

    if not isinstance(numVariables, int) or numVariables <= 1:
        raise ValueError('Number of variables should be an integer higher than 1.')

    if criterion not in ['maxdist', 'mincorr', None]:
        raise ValueError('Criterion should equal "maxdist" (default), "mincorr", or None.')

    # Starting conditions
    bestDesign = _makeSample(numSamples, numVariables, smooth)
    bestScore  = _getScore(bestDesign, criterion)
    curIter    = 0

    if numSamples < 2 or criterion is None: return bestDesign # Nothing more to do

    while curIter < MAX_ITER:

        # Make a new design
        x = _makeSample(numSamples, numVariables, smooth)
        s = _getScore(x, criterion)
        if s > bestScore: bestDesign, bestScore = x, s        
        curIter += 1

    return bestDesign
