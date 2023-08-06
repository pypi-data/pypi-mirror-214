import numpy as np
from functions import custom_quantum_machine_learning

# Generate custom training and testing data
X_train = np.random.rand(100, 2)
Y_train = np.random.choice([-1, 1], 100)
X_test = np.random.rand(20, 2)
Y_test = np.random.choice([-1, 1], 20)

# Define the parameters
num_qubits = 2
num_layers = 4
num_steps = 100

# Perform custom quantum machine learning
accuracy = custom_quantum_machine_learning(X_train, Y_train, X_test, Y_test, num_qubits, num_layers, num_steps)
print("Accuracy (custom):", accuracy)
