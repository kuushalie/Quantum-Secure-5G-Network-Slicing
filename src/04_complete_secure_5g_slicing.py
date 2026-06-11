import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import random
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit import transpile
import os

# random bitstring generation
def random_bitstring(length):
    return np.random.choice(['0', '1'], size=length)

# BB84 Quantum Key Distribution Protocol
def bb84_protocol(target_length=8):
    simulator = AerSimulator()
    key = []

    while len(key) < target_length:
        alice_bits = random_bitstring(target_length)
        alice_bases = random_bitstring(target_length)
        bob_bases = random_bitstring(target_length)

        for i in range(target_length):
            if len(key) >= target_length:
                break  

            qc = QuantumCircuit(1, 1)
            if alice_bases[i] == '0':               # Z-basis
                if alice_bits[i] == '1':
                    qc.x(0)                         # Prepare |1>
            else:                                   # X-basis
                if alice_bits[i] == '0':
                    qc.h(0)                         # Prepare |+>
                else:
                    qc.x(0)
                    qc.h(0)                         # Prepare |->

            if bob_bases[i] == '1':  
                qc.h(0)
            qc.measure(0, 0)

            compiled_circuit = transpile(qc, simulator)
            result = simulator.run(compiled_circuit).result()
            measured_bit = list(result.get_counts().keys())[0]

            # bits where bases match
            if alice_bases[i] == bob_bases[i]:
                key.append(measured_bit)

    return ''.join(key[:target_length])

# PQC Encryption and Decryption 
def pqc_encrypt(data, key):
    backend = default_backend()
    salt = os.urandom(16)
    iv = os.urandom(12)  

    # key from the input key using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    derived_key = kdf.derive(key.encode('utf-8'))

    # AES-GCM encryption
    cipher = Cipher(algorithms.AES(derived_key), modes.GCM(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data.encode('utf-8')) + encryptor.finalize()
    return {
        "ciphertext": ciphertext,
        "tag": encryptor.tag,
        "iv": iv,
        "salt": salt
    }

def pqc_decrypt(encrypted_data, key):
    backend = default_backend()

    # get the parameters
    ciphertext = encrypted_data["ciphertext"]
    tag = encrypted_data["tag"]
    iv = encrypted_data["iv"]
    salt = encrypted_data["salt"]

    # Derive the key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    derived_key = kdf.derive(key.encode('utf-8'))

    # AES-GCM decryption
    cipher = Cipher(algorithms.AES(derived_key), modes.GCM(iv, tag), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_data.decode('utf-8')

# network Parameters
num_slices = 3       
nodes_per_slice = 5  
min_weight = 1       
max_weight = 5        
length = 8  

# graph representing the 5G network with different slices
G = nx.Graph()
#nodes generation
slices = {}
for i in range(1, num_slices + 1):
    nodes = [(f"{chr(65 + j + (i - 1) * nodes_per_slice)}", random.randint(min_weight, max_weight)) 
             for j in range(nodes_per_slice)]
    slices[f"Slice {i}"] = nodes
    for node_name, weight in nodes:
        G.add_node(node_name, weight=weight, slice=f"Slice {i}")

#edge generation
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

for slice1, nodes1 in slices.items():
    for slice2, nodes2 in slices.items():
        if slice1 < slice2:
            edges = [
                (n1[0], n2[0], random.randint(min_weight, max_weight))
                for n1 in nodes1 for n2 in nodes2 if random.random() < 0.2
            ]
            G.add_weighted_edges_from(edges)
            edge_colors.extend(["black"] * len(edges))

# Network slicing
plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G)
nx.draw(
    G, pos, with_labels=True, node_color="skyblue", node_size=2000, 
    font_size=10, font_color="black", edge_color=edge_colors, width=2
)
node_labels = {node: f"{node}\nWeight={G.nodes[node]['weight']}" for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10)
nx.draw_networkx_edge_labels(
    G, pos, edge_labels={(u, v): w for u, v, w in G.edges(data="weight")}, font_color="blue"
)
plt.title("Network Model with 5G Network Slicing")
plt.show()

# QKD Key Generation
qkd_keys = {edge: bb84_protocol(target_length=length) for edge in G.edges()}
for link, key in qkd_keys.items():
    print(f"Link {link}: BB84 QKD Key = {key}")

random_link = random.choice(list(qkd_keys.keys()))  
qkd_key_for_encryption = qkd_keys[random_link] 
print(f"Using QKD Key for Link {random_link}: {qkd_key_for_encryption}")

# Encrypt the data 
data_to_send = "5G "
encrypted = pqc_encrypt(data_to_send, qkd_key_for_encryption)  # Passing QKD key for PBKDF2
print(f"Encrypted Data: {encrypted}")

# Decrypt the data
decrypted = pqc_decrypt(encrypted, qkd_key_for_encryption)  # Passing QKD key for PBKDF2
print(f"Decrypted Data: {decrypted}")


# Simulate Link Failure
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

# Link failure of a random link
random_edge = random.choice(list(G.edges()))
simulate_link_failure(G, random_edge)

# network graph after failure
plt.figure(figsize=(10, 7))
nx.draw(G, with_labels=True, node_color="lightgreen", node_size=1500, font_size=15, font_color="black", edge_color="gray")
plt.title("Network Model After Link Failure")
plt.show()

# Self-Healing Network 
def self_heal_network(graph):
    if not nx.is_connected(graph):
        print("Network is fragmented. Attempting self-healing...")
        components = list(nx.connected_components(graph))
        node_from_component1 = list(components[0])[0]
        node_from_component2 = list(components[1])[0]
        graph.add_edge(node_from_component1, node_from_component2)
        print(f"Reconnected {node_from_component1} to {node_from_component2}")

self_heal_network(G)

# Graph after self-healing
plt.figure(figsize=(10, 7))
nx.draw(G, with_labels=True, node_color="orange", node_size=1500, font_size=15, font_color="black", edge_color="gray")
plt.title("Network Model After Self-Healing")
plt.show()
