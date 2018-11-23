# -*- coding: utf-8 -*-
"""
pydot example 1
@author: Federico Cáceres
@url: http://pythonhaven.wordpress.com/2009/12/09/generating_graphs_with_pydot
"""
import pydot # import pydot or you're not going to get anywhere my friend :D
from classes.Case import Case
from classes.Model import Tree

def graph_model(model):
    """
    Construct a Graphviz tree from the decision tree model
    :param model: a classes.Model, which contains a decision tree we wish to graph
    :return: Binary image data, type `bytes` in Python 3
    """
    graph = pydot.Dot(graph_type="graph")

    __build_tree_graph(model.treeRoot, graph)

    graph.write_png('model_graph.png')

    return graph.create_gif(prog="dot")


def __build_tree_graph(node: Tree, graph: pydot.Graph):
    if not node.isLeaf:
        graph.add_edge(pydot.Edge(__label_node(node), __label_node(node.leftChild)))
        __build_tree_graph(node.leftChild, graph)
        graph.add_edge(pydot.Edge(__label_node(node), __label_node(node.rightChild)))
        __build_tree_graph(node.rightChild, graph)


def __label_node(node):
    if node.isLeaf:
        return str(node.debug_id) + ". " + node.predicted
    else:
        return str(node.debug_id) + ". " + Case.attributes_names[node.splitAttribute] + "<" + ("%.1f" % node.threshold)


def create_sample_graph():
    # first you create a new graph, you do that with pydot.Dot()
    graph = pydot.Dot(graph_type='graph')

    # the idea here is not to cover how to represent the hierarchical data
    # but rather how to graph it, so I'm not going to work on some fancy
    # recursive function to traverse a multidimensional array...
    # I'm going to hardcode stuff... sorry if that offends you

    # let's add the relationship between the king and vassals
    for i in range(3):
        # we can get right into action by "drawing" edges between the nodes in our graph
        # we do not need to CREATE nodes, but if you want to give them some custom style
        # then I would recomend you to do so... let's cover that later
        # the pydot.Edge() constructor receives two parameters, a source node and a destination
        # node, they are just strings like you can see
        edge = pydot.Edge("king", "lord%d" % i)
        # and we obviosuly need to add the edge to our graph
        graph.add_edge(edge)

    # now let us add some vassals
    vassal_num = 0
    for i in range(3):
        # we create new edges, now between our previous lords and the new vassals
        # let us create two vassals for each lord
        for j in range(2):
            edge = pydot.Edge("lord%d" % i, "vassal%d" % vassal_num)
            graph.add_edge(edge)
            vassal_num += 1

    # ok, we are set, let's save our graph into a file
    graph.write_png('example1_graph.png')

    # and we are done!

    return graph.create_gif(prog="dot")