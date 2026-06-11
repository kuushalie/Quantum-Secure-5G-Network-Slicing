# Import necessary libraries
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import random
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit import transpile

# Define random bitstring generation for BB84
def random_bitstring(length):
    """Generate a random bitstring of the given length."""
    return np.random.choice(['0', '1'], size=length)

# BB84 Quantum Key Distribution Protocol
def bb84_protocol(length=8):
    """Simulate the BB84 protocol for generating a QKD key."""
    alice_bits = random_bitstring(length)
    alice_bases = random_bitstring(length)
    bob_bases = random_bitstring(length)
    key = []
    simulator = AerSimulator()
    for i in range(length):
        qc = QuantumCircuit(1, 1)
        if alice_bases[i] == '0':  # Z-basis
            if alice_bits[i] == '1':
                qc.x(0)  # Prepare |1>
        else:  # X-basis
            if alice_bits[i] == '0':
                qc.h(0)  # Prepare |+>
            else:
                qc.x(0)
                qc.h(0)  # Prepare |->
        if bob_bases[i] == '1':  # Bob measures in X-basis
            qc.h(0)
        qc.measure(0, 0)
        compiled_circuit = transpile(qc, simulator)
        result = simulator.run(compiled_circuit).result()
        measured_bit = list(result.get_counts().keys())[0]
        if alice_bases[i] == bob_bases[i]:  # Use only matching bases
            key.append(measured_bit)
    return ''.join(key)

# Network slicing and resource allocation code (adjusted for fewer slices and nodes)
num_slices = 2          # Reduced number of slices
nodes_per_slice = 3     # Reduced number of nodes per slice
length = 64             # Reduced QKD key length for faster generation

# Create the main graph representing the 5G network with different slices
G = nx.Graph()

# Randomly generate nodes and add them to slices
slices = {}
for i in range(1, num_slices + 1):
    nodes = [(f"{chr(65 + j + (i - 1) * nodes_per_slice)}", random.randint(1, 5))
             for j in range(nodes_per_slice)]
    slices[f"Slice {i}"] = nodes
    for node_name, weight in nodes:
        G.add_node(node_name, weight=weight, slice=f"Slice {i}")

# Generate edges within each slice with random weights, simulating intra-slice routing
edge_colors = []
for slice_name, nodes in slices.items():
    edges = [
        (nodes[i][0], nodes[j][0], random.randint(1, 5))
        for i in range(len(nodes)) for j in range(i + 1, len(nodes))
        if random.random() < 0.5  # Randomly decide if an edge exists
    ]
    G.add_weighted_edges_from(edges)
    edge_colors.extend(["blue" if slice_name == "Slice 1"
                        else "green" if slice_name == "Slice 2"
                        else "red"] * len(edges))

# Generate inter-slice edges for connectivity between slices
for slice1, nodes1 in slices.items():
    for slice2, nodes2 in slices.items():
        if slice1 < slice2:
            edges = [
                (n1[0], n2[0], random.randint(1, 5))
                for n1 in nodes1 for n2 in nodes2 if random.random() < 0.2
            ]
            G.add_weighted_edges_from(edges)
            edge_colors.extend(["black"] * len(edges))

# Visualizing data transfer paths with node weights representing resource availability in each slice
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
plt.title("Network Model with 5G Network Slicing")
plt.show()

# Assign QKD keys to each link for secure data transfer in each slice using BB84
qkd_keys = {edge: bb84_protocol(length=length) for edge in G.edges()}
for link, key in qkd_keys.items():
    print(f"Link {link}: BB84 QKD Key = {key}")

# PQC Encryption to secure data transfer across network slices
def encrypt_data(data):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(data.encode('utf-8'))
    return digest.finalize().hex()

# Example encryption for communication between nodes
data_to_send = "Sample data for PQC encryption"
encrypted_data = encrypt_data(data_to_send)
print(f"Encrypted data: {encrypted_data}")

# Simulate Link Failure to test routing protocols and self-healing mechanism
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

# Re-draw the network graph after failure to visualize impact on connectivity
plt.figure(figsize=(10, 7))
nx.draw(G, with_labels=True, node_color="lightgreen", node_size=1500, font_size=15, font_color="black", edge_color="gray")
plt.title("Network Model After Link Failure")
plt.show()

# Self-Healing Network to restore connectivity after link failure
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
