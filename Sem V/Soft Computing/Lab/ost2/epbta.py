import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))  

def sigmoid_derivative(x):
    return x * (1 - x)

def backpropagation():
    print("="*70)
    print("EBPTA")
    print("="*70)
    
    w_hidden = np.array([
        [0.6, -0.3],
        [-0.1, 0.4]
    ])

    w_output = np.array([0.4, 0.1])

    b_hidden = np.array([0.3, 0.5])
    b_output = -0.2  # changed from list [-0.2] → scalar

    X = np.array([0, 1])
    t = 1

    lr = 0.25

    print("-"*50)
    print("Initial Values as per the question")
    print("-"*50)

    print(f"Weights: input->hidden ==> {w_hidden}")
    print(f"Bias: input->hidden ==> {b_hidden}")
    print(f"Weights: hidden->output ==> {w_output}")
    print(f"Bias: hidden->output ==> {b_output}")

    # forward propagation
    z_in = np.dot(X, w_hidden) + b_hidden
    z = sigmoid(z_in)

    y_in = np.dot(z, w_output) + b_output
    y = sigmoid(y_in)

    error = t - y

    # backpropagation
    delta_output = error * sigmoid_derivative(y)

    delta_hidden = sigmoid_derivative(z) * delta_output * w_output

    # weight updates
    w_output_new = w_output + lr * delta_output * z
    b_output_new = b_output + lr * delta_output

    w_hidden_new = w_hidden + lr * np.outer(X, delta_hidden)
    b_hidden_new = b_hidden + lr * delta_hidden

    print("\nFinal Results:")
    print("-"*70)
    print(f"Output [y]: {y}")
    print(f"Target [t]: {t}")
    print(f"Output error: {error}")
    print(f"Updated weights:\nHidden layer weights: {w_hidden_new}")
    print(f"Hidden layer bias: {b_hidden_new}")
    print(f"Output layer weights: {w_output_new}")
    print(f"Output layer bias: {b_output_new}")
    print("-"*70)

if __name__ == "__main__":
    backpropagation()
