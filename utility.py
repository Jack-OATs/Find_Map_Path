import matplotlib.pyplot as plt
import networkx as nx
from networkx.classes import Graph


class MyGraph(Graph):
    """
    Class that extends Graph so that the explored nodes will be kept with the graph.
    """
    def __init__(self):
        Graph.__init__(self)
        self.explored_nodes = set([])

    def __iter__(self):
        self.explored_nodes = set([n for n in iter(self.nodes)])
        return iter(self.nodes)

    def __getitem__(self, item):
        self.explored_nodes = self.explored_nodes | set([item])
        return self.adj[item]

    def get_explored_nodes(self):
        return self.explored_nodes

    def reset_search(self):
        self.explored_nodes = set([])

    def get_node_position(self, node):
        return self.nodes[node]['pos']


def build_graph(file_name):
    """
    Build a graph file to keep track of the nodes and edges that will be searched.
    :param file_name: The name of the input file.
    :return: It will of type MyGraph that extends Graph to handle the explored list.
    """
    graph = MyGraph()
    with open(file_name, 'r') as fin:
        line = fin.readline().replace('\n', '')
        while line != "":
            vals = line.split(':')
            graph.add_node(vals[0], pos=(int(vals[1]),int(vals[2])))
            line = fin.readline().replace('\n', '')
        dest = fin.readline().replace('\n','').split('\t')
        line = fin.readline().replace('\n', '')
        edges = []
        while line != '':
            node_info = line.split('\t')
            src = node_info[0]
            for node in range(1,len(node_info)):
                if node_info[node] != '':
                    if (dest[node],src) not in edges:
                        edges.append((src,dest[node], node_info[node]))
            line = fin.readline().replace('\n','')
    for edge in edges:
        graph.add_edge(edge[0], edge[1], weight=int(edge[2]))

    return graph


def draw_graph(graph, start, goal, path=[], save_file=None):
    """
    Method to visualize the map to see what path was taken and which nodes were explored.
    :param graph: The MyGraph object that is being search (use build_graph to obtain)
    :param path: The list of nodes used to find the path from start to finish.
    :param save_file: If one is given then save the file to the path (via string) given.
    :return: Nothing is returned.
    """
    explored = graph.get_explored_nodes()
    node_pos = {n: graph.nodes[n]['pos'] for n in graph.nodes.keys()}
    edge_labels = {}
    for edge in graph.edges():
        edge_labels[edge] = graph[edge[0]][edge[1]]['weight']

    labels = {}
    for node in graph:
        labels[node] = node

    nx.draw_networkx_nodes(graph, node_pos, node_color='gray') #, nodelist=romania.nodes, node_color='w', node_size=500)
    nx.draw_networkx_edges(graph, node_pos, style='dashed')
    if len(explored) > 0:
        print("Explored = "+str(explored))
        nx.draw_networkx_nodes(graph, node_pos, nodelist=explored, node_color='r')

    if len(path) > 0:
        nx.draw_networkx_nodes(graph, node_pos, nodelist= path, node_color='y')
        edgelist = []
        for i in range(1,len(path)):
            edgelist.append((path[i - 1], path[i]))
        nx.draw_networkx_edges(graph, node_pos, edgelist, edge_color='b', width=3)
    nx.draw_networkx_nodes(graph, node_pos, nodelist=[start, goal], node_color='g')



    nx.draw_networkx_labels(graph, node_pos, labels)
    nx.draw_networkx_edge_labels(graph, node_pos, edge_labels, font_size=8)

    plt.axis('off')
    plt.show() # display
    if save_file is not None:
        plt.savefig(save_file) # save as png
