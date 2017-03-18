import scipy as sp


def createLinks(jncs, diff):
    maxDiff = diff.max()
    linkedJncsInd = list()
    unlinkedInd = [ee.getIndex() for ee in jncs]
    numJnc = len(diff)

    # Create first link for shortest distance, and remove from list
    ind = list(sp.unravel_index(diff.argmin(), diff.shape))
    jnc = [ee for ee in jncs for kk in ind if ee.getIndex() == kk]
    jnc[0].addChildren([jnc[1]])
    jnc[1].setDist(diff[tuple(ind)])
    linkedJncsInd.extend(ind)
    unlinkedInd = [ee for ee in unlinkedInd if ee not in ind]

    while unlinkedInd:
        # find point with shortest distance to existing
        unusedDiff = diff[linkedJncsInd, :][:, unlinkedInd]
        ind = sp.unravel_index(unusedDiff.argmin(), unusedDiff.shape)
        newJncInd = unlinkedInd[ind[1]]
        ClosJncInd = linkedJncsInd[ind[0]]

        # get the closest junction
        CJ = [ee for ee in jncs if ee.getIndex() == ClosJncInd][0]

        # Determine which link to splice into
        possJnc = list()
        if CJ.parent:
            possJnc.append(CJ)
        possJnc.extend(CJ.getChildren())
        D01 = [jn.getDistance() for jn in possJnc]
        D02 = diff[newJncInd, [jn.parent.getIndex() for jn in possJnc]]
        D12 = diff[newJncInd, [jn.getIndex() for jn in possJnc]]
        D = sp.array([D01, D02, D12]).T
        chInd = spliceWhich(D)

        # get the actual points (junction)
        addPt = [ee for ee in jncs if ee.getIndex() == newJncInd][0]
        chld = possJnc[chInd]

        # must get distances to junctions associated to link, in correct order
        d02 = D[chInd, 1]  # to parent
        d12 = D[chInd, 2]  # to child

        # add the point to existing links
        newFork = appendLink(jncs, addPt, chld, d02, d12)

        linkedJncsInd.append(newJncInd)
        unlinkedInd.remove(newJncInd)

        # update linkList with first to new fork
        if newFork:
            newFork.setInd(numJnc)
            jncs.append(newFork)
            linkedJncsInd.append(numJnc)

            newDiff = maxDiff * sp.ones([numJnc + 1, numJnc + 1])
            newDiff[0:numJnc, 0:numJnc] = diff
            for jn in list([chld, newFork, addPt]):
                newDiff[jn.getIndex(), jn.parent.getIndex()] = jn.getDistance()
                newDiff[jn.parent.getIndex(), jn.getIndex()] = jn.getDistance()

            d0f = newFork.getDistance()
            d1f = chld.getDistance()
            ind0 = newFork.parent.getIndex()
            ind1 = chld.getIndex()
            for indJ in unlinkedInd:
                d02 = diff[ind0, indJ]
                d12 = diff[ind1, indJ]
                dnf = dist2Fork(d0f, d1f, d02, d12)
                newDiff[indJ, numJnc] = dnf
                newDiff[numJnc, indJ] = dnf
            numJnc += 1
            diff = newDiff

    return jncs


def spliceWhich(D):
    # return the index of best one to splice
    # D is a 2D array, each row composed of [d01[kk],d02[kk],d12[kk]]
    x = sp.array([spliceLoc(D[kk, 0], D[kk, 1], D[kk, 2])[0]
        for kk in range(len(D[:, 0]))])

    indBW = [kk for kk, xx in enumerate(x) if 0 < xx < D[kk, 0]]
    if indBW:
        tmp = [(kk, D[kk, 0] - xx) for kk, xx in enumerate(x) if kk in indBW]
    else:
        tmp = [(kk, xx) for kk, xx in enumerate(x) if kk not in indBW]
    ind = tmp[sp.array(tmp)[:, 1].argmin()][0]

    return ind


def spliceLoc(d01, d02, d12):
    d0f = (d02 + d01 - d12) / 2  # x (parent to fork)
    d1f = (d01 + d12 - d02) / 2  # d01-x (child to fork)
    d2f = (d02 + d12 - d01) / 2  # y (new to fork)
    return (d0f, d1f, d2f)


def appendLink(jncs,addPt,jnc1,d02,d12):
    #
    #      |<--x-->|
    #      O=======F====1
    #              |
    #              |
    #              |
    #              2

    # get parent junction
    jnc0 = jnc1.parent
    # get distance to parent junction
    d01 = jnc1.getDistance()

    d0f, d1f, d2f = spliceLoc(d01, d02, d12)

    newFork = None

    if(d0f == 0):
        # connect to 0 (parent)
        jnc0.addChildren(addPt)
        addPt.setDist(d2f)
    elif(d1f == 0):
        # connect to 1 (child)
        jnc1.addChildren(addPt)
        addPt.setDist(d2f)
    elif(d2f == 0):
        # In between, on the the current link
        # This shouldn't happen if doing them in order of shortest to longst
        jnc1.forkAbove(addPt)
        addPt.setDist(d0f)
        jnc1.setDist(d1f)
    else:
        # fork
        from .class_junction import Fork
        newFork = Fork()
        jnc1.forkAbove(newFork, addPt)
        newFork.setDist(d0f)
        jnc1.setDist(d1f)
        addPt.setDist(d2f)

    return (newFork)


def dist2Fork(d0f, d1f, d02, d12):
    # get the distance to a new fork that splits a link
    #  d0f, d1f distances from fork to end points that are split by fork
    #  d02, d12 distances from pt in question to end points
    #  d2f distance from pt in question to the fork
    #
    #      |<-x->|
    #      O========F======1
    #            |
    #            |
    #            |
    #            2

    x = spliceLoc(d0f + d1f, d02, d12)[0]
    if(x <= 0):
        d2f = (d02 + d12 + d0f - d1f) / 2
    elif(x >= d0f + d1f):
        d2f = (d02 + d12 + d1f - d0f) / 2
    elif(x <= d0f):
        d2f = d12 - d1f
    else:
        d2f = d02 - d0f

    return d2f