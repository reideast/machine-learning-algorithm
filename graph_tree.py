import base64
from tkinter import PhotoImage

import pydot
from classes.Case import Case
from classes.Model import Tree

def graph_model(model):
    """
    Construct a Graphviz tree from the decision tree model
    :param model: a classes.Model, which contains a decision tree we wish to graph
    :return: tkinter.PhotoImage data, type `bytes` in Python 3, along with a PNG image data obj
             PNG img can be written with: open("outfile.png", "wb").write(png_file)
    """
    graph = pydot.Dot(graph_type="graph")

    __build_tree_graph(model.treeRoot, graph)

    # Made Graph using pydot python objects and return as binary image data
    binary_img_data = graph.create_gif(prog="dot")

    # Convert to a tkinter picture object, which first requires converting the binary data into base64 data
    # Also make the PNG image data
    return PhotoImage(data=base64.standard_b64encode(binary_img_data)), graph.create_png(prog="dot")


def __build_tree_graph(node: Tree, graph: pydot.Graph):
    """
    Recursively build up the Pydot graph object
    :param node: root of the subtree to build from
    :param graph: graph object, passed by reference, into which node/edge data will be built
    """
    if not node.isLeaf:
        graph.add_edge(pydot.Edge(__label_node(node), __label_node(node.leftChild)))
        __build_tree_graph(node.leftChild, graph)
        graph.add_edge(pydot.Edge(__label_node(node), __label_node(node.rightChild)))
        __build_tree_graph(node.rightChild, graph)


def __label_node(node):
    """
    Build the text contents that describes any node, appropriate to either leaf or internal
    :param node: node to describe
    :return: str
    """
    if node.isLeaf:
        return "%d. %s n=%d" % (node.debug_id, node.predicted, node.numCases)
    else:
        return "%d. %s < %.1f n=%d" % (node.debug_id, Case.attributes_names[node.splitAttribute], node.threshold, node.numCases)
