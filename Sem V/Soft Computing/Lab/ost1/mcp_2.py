inputs = [
    [0,0],
    [0,1],
    [1,0],
    [1,1]
]

weights1 = [1,1]
weights2 = [1,-1]



def f_and(x,w):
    sum_f = sum(x[i] * w[i] for i in range(len(x)))
    theta = 2
    y = 0 if sum_f<theta else 1
    return sum_f, y

def f_andnot(x,w):
    sum_f = sum(x[i] * w[i] for i in range(len(x)))
    theta = 1
    y = 1 if sum_f >= theta else 0
    return sum_f, y

print("-"*10 + "MP Neuron for AND Gate: " + "-"*10)
print("{:<15}{:<15}{:<15}{:<25}{:<15}".format(
    "#", "x1", "x2", "sum (y_in)", "y"
))

for idx, x in enumerate(inputs, start=1):
    net, y = f_and(x, weights1)
    print("{:<15}{:<15}{:<15}{:<25}{:<15}".format(
        idx, x[0], x[1], net, y
    ))

print("-"*10 + "MP Neuron for ANDNOT Gate: " + "-"*10)
print("{:<15}{:<15}{:<15}{:<25}{:<15}".format(
    "#", "x1", "x2", "sum (y_in)", "y"
))

for idx, x in enumerate(inputs, start=1):
    net, y = f_andnot(x, weights2)
    print("{:<15}{:<15}{:<15}{:<25}{:<15}".format(
        idx, x[0], x[1], net, y
    ))




