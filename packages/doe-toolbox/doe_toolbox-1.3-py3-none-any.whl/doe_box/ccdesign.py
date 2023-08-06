""" This module implements the central composite design. """

from string     import ascii_lowercase as alphabet
from typing     import Union, Literal, Tuple
from .fracfact  import fracfact
from .fullfact  import ff2n
import numpy as np

# Dict containing a catalog of confounded factors:
# (Number of factors, fraction number): confounded factors
# Source: https://www.itl.nist.gov/div898/handbook/pri/section3/pri3347.htm
CONFOUNDED_FACTORS = {} 
CONFOUNDED_FACTORS[ (3, 1)   ] = 'ab'
CONFOUNDED_FACTORS[ (4, 1)   ] = 'abc'
CONFOUNDED_FACTORS[ (5, 1)   ] = 'abcd'
CONFOUNDED_FACTORS[ (5, 2)   ] = 'ab ac'
CONFOUNDED_FACTORS[ (6, 1)   ] = 'abcde'
CONFOUNDED_FACTORS[ (6, 2)   ] = 'abc bcd'
CONFOUNDED_FACTORS[ (6, 3)   ] = 'ab ac bc'
CONFOUNDED_FACTORS[ (7, 1)   ] = 'abcdef'
CONFOUNDED_FACTORS[ (7, 2)   ] = 'abcd abde'
CONFOUNDED_FACTORS[ (7, 3)   ] = 'abc bcd acd'
CONFOUNDED_FACTORS[ (7, 4)   ] = 'ab ac bc abc'
CONFOUNDED_FACTORS[ (8, 1)   ] = 'abcdefg'
CONFOUNDED_FACTORS[ (8, 2)   ] = 'abcd abef'
CONFOUNDED_FACTORS[ (8, 3)   ] = 'abc abd bcde'
CONFOUNDED_FACTORS[ (8, 4)   ] = 'bcd acd abc abd'
CONFOUNDED_FACTORS[ (9, 1)   ] = 'abcdefgh'
CONFOUNDED_FACTORS[ (9, 2)   ] = 'acdfg bcefg'
CONFOUNDED_FACTORS[ (9, 3)   ] = 'abcd acef cdef'
CONFOUNDED_FACTORS[ (9, 4)   ] = 'bcde acde abde abce'
CONFOUNDED_FACTORS[ (9, 5)   ] = 'abc bcd acd abd abcd'
CONFOUNDED_FACTORS[ (10, 1)  ] = 'abcdefghi'
CONFOUNDED_FACTORS[ (10, 2)  ] = 'abcde defgh'
CONFOUNDED_FACTORS[ (10, 3)  ] = 'abcg bcde acdf'
CONFOUNDED_FACTORS[ (10, 4)  ] = 'bcdf acdf abde abce'
CONFOUNDED_FACTORS[ (10, 5)  ] = 'abcd abce abde acde bcde'
CONFOUNDED_FACTORS[ (10, 6)  ] = 'abc bcd acd abd abcd ab'
CONFOUNDED_FACTORS[ (11, 1)  ] = 'abcdefghij'
CONFOUNDED_FACTORS[ (11, 2)  ] = 'abcdef defghi'
CONFOUNDED_FACTORS[ (11, 3)  ] = 'abcde bcdgh acefg'
CONFOUNDED_FACTORS[ (11, 4)  ] = 'abcg bcde acdf abcdefg'
CONFOUNDED_FACTORS[ (11, 5)  ] = 'cde abcd abf bdef adef'
CONFOUNDED_FACTORS[ (11, 6)  ] = 'abc bcd cde acd ade bde'
CONFOUNDED_FACTORS[ (11, 7)  ] = 'abc bcd acd abd abcd ab ac'
CONFOUNDED_FACTORS[ (15, 11) ] = 'ab ac ad bc bd cd abc abd acd bcd abcd'
CONFOUNDED_FACTORS[ (31, 26) ] = 'ab ac ad ae bc bd be cd ce de abc abd abe acd ace ade bcd bce bde cde abcd abce abde acde bcde abcde'


