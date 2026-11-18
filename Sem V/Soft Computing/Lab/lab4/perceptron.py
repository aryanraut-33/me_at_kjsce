import numpy as np

def sign(x):
    return 1 if x >= 0 else -1

# Inputs
X = np.array([
    [1.0, -2.0, 0.0, -1.0],   
    [0.0, 1.5, -0.5, -1.0],    
    [-1.0, 1.0, 0.5, -1.0]   
])
d = np.array([-1, -1, 1])

w = np.array([1.0, -1.0, 0.0, 0.5])
c = 0.1

print(f"Initial weights: {w}")
print(f"c value : {c}\n")
count =0
for i in range(len(X)):
    x = X[i]
    target = d[i]
    net = 0
    
    for j in range(len(x)):
        net += w[j] * x[j]
        
    output = sign(net)
    
    print(f"Step {i+1}: x{i+1}= {x}, d{i+1} = {target}")

    if output != target:
        count+=1
        delta_w = c * (target - output) * x
        w = w + delta_w
        print(f" Correction needed: updating weights")
        print(f" x{i+1}_delta_w{count}= {delta_w}")

    else:
        print(" No correction needed")

    print(f"weights after the step {i+1} : [w{i+1}_1, w{i+1}_2, w{i+1}_3, w{i+1}_4] = {w}\n")
