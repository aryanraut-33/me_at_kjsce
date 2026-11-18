import numpy as np

X = np.array([
    [0.25, 0.353],
    [0.25, 0.471],
    [0.50, 0.353],
    [0.50, 0.647],
    [0.75, 0.705],
    [0.75, 0.882],
    [1.00, 0.705],
    [1.00, 1.000]
])

y = np.array([0, 1, 0, 1, 0, 1, 0, 1])

X_bias = np.c_[np.ones(X.shape[0]), X]

w = np.zeros(X_bias.shape[1])
alpha = 1

print("Initial weights:", w)

for epoch in range(10):
    print(f"\nEpoch {epoch+1}")
    errors = 0
    
    for i in range(len(X_bias)):
        xi = X_bias[i]
        target = y[i]
        y_pred = 1 if np.dot(w, xi) >= 0 else 0
        delta = alpha * (target - y_pred)
        print(f"Sample {i+1}: X={xi}, Target={target}, Pred={y_pred}, "
              f"Update={delta}, Old Weights={w}", end='')
        w = w + delta * xi
        print(f", New Weights={w}")
        if delta != 0:
            errors += 1
    
    if errors == 0:
        print("Converged!")
        break

print("\nFinal Weights:", w)
