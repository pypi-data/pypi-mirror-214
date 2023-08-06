""" This module implements the Box-Behnken design. """

from .fracfact import fracfact
import numpy as np

# Tabulated Box-Behnken design, for various numbers of factors.
# designTab: {k, v} with k: Number of factors, v: Balanced factor pairs
BALANCED_DESIGNS = {}
BALANCED_DESIGNS[3] = np.array([[1, 2], [1, 3], [2, 3]])

BALANCED_DESIGNS[4] = np.array([[1, 2], [3, 4], [1, 4], [2, 3], [1, 3], [2, 4]])

BALANCED_DESIGNS[5] = np.array([
    [1, 2], [3, 4], [2, 5], [1, 3], [4, 5], [2, 3], [1, 4], [3, 5], [1, 5], [2, 4]
    ])
BALANCED_DESIGNS[6] = np.array([
    [1, 2, 4], [2, 3, 5], [3, 4, 6], [1, 4, 5], [2, 5, 6], [1, 3, 6]
    ])
BALANCED_DESIGNS[7] = np.array([
    [4, 5, 6], [1, 6, 7], [2, 5, 7], [1, 2, 4], [3, 4, 7], [1, 3, 5], [2, 3, 6]
    ])
BALANCED_DESIGNS[9] = np.array([
        [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 5, 9], 
        [3, 4, 8], [2, 6, 7], [1, 6, 8], [2, 4, 9], [3, 5, 7], [1, 4, 7], [2, 5, 8], 
        [3, 6, 9]
        ])
BALANCED_DESIGNS[10] = np.array([
        [2, 6, 7, 10], [1, 2, 5, 10], [2, 3, 7, 8], [2, 4, 6, 9], [1, 8, 9, 10], 
        [3, 4, 5, 10], [1, 4, 7, 8],  [3, 5, 7, 9], [1, 3, 6, 9], [4, 5, 6, 8]
        ])
BALANCED_DESIGNS[11] = np.array([
        [3, 7, 8, 9, 11], [1, 4, 8, 9, 10], [2, 5, 9, 10, 11], [1, 3, 6, 10, 11],
        [1, 2, 4, 7, 11], [1, 2, 3, 5, 8],  [2, 3, 4, 6, 9],   [3, 4, 5, 7, 10],
        [4, 5, 6, 8, 11], [1, 5, 6, 7, 9],  [2, 6, 7, 8, 10]
        ])

BALANCED_DESIGNS[12] = np.array([
        [1, 2, 5, 7],   [2, 3, 6, 8],   [3, 4, 7, 9],   [4, 5, 8, 10], 
        [5, 6, 9, 11],  [6, 7, 10, 12], [1, 7, 8, 11],  [2, 8, 9, 12], 
        [1, 3, 9, 10],  [2, 4, 10, 11], [3, 5, 11, 12], [1, 4, 6, 12]
        ])
BALANCED_DESIGNS[16] = np.array([
        [1, 2, 6, 9],   [3, 4, 8, 11],  [5, 10, 13, 14], [7, 12, 15, 16],
        [2, 3, 7, 10],  [1, 4, 5, 12],  [6, 11, 14, 15], [8, 9, 13, 16],
        [2, 5, 6, 13],  [4, 7, 8, 15],  [1, 9, 10, 14],  [3, 11, 12, 16],
        [3, 6, 7, 14],  [1, 5, 8, 16],  [2, 10, 11, 15], [4, 9, 12, 13],
        [1, 3, 13, 15], [2, 4, 14, 16], [5, 7, 9, 11],   [6, 8, 10, 12],
        [4, 6, 10, 16], [3, 5, 9, 15],  [1, 7, 11, 13],  [2, 8, 12, 14]
        ])


def getNumberCenterpoints(numFactors: int) -> int:
    """ Computes the number of centerpoints in the design. 
        Inputs:
            numFactors: Number of factors in the design
        Outputs:
            numCenter: Number of centerpoints
    """
    v = [None, None, 3, 3, 6, 6, 6, 8, 10, 10, 12, 12, 12, 12, 12, 12]
    
    return v[min(numFactors, len(v) - 1)]


