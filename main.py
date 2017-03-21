import scipy as sp
from class_junction import Point
from visualize import visualize
from linkPoints import createLinks
from organizeJunctions import organizeJunctions
import os


def main(theDir, theFile, ignLinBeg=0, ignLinEnd=0):
    import Levenshtein as lev
    # unfortunately, difflib gives results that depend on order of files
    import glob

    # get all files
    fileList = glob.glob("%s/%s*[!~]" % (theDir, theFile))
    fileList = sorted(fileList, key=os.path.getsize)
    names = [os.path.splitext(os.path.basename(ff))[0] for ff in fileList]
    names = [str.replace(theFile, '') for str in names]
    numFil = len(fileList)

    jncInd = list(range(numFil))
    diff = sp.zeros((numFil, numFil))
    TBD = set()
    for kk in range(0, numFil):
        print(('Calculating differences for: %s' % names[kk]))
        # open File
        f = open(fileList[kk], 'r')
        # Read file, converting all tabs, newlines, form feeds,
        # multiple spaces to single space
        lines = f.readlines()
        numLin = len(lines)
        theStr = ''.join(lines[0+ignLinBeg:numLin-ignLinEnd])
        ver1 = " ".join(theStr.split())
        for jj in range(kk + 1, numFil):
            # open File
            f = open(fileList[jj], 'r')
            # Read file, converting all tabs, newlines, form feeds,
            # multiple spaces to single space
            lines = f.readlines()
            numLin = len(lines)
            theStr = ''.join(lines[0+ignLinBeg:numLin-ignLinEnd])
            ver2 = " ".join(theStr.split())
            # calculate char-by-char % match
            p = lev.ratio(ver1, ver2)
            # calculate number of different characters
            numDiff = round((len(ver1) + len(ver2)) * (1 - p))
            diff[kk, jj] = numDiff
            diff[jj, kk] = numDiff
            # remove equivalent files
            if(numDiff == 0 and jj in jncInd):
                TBD.add(jj)

    # ignore zero distance (change them so that dist is far
    #  away and they will be ignored)
    maxDiff = 10 * diff.max()
    for jj in TBD:
        diff[:, jj] = maxDiff
        diff[jj, :] = maxDiff
    jncInd = [ind for kk, ind in enumerate(jncInd) if kk not in TBD]
    for kk in range(0, numFil):
        diff[kk, kk] = maxDiff

    # create the points
    jncs = [Point(kk, names[kk]) for kk in jncInd]

    # link them
    jncs = createLinks(jncs, diff)

    # Organize the junction locations for best visual appearance
    organizeJunctions(jncs)

    # print the files list with index
    for jn in jncs:
        if jn.parent:
            pnt = '%3d' % jn.parent.getIndex()
        else:
            pnt = '---'
        if isinstance(jn, Point):
            name = jn.getName()
        else:
            name = 'fork'
        print((
            'ind: %3d, parent: %s:, dist: %7d name: %s' %
            (jn.getIndex(), pnt, jn.getDistance(), name)))

    # make a plot
    visualize(jncs)


main('/media/sebatian/Backup/RECOVER/functions_rest/theFuncs', 'stat_tokenizer',1,1)