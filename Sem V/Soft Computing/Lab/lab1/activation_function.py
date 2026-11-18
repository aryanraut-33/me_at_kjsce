import math
import matplotlib.pyplot as plt

x = [x for x in range(-100, 110)]

def identity(x):
    return x

y1 = [identity(i) for i in x]

# plt.plot(x, y1, label='Identity Function')
# plt.title('Identity Function')
# plt.xlabel('x')
# plt.ylabel('Identity(x)')
# plt.legend()
# plt.show()

def step_unipolar(x):
    return 1 if x >= 0 else 0

y2 = [step_unipolar(i) for i in x]

# plt.plot(x, y2, label='Unipolar Step Function', color='orange')
# plt.title('Unipolar Step Function')
# plt.xlabel('x')
# plt.ylabel('Unipolar Step(x)')
# plt.legend()
# plt.show()

def step_bipolar(x):
    return 1 if x >= 0 else -1

y3 = [step_bipolar(i) for i in x]
# plt.subplot(5, 1, 3)
# plt.plot(x, y3, label='Bipolar Step Function', color='green')
# plt.title('Bipolar Step Function')
# plt.xlabel('x')
# plt.ylabel('Bipolar Step(x)')
# plt.legend()
# plt.show()

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

y4 = [sigmoid(i) for i in x]
# plt.plot(x, y4, label='Sigmoid Function', color='red')
# plt.title('Sigmoid Function')
# plt.xlabel('x')
# plt.ylabel('Sigmoid(x)')
# plt.legend()
# plt.show()

def bipolar_sigmoid(x):
    return (1-math.exp(-x))/(1+math.exp(-x))

y6 = [bipolar_sigmoid(i) for i in x]
# plt.plot(x, y6, label = 'Bipolar Sigmoid', color = 'red')
# plt.title('Bipolar Sigmoid')
# plt.xlabel('x')
# plt.ylabel('bipolar_sigmoid(x)')
# plt.show()

def ramp(x, theta):
    return x/math.cos(theta) if x >= 0 else 0

y7 = [ramp(i, math.pi/4) for i in x]

# plt.plot(x,y7, color='red')
# plt.xlabel('x')
# plt.ylabel('Ramp(x)')
# plt.title('Ramp Function')
# plt.show()
    
def relu(x):
    return max(0,x)

y5 = [ramp(i, math.pi/2) for i in x]

plt.plot(x, y5, label='Ramp Function', color='purple')
plt.title('Ramp Function')
plt.xlabel('x')
plt.ylabel('Ramp(x)')
plt.legend()
plt.grid()
plt.show()



