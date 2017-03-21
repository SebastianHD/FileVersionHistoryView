from class_junction import Point


def visualize(jncs):
    # temporary copy paste from internet (not checked)
    import numpy as np
    import pylab as pl
    import matplotlib.pyplot as plt
    from matplotlib import collections as mc

    fs = 14

    lines = list()

    fig, ax = pl.subplots()
    for jn in jncs:
        if jn.parent:
            lines.append([jn.parent.getLocation(), jn.getLocation()])

        if(isinstance(jn, Point)):
            plt.scatter(jn.getLocation()[0], jn.getLocation()[1], marker='o',
                s=fs ** 2 / 2, label='%d: %s' % (jn.getIndex(), jn.getName()))
        else:
            plt.scatter(jn.getLocation()[0], jn.getLocation()[1], color='red',
                marker='o', s=fs ** 2 / 2, label='%d: fork' % jn.getIndex())

        plt.annotate('%d' % (jn.getIndex()),
            xy=tuple(jn.getLocation()), xytext=tuple(jn.getLabelLocation(fs)),
            fontsize=fs, textcoords='offset points',horizontalalignment='center',
            verticalalignment='center')

    lc = mc.LineCollection(lines, linewidths=2)
    ax.add_collection(lc)
    ax.legend(loc='upper left', fontsize=fs)
    ax.autoscale()
    ax.margins(0.1)
    plt.axis('equal')
    plt.show()