def checkInputs(numFactors: int, centerPoints: Union[int, str], designType: str, fraction: int):
    """ 
    Checks the user inputs.

    Inputs:     
        numFactors  : Number of factors in the design. Must be an integer > 2
        centerPoints: Number of center points to be added in the factorial and axial parts of the design.
            Can be one of:
            * 'orthogonal': Number of center points will be computed so that an orthogonal design will be provided.
            * 'uniform'   : Number of center points will be computed so that uniform precision will be achieved.
            * integer     : Number of center points to be used in the design.
        designType  : Options that defines the type of the CCD. 
            Can be one of:
            * 'circumscribed': is the original type of CCD, where axial points are located at 
                            distance a from the center point.
            * 'inscribed'    : inscribed CCD is characterized by that axial points are 
                            located at factor levels −1 and 1, while factorial points are brought 
                            into the interior of the design space and located at distance 1/α from the center point.
            * 'faced'        : In face-centered CCD axial points are located at a distance 1 from the center 
                            point, i.e., at the face of the design cube, if the design involves three experimental factors.
        fraction    : Fraction of full-factorial cube, expressed as an exponent of 1/2.

    Outputs: None

    Note: Raises ValueError if the inputs are invalid
    """

    designType = checkLiteralInput(
        input_   = designType, 
        valid    = ["circumscribed", "inscribed", "faced"], 
        errorMsg = 'Invalid designType specified.'
        )

    if isinstance(centerPoints, int) and centerPoints < 1:
        raise ValueError("If an integer number of centerpoints is provided, it should be positive." )
    elif not isinstance(centerPoints, int):
        centerPoints = checkLiteralInput(
        input_   = centerPoints, 
        valid    = ["orthogonal", "uniform"], 
        errorMsg = 'Invalid centerPoints specified.'
        )

    if not (isinstance(numFactors, int) and 2 <= numFactors <= 26): # 26: Letters in the Roman alphabet
        raise ValueError("Number of factors should be an integer in the interval [2, 26]." )

    if not (isinstance(fraction, int) and 0 <= fraction <= 4):
        raise ValueError("Fraction should be an integer in the interval [0, 4]." )

    checkFactorFractionCombination(numFactors, fraction)

    return 


def checkLiteralInput(input_: str, valid: list, errorMsg: str):
    """ Checks if the literal type input is valid.
        Inputs:
            input_   : Input string to be checked
            valid    : List of valid values that input_ can take
            errorMsg : Error message to be printed if the input is 
                       not in the acceptableValues list.
        Outputs:
            input_: Valid input lowercased
    """
    if not isinstance(input_, str): 
        raise ValueError(errorMsg)
    else:
        input_ = input_.lower()
        if not (input_ in valid):
            raise ValueError(errorMsg)

    return 


def makeStarMatrix(numFactors: int, fraction: tuple, designType: str) -> Tuple[np.array, float]:
    """ Generates the star matrix of the central composite design.
        Inputs:
            numFactors: Number of factors in the design.
            fraction  : Fraction of full-factorial cube, expressed as an exponent of 1/2.
            designType: Options that defines the type of the CCD. 
                Can be one of:
                * 'circumscribed': is the original type of CCD, where axial points are located at 
                                    distance a from the center point.
                * 'inscribed'    : inscribed CCD is characterized by that axial points are 
                                    located at factor levels −1 and 1, while factorial points are brought 
                                    into the interior of the design space and located at distance 1/α from the center point.
                * 'faced'        : In face-centered CCD axial points are located at a distance 1 from the center 
                                    point, i.e., at the face of the design cube, if the design involves three experimental factors.
        Outputs:
            Star 'portion' of the central composite design matrix.
    """

    # Compute the value of alpha
    if designType == 'faced': alpha = 1
    else: alpha = 2 ** ( 0.25 * (numFactors - fraction) )

    return np.kron(np.eye(numFactors), np.array([[-alpha], [alpha]])), alpha


