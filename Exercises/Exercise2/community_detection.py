'''
Notes:

nodeinfo.node:
node id - x - y - z - module - weighted degree - labels

- we don't really have the node id, just index of the list.

edgeinfo.edge:
in the form of a weighted adjacency matrix

https://pypi.org/project/communities/

'''




import networkx as nx
import pandas as pd
import numpy as np
from communities.algorithms import louvain_method # is this what we want?
from community import community_louvain

# Function 1: Load data!

def load_data(node_file, edge_file):
    
    # First, load our data through file IO
    node_data = pd.read_csv(node_file, delim_whitespace=True, header=None, names=["x", "y", "z", "module", "weighted_degree", "label"])
    # print(node_data)
    
    edge_data = np.loadtxt(edge_file)
    
    # Next, create a graph
    
    G = nx.Graph()
    
    for i, row in node_data.iterrows():
        # Create node
        G.add_node(i, label=row["label"], x=row["x"], y=row["y"], z=row["z"], degree=row["weighted_degree"])

        # add edges
        for i in range(len(edge_data)):
            for j in range (i + 1, len(edge_data)):
                if edge_data[i, j] > 0:
                    G.add_edge(i, j, weight=edge_data[i, j])
                    
        return G, node_data


def community_detection(graph, resolution=1.0):
    partition = community_louvain.best_partition(graph, weight='weight', resolution=resolution)
    
    num_modules = len(set(partition.values()))
    print(f"Number of modules after louvain: {num_modules}")
    
    return partition

def participation_coeff(G, partition):
    community_dict = {}
    for node, community_id in partition.items():
            community_dict.setdefault(community_id, []).append(node)
        
    participation_coefficients = {}
    for node in G.nodes():
        degree = G.degree(node, weight='weight')
        if degree == 0:
            participation_coefficients[node] = 0
            continue
        
        community = partition[node]
        in_community_edges = sum(1 for neighbor in G[node] if partition[neighbor] == community)
        participation_coefficients[node] = 1 - (in_community_edges / degree) ** 2
        
    return participation_coefficients


def output_brain_net_viewer(node_data, G, partition, participation_coefficients, output_node_name, output_edge_name):
    node_data['module'] = node_data.index.map(partition)
    node_data['participation'] = node_data.index.map(participation_coefficients)
    
    node_data[['x', 'y', 'z', 'module', 'participation', 'label']].to_csv(output_node_name, sep='\t', index=False, header=False)

    edge_matrix = nx.to_numpy_array(G, weight='weight')
    np.savetxt(output_edge_name, edge_matrix)
    
def output_gephi():
    #TODO
    return

if __name__ == '__main__':
    
    G, node_data = load_data('nodeinfo.node', 'edgeinfo.edge')
    partition = community_detection(G, 1.12)
    coefficients = participation_coeff(G, partition)
    # print(coefficients)
    output_brain_net_viewer(node_data, G, partition, coefficients, 'output.node', 'output.edge')