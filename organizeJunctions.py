# Find the best organization of junction locations,
#  by spreading them out
import scipy as sp


def organizeJunctions(jncs):
    # Determine which method is optimal,
    #  for small data sets, just run brute force

    # determine number of possible combinations
    # numPerm = [sp.math.factorial(num) for num in numChld]
    # numTot = sp.prod(numPerm)

    # currently have no other option than to do brute force method
    bruteForce(jncs)


def bruteForce(jncs):
    import itertools

    # get number of children
    numChld = [jn.numChildren() for jn in jncs]

    # generate list of tuples representing all posibilities
    perms = [list(itertools.permutations(range(nn))) for nn in numChld]
    allPoss = list(itertools.product(*perms))

    # loops through all possible combinates calculating fitness function
    bestfit = (0, 0)
    for jj, pp in enumerate(allPoss):
        for kk, jn in enumerate(jncs):
            jn.updateOrder(list(pp[kk]))
        fit = fitScore(jncs)
        if(fit > bestfit[1]):
            bestfit = (jj, fit)

    for kk, jn in enumerate(jncs):
            pp = allPoss[bestfit[0]]
            jn.updateOrder(list(pp[kk]))


def fitScore(jncs):
    # caluclate the fitness score
    return longDist(jncs) + sp.sqrt(4 * area(jncs))


def longDist(jncs):
    from scipy.spatial.distance import pdist
    # Determine the maximum (euclidian) distance between collection of pts

    # get pts
    pts = [ee.getLocation() for ee in jncs]

    # calculate distance
    return max(pdist(pts))


def area(jncs):
    from scipy.spatial import ConvexHull
    # Get the area of convex hull enclosing points (2D)

    # get pts
    pts = [ee.getLocation() for ee in jncs]

    # calculate convex hull of pts
    hull = ConvexHull(pts)

    return hull.volume