# Perceptron Learning Algorithm for AND gate (bipolar inputs/outputs)

# Training data: bipolar inputs
inputs = [
   [0.25, 0.353],
    [0.25, 0.471],
    [0.50, 0.353],
    [0.50, 0.647],
    [0.75, 0.705],
    [0.75, 0.882],
    [1.00, 0.705],
    [1.00, 1.000]
]

# Target for AND gate in bipolar form
# AND truth table: only (1,1) -> 1, rest -1
targets = ([0, 1, 0, 1, 0, 1, 0, 1])

# Initialize weights and bias
w = [0, 0]   # w1, w2
b = 0
eta = 1      # learning rate

# Activation function (sign function)
def activation(y_in):
    if y_in > 0:
        return 1
    elif y_in == 0:
        return 0
    else:
        return -1

max_epochs = 10
epoch = 0

while epoch < max_epochs:
    epoch += 1
    print(f"\nEpoch {epoch}")
    print("{:<5}{:<5}{:<5}{:<8}{:<8}{:<8}{:<8}{:<8}{:<8}{:<8}{:<8}".format(
        "x1","x2","t","y_in","y","Δw1","Δw2","Δb","w1","w2","b"
    ))

    error_count = 0

    for x, t in zip(inputs, targets):
        # Net input
        y_in = x[0]*w[0] + x[1]*w[1] + b

        # Calculated output
        y = activation(y_in)

        # Weight changes
        dw1 = eta * x[0] * (t - y)
        dw2 = eta * x[1] * (t - y)
        db  = eta * (t - y)

        # Update weights
        w[0] += dw1
        w[1] += dw2
        b += db

        # Count errors
        if y != t:
            error_count += 1

        # Print row
        print("{:<5}{:<5}{:<5}{:<8}{:<8}{:<8}{:<8}{:<8}{:<8}{:<8}{:<8}".format(
            x[0], x[1], t, y_in, y, dw1, dw2, db, w[0], w[1], b
        ))

    # Stop early if no errors
    if error_count == 0:
        print("\nTraining converged early.")
        break

print("\nTraining finished.")
print(f"Final Weights: w1={w[0]}, w2={w[1]}, Bias={b}")