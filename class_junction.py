import numpy as np


class Junction(object):
    def __init__(self, ind, par=None):
        self.ind = ind
        self.parent = par
        self.children = set()
        self.childOrder = []
        self.location = [0, 0]
        self.orientation = 0
        self.isUpdated = False
        self.distance = 0  # distance to parent

    def isRoot(self):
        if self.parent is None:
            return True
        else:
            return False

    def hasChildren(self):
        if not self.children:
            return False
        else:
            return True

    def numChildren(self):
        return len(self.children)

    def numConnected(self):
        return self.numChildren() + (not self.isRoot())

    def getDistance(self):
        return self.distance

    def setDist(self, dist):
        self.distance = dist

    def needUpdate(self):
        self.isUpdated = False
        for ch in self.getChildren():
            ch.needUpdate()

    def indOrder(self, chld):
        #consider parent a link, so add one if not root
        ind = [self.childOrder[ii] for ii, cc in enumerate(self.children)
            if cc == chld][0] + (not self.isRoot())
        return ind

    def updateOrder(self, ind):
        if not ind or self.numChildren() == 0:
            return
        ind.extend(range(self.numChildren()))  # ensure that all will be present
        uind = []
        [uind.append(it) for it in ind if it not in uind]  # drop repeats
        self.childOrder = ind[0:self.numChildren()]  # take first n
        self.needUpdate()

    def setLocation(self):
        if self.isRoot():
            self.location = np.array([0, 0])
            self.orientation = np.pi
        else:
            pp = self.parent
            ind = pp.indOrder(self)
            numTot = pp.numConnected()
            strtPos = pp.getLocation()
            ang = pp.orientation + np.pi + 2 * np.pi * ind / numTot
            self.location = strtPos + \
                self.distance * np.array([np.cos(ang), np.sin(ang)])
            self.orientation = np.mod(ang, 2 * np.pi)

        self.isUpdated = True

    def getLocation(self):
        if not self.isUpdated:
            print('%d: updating location from %d, %d' % (self.getIndex(), self.location[0], self.location[1]))
            self.setLocation()
        print('%d: is up to date to %d, %d' % (self.getIndex(), self.location[0], self.location[1]))
        return self.location

    def getName(self):
        return self.name

    def getIndex(self):
        return self.ind

    def updateParent(self, newParent):
        oldParent = self.parent
        if oldParent is not None:
            oldParent._removeChildren(self)
            oldParent.needUpdate()

        self.parent = newParent
        newParent._addChildren(self)
        newParent.needUpdate()

    def _addChildren(self, child):
        #internal helper function
        #adds the associated children to the current junction
        try:
            self.children.update(child)
        except TypeError:
            self.children.add(child)

        #since order will not be preseved in the set, might as well newly index
        self.childOrder = range(self.numChildren())


    def addChildren(self, childs):
        #adds the associated children to the current junction
        #expect childs to be list, but single elements will work also
        try:
            for ch in childs:
                ch.updateParent(self)
        except TypeError:
            childs.updateParent(self)

    def _removeChildren(self, childs):
        #removes the childs from the current junction
        #expect childs to be list, but single elements will work also
        try:
            for ll in childs:
                self.children.remove(ll)
        except TypeError:
            self.children.remove(childs)

        #since order will not be preseved in the set, might as well newly index
        self.childOrder = range(self.numChildren())

    def forkAbove(self, fork, childs=[]):
        #fork between current and parent
        #try:
            fork.updateParent(self.parent)
            self.updateParent(fork)
            try:
                for ch in childs:
                    ch.updateParent(fork)
            except TypeError:
                childs.updateParent(fork)
        #except:
        #    pass

    def getChildren(self, ignoreChilds=None):
        #return a list of all children not given in ignore list
        #expect ignoreChilds to be list, but single elements will work also
        try:
            return list(self.children.difference(set(ignoreChilds)))
        except TypeError:
            return list(self.children.difference(set([ignoreChilds])))

    def getLinked(self, ignoreJncs=[]):
        #return a list of all juncs that are linked and not given in ignore list
        #expect ignoreJncs to be list, but single elements will work also
        tmp = self.getChildren(ignoreJncs)
        try:
            tmp.update([self.parent] if self.parent not in ignoreJncs else [])
        except TypeError:
            tmp.update([self.parent] if self.parent not in [ignoreJncs] else [])
        return tmp


class Point(Junction):
    def __init__(self, ind, name=''):
        #python 2 super(whos line are we searching, where are we in the line)
        super(Point, self).__init__(ind)
        self.name = name


class Fork(Junction):
    def __init__(self, ind=0):
        super(Fork, self).__init__(ind)

    def setInd(self, ind):
        self.ind = ind