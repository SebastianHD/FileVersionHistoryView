import scipy as sp
from .class_junction import Point
from .visualize import visualize
from .linkPoints import createLinks
from .organizeJunctions import organizeJunctions
import os


def main(theDir, theFile):
    import Levenshtein as lev
    # unfortunately, difflib gives results that depend on order of files
    import glob

    # get all files
    fileList = glob.glob("%s/%s*[!~]" % (theDir, theFile))
    fileList = sorted(fileList, key=os.path.getsize)
    names = [os.path.splitext(os.path.basename(ff))[0] for ff in fileList]
    names = [str.replace(theFile, '') for str in names]
    numFil = len(fileList)

    jncInd = range(numFil)
    diff = sp.zeros((numFil, numFil))
    TBD = list()
    for kk in range(0, numFil):
        # open File
        f = open(fileList[kk], 'r')
        # Read file, converting all tabs, newlines, form feeds,
        # multiple spaces to single space
        ver1 = " ".join(f.read().split())
        for jj in range(kk + 1, numFil):
            # open File
            f = open(fileList[jj], 'r')
            # Read file, converting all tabs, newlines, form feeds,
            # multiple spaces to single space
            ver2 = " ".join(f.read().split())
            # calculate char-by-char % match
            p = lev.ratio(ver1, ver2)
            # calculate number of different characters
            numDiff = round((len(ver1) + len(ver2)) * (1 - p))
            diff[kk, jj] = numDiff
            diff[jj, kk] = numDiff
            # remove equivalent files
            if(numDiff == 0 and jj in jncInd):
                TBD.append(jj)

    # ignore zero distance (change them so that dist is far
    #  away and they will be ignored)
    maxDiff = 10 * diff.max()
    for jj in TBD:
        jncInd.remove(jj)
        diff[:, jj] = maxDiff
        diff[jj, :] = maxDiff
    for kk in range(0, numFil):
        diff[kk, kk] = maxDiff

    # create the points
    jncs = [Point(kk, names[kk]) for kk in jncInd]

    # link them
    jncs = createLinks(jncs, diff)

    # Organize the junction locations for best visual appearance
    organizeJunctions(jncs)

    # make a plot
    visualize(jncs)



