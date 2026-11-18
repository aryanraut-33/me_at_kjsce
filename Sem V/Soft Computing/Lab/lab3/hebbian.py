weights = [1, 1, 0, 0.5]
inputs = [
    [1, -2, 1.5, 0],
    [1, -0.5, -2, -1.5],
    [0, 1, -1, 1.5]
]
def binary_activation(net):
    return 1 if net >= 0 else 0
def bipolar_activation(net):
    return 1 if net >= 0 else -1
def hebbian_update(weights, input_vec, output):
    new_weights = []
    for w, x in zip(weights, input_vec):
        new_weights.append(w + x * output)
    return new_weights
print("+-----+------+--------+--------+------------+------------------+--------------------+------------------------+")
print("| x1  |  x2  |   x3   |  x4    | Net Input  | Output (Binary)  | Output (Bipolar)   | Updated Weights        |")
print("+-----+------+--------+--------+------------+------------------+--------------------+------------------------+")
for idx, X in enumerate(inputs):
    net = weights[0]*X[0] + weights[1]*X[1] + weights[2]*X[2] + weights[3]*X[3]
    out_binary = binary_activation(net)
    out_bipolar = bipolar_activation(net)
    weights = hebbian_update(weights, X, out_bipolar)
    row = "|{:^5}|{:^6}|{:^8}|{:^8}|{:^12}|{:^18}|{:^20}|{:^24}|".format(
        X[0], X[1], X[2], X[3], round(net,2), out_binary, out_bipolar, str([round(w,2) for w in weights])
    )
    print(row)
