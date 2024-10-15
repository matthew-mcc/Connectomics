
'''
Matthew McConnell - 30094710
CPSC 601 - Connectomics
Exercise 2, relevant code

Below is a community detection implementation in which previous .edge and .node files are read in, fed through a community detection algorithm (louvain). Participation coeffecients
were also calculated. Outputs both a (.node, .edge) as well as a (.csv).
'''

import networkx as nx
import pandas as pd
import numpy as np
from community import community_louvain # https://python-louvain.readthedocs.io/en/latest/api.html

# Function 1: Load data!
def load_data(node_file, edge_file):
    '''
    This is a simple function to laod the data from our .edge and .node files, that we were using for exploring Brain Net Viewer in class.
    It stores the information in a networkX graph, and a Dataframe containing node_information.
    '''
    
    # First, load our data through file IO
    node_data = pd.read_csv(node_file, delim_whitespace=True, header=None, names=["x", "y", "z", "module", "weighted_degree", "label"]) # nodes
    edge_data = np.loadtxt(edge_file) # edges
    
    # Next, create a graph
    G = nx.Graph()
    # Load our data
    for i, row in node_data.iterrows():
        # Create node
        G.add_node(i, label=row["label"], x=row["x"], y=row["y"], z=row["z"], degree=row["weighted_degree"])

        # add edges
        for i in range(len(edge_data)):
            for j in range (i + 1, len(edge_data)):
                if edge_data[i, j] > 0:
                    G.add_edge(i, j, weight=edge_data[i, j])
                    
        return G, node_data

# Function 2: Community Detection!
def community_detection(graph, resolution=1.0):
    '''
    Function to perform our community detection algorithm. We are using the louvain method, present in python's community library.
    Returns a dictionary partition of the new community representation.
    '''
    partition = community_louvain.best_partition(graph, weight='weight', resolution=resolution)
    
    num_modules = len(set(partition.values()))
    print(f"Number of modules after louvain: {num_modules}")
    
    return partition

# Function 3: Participation Coeffecient Calculation!
def participation_coeff(G, partition):
    '''
    Function to calculate the participation coeffecients for each node.
    For the calculation, I used the formula present in the Hubs lecture from class.
    '''
    # Create a default dict, initial partition information.
    community_dict = {}
    for node, community_id in partition.items():
            community_dict.setdefault(community_id, []).append(node)
        
    # Dict
    participation_coefficients = {}
    # For each node in graph, calculate the participation coeffecient
    for node in G.nodes():
        # Get the degree
        degree = G.degree(node, weight='weight')
        # If it's isolated, no participation
        if degree == 0:
            participation_coefficients[node] = 0
            continue
        # Get the community the node belongs to
        community = partition[node]
        # Count the number of edges that the node has within community
        in_community_edges = sum(1 for neighbor in G[node] if partition[neighbor] == community)
        # Calculate participation coeffecient as seen in class.
        participation_coefficients[node] = 1 - (in_community_edges / degree) ** 2 # formula from class
        
    return participation_coefficients

# Function 4: Brain Net Output!
def output_brain_net_viewer(node_data, G, partition, participation_coefficients, output_node_name, output_edge_name):
    '''
    This function exists to format our data in a way that Brain Net Viewer Wants. 
    Unfortunately, it is rather picky on how we store info, so we need to be careful here.
    Creates a .node and a .edge file.
    '''
    # Store our node data
    node_data['module'] = node_data.index.map(partition)
    node_data['participation'] = node_data.index.map(participation_coefficients)
    node_data[['x', 'y', 'z', 'module', 'participation', 'label']].to_csv(output_node_name, sep='\t', index=False, header=False)

    # Store our edge matrix, luckily nx.to_numpy_array creates an adjacency matrix for us
    edge_matrix = nx.to_numpy_array(G, weight='weight')
    np.savetxt(output_edge_name, edge_matrix)
    
# Function 5: Gephi Output (CSV)!
def output_gephi(node_data, G, partition, participation_coefficients, output_node_name, output_edge_name):
    '''
    This function exists to format our data as a CSV, such that we can bring it in to Gephi.
    Creates two .csv files, one for nodes, one for edges.
    '''
    
    gephi_output_nodes = pd.DataFrame()
    
    # Follow CSV from class, nodes first
    gephi_output_nodes['ID'] = node_data.index
    gephi_output_nodes['Module'] = node_data.index.map(partition)
    gephi_output_nodes['participation'] = node_data.index.map(participation_coefficients)
    gephi_output_nodes['label'] = node_data['label']
    gephi_output_nodes.to_csv(output_node_name, index=False)
    
    # Edges next
    gephi_output_edges = pd.DataFrame()
    gephi_output_edges['Source'] = [u for u, v, d in G.edges(data=True)]
    gephi_output_edges['Target'] = [v for u, v, d in G.edges(data=True)]
    gephi_output_edges['Weight'] = [d['weight'] for u, v, d in G.edges(data=True)]
    gephi_output_edges.to_csv(output_edge_name, index=False)
    
    

# Main!
if __name__ == '__main__':
    
    G, node_data = load_data('nodeinfo.node', 'edgeinfo.edge')
    partition = community_detection(G, 1.12)
    coefficients = participation_coeff(G, partition)
    output_brain_net_viewer(node_data, G, partition, coefficients, 'output.node', 'output.edge')
    output_gephi(node_data, G, partition, coefficients, 'output_nodes.csv', 'output_edges.csv')