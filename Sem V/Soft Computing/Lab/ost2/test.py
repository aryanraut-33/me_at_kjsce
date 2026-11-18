import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def sig_derivative(x):
    return x(1-x)

def backpropagation():
    #define the initial weights and bias

    w_hidden = np.array([[0.6, -0.3], [-0.1, 0.4]])
    b_hidden = np.array([0.3, 0.5])

    w_output = np.array([0.4, 0.1])
    b_output = -0.2

    X = np.array([0,1])
    t = 1
    lr = 0.25

    #forward propagation
    z_in = np.dot(X, w_hidden) + b_hidden
    z = sigmoid(z_in)

    y_in = np.dot(z, w_output) + b_output
    y = sigmoid(y_in)

    error = t - y

    #backpropagation 
    delta_output = error*sig_derivative(y)
    delta_hidden = sig_derivative(z) * delta_output * lr

    # weight update
    w_hidden_new = w_hidden + lr*np.outer(X, delta_hidden)
    b_hidden_new = b_hidden + lr * delta_hidden

    w_output_new = w_output + lr*z*delta_output
    b_output_new = b_output + lr*delta_output
