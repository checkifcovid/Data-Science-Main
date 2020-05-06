# This file builds a linear regression model for ?some data? predicting ?some prediction?

import os
import pathlib
import numpy as np
import pandas as pd


file_path = pathlib.Path("archive/data/data_latest.csv")
data = pd.read_csv(file_path)

# Cleaning data, matching arrays to axes
data = np.asarray(data)
X = data[:, :-1]
Y = data[:, -1] # This assumes Y is the last column?

# YB: The code below is not appropriate to use... Instead, use a fillna or dropna?
# Replacing nan value with average value of values from the same column
for column in range(X.shape[1]):
    mean = np.mean(v for v in X[:, column] if not np.isnan(v))
    X[:, column][np.isnan(X[:, column])] = mean

# Feature scaling to range[0:1]
for column in range(X.shape[1]):
    min_value = min(X[:, column])
    max_value = max(X[:, column])
    diff = max_value - min_value
    scaled_vector = list(map(lambda v: (v - min_value)/ diff, X[:, column]))
    X[:, column] = scaled_vector

# Extend data by adding x0 = 1 to each input entry point
X = np.concatenate((np.ones((X.shape[0], 1)), X), axis = 1)

# Randomize the order of data
permutation = np.random.permutation(X.shape[0])
X = X[permutation]
Y = Y[permutation]

# Use 15% of total input for testing, and the rest for training
num_test = int(0.15 * len(X))
# Training dataset
X_train = X[: -num_test]
Y_train = Y[: -num_test]
# Testing dataset
X_test = X[-num_test:]
Y_test = Y[-num_test:]
# ML application sigmoid function
def sigmoid(s):
    return 1/(1 + np.exp(-s))

# Method to train logistic regression model with the training dataset
def logistic_regression(X, Y, w_init, alpha, eps = 1e-4, max_cnt = 100000):
    w = [w_init]
    N = X.shape[0]
    d = X.shape[1]
    cnt = 0
    check_w_after = 20
    while cnt < max_cnt:
        # Randomize the order of training point in the dataset
        permutation = np.random.permutation(N)
        for i in permutation:
            xi = X[i, :].reshape(d, 1)
            yi = Y[i]
            zi = sigmoid(np.dot(w[-1].T, xi))
            w_new = w[-1] + alpha * (yi - zi) * xi
            cnt += 1
            # Stop when the weight barely changes after 20 iterations
            if cnt % check_w_after == 0:
                if np.linalg.norm(w_new - w[-check_w_after]) < eps:
                    return w
            w.append(w_new)
    return w

# Train
alpha = 0.05
d = X.shape[1]
w_init = np.random.randn(d, 1)
w = logistic_regression(X_train, Y_train, w_init, alpha)
w = w[-1]
# Test the logistic regression model with testing dataset
correctTest = 0
num_test = len(X_test)
for i in range(num_test):
    prob = np.dot(X_test[i].T, w)
    if prob >= 0.5 and Y_test[i] == 1:
        correctTest += 1
    elif prob < 0.5 and Y_test[i] == 0:
        correctTest += 1
print("Accuracy: {} %".format((correctTest / num_test) * 100))
