# Machine Learning Project
# By James Quaife: j.quiafe1@nuigalway.ie, SID: 14100104
# and Andrew East: a.east1@nuigalway.ie, SID: 16280042
# National University of Ireland, Galway
# Computer Science CT475: Machine Learning
# November 2018
# Supervisor: Dr. Michael Madden

# Teamwork Attribution: This file was written by Andrew East

import base64
import logging
from tkinter import PhotoImage
from typing import List

import pydot
from pydot import Node as GraphNode, Graph

from classes.Case import Case
from classes.Model import Model, Tree, PredictionNode, InternalNode, ContinuousSplitNode, CategoricalSplitNode


def graph_model(model: Model) -> (PhotoImage, bytes):
    """
    Construct a Graphviz tree from the decision tree model
    :param model: a classes.Model, which contains a decision tree we wish to graph
    :return: tkinter.PhotoImage data, type `bytes` in Python 3, along with a PNG image data obj
             Note: PNG img can be written with: open("outfile.png", "wb").write(png_file)
    """
    graph = pydot.Dot(graph_type="graph")
    graph.set_node_defaults(fontsize="10", width=0, height=0, margin="0.11,0.05")

    # Build up the tree recursively, seeded by root node
    root_node = __make_node(model.decision_tree)
    graph.add_node(root_node)
    __build_tree_graph(model.decision_tree, root_node, graph)

    # Made Graph using pydot python objects and return as binary image data (must be GIF for tk)
    binary_img_data = graph.create_gif(prog="dot")

    # Convert to a tkinter picture object, which first requires converting the binary data into base64 data
    # Also make the PNG image data
    return PhotoImage(data=base64.standard_b64encode(binary_img_data)), graph.create_png(prog="dot")


def __build_tree_graph(node: Tree, parent_node: GraphNode, graph: Graph) -> None:
    """
    Recursively build up the Pydot graph object: Each call will make its children nodes, and link them to the node its parent generated
    Terminates if this is a leaf node, which will already have been built by its parent
    :param node: root of the subtree to build from
    :param parent_node: the graphviz node for this subtree's parent
    :param graph: graph object, passed by reference, into which node/edge data will be built
    """
    if isinstance(node, InternalNode):
        edge_labels = __make_edge_labels(node)
        for idx, child in enumerate(node.children):
            child_graph_node = __make_node(child)
            graph.add_node(child_graph_node)
            graph.add_edge(pydot.Edge(parent_node, child_graph_node, label=edge_labels[idx], fontsize="10.0"))
            __build_tree_graph(child, child_graph_node, graph)


def __make_node(node: Tree) -> GraphNode:
    """
    Build a pydot node that describes a tree node, appropriate to either leaf or internal
    :param node: the Tree node to describe
    :return: pydot.Node
    """

    # Build label
    if isinstance(node, PredictionNode):
        if node.num_cases_majority_class == -1:  # TODO: show majority class label for all nodes, even if it's "10/10" or whatnot
            node_label = node.predicted
        else:
            node_label = "%s\n%.1f%% (%d/%d)" % (node.predicted, (100 * node.num_cases_majority_class / node.num_cases), node.num_cases_majority_class, node.num_cases)
    elif isinstance(node, InternalNode):
        node_label = Case.attributes_names[node.split_attribute]
    else:
        raise NotImplementedError("Other node types implemented yet")  # TODO: this should probably just be an error? there's no other node types besides internal and leaf

    if node.unique_id is None:
        logging.error("Node's unique ID was not set by the GUI. Tree may have erroneously connected nodes")

    # Build node
    return pydot.Node(str(node.unique_id),
                      label=node_label,
                      style="rounded, filled" if isinstance(node, PredictionNode) else "filled",
                      shape="box",
                      fillcolor="#e2fff1" if isinstance(node, PredictionNode) else "#e2f1ff")


def __make_edge_labels(node: InternalNode) -> List[str]:
    labels = []
    if isinstance(node, ContinuousSplitNode):
        for threshold in node.thresholds:
            labels.append("< %.1f" % threshold)  # TODO: format the middle threshold labels with range, e.g. n <= THIS < m
        labels.append("")
    elif isinstance(node, CategoricalSplitNode):
        for category in Case.attribute_categories[node.split_attribute]:
            labels.append(category)
    else:
        raise NotImplementedError("Other node types implemented yet")  # TODO: Should this be an error? probably, since it's checking classes on the leaf of the hierarchy tree
    # print(labels)  # DEBUG
    return labels
