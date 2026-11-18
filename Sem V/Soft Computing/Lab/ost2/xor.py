import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def sigmoid_derivative(x):
    return x(1-x)

X = np.array([[0,0], [0,1], [1,0], [1,1]])
Y = np.array([0,1,1,0])

np.random.seed(1)

input_units = 2
hidden_units = 2
output_unit = 1

w_hidden = np.randon.uniform(size=(input_units, hidden_units))
b_hidden = np.random.uniform(size = (1, hidden_units))
w_output = np.random.uniform(size=(hidden_units, output_unit))
b_output = np.random.uniform (size=(1,output_unit))

lr = 0.5

for epochs in range(10000):
    z_in = np.dot(X, w_hidden) + b_hidden
    z = sigmoid(z_in)
    y_in = np.dot(z, w_output) + b_output
    y = sigmoid(y_in)

    error = Y-y
    d_output = error*sigmoid_derivative(y)
    error_hidden = d_output.dot(w_output.T)
    d_hidden = error*sigmoid(error_hidden)

    w_output = w_output + z.T.dot(d_output)*lr
    b_output = b_output + np.sum(d_output, axis = 0, keepdims=True)*lr
    w_hidden = w_hidden + X.T.dot(d_hidden)*lr
    b_hidden = b_hidden + np.sum(d_hidden, axis = 0, keepdims=True)*lr




