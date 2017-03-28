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

    # get number of children and total connections
    numChld = [jn.numChildren() for jn in jncs]
    numLnks = [jn.numConnected() for jn in jncs]

    # determine number of permutations
    numTot = sp.prod([sp.math.factorial(num) for num in numChld])
    print(('Organizing Junctions. Checking %d permuations.' % numTot))

    # generate list of tuples representing all posibilities
    perms = [list(itertools.permutations(list(range(nn)))) for nn in numChld]
    allPoss = itertools.product(*perms)
    # all possible combinates calculating fitness function for junctions
    bestfit = (0, None)
    for jj, pp in enumerate(allPoss):
        for kk, jn in enumerate(jncs):
            jn.updateOrder(list(pp[kk]))
        pts = locJunctions(jncs)
        fit = fitScore(pts)
        if(fit > bestfit[0]):
            bestfit = (fit, pp)
            print(('%d of %d: %3.2f' % (jj, numTot, fit)))

    for kk, jn in enumerate(jncs):
        jn.updateOrder(list(bestfit[1][kk]))

    # First, get the important labels (otherwise too many to check)
    impPts = importantLocs(jncs)
    bestfit = 0
    checkedPts = list()
    for ptLoc in impPts:
        clsInd = nearbyJunctions(jncs, ptLoc)
        redNumLnks = [
            nn if kk in clsInd else 1 for kk, nn in enumerate(numLnks)]
        tfChange = [True if nn > 1 else False for nn in redNumLnks]
        currLabelPosInd = [jn.labelPos for jn in jncs]
        newPos = currLabelPosInd
        numTot = sp.prod(redNumLnks)
        chngPts = [jncs[kk].getIndex() for kk, tf in enumerate(tfChange) if tf]
        if not any([chngPts == dd for dd in checkedPts]):
            checkedPts.append(chngPts)
            print((
                'Organizing Labels for junctions %s. Checking %d permuations.'
                % (', '.join([str(nn) for nn in chngPts]), numTot)))

            # create generator representing all posibilities
            perms = [list(range(nn)) for nn in redNumLnks]
            allPoss = itertools.product(*perms)
            # all possible permutations calculating fitness function for labels
            for jj, pp in enumerate(allPoss):
                [jn.setLabelPos(pp[kk])
                    for kk, jn in enumerate(jncs) if tfChange[kk]]
                pts = locAll(jncs)
                fit = fitScore(pts, False)
                if(fit > bestfit):
                    newPos = [
                        pp[kk] if tfChange[kk] else currLabelPosInd[kk]
                        for kk, jn in enumerate(jncs)]
                    bestfit = fit
                    print(('%d of %d: %3.5f' % (jj, numTot, fit)))
            # set the best combination
            [jn.setLabelPos(newPos[kk]) for kk, jn in enumerate(jncs)]



def locJunctions(jncs):
    return [ee.getLocation() for ee in jncs]


def locJunctionsLabels(jncs):
    return [ee.getLocation()+ee.getLabelLocation() for ee in jncs]


def locAll(jncs):
    loc = locJunctions(jncs)
    loc.extend(locJunctionsLabels(jncs))
    return loc


def fitScore(pts, tfglobal=True):
    # caluclate the fitness score
    if(tfglobal):
        return longDist(pts) + sp.sqrt(2 * area(pts))
    else:
        return shortDist(pts)


def longDist(pts):
    from scipy.spatial.distance import pdist
    # Determine the maximum (euclidian) distance between collection of pts

    # calculate distance
    return max(pdist(pts))


def shortDist(pts):
    from scipy.spatial.distance import pdist
    # Determine the "average distance" with closer ones weighted more

    # calculate distance
    d = pdist(pts)
    w = pow(d, -1)
    return sum(w*d)/sum(w)


def importantLocs(jncs, fracDistKeep=.04):
    from scipy.spatial.distance import pdist
    import itertools

    pts = locJunctionsLabels(jncs)
    dist = pdist(pts)
    maxDist = max(dist)

    ptIndComb = list(itertools.combinations(list(range(len(pts))), 2))
    indS = list(sp.array(dist).argsort())

    midPts = [
        (pts[ptIndComb[kk][0]] + pts[ptIndComb[kk][1]] + 0.) / 2
        for kk in indS if dist[kk] < fracDistKeep*maxDist]

    return midPts


def nearbyJunctions(jncs, loc, fracDistKeep=.04):
    # find the junctions are are closest to a point
    # return index of junctions that are within specified distance

    pts = locJunctions(jncs)
    dist = [sp.sqrt(sum((pt - loc) ** 2)) for pt in pts]
    maxDist = max(dist)

    return [kk for kk, dd in enumerate(dist) if dd < fracDistKeep*maxDist]


def area(pts):
    from scipy.spatial import ConvexHull
    # Get the area of convex hull enclosing points (2D)

    # check if collinear
    tfcollinear = True
    eps = sp.finfo(float).eps
    for kk in range(2, len(pts)):
        if(
         pts[0][0] * (pts[1][1] - pts[kk][1]) +
         pts[1][0] * (pts[kk][1] - pts[0][1]) +
         pts[kk][0] * (pts[0][1] - pts[1][1]) > eps):
            tfcollinear = False
            break

    # calculate convex hull of pts
    if tfcollinear:
        area = 0
    else:
        hull = ConvexHull(pts)
        area = hull.volume

    return area
