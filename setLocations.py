#Define the junction locations recursively
import scipy as sp

def bruteFitness(jncs):

<<<<<<< HEAD
=======
    #get number of children
    numC = [jn.numChildren for jn in jncs]

>>>>>>> AddBruteForceFitness
    #determine all possible combinations

    #loops through all possible combinates calculating fitness function
    fit = longDist(jncs) + area(jncs)

def longDist(jncs):
    from scipy.spatial.distance import pdist
    #Determine the maximum (euclidian) distance between collection of pts

    #get pts
    pts = [ee.getLocation() for ee in jncs]

    #calculate distance
    return max(pdist(pts))


def area(jncs):
    from scipy.spatial import ConvexHull
    #Get the area of convex hull enclosing points (2D)

    #get pts
    pts = [ee.getLocation() for ee in jncs]

    #calculate convex hull of pts
    hull = ConvexHull(pts)

    return hull.volume