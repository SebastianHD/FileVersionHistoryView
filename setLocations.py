#Define the junction locations recursively
import scipy as sp

def setLocations(jncs):
    locs = [jn.getLocation() for jn in jncs]
    #should optimize child order here


def longDist(jncs):
    from scipy.spatial.distance import pdist, squareform
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