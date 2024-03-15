import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import sys

def load_and_process_matrix(file_path, sep):
    
    matrix = pd.read_csv(file_path, sep=sep, header=0)
    if file_path.endswith('.tsv'):
        matrix = matrix.set_index(matrix.columns[0])
    return matrix

def calculate_graph_statistics(G, title):
    if nx.is_empty(G):
        print("Graph is empty. No statistics to calculate.")
        return

    # Basic stats
    print("Number of nodes:", G.number_of_nodes())
    print("Number of edges:", G.number_of_edges())
    print("Graph density:", nx.density(G))

    # Degree distribution
    degrees = [deg for _, deg in G.degree()]
    print("Average degree:", np.mean(degrees))
    print("Maximum degree:", np.max(degrees))
    print("Minimum degree:", np.min(degrees))

    # Clustering
    clustering_coeffs = nx.clustering(G)
    print("Average clustering coefficient:", np.mean(list(clustering_coeffs.values())))

    # Check if graph is connected before calculating path-based metrics
    if nx.is_connected(G):
        print("Average shortest path length:", nx.average_shortest_path_length(G))
        print("Diameter of the graph:", nx.diameter(G))  # Longest shortest path
    else:
        print("Graph is not connected. Cannot calculate diameter and average shortest path length.")

    # Centrality measures
    degree_centrality = nx.degree_centrality(G)
    print("Highest degree centrality:", max(degree_centrality.values()))

    betweenness_centrality = nx.betweenness_centrality(G)
    print("Highest betweenness centrality:", max(betweenness_centrality.values()))

    closeness_centrality = nx.closeness_centrality(G)
    print("Highest closeness centrality:", max(closeness_centrality.values()))
    
    


def draw_custom_graph(distance_matrix, title, threshold):
    # Calculate the threshold as the first quantile of non-zero distances
    np.fill_diagonal(distance_matrix.values, np.nan)
    threshold = np.nanquantile(distance_matrix.values, threshold)

    print("Distance threshold:", threshold)

    # Create a graph
    G = nx.Graph()
    
    # Add edges only if the weight is above the threshold
    for i, row in distance_matrix.iterrows():
        for j, weight in row.items():
            if weight >= threshold and i != j:
                G.add_edge(i, j, weight=weight)
    calculate_graph_statistics(G)
    if G.nodes():
        # Node color and size based on degree
        degrees = dict(G.degree())
        node_color = [degrees[n] for n in G.nodes()]
        node_size = [(degrees[n] / len(G.nodes())) * 1000 for n in G.nodes()]  # Adjust size factor as needed
        edge_width = [(1 / (G.get_edge_data(u, v)["weight"]*10)) for u, v in G.edges()]
        # Use a spring layout
        pos = nx.spring_layout(G, k=3.5, iterations=20, seed=50)
        # Draw the graph
        plt.figure(figsize=(10, 10))
        nx.draw_networkx_edges(G, pos, width=edge_width, edge_color="grey")
        nx.draw_networkx_nodes(
            G,
            pos,
            node_size=node_size,
            node_color=node_color,
            cmap=plt.cm.viridis,
        )

        plt.axis("off")
        plt.title(title)
        
        plt.savefig(title + '.png')
        plt.show()
    else:
        print("Graph is empty. No nodes to draw.")

def main():
    
    metadata = sys.argv[1]
    
    path_docker = '/home/microbiome/data'
    distance_tree_path = path_docker + '/3_feature_tables/Distance_matrix.csv'
    distance_matrix_asv = path_docker + '/7.1_asv_gmpr_core_metrics_phylogenetic/distance-matrix.tsv'
    distance_matrix_genus = path_docker + '/7.2_genus_gmpr_core_metrics_phylogenetic/distance-matrix.tsv'
    distance_matrix_species = path_docker + '/7.3_species_gmpr_core_metrics_phylogenetic/distance-matrix.tsv'
    # create folder to save the images
    folder_path = path_docker + '/13_network_analysis/'
    distance_tree = load_and_process_matrix(distance_tree_path, ',')
    draw_custom_graph(distance_tree, folder_path + 'distance-tree', 0.99)
    distanc_matrix_asv = load_and_process_matrix(distance_matrix_asv, '\t')
    draw_custom_graph(distanc_matrix_asv, folder_path + 'distance-sample-asv', 0.25 )
    distance_matrix_genus = load_and_process_matrix(distance_matrix_genus, '\t')
    draw_custom_graph(distance_matrix_genus, folder_path + 'distance-sample-genus', 0.25 )
    distance_matrix_species = load_and_process_matrix(distance_matrix_species, '\t')
    draw_custom_graph(distance_matrix_species, folder_path + 'distance-sample-species', 0.25 )
    

if __name__ == "__main__":
    main()


