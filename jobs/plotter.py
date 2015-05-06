import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

import networkx as nx

figure_path = "/home/knossos/figures/"


def save_histogram(data, bin_range, x_label, y_label, name, show_col_height=True):
    figure = plt.figure()
    histo = figure.add_subplot(111)
    histo.hist(data, bins=bin_range)
    if show_col_height:
        rects = [rect for rect in histo.get_children() if isinstance(rect, mpl.patches.Rectangle)]
        for rect in rects:
            height = rect.get_height()
            if height == 1:
                continue
            histo.text(rect.get_x()+rect.get_width()/2., height, str(height), ha='center', va='bottom')
    histo.set_yticks([x for x in range(5)])
    histo.set_xlabel(x_label)
    histo.set_ylabel(y_label)
    figure.savefig(figure_path + name)


def plot_graph(graph, file_name):
    # nx.write_dot(graph, file_name)
    pass
