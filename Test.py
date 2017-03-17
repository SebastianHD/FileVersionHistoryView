import scipy as sp
from junction import *
from link import *
from visualize import *
from linkPoints import createLinks
from setLocations import *
import os


#def main(theDir,theFile):
    #import Levenshtein as lev
    ##import difflib #unfortunately, this gives results that depend on order of files
    #import glob

    ##get all files
    #fileList = glob.glob("%s/%s*[!~]" % (theDir, theFile))
    #fileList = sorted(fileList, key=os.path.getsize)
    #names = [os.path.splitext(os.path.basename(ff))[0] for ff in fileList]
    #names = [str.replace(theFile, '') for str in names]

    #order = sp.array(names).argsort()
    #print order
    #numFil = len(fileList)

    #jncInd = range(numFil)
    #diff = sp.zeros((numFil,numFil))
    #delta = sp.zeros((numFil*(numFil-1)/2,4),int)
    #count = 0
    #for kk in range(numFil):
        ##open File
        #f = open(fileList[kk], 'r')
        ##Read file, converting all tabs, newlines, form feeds, multiple spaces to single space
        #ver1=" ".join(f.read().split())
        #for jj in range(kk+1,numFil):
            ##open File
            #f = open(fileList[jj], 'r')
            ##Read file, converting all tabs, newlines, form feeds, multiple spaces to single space
            #ver2=" ".join(f.read().split())
            ##calculate char-by-char % match
            #p = lev.ratio(ver1,ver2)
            ##calculate number of different characters
            #numDiff1 = round((len(ver1)+len(ver2))*(1-p))
            ##calculate char-by-char % match
            #p = lev.ratio(ver2,ver1)
            ##calculate number of different characters
            #numDiff2 = round((len(ver1)+len(ver2))*(1-p))
            #diff[kk,jj] = numDiff1
            #diff[jj,kk] = numDiff2
            #delta[count,:] = [jj,kk,numDiff1,numDiff2]
            #count += 1


    ##diff[order,:][:,order]
    ##print diff

    ##sort
    #indS = sp.squeeze(delta[:,2].argsort())

    #sp.set_printoptions(threshold=sp.nan)

    #print([dd[0:2] for dd in delta if dd[2] != dd[3] ])
    #print(delta[indS,:])

#theDir = "/home/sebatian/Desktop/manipulate/"
#theFile = 'stat_solve'
#main(theDir,theFile)

def main():
    jncs = [Point(kk,'name') for kk in range(5)]

    for jj in jncs:
        jj.setLocation(sp.squeeze((5*sp.rand(1,2)).tolist()))

    from linkPoints import area, longDist

    s = '''
from junction import Point
from linkPoints import area, longDist
import scipy as sp
jncs = [Point(kk,'name') for kk in range(50)]
for jj in jncs:
    jj.setLocation(sp.squeeze((5*sp.rand(1,2)).tolist()))
    '''
    import timeit
    t = sp.median(timeit.Timer(stmt='area(jncs)',setup=s).repeat(10,1000))*1000
    print '%d usec per call' % (t)

    #print longDist(jncs)
    #print(area(jncs))

main()

#import timeit
#t = timeit.Timer(stmt='main()')
#t.timeit(number=10)

#timeit.timeit(stmt='main()', number=10)