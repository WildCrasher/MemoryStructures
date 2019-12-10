import matplotlib.pyplot as plt
import numpy as np


def plot_result(x, y, labels, colors, title=""):
    fig = plt.figure()
    ax = plt.subplot(111)
    for i in range(0, len(y)):
        ax.plot(x, y[i], colors[i], label=labels[i])
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_ylabel('time [s]')
    ax.set_xlabel('number of elements')
    ax.set_title(title)
    intervals = 5
    ax.set_xticks(np.arange(x[0], x[-1]+1, (x[-1]-x[0])/intervals))
    plt.show()


def plot_all(xdim, result, construct_averaged):
    colors = ['b', 'y', 'g', 'r']
    plot_result(xdim, [construct_averaged.array[0], construct_averaged.avl[0], construct_averaged.bst[0],
                       construct_averaged.rb[0]],
                ["array", "avl", "bst", "red black"], colors, "Construct structure")
    plot_result(xdim, [np.cumsum(construct_averaged.array[0]), np.cumsum(construct_averaged.avl[0]),
                       np.cumsum(construct_averaged.bst[0]),
                       np.cumsum(construct_averaged.rb[0])],
                ["array", "avl", "bst", "red black"], colors, "Construct structure (cumulative)")
    plot_result(xdim, [list(map(lambda x: x[0], result.array)),
                       list(map(lambda x: x[0], result.avl)),
                       list(map(lambda x: x[0], result.bst)),
                       list(map(lambda x: x[0], result.rb))],
                ["array", "avl", "bst", "red black"], colors, "Insert elements")
    plot_result(xdim, [list(map(lambda x: x[1], result.array)),
                       list(map(lambda x: x[1], result.avl)),
                       list(map(lambda x: x[1], result.bst)),
                       list(map(lambda x: x[1], result.rb))],
                ["array", "avl", "bst", "red black"], colors, "Delete elements")
    plot_result(xdim, [list(map(lambda x: x[2], result.array)),
                list(map(lambda x: x[2], result.avl)),
                list(map(lambda x: x[2], result.bst)),
                list(map(lambda x: x[2], result.rb))],
                ["array", "avl", "bst", "red black"], colors, "Find elements")
    plot_result(xdim, [list(map(lambda x: x[3], result.array)),
                       list(map(lambda x: x[3], result.avl)),
                       list(map(lambda x: x[3], result.bst)),
                       list(map(lambda x: x[3], result.rb))],
                ["array", "avl", "bst", "red black"], colors, "Find elements in interval")


def plot_tree(xdim, result, xconstruct, construct_averaged):
    colors = ['y', 'g', 'r']
    plot_result(xconstruct, [np.cumsum(construct_averaged.avl[0]), np.cumsum(construct_averaged.bst[0]),
                             np.cumsum(construct_averaged.rb[0])],
                ["avl", "bst", "red black"], colors, "Construct structure (cumulative)")
    plot_result(xconstruct, [construct_averaged.avl[0], construct_averaged.bst[0],
                       construct_averaged.rb[0]],
                ["avl", "bst", "red black"], colors, "Construct structure")
    plot_result(xdim, [list(map(lambda x: x[0], result.avl)),
                       list(map(lambda x: x[0], result.bst)),
                       list(map(lambda x: x[0], result.rb))],
                ["avl", "bst", "red black"], colors, "Insert elements")
    plot_result(xdim, [list(map(lambda x: x[1], result.avl)),
                       list(map(lambda x: x[1], result.bst)),
                       list(map(lambda x: x[1], result.rb))],
                ["avl", "bst", "red black"], colors, "Delete elements")
    plot_result(xdim, [list(map(lambda x: x[2], result.avl)),
                       list(map(lambda x: x[2], result.bst)),
                       list(map(lambda x: x[2], result.rb))],
                ["avl", "bst", "red black"], colors, "Find elements")
    plot_result(xdim, [list(map(lambda x: x[3], result.avl)),
                       list(map(lambda x: x[3], result.bst)),
                       list(map(lambda x: x[3], result.rb))],
                ["avl", "bst", "red black"], colors, "Find elements in interval")
