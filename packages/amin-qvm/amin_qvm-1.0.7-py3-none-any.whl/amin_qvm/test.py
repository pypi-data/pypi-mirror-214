import numpy as np
from functions import *

# Generate training data
np.random.seed(0)
num_data = 20
train_features = np.random.normal(size=(num_data, 2))
train_labels = np.concatenate([np.ones(num_data // 2), -np.ones(num_data // 2)])

# Train the QNN
trained_weights = train_qnn(train_features, train_labels, num_layers=2, num_steps=100, stepsize=0.1)

# Test the QNN
test_data = np.array([[0.2, 0.4], [-0.3, 0.1]])
predictions = test_qnn(trained_weights, test_data)
print("Predictions:", predictions)