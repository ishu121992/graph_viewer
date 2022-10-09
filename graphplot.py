import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import io

class GraphVisualizer():
    """Graph Visualization Class

    This module demonstrates weighted graph visualization using adjacency lists.
    
    Parameters
    ----------
    adjacency_list : input graph as adjacency list.
    E.g.,
    adjacency_list = {
    'A': [('B', 8), ('C', 2), ('D', 4)],
    'B': [('A', 8), ('C', 7), ('E', 2)], 
    'C': [('A', 2), ('B', 7), ('E', 3), ('F', 9), ('D', 1)], 
    'D': [('A', 4), ('C', 1), ('F', 5)], 
    'E': [('B', 2), ('C', 3)], 
    'F': [('C', 9), ('D', 5)]
    }
    
    Params (Dict): 
        draw_pattern
            Default is 'draw_spring' 
                'draw_circular': nx.circular_layout(G), 
                'draw_kamada_kawai':nx.kamada_kawai_layout(G), 
                'draw_planar': nx.planar_layout(G), 
                'draw_random': nx.random_layout(G), 
                'draw_spectral': nx.spectral_layout(G), 
                'draw_spring': nx.spring_layout(G), 
                'draw_shell': nx.shell_layout(G)
        color_node (str): Color of node in visualization. Default is 'black', 
        fig_size (tuple): size of figure. Default is (5,5) 
        nodesize (int): size of node in graph. Default is 500
        fontsize (int): Size of node labels. Default is 8. 
    
    Example:
    You can also skip all parameters in list.
    params = {
            'graph_layout':'draw_spring', 
            'node_color':'pink', 
            'graph_size':(5,5), 
            'node_size':200
    }
    r = requests.post(endpoint_url, params = params, json=adjacency_list)
    image = Image.open(io.BytesIO(r.content))
    
    Need to import PIL and io package
    """
    
    def __init__(self, 
                 graphdata, 
                 params= {'graph_layout':'draw_spring', 
                            'node_color':'pink', 
                            'fig_size':(5,5), 
                            'node_size':200}):        
        self.graphdata = graphdata
        self.params = params
        self.node_list = list(self.graphdata.keys())
        self.node_count = len(self.node_list)
        self.adjmat = np.zeros((self.node_count, self.node_count)).astype(float)
        
        
    def weighted_graph_show(self):
        i = 0
        while(i<self.node_count):
            node_weight_pairs = dict(self.graphdata.get(self.node_list[i]))
            node_keys = list(node_weight_pairs.keys())
            for j in range(self.node_count):
                if self.node_list[j] in node_keys:
                    self.adjmat[i][j] = node_weight_pairs[self.node_list[j]]
                else:
                    if i == j:
                        self.adjmat[i][j] = 0.0
                    else:
                        self.adjmat[i][j] = np.inf
            i = i + 1
        
        result = (self.adjmat == self.adjmat.T)
        if False in result:
            directed = True
        else:
            directed = False
        
        node_labels = {}
        for i in range(len(self.node_list)):
            node_labels[i] = self.node_list[i]
        
        pattern = self.params['graph_layout']
        color_node = self.params['node_color']
        fig_size = self.params['fig_size']
        nodesize = self.params['node_size']
        
        G = nx.graph.Graph()        
        for i in range(self.adjmat.shape[0]):
            for j in range(self.adjmat.shape[0]):
                if self.adjmat[i][j] != np.inf:
                    if self.adjmat[i][j] != 0.0:
                        G.add_edge(i, j, weight = self.adjmat[i][j])
        draw_pattern = {'draw_circular': nx.circular_layout(G), 
                'draw_kamada_kawai':nx.kamada_kawai_layout(G), 
                'draw_planar': nx.planar_layout(G), 
                'draw_random': nx.random_layout(G), 
                'draw_spectral': nx.spectral_layout(G), 
                'draw_spring': nx.spring_layout(G), 
                'draw_shell': nx.shell_layout(G)}
        
        try: 
            if pattern in draw_pattern.keys():
                pattern = draw_pattern[pattern]
        except:
            print('incorrect graph pattern')
        
        fig, ax = plt.subplots(figsize=fig_size)
        labels_edge = nx.get_edge_attributes(G,'weight')
        if directed == True:
            nx.draw_networkx_edges(G, pos=pattern, arrows=True, arrowstyle="->")
        nx.draw(G, pos=pattern, node_color=color_node, node_size=nodesize, labels = node_labels, font_size=8, with_labels = True, ax=ax)
        
        nx.draw_networkx_edge_labels(G,pos=pattern,edge_labels=labels_edge)
        
        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)
        return bytes_image