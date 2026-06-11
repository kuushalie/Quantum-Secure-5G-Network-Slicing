# Importing necessary libraries
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import random

# Parameters
num_slices = 3          # Number of slices
nodes_per_slice = 5     # Number of nodes per slice
min_weight = 1          # Minimum weight for nodes and edges
max_weight = 5          # Maximum weight for nodes and edges

# CO1 - Network slicing architecture (5G) and resource allocation using graph theory
# Create the main graph representing the 5G network with different slices
G = nx.Graph()

# Randomly generate nodes and add them to slices
slices = {}
for i in range(1, num_slices + 1):
    nodes = [(f"{chr(65 + j + (i - 1) * nodes_per_slice)}", random.randint(min_weight, max_weight)) 
             for j in range(nodes_per_slice)]
    slices[f"Slice {i}"] = nodes
    for node_name, weight in nodes:
        # Adding nodes with weight to represent resource allocation
        G.add_node(node_name, weight=weight, slice=f"Slice {i}")

# CO1, CO4 - Generate edges within each slice with random weights, simulating intra-slice routing
# CO2 - Programmatically manage network slices for different use cases
edge_colors = []
for slice_name, nodes in slices.items():
    edges = [
        (nodes[i][0], nodes[j][0], random.randint(min_weight, max_weight)) 
        for i in range(len(nodes)) for j in range(i + 1, len(nodes))
        if random.random() < 0.5  # Randomly decide if an edge exists
    ]
    G.add_weighted_edges_from(edges)
    edge_colors.extend(["blue" if slice_name == "Slice 1" 
                        else "green" if slice_name == "Slice 2" 
                        else "red"] * len(edges))

# CO1, CO4 - Generate inter-slice edges to allow connectivity between slices, simulating inter-slice routing
for slice1, nodes1 in slices.items():
    for slice2, nodes2 in slices.items():
        if slice1 < slice2:
            edges = [
                (n1[0], n2[0], random.randint(min_weight, max_weight))
                for n1 in nodes1 for n2 in nodes2 if random.random() < 0.2
            ]
            G.add_weighted_edges_from(edges)
            edge_colors.extend(["black"] * len(edges))

# CO3 - Visualizing data transfer paths with node weights representing resource availability in each slice
# Draw the complex network graph with node weights as labels
plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G)
nx.draw(
    G, pos, with_labels=True, node_color="skyblue", node_size=2000, 
    font_size=10, font_color="black", edge_color=edge_colors, width=2
)

# Annotate nodes with weights
node_labels = {node: f"{node}\nWeight={G.nodes[node]['weight']}" for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10)

# Draw edge labels to show weights
nx.draw_networkx_edge_labels(
    G, pos, edge_labels={(u, v): w for u, v, w in G.edges(data="weight")}, font_color="blue"
)
plt.title(" Network Model with 5G Network Slicing")
plt.show()

# CO3 - QKD Key Generation for secure data transfer within slices
def generate_qkd_key():
    return ''.join(np.random.choice(['0', '1'], size=256))

# Assign QKD keys to each link for secure data transfer in each slice
qkd_keys = {edge: generate_qkd_key() for edge in G.edges()}
for link, key in qkd_keys.items():
    print(f"Link {link}: QKD Key = {key}")

# CO2 - PQC Encryption to secure data transfer across network slices
def encrypt_data(data):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(data.encode('utf-8'))
    return digest.finalize().hex()

# Example encryption for communication between nodes
data_to_send = "Sample data for PQC encryption"
encrypted_data = encrypt_data(data_to_send)
print(f"Encrypted data: {encrypted_data}")

# CO4 - Simulate Link Failure to test routing protocols and self-healing mechanism
def simulate_link_failure(graph, edge):
    print(f"Link {edge} has failed. Recomputing routes...")
    graph.remove_edge(*edge)
    if nx.is_connected(graph):
        try:
            path = nx.shortest_path(graph, source=edge[0], target=edge[1])
            print(f"Alternative route found: {path}")
        except nx.NetworkXNoPath:
            print("No alternative path available!")
    else:
        print("Network is now disconnected!")

# Simulate a failure of a random link
random_edge = random.choice(list(G.edges()))
simulate_link_failure(G, random_edge)

# CO4 - Re-draw the network graph after failure to visualize impact on connectivity
plt.figure(figsize=(10, 7))
nx.draw(G, with_labels=True, node_color="lightgreen", node_size=1500, font_size=15, font_color="black", edge_color="gray")
plt.title("Network Model After Link Failure")
plt.show()

# CO5 - Self-Healing Network to restore connectivity after link failure, illustrating error-handling protocols
def self_heal_network(graph):
    if not nx.is_connected(graph):
        print("Network is fragmented. Attempting self-healing...")
        components = list(nx.connected_components(graph))
        node_from_component1 = list(components[0])[0]
        node_from_component2 = list(components[1])[0]
        graph.add_edge(node_from_component1, node_from_component2)
        print(f"Reconnected {node_from_component1} to {node_from_component2}")

self_heal_network(G)

# Re-draw the network graph after self-healing to verify restored connectivity
plt.figure(figsize=(10, 7))
nx.draw(G, with_labels=True, node_color="orange", node_size=1500, font_size=15, font_color="black", edge_color="gray")
plt.title("Network Model After Self-Healing")
plt.show()
