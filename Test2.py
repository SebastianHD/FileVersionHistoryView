#from class_AVLT import AVLT
from class_junction import *

#T = AVLT()

#T.put(4,Point(4))
#print T.root.key
#T.put(7,Point(2))
#print T.root.key
#T.put(6,Point(1))
#print T.root.key
#print T.root.leftChild.key
#print T.root.rightChild.key

#print T
#print [ee.getIndex() for ee in T.sort()]


pts = [Point(kk) for kk in range(8)]

for pt in pts:
    pt.distance = 5

pts[1].updateParent(pts[0])
print[ ee.parent.getIndex() if ee.parent is not None else '' for ee in pts ], [[ee.getIndex() for ee in jj.children] for jj in pts]

pts[2].updateParent(pts[1])
print[ ee.parent.getIndex() if ee.parent is not None else '' for ee in pts ], [[ee.getIndex() for ee in jj.children] for jj in pts]

pts[3].updateParent(pts[1])
print[ ee.parent.getIndex() if ee.parent is not None else '' for ee in pts ], [[ee.getIndex() for ee in jj.children] for jj in pts]

pts[3].forkAbove(pts[4],pts[5:8])
print[ ee.parent.getIndex() if ee.parent is not None else '' for ee in pts ], [[ee.getIndex() for ee in jj.children] for jj in pts]

print('isupdated', [ee.isUpdated for ee in pts])
locs = [ pt.getLocation() for pt in pts ]

pts[6].addChildren(pts[7])
print[ ee.parent.getIndex() if ee.parent is not None else '' for ee in pts ], [[ee.getIndex() for ee in jj.children] for jj in pts]
print('isupdated', [ee.isUpdated for ee in pts])
locs = [ pt.getLocation() for pt in pts ]

print [ee.getIndex() for ee in pts[4].getLinked(None)]

#import matplotlib.pyplot as plt

#for ii,lc in enumerate(locs):
    #plt.scatter(lc[0], lc[1], marker='o', s=12,label='%d: %s' % (pts[ii].getIndex(), pts[ii].getName()))
    #plt.annotate('%d'%(pts[ii].getIndex()), xy = tuple(lc), xytext = (0,0),fontsize=12, textcoords = 'offset points')
#plt.show()