# Quantum Secure and Resilient 5G Network Slicing

## Overview

This project presents a **Quantum Secure and Resilient 5G Network Slicing Framework** that integrates **Quantum Key Distribution (QKD)**, **Post-Quantum Cryptography (PQC)**, and **Self-Healing Network Mechanisms** to improve the security and reliability of next-generation communication networks.

The framework simulates a 5G network environment where multiple virtual network slices share a common physical infrastructure. To secure communication against future quantum computing threats, the project implements the **BB84 Quantum Key Distribution protocol** and **AES-256 GCM encryption**. In addition, the system demonstrates fault tolerance through **link failure detection**, **route recalculation**, and **automatic self-healing**.

---

## Key Features

### 5G Network Slicing

* Creation of multiple virtual network slices.
* Resource allocation using graph-based network models.
* Support for inter-slice and intra-slice communication.

### Quantum Key Distribution (QKD)

* Implementation of the BB84 protocol using Qiskit.
* Generation of secure cryptographic keys.
* Quantum-safe communication between network nodes.

### Post-Quantum Cryptography (PQC)

* AES-256 GCM encryption and decryption.
* PBKDF2-based key derivation.
* Secure data transmission using QKD-generated keys.

### Network Reliability

* Link failure simulation.
* Alternative route discovery.
* Self-healing network recovery mechanism.
* Automatic restoration of network connectivity.

### Network Visualization

* Graphical representation of network slices.
* Visualization of link failures and recovery processes.
* Resource allocation and routing analysis.

---

## System Architecture

```text
                +----------------------+
                | 5G Physical Network  |
                +----------+-----------+
                           |
         -----------------------------------------
         |                  |                    |
         |                  |                    |
   +-----------+     +-----------+      +-----------+
   | Slice 1   |     | Slice 2   |      | Slice 3   |
   +-----------+     +-----------+      +-----------+
         |                  |                    |
         -----------------------------------------
                           |
                   BB84 QKD Security
                           |
                   AES-256 GCM Encryption
                           |
                  Secure Data Transmission
                           |
                 Link Failure Detection
                           |
                  Self-Healing Recovery
```

---

## Technologies Used

| Technology   | Purpose                         |
| ------------ | ------------------------------- |
| Python       | Core Development                |
| NetworkX     | Network Graph Modeling          |
| Matplotlib   | Network Visualization           |
| NumPy        | Random Data Generation          |
| Qiskit       | BB84 Quantum Key Distribution   |
| Cryptography | AES-256 Encryption & Decryption |

---

## Project Structure

```text
Quantum-Secure-5G-Network-Slicing/
│
├── src/
│   ├── 01_network_slicing_basic.py
│   ├── 02_qkd_bb84.py
│   ├── 03_qkd_network_slicing.py
│   └── 04_complete_secure_5g_slicing.py
│
├── docs/
│   ├── Project_Report.docx
│   └── Presentation.pptx
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/kuushalie/Quantum-Secure-5G-Network-Slicing.git
cd Quantum-Secure-5G-Network-Slicing
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

Run the complete implementation:

```bash
python src/04_complete_secure_5g_slicing.py
```

---

## Workflow

1. Create multiple 5G network slices.
2. Allocate resources using graph theory.
3. Generate secure keys using BB84 QKD.
4. Derive encryption keys using PBKDF2.
5. Encrypt and decrypt data using AES-256 GCM.
6. Simulate network link failures.
7. Recompute communication routes.
8. Perform self-healing and restore connectivity.
9. Visualize the network before and after recovery.

---

## Results

The project successfully demonstrates:

* Dynamic 5G Network Slice Creation
* BB84 Quantum Key Generation
* Secure Data Encryption and Decryption
* Link Failure Detection
* Alternative Route Discovery
* Automatic Self-Healing Mechanism
* Network Visualization and Analysis

---

## Applications

* Smart Cities
* Internet of Things (IoT)
* Autonomous Vehicles
* Industrial Automation
* Healthcare Systems
* Beyond 5G and 6G Networks
* Secure Military Communications

---

## Future Enhancements

* Integration with Software Defined Networking (SDN)
* Network Function Virtualization (NFV)
* AI-based Dynamic Slice Management
* Real Quantum Hardware Deployment
* 6G Network Support
* Advanced Resource Optimization Algorithms

---

## Authors

**Asi Kuushalie**
Department of Computer Science and Engineering
Amrita School of Engineering, Bengaluru

Project Title:
**Quantum Secure and Resilient 5G Network Slicing**

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

## Acknowledgement

This project was developed as part of academic research on secure and resilient next-generation communication systems, focusing on the integration of quantum-safe security mechanisms and fault-tolerant networking in 5G environments.
