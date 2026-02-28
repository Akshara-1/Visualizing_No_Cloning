import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.providers.basic_provider import BasicProvider
from qiskit.visualization import plot_histogram

def run_hackathon_project():
    """
    Consolidated No-Cloning Theorem Simulation for Hackathon Stage 1.
    Demonstrates how eavesdropping (cloning) creates detectable entanglement.
    """
    
    # --- 1. INITIALIZATION ---
    # We use BasicProvider to ensure the code runs on any machine without extra installs.
    # 1024 shots provide a large enough sample size for statistical accuracy.
    backend = BasicProvider().get_backend('basic_simulator')
    shots = 1024

    # --- 2. CIRCUIT DESIGN: ALICE'S PREPARATION ---
    # We use 2 qubits: q0 (Alice's message) and q1 (Eve's blank target for cloning).
    qc = QuantumCircuit(2, 2)
    
    # Hadamard (H) puts the qubit in superposition (50% |0> and 50% |1>).
    qc.h(0)            
    
    # Phase (P) gate adds a pi/4 rotation (45 degrees).
    # This ensures the state is 'unknown' and complex, making cloning impossible.
    qc.p(np.pi/4, 0)   
    
    # Barriers prevent the compiler from combining gates for optimization.
    # This keeps Alice's preparation separate from Eve's interaction.
    qc.barrier()       
    
    # --- 3. EVE'S ATTACK: THE CLONING ATTEMPT ---
    # Eve uses a CNOT (Controlled-NOT) gate to attempt a logical copy.
    # q0 is the 'Control' and q1 is the 'Target'.
    # Because q0 is in superposition, this results in ENTANGLEMENT, not a CLONE.
    qc.cx(0, 1)        
    qc.barrier()
    
    # --- 4. MEASUREMENT ---
    # We measure both qubits to see if Eve's qubit (q1) matches Alice's (q0).
    qc.measure([0, 1], [0, 1])

    # --- 5. EXECUTION & DATA PROCESSING ---
    # Transpile optimizes the circuit for the simulator's specific basis gates.
    tqc = transpile(qc, backend)
    result = backend.run(tqc, shots=shots).result()
    counts = result.get_counts()

    # --- 6. ANALYSIS: QBER (Quantum Bit Error Rate) ---
    # In the Z-basis, 00 and 11 outcomes show Alice and Eve are correlated.
    # In a perfect simulation, errors (01 or 10) are 0.
    # However, this 'perfect' correlation is the signature of an attack.
    errors = counts.get('01', 0) + counts.get('10', 0)
    qber = (errors / shots) * 100

    # --- 7. VISUALIZATION FOR PRESENTATION ---
    print("-" * 40)
    print("HACKATHON ANALYSIS REPORT")
    print("-" * 40)
    print(f"Experimental Counts: {counts}")
    print(f"Calculated QBER: {qber:.2f}%")
    print("-" * 40)

    # Creating a dual-plot figure for Slide 4 and Slide 5.
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left Plot: Histogram showing the 503/521 style counts.
    plot_histogram(counts, ax=ax1, color='midnightblue')
    ax1.set_title("Result: Entanglement Signature (00 and 11)")
    
    # Right Plot: QBER Comparison chart.
    # We show a 25% theoretical error to represent the impact of the No-Cloning law.
    categories = ['Secure Channel', 'Attacked Channel']
    values = [0.0, 25.0] # Theoretical jump in error due to interference
    ax2.bar(categories, values, color=['green', 'crimson'])
    ax2.axhline(y=11, color='black', linestyle='--', label='Security Threshold (11%)')
    ax2.set_ylabel('Error Rate (QBER) %')
    ax2.set_title("Detection Metric: QBER Analysis")
    ax2.legend()

    plt.tight_layout()
    
    # Automatically save the diagram for Slide 3.
    qc.draw('mpl', filename='cloning_circuit.png')
    print("Circuit diagram saved as 'cloning_circuit.png' for Slide 3.")
    
    plt.show()

if __name__ == "__main__":
    run_hackathon_project()
