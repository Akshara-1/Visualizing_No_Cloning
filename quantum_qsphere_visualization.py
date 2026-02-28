import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_qsphere

def generate_qsphere_proof():
    """
    Generates a QSphere to visually prove the No-Cloning Theorem.
    Nodes at 00 and 11 show entanglement; color shows the pi/4 phase.
    """
    # 1. CIRCUIT DESIGN
    qc = QuantumCircuit(2)
    
    # Alice's State Preparation
    qc.h(0)            # Superposition
    qc.p(np.pi/4, 0)   # Phase rotation (the 'unknown' factor)
    qc.barrier()
    
    # Eve's Attack (CNOT)
    qc.cx(0, 1)        # Creates entanglement instead of a copy
    
    # 2. STATE EXTRACTION
    # We look at the vector without measuring to see the full quantum 'globe'
    final_state = Statevector.from_instruction(qc)
    
    # 3. VISUALIZATION
    print("Generating QSphere for Slide 5...")
    # The QSphere shows two nodes (00 and 11) representing the Bell state.
    # The color of the '11' node will reflect the pi/4 phase shift.
    plot_state_qsphere(final_state)
    
    plt.show()

if __name__ == "__main__":
    generate_qsphere_proof()