def makeBalancedPart(numFactors: int) -> np.array:
    """
    Computes the balanced part of the Box-Behnken design, according to the tabulated 
    designs for various numbers of factors. If the design is not in the catalog, it is
    generated.
    Inputs:
        numFactrors: Number of factors in the design
    Outputs:
        out: Matrix containing the balanced part of the design
    """

    # Get the part of the design from the table if it exists
    out = BALANCED_DESIGNS.get(numFactors, None)

    # If not, generate all factor number pairs
    if out is None:
        
        p = np.arange(numFactors - 1, 1, -1)
        f = int(numFactors * (numFactors - 1) / 2)

        # Make 1st column
        mtrx1     = np.zeros(f) 
        ix        = np.cumsum(np.insert(p, 0, 1)) - 1
        mtrx1[ix] = 1
        mtrx1     = np.cumsum(mtrx1)

        # Make second column
        mtrx2     = np.ones(f)
        ix        = np.cumsum(p)
        mtrx2[ix] = 2 - p
        mtrx2[0]  = 2
        mtrx2     = np.cumsum(mtrx2)

        # Merge
        out = np.stack([mtrx1, mtrx2], axis = 1).astype(int)
        
    return out


def makeFactorialPart(numFactors: int) -> np.array:
    """ Generates the factorial part of the design.
        Inputs:
            numFactors: Number of factors in the design
        Outputs:
            out: Matrix containing the factorial part of the design
    """
    if   numFactors in [6, 7, 9]    : out = fracfact('a b c')
    elif numFactors in [10, 12, 16] : out = fracfact('a b c d')
    elif numFactors == 11           : out = fracfact('a b c d abcd')
    else                            : out = fracfact('a b')

    return out


def merge(
    factorial: np.array, balanced: np.array, 
    numFactors: int, numCenter: int) -> np.array:
    """ Merges the factorial and balanced parts of the design
        Inputs: 
            factorial   : Array containing the factorial part of the design
            balanced    : Array containing the balanced part of the design
            numFactors  : Number of factors in the design
            numCenter   : Number of centerpoints in the design
        Outputs:
            out: Box-Behnken design of experiments array
    """

    numFactorial = factorial.shape[0]
    numBalanced  = balanced.shape[0]
    numRuns      = numBalanced * numFactorial + numCenter

    # Make row and column indices to merge the two arrays
    r = np.repeat(np.arange(numFactorial * numBalanced)[:, None], factorial.shape[1], 1)
    r = r.flatten(order ='F')
    c = balanced.T.flatten() - 1
    c = np.repeat(c[None, :], numFactorial, 0)
    c = c.flatten(order ='F')

    # Create full-size design
    sh  = (numRuns, numFactors)
    out = np.zeros(shape = sh, dtype = int)

    # Convert to linear indices
    ix = np.ravel_multi_index([r, c], sh, order ='F')
    ix = np.unravel_index(ix, sh, order = 'F')

    out[ix] = np.tile(factorial, (numBalanced, 1)).flatten(order = 'F')

    return out


def bbdesign(numFactors: int, numCenter: int = None) -> np.array:

    """ Generator of Box-Behnken designs
    Inputs:
        numFactors: Number of factors in the design
        numCenter:  Number of centerpoints in the design 
    Outputs:
        out: Box-Behnken design of experiments array
    """

    # Check inputs
    if not isinstance(numFactors, int) or numFactors < 3:
        raise ValueError('Number of factors should be an integer higher than or equal to 3.')

    if numCenter is None: # Evaluate number of centerpoints if needed
        numCenter = getNumberCenterpoints(numFactors) 

    if numCenter is None or not( isinstance(numCenter, int) and numCenter >= 1 ):
            raise ValueError('Number of centerpoints should be an integer higher than or equal to 1.')

    balancedPart  = makeBalancedPart(numFactors)
    factorialPart = makeFactorialPart(numFactors)

    return merge(factorialPart, balancedPart, numFactors, numCenter)
