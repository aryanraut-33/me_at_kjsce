inputs = [
    [0.0,0.0],
    [0.0,1],
    [1,0.0],
    [1,1]
]

w = [0.0,0.0]
b = 0.0
lr = 0.1
bin_target = [0,0,0,1]
bip_target = [1,-1,1,-1]

def bin_activation(y_in):
    return 1 if y_in>=0 else 0

def bip_activation(y_in):
    if y_in>0:
        return 1
    elif y_in == 0:
        return 0
    else: 
        return -1

def delta_model(targets, activation_func, max_epochs = 10):
    global w,b
    w = [0.0, 0.0]
    b = 0.0

    print("Training now:")

    for epoch in range(1, max_epochs+1):
        print(f"Epoch number {epoch} ===>")
        error_count = 0
        for x, t in zip(inputs, targets):
            y_in = w[0]*x[0] + w[1]*x[1] + b

            y = activation_func(y_in)

            e = t-y

            w[0] = w[0] + lr*e*x[0]
            w[1] = w[1] + lr*e*x[1]

            b = b + lr*e
            if e !=0:
                error_count = error_count+1

            print(f"x = {x}" + "t = {t}" + "y_in = {y_in}" + "y = {y}" + "e = {e}" + "w = {w}" + "b = {b}")

    print(f"Final weight : {w}\nFinal bias : {b}")

delta_model(bin_target, bin_activation, 10)
delta_model(bip_target, bip_activation, 10)

