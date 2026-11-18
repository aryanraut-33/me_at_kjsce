inputs = [
    [1.0, -2, 1.5, 0],
    [1, -0.5, -2, -1.5],
    [0, 1, -1, 1.5]
]
weights = [1, -1, 0, 0.5]

def dot(x,w):
    return sum(x[i]*w[i] for i in range(len(x)))

def wt_update(weights,x,y):
    return [weights[i]+x[i]*y for i in range(len(weights))]

def bipolar(y):
    return 1 if y>=0 else -1

def binary(y):
    return 1 if y>=0 else 0

print("-"*105)

print("{:<8}{:<28}{:<10}{:<12}{:<12}{:<30}".format(
    "#", "input", "y", "bipolar ", "binary ", "new weights"
))
print("-"*105)

for idx, x in enumerate(inputs, start=1):
    y = dot(x, weights)
    bip = bipolar(y)
    bin = binary(y)

    new_wt = wt_update(weights, x, y)

    print("{:<8}{:<28}{:<10}{:<12}{:<12}{:<30}".format(
        idx, str(x), round(y,3), bip, bin, str([round(w,3) for w in new_wt])
    ))
    print("-"*105)

    weights = new_wt



    