def makeFraction(numFactors: int) -> int:
    """ Sets the fraction of the full-factorial cube, expressed as an exponen of 1/2
        if not provided by the user.
        Inputs:
            numFactors: Number of factors in the design
        Outputs:
            fraction: The fraction of the full-factorial cube
    """

    if   numFactors <= 4    : fraction = 0
    elif 4 < numFactors <= 7: fraction = 1
    elif 7 < numFactors <= 9: fraction = 2
    elif numFactors == 10   : fraction = 3
    elif numFactors == 11   : fraction = 4
    else                    : fraction = 1 # numFactors > 11

    return fraction


def checkFactorFractionCombination(numFactors: int, fraction: int):
    """ Raises a value error when an invalid set of number of factors and fraction 
        have been provided for the design.
        Inputs:
            numFactors: Number of factors in the central composite design
            fraction  : Fraction of full-factorial cube, expressed as an exponent of 1/2.
        Outputs:
            None
    """

    if fraction > 0 and not (numFactors, fraction) in CONFOUNDED_FACTORS.keys():

        valid = [str(fr) for nf, fr in CONFOUNDED_FACTORS.keys() if nf == numFactors] + ['0']
        valid = ', '.join(valid)
        msg   = f'For {numFactors} factors, one of the following fractions should be selected: {valid}'
        raise ValueError(msg)

    return


def makeCubeGenenerator(numFactors: int, fraction: int) -> str:
    """ Makes the generator for the cube (factorial) part of the design.
        Inputs:
            numFactors: Number of factors in the central composite design
            fraction  : Fraction of full-factorial cube, expressed as an exponent of 1/2.
        Outputs:
            gen: Fractional factorial design generator for the cube part.
    """

    # Make the generator for the confounded factors
    cgen = CONFOUNDED_FACTORS.get((numFactors, fraction), None)

    # Make the generator for the first few (unconfounded) factors
    ugen = ' '.join(alphabet[:numFactors - fraction])

    # Combine them
    gen = ' '.join( [ugen, cgen] ).strip()

    return gen


def numCenterPointsUniform(numFactors: int, fraction: int) -> int:
    """ Evaluates the number of centerpoints for uniform precision according to [1].
        Inputs:
            numFactors: Number of factors in the design. Must be an integer > 2
            fraction  : Fraction of full-factorial cube, expressed as an exponent of 1/2.
        
        Outputs:
            numCenter : Number of center points

        References:
        [1] Multi-Factor Experimental Designs for Exploring Response Surfaces
            G. E. P. Box, J. S. Hunter
            Ann. Math. Statist. 28(1): 195-241 (March, 1957). 
            DOI: 10.1214/aoms/1177707047
    """
    
    # For some designs determining the number of center points to
    # get uniform precision is not possible. For those cases 
    # 'None' values will be returned,(and the number of center 
    # points for orthogonality will be used).
    
    numCenter = None
    if 2 <= numFactors <= 8 and fraction == 0:
        v  = [None, 5, 6, 7, 10, 15, 21, 28]
        numCenter = v[numFactors - 1]
    elif 5 <= numFactors <= 8 and fraction == 1:
        v = [None, None, None, None, 6, 9, 14, 20]
        numCenter = v[numFactors - 1]
    elif numFactors == 8 and fraction == 2:
        numCenter = 13

    return numCenter


def numCenterPointsOrthogonal(numFactors: int, fraction: int) -> int:
    """ Evaluates the number of centerpoints for an orthogonal design according to [1].
        Inputs:
            numFactors: Number of factors in the design. Must be an integer > 2
            fraction  : Fraction of full-factorial cube, expressed as an exponent of 1/2.
        
        Outputs:
            numCenter : Number of center points

        References:
        [1] Multi-Factor Experimental Designs for Exploring Response Surfaces
            G. E. P. Box, J. S. Hunter
            Ann. Math. Statist. 28(1): 195-241 (March, 1957). 
            DOI: 10.1214/aoms/1177707047
    """

    c = 2 ** (numFactors - fraction)

    # Eq. 81 (lambda4 = 1) of [1]
    numCenter = max(1, np.ceil(4 * np.sqrt(c) + 4 - 2 * numFactors))

    return int(numCenter)


def numCenterPoints(numFactors: int, fraction: int, centerPoints: Union[str, int]) -> int:
    """ Evaluates the number of centerpoints.
        Inputs:
            numFactors: Number of factors in the design. Must be an integer > 2
            fraction  : Fraction of full-factorial cube, expressed as an exponent of 1/2.
            centerPoints: Number of center points to be added in the factorial and axial parts of the design.
            Can be one of:
            * 'orthogonal': Number of center points will be computed so that an orthogonal design will be provided.
            * 'uniform'   : Number of center points will be computed so that uniform precision will be achieved.
            * integer     : Number of center points to be used in the design.

        Outputs:
            numCenter : Number of center points
    """

    if isinstance(centerPoints, int): numCenter = centerPoints
    elif centerPoints == "uniform":   numCenter = numCenterPointsUniform(numFactors, fraction)

    if centerPoints == "orthogonal" or numCenter is None: # numCenterUniform() may return None
        numCenter = numCenterPointsOrthogonal(numFactors, fraction)

    if not isinstance(numCenter, int):
        raise RuntimeError('Number of center points could not be evaluated.')
        
    return numCenter


def ccdesign(
    numFactors  : int, 
    fraction    : int = None,
    centerPoints: Union[int, Literal["orthogonal", "uniform"]] = 'orthogonal', 
    designType  : Literal["circumscribed", "inscribed", "faced"] = 'circumscribed', 
    ) -> np.array:
    """ Central composite design (CCD)

        numFactors: Number of factors in the design. Must be an integer > 2

        centerPoints: Number of center points to be added in the factorial and axial parts of the design.
            Can be one of:
            * 'orthogonal': Number of center points will be computed so that an orthogonal design will be provided.
            * 'uniform'   : Number of center points will be computed so that uniform precision will be achieved.
            * integer     : Number of center points to be used in the design.

        designType: Option that defines the type of the CCD. 
            Can be one of:
            * 'circumscribed': is the original type of CCD, where axial points are located at 
                            distance a from the center point.
            * 'inscribed'    : inscribed CCD is characterized by that axial points are 
                            located at factor levels −1 and 1, while factorial points are brought 
                            into the interior of the design space and located at distance 1/α from the center point.
            * 'faced'        : In face-centered CCD axial points are located at a distance 1 from the center 
                            point, i.e., at the face of the design cube, if the design involves three experimental factors.
        
        fraction: Fraction of full-factorial cube, expressed as an exponent of 1/2.
    """


    # Get fraction for the full factorial cube if not set
    if fraction is None: fraction = makeFraction(numFactors)

    # Check inputs
    checkInputs(numFactors, centerPoints, designType, fraction)

    # Make cube portion of the design
    if fraction == 0: 
        cubePart = ff2n(numFactors)
    else:
        gen = makeCubeGenenerator(numFactors, fraction)
        cubePart = fracfact(gen)

    # Star portion of the matrix
    starPart, alpha = makeStarMatrix(numFactors, fraction, designType)

    # Get number of center points to be used
    numCenter  = numCenterPoints(numFactors, fraction, centerPoints)
    centerPart = np.zeros(shape = (numCenter, numFactors))

    # Make full design
    mtrx = np.concatenate([cubePart, starPart, centerPart], axis = 0)

    # Inscribe if requested
    if designType == 'inscribed':  mtrx /= alpha

    return mtrx