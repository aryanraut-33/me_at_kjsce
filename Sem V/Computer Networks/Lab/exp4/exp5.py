def dot(a, b):
    return sum(i * j for i, j in zip(a, b))

p1 = [2, 1, 0, 1]
p2 = [-1.5, 2, 0, -1]
p3 = [0, 0, 1, 1]

weights = [1, -1, 0, 0.5]
eta = 0.1
slope = 1

t1, t2, t3 = 1, -1, 1

def act_func(net):
    return 2 / (1 + (2.718281828459045 ** (-slope * net))) - 1

def act_func_deriv(output):
    return 0.5 * (1 - output**2)

def train_step(x, target, w):
    net_val = dot(w, x)
    out = act_func(net_val)
    deriv = act_func_deriv(out)
    delta = [eta * (target - out) * deriv * xi for xi in x]
    updated = [wi + di for wi, di in zip(w, delta)]

    print(f"Input={x}, η={eta}, Weights(before)={w}")
    print(f"net={net_val:.3f}, out={out:.3f}, f'={deriv:.3f}")
    print(f"Δw={delta}")
    print(f"Weights(after)={updated}\n")

    return updated

for epoch in range(1, 5):
    print(f"# Epoch {epoch} =>")
    weights = train_step(p1, t1, weights)
    weights = train_step(p2, t2, weights)
    weights = train_step(p3, t3, weights)
