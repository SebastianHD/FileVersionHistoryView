from class_junction import Point

def visualize(jncs):
    #temporary copy paste from internet (not checked)
    import numpy as np
    import pylab as pl
    import matplotlib.pyplot as plt
    from matplotlib import collections as mc

    fs = 14

    lines = list()

    fig, ax = pl.subplots()
    for jn in jncs:
        print(jn.getIndex())
        if jn.parent:
            loc2 = jn.getLocation()
            loc1 = jn.parent.location #for some reason this needs to be calculated after the other one, but this doesnt make sense
            lines.append([loc1, loc2])

        if(isinstance(jn, Point)):
            plt.scatter(jn.getLocation()[0], jn.getLocation()[1], marker='o',
                s=fs ** 2 / 2, label='%d: %s' % (jn.getIndex(), jn.getName()))
        else:
            plt.scatter(jn.getLocation()[0], jn.getLocation()[1], color='red',
                marker='o', s=fs ** 2 / 2, label='%d: fork' % jn.getIndex())

        numTot = jn.numConnected()
        strtAng = jn.orientation
        th = strtAng + 2 * np.pi / numTot
        offset = (fs * np.cos(th), fs * np.sin(th))
        plt.annotate('%d' % (jn.getIndex()), xy=tuple(jn.getLocation()),
            xytext=tuple(map(sum, zip((-fs / 2, -fs / 2), offset))),
            fontsize=fs, textcoords='offset points')

    print 'numLines', len(lines)
    print lines
    lc = mc.LineCollection(lines, linewidths=2)
    ax.add_collection(lc)
    ax.legend(loc='upper left', fontsize=fs)
    ax.autoscale()
    ax.margins(0.1)
    plt.axis('equal')
    plt.ion()
    plt.show()

