import scipy as sp
from class_junction import *
from visualize import *
from linkPoints import createLinks
from setLocations import *
import os


def main(theDir, theFile):
    import Levenshtein as lev
    #unfortunately, difflib gives results that depend on order of files
    import glob

    #get all files
    fileList = glob.glob("%s/%s*[!~]" % (theDir, theFile))
    fileList = sorted(fileList, key=os.path.getsize)
    names = [os.path.splitext(os.path.basename(ff))[0] for ff in fileList]
    names = [str.replace(theFile, '') for str in names]
    numFil = len(fileList)

    jncInd = range(numFil)
    diff = sp.zeros((numFil, numFil))
    TBD = list()
    for kk in range(0, numFil):
        #open File
        f = open(fileList[kk], 'r')
        #Read file, converting all tabs, newlines, form feeds,
        # multiple spaces to single space
        ver1 = " ".join(f.read().split())
        for jj in range(kk + 1, numFil):
            #open File
            f = open(fileList[jj], 'r')
            #Read file, converting all tabs, newlines, form feeds,
            # multiple spaces to single space
            ver2 = " ".join(f.read().split())
            #calculate char-by-char % match
            p = lev.ratio(ver1, ver2)
            #calculate number of different characters
            numDiff = round((len(ver1) + len(ver2)) * (1 - p))
            diff[kk, jj] = numDiff
            diff[jj, kk] = numDiff
            #remove equivalent files
            if(numDiff == 0 and jj in jncInd):
                TBD.append(jj)

    #ignore zero distance (change them so that dist is far
    # away and they will be ignored)
    #diff[diff==0] = 10*diff.max()
    maxDiff = 10 * diff.max()
    for jj in TBD:
        jncInd.remove(jj)
        diff[:, jj] = maxDiff
        diff[jj, :] = maxDiff
    for kk in range(0, numFil):
        diff[kk, kk] = maxDiff

    print TBD
    print jncInd

    #create the points
    jncs = [Point(kk, names[kk]) for kk in jncInd]

    #link them
    jncs = createLinks(jncs, diff)

    #determine location of junctions based on links
    setLocations(jncs)

    for jn in jncs:
        print('jnc: %d, parent: %s, dist: %2.1f' % (
            jn.getIndex(),
            [jn.parent.getIndex() if jn.parent else jn.parent][0],
            jn.getDistance()))

    #make a plot
    visualize(jncs)

    import random
    for jn in jncs:
        numC = jn.numChildren()
        ind = list(range(numC))
        random.shuffle(ind)
        jn.updateOrder(ind)

    for jn in jncs:
        print jn.getIndex(), jn.isUpdated
    visualize(jncs)

    for jn in jncs:
        numC = jn.numChildren()
        ind = list(range(numC))
        random.shuffle(ind)
        jn.updateOrder(ind)
    visualize(jncs)

theDir = "/home/sebatian/Desktop/manipulate/"
theFile = 'stat_solve'
main(theDir, theFile)

