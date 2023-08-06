# DOE Toolbox

## Description

A simple Design of Experiments (DoE) toolbox written in python, which provides a range of tools and functions to facilitate the planning of experimental designs. It is intended to assist researchers, engineers, and analysts in efficiently exploring and optimizing systems, processes, and products by systematically varying factors and analyzing their effects on the response variable.

It includes:
1. [Factorial designs](#factorial)
    * *Generic full-factorial* (`fullfact`): A design in which every setting of every factor appears with every setting of every other factor, for all possible combinations.
    * *2-level full-factorial* (`ff2n`): Same as above, but the factors are constrained to have two levels each (high/low or +1 and -1).
    * *2-level fractional factorial* (`fracfact`): Similar to a full factorial DoE, but a subset of factor combinations is selected, based on specific rules to ensure that important main effects and interactions can still be estimated with a reduced number of experimental runs.
    * *2-level fractional factorial generator* (`fracfactgen`): Convenient design generator to control how the fraction (or subset of runs) iwill selected from the full set of runs in a fractional factorial design.
2. [Response surface designs](#rsm)
    * *Box-Wilson Central Composite Designs (CCD)* (`ccdesign`): CCD designs start with a factorial or fractional factorial design (with center points) and add "star" points to estimate curvature for the estimation of quadratic models.
    * *Box-Behnken* (`bbdesign`): An alternative to CCD, being an independent quadratic design in that it does not contain an embedded factorial or fractional factorial design. For three factors, the Box-Behnken design offers some advantage in requiring a fewer number of runs than a CCD. However, for four or more factors, this advantage disappears.
3. [Latin Hypercube sampling (LHS)](#lhs): An experimental design in which the range of each factor is divided into equal intervals or bins. Within each bin, one and only one sample point is selected randomly. The selection process ensures that the samples are evenly distributed across the parameter space and that each combination of factor levels occurs exactly once. It is especially useful for, and commonly employed in, simulation studies, sensitivity analysis, and optimization problems.

## Installation

The package can be easily installed with pip via a DOS or Unix command shell:

```bash
pip install doe-toolbox
```

### Requirements
The following packages are required:
* numpy >= 1.24.2,
* scipy >= 1.10.1.

See `requirements.txt` file


## Usage

### Factorial Design of Experiments <a name="factorial"></a>

#### fullfact

##### Description

Full factorial designs consist of two or more factors, each with discrete possible values or "levels", and whose experimental units take on all possible combinations of these levels across all such factors.
Such designs can be generated using the `fullfact` function  outputs factor settings for a full factorial design with *n* factors, where the number of levels for each factor is given by the vector `levels` of length *n*. 

The output is an *m*-by-*n* numpy array, where *m* is the number of treatments in the full-factorial design. 
Each row corresponds to a single treatment, and each column contains the settings for a single factor, with floating point scalars ranging from -1 to +1.

##### Example
The following generates a ten-run full-factorial design with five levels for the first factor and two levels for the second factor:

```python
>>> import doe_box as dbox
>>> dbox.fullfact(levels = [5, 2])
array([[-1. , -1. ],
       [-1. ,  1. ],
       [-0.5, -1. ],
       [-0.5,  1. ],
       [ 0. , -1. ],
       [ 0. ,  1. ],
       [ 0.5, -1. ],
       [ 0.5,  1. ],
       [ 1. , -1. ],
       [ 1. ,  1. ]])
```

#### fracfact

##### Description

Fractional factorial designs are experimental designs consisting of a carefully chosen subset (fraction) of the experimental runs of a full factorial design. 
The subset is chosen so as to exploit the sparsity-of-effects principle to expose information about the most important features of the problem studied, while using a fraction of the effort of a full factorial design in terms of experimental runs and resources. 
In simple terms, it makes use of the fact that many experiments in full factorial design are often redundant, giving little or no new information about the system.

Such designs can be generated using the `fracfact` function, which creates the two-level fractional factorial designs defined by the generator `gen`. 
The latter is a (case-sensitive) string listing the factors in the design, formed from the 52 case-sensitive letters *a*-*Z*, separated by spaces.
Standard convention notation indicates to use *a*-*z* for the first 26 factors, and, if necessary, *A*-*Z* for the remaining factors. 
A valid example would be: `gen = 'a b c abc'`.

Similar to the previous, the output is an *m*-by-*n* numpy array, where *m* is the number of treatments in the fractional-factorial design. 
Each row corresponds to a single treatment, and each column contains the settings for a single factor, with floating point scalars ranging from -1 to +1.

##### Example
The following generates an eight-run fractional factorial design for four factors, in which the fourth factor is the product of the first three:

```python
>>> gen = 'a b c abc'
>>> dbox.fracfact(gen)

array([[-1, -1, -1, -1],
       [-1, -1,  1,  1],
       [-1,  1, -1,  1],
       [-1,  1,  1, -1],
       [ 1, -1, -1,  1],
       [ 1, -1,  1, -1],
       [ 1,  1, -1, -1],
       [ 1,  1,  1,  1]])
```

Note that more sophisticated generator strings can be created using the +" and "-" operators. The "-" operator will swap the column levels:

```python
>>> gen = 'a b c -abc'
>>> dbox.fracfact(gen)

array([[-1, -1, -1,  1],
       [-1, -1,  1, -1],
       [-1,  1, -1, -1],
       [-1,  1,  1,  1],
       [ 1, -1, -1, -1],
       [ 1, -1,  1,  1],
       [ 1,  1, -1,  1],
       [ 1,  1,  1, -1]])
```

#### fracfactgen

##### Description

The `fracfactgen` function uses the Franklin-Bailey algorithm to find generators for the smallest two-level fractional-factorial design.

It requires two inputs:
* `terms`: Is a string of factors formed formed from the 52 case-sensitive letters *a*-*Z*, separated by spaces.
Standard convention notation indicates to use 'a'-'z' for the first 26 factors, and, if necessary, 'A'-'Z' for the remaining factors. 
A valid example would be: `terms = 'a b c ab ac'`. 
Single-letter factors indicate the main effects to be estimated, whereas multiple-letter factors indicate the interactions to be estimated. 
You can pass the output generators of `fracfactgen` to `fracfact`, in order to produce the corresponding fractional-factorial design.
* `resolution`: Is an integer indicating the required resolution of the design. A design of resolution *R* is one in which no *n*-factor interaction is confounded with any other effect containing less than *R – n* factors. Thus, a resolution *III* design does not confound main effects with one another but may confound them with two-way interactions, while a resolution *IV* design does not confound either main effects or two-way interactions but may confound two-way interactions with each other. It is an optional argument, with the default value being equal to 3.

If `fracfactgen` is unable to find a design at the requested resolution, it tries to find a lower-resolution design sufficient to calibrate the model. If it is successful, it returns the generators for the lower-resolution design along with a warning. If it fails, an error is raised.

##### Example
The following will determine the effects of four two-level factors, for which there may be two-way interactions. A full-factorial design would require 2<sup>4</sup> = 16 runs. The `fracfactgen` function will generators for a resolution *IV* (separating main effects) fractional-factorial design that requires only 2<sup>3</sup> = 8 runs:


```python
>>> dbox.fracfactgen(terms = 'a b c d', resolution = 4)

'a b c abc'
```

### Response Surface Designs <a name="rsm"></a>

#### ccdesign

##### Description

Central Composite Designs (CCDs) are a type of experimental design useful in response surface methodology, for building a second order (quadratic) model for the response variable without needing to use a complete three-level factorial experiment. Such designs can be generated using the `ccdesign` function. 
It needs the following input arguments:

* `numFactors`: Number of factors in the design. Must be an integer at least equal to *2*.

The following optional arguments can be set:
*  `fraction`: Integer indicating the fraction of full-factorial cube, expressed as an exponent of 1/2. If not set by the user, the default values are the following:
    * 0, i.e. full factorial design, when `numFactors` &le; 4
    * 1, i.e. a 1/2 fraction design, when 4 <  `numFactors` &le;  7 or `numFactors` > 11
    * 2, i.e. a 1/4 fraction design, when 7 < `numFactors` &le;  9 
    * 3, i.e. a 1/8 fraction design, when `numFactors` = 10 
    * 4, i.e. a 1/16 fraction design, when `numFactors` = 11
* `centerPoints`: Number of center points to be added in the factorial and axial parts of the design.
    Can be one of:
    * 'orthogonal' (default): Number of center points will be computed so that an orthogonal design will be provided.
    * 'uniform'   : Number of center points will be computed so that uniform precision will be achieved.
    * A strictly positive integer, specifying the number of center points directly.
* `designType`: It defines the type of the CCD. 
    Can be one of:
    * 'circumscribed' (default): It is the original type of CCD, where axial points are located at distance *a* from the center point.
    * 'inscribed' : The inscribed CCD is characterized by that axial points are 
                    located at factor levels *−1* and *1*, while the factorial points are brought into the interior of the design space and are located at distance *1/a* from the center point.
    * 'faced': In a face-centered CCD, the axial points are located at a distance equal to *1* from the center point, i.e. at the face of the design cube if the design involves three experimental factors.

For *n > 2* factors, the output DoE matrix has dimensions *m* by *n*, with *m* being the number of runs in the design. 
Each row represents one run, with settings for all factors represented in the corresponding columns. The resulting factor values are normalized, so that the cube points take values between *-1* and *1*.

##### Example
The following generates a two-factor, full-factorial, circumscribed, orthogonal CCD:

```python
>>> dbox.ccdesign(numFactors = 2)

array([[-1.        , -1.        ],
       [-1.        ,  1.        ],
       [ 1.        , -1.        ],
       [ 1.        ,  1.        ],
       [-1.41421356, -0.        ],
       [ 1.41421356,  0.        ],
       [-0.        , -1.41421356],
       [ 0.        ,  1.41421356],
       [ 0.        ,  0.        ],
       [ 0.        ,  0.        ],
       [ 0.        ,  0.        ],
       [ 0.        ,  0.        ],
       [ 0.        ,  0.        ],
       [ 0.        ,  0.        ],
       [ 0.        ,  0.        ],
       [ 0.        ,  0.        ]])
```

#### bbdesign

##### Description

Box–Behnken designs are experimental designs also used in response surface methodology, for the estimation of second order (quadratic) models for the response variable.
Box-Behnken designs are considered to be more proficient and most powerful than CCD designs, despite their poor coverage of the corners of nonlinear design spaces.

This type of design can be generated using the `bbdesign` function, which takes the following input arguments:

* `numFactors`: Number of factors in the design. Must be an integer at least equal to *3*.
* `numCenter` : Number of centerpoints in the design. It is an optional argument, and if no input is provided, a pre-determined number of points are automatically included, whose number depends on the value of `numFactors`.

For *n > 2* factors, the output DoE matrix has dimensions *m* by *n*, with *m* being the number of runs in the design. 
Each row represents one run, with settings for all factors represented in the corresponding columns. The resulting factor values are normalized, so that the cube points thaveake values between *-1* and *1*.

The output matrix dBB is m-by-n, where m is the number of runs in the design. Each row represents one run, with settings for all factors represented in the columns. Factor values are normalized so that the cube points take values between -1 and 1.

##### Example
The following generates a two-factor, full-factorial, circumscribed, orthogonal CCD:

```python
>>> dbox.bbdesign(numFactors = 3)

array([[-1, -1,  0],
       [-1,  1,  0],
       [ 1, -1,  0],
       [ 1,  1,  0],
       [-1,  0, -1],
       [-1,  0,  1],
       [ 1,  0, -1],
       [ 1,  0,  1],
       [ 0, -1, -1],
       [ 0, -1,  1],
       [ 0,  1, -1],
       [ 0,  1,  1],
       [ 0,  0,  0],
       [ 0,  0,  0],
       [ 0,  0,  0]])
```

### Latin Hypercube Sampling <a name="lhs"></a>

#### lhs

##### Description
Latin Hypercube Sampling (LHS) is a statistical sampling technique used to efficiently explore the parameter space of a system or model. It is commonly employed in simulation studies, sensitivity analysis, and optimization problems.

In LHS, the range of each input variable or factor is divided into equally spaced intervals. Within each interval, a single sample point is randomly selected. The key feature of LHS is that it ensures that each level or bin of each factor occurs exactly once in the sampled dataset, providing a representative and evenly distributed coverage of the parameter space.

To generate a design of this type, the `lhs` function can be used.
Its input arguments include:
* `numSamples`  : Number of samples to be generated, specified as a positive integer.
* `numVariables`: Number of variables in the design, specified as a positive integer.

Additional optional arguments include:
* `criterion` : Criterion to be used to evaluate the improvement of the  design over each iteration. It can be one of:
    * 'maxdist' (default): Maximizes the minimum sample-to-sample distance.
    * 'mincorr': Minimize the sum of between-column squared correlations.
* `smooth`: Boolean indicator whether the points that will be produced 
    should be randomly distributed.
    * If `smooth = True` (default): One point from each of the
    intervals: (0, 1/*n*), (1/*n* , 2/*n*),
    (1-1/*n*, 1), will be sampled, with a subsequent random permutation.
    * If `smooth = False`:
    The points will produced by sampling only at the midpoints of the intervals, i.e. at  
    .5/*n*, 1.5/*n*, ..., 1 - .5/*n*,
    with *n* being the value of `numSamples` selected.
    The de

For *n* `numSamples` and *m* `numVariables`, the function returns a Latin hypercube sample matrix of size *n*-by-*m*. For each column of the output matrix, the *n* values are randomly distributed, with each one from the intervals defined according to the value of `smooth`.

##### Example

The following generates a Latin hypercube sample of ten rows (samples) and three columns (variables):

```python
>>> import numpy as np
>>> np.random.seed(10) # Set the seed for reproducibility
>>> dbox.lhs(numSamples = 10, numVariables = 3)

array([[0.75248678, 0.9707202 , 0.69357489],
       [0.60211809, 0.16602922, 0.45049514],
       [0.10229193, 0.35592262, 0.26817272],
       [0.8480203 , 0.24218636, 0.51460662],
       [0.49319027, 0.75354692, 0.32180509],
       [0.02813972, 0.8413978 , 0.99629056],
       [0.96493436, 0.44368093, 0.87002701],
       [0.54876658, 0.63265331, 0.08408063],
       [0.39495223, 0.06621841, 0.18919362],
       [0.28210972, 0.51141729, 0.7634635 ]])
```

Each column of the output matrix contains one random number in each interval [0,0.1], [0.1,0.2], [0.2,0.3], [0.3,0.4], [0.4,0.5], [0.5,0.6], [0.6,0.7], [0.7,0.8], [0.8,0.9], and [0.9,1].

To obtain a discrete design, the default value of `smooth` should be overwritten, and set to `False`:

```python
>>> import numpy as np
>>> np.random.seed(10) # Set the seed for reproducibility
>>> x = dbox.lhs(numSamples = 10, numVariables = 3, smooth = False)
>>> x 

array([[0.75, 0.85, 0.15],
       [0.05, 0.95, 0.55],
       [0.65, 0.55, 0.05],
       [0.35, 0.15, 0.45],
       [0.15, 0.25, 0.25],
       [0.25, 0.75, 0.65],
       [0.45, 0.05, 0.75],
       [0.95, 0.45, 0.95],
       [0.55, 0.35, 0.85],
       [0.85, 0.65, 0.35]])
```

To see the effect of changing the default `criterion`, first evaluate the sum the squared correlation of the *x* matrix above:

```python
>>> corr  = np.corrcoef(x, rowvar = False) 
>>> (sum(corr.flatten() ** 2) - 3)/2

0.07004591368227708
```

Subsequently, generating a new matrix with `criterion = mincorr`, the same evaluations result in a squared-correlation sum of:

```python
>>> np.random.seed(10)
>>> x = dbox.lhs(numSamples = 10, numVariables = 3, smooth = False, criterion = 'mincorr')
>>> corr  = np.corrcoef(x, rowvar = False) 
>>> (sum(corr.flatten() ** 2) - 3)/2

0.027731864095500214
```

As can be seen, minimizing the correlations results in a design with much lower sum of squared correlations.

## References

Good starting points for additional information on each experimental design type can be found on:

* [Factorial designs](https://en.wikipedia.org/wiki/Factorial_experiment)
* [Box-Behnken designs](https://en.wikipedia.org/wiki/Box%E2%80%93Behnken_design)
* [Central composite designs](https://en.wikipedia.org/wiki/Central_composite_design)
* [Latin-Hypercube designs](https://en.wikipedia.org/wiki/Latin_hypercube_sampling)

In addition, a wealth of information about DoE can be found on the [NIST](https://www.itl.nist.gov/div898/handbook/pri/pri.htm) website, including discussion on how to choose and analyze various DoEs, as well as several case studies.