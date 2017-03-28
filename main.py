import scipy as sp
from class_junction import Point
from visualize import visualize
from linkPoints import createLinks
from organizeJunctions import organizeJunctions
import os


def getLines(fileName, ignLinBeg, ignLinEnd):
    import re
    with open(fileName, 'r') as f:
        lines = f.readlines()
    numLin = len(lines)
    lines = [
        re.sub('[\s+]', ' ', ll).strip()
        for ll in lines[0+ignLinBeg:numLin-ignLinEnd]]
    return [ll for ll in lines if ll]


def keepCommon(allLines):
    commLines = set.intersection(*[set(ll) for ll in allLines])

    keepLines = list()
    for AL in allLines:
        linNum = [kk for kk, ll in enumerate(AL) if ll in list(commLines)]
        keepLines.append(AL[min(linNum):max(linNum)+1])
    return keepLines


def numCharDiff(theStrs):
    import Levenshtein as lev
    p = lev.ratio(theStrs[0], theStrs[1])
    return round((len(theStrs[0]) + len(theStrs[1])) * (1 - p))


def main(theDir, theFile, tfCutEnds=False, ignLinBeg=0, ignLinEnd=0):
    # unfortunately, difflib gives results that depend on order of files
    import glob
    import multiprocessing
    from itertools import combinations
    import scipy.spatial.distance as spsd

    # get all files
    fileList = glob.glob("%s/%s*[!~]" % (theDir, theFile))
    fileList = sorted(fileList, key=os.path.getsize)
    names = [os.path.splitext(os.path.basename(ff))[0] for ff in fileList]
    names = [str.replace(theFile, '') for str in names]
    numFil = len(fileList)

    if(numFil < 3):
        print('Found less than three files, there is no point continuing.')
        return

    # read in all of the files
    print('Reading Files ...')
    allLines = map(
        getLines, fileList, [ignLinBeg] * numFil, [ignLinEnd] * numFil)

    if(tfCutEnds):
        print('Stripping uncommon portions at beginning and end ...')
        # Start and End with lines that are common to all
        allLines = keepCommon(allLines)
    allLines = [' '.join(ll) for ll in allLines]

    print('Removing duplicates ... ')
    allLines, uind = sp.unique(allLines, return_index=True)
    dups = list(set(range(numFil)) - set(uind))
    for dd in list(dups):
        print(('Ignoring file: %s' % names[dd]))

    if(len(uind) < 3):
        print('Less than three unique sections, there is no point continuing.')
        for uu in list(uind):
            print(('Unique file: %s' % names[uu]))
        return

    fileCombos = combinations(allLines, 2)

    print('Calculating Levenshtein difference ...')
    pool = multiprocessing.Pool()
    ps = pool.map(numCharDiff, fileCombos)
    diff = spsd.squareform(ps)

    # ignore zero distance to self by setting it to something large
    theMax = 10 * diff.max()
    diff[range(len(uind)), range(len(uind))] = theMax

    # create the points
    jncs = [Point(kk, names[uu]) for kk, uu in enumerate(uind)]

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

