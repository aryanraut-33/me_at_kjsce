import matplotlib.pyplot as plt

X = [i for i in range(11)]

A = [0, 0.1, 0.3, 0.5, 0.7, 0.9, 1, 0.8, 0.6, 0.4, 0.2]
B = [1, 0.9, 0.8, 0.6, 0.4, 0.3, 0.2, 0.4, 0.6, 0.8, 1]

union = [max(A[i], B[i]) for i in range(len(X))]
intersection = [min(A[i], B[i]) for i in range (len(X))]
complement_A = [1-A[i] for i in range(len(X))]

# plotting

#a. fuzzy set plot

plt.figure(figsize=(10,6))
plt.plot(X, A, 'b', label = 'Set A', marker = 'o')
plt.plot(X, B, 'r', label = 'Set B', marker = 'x')
plt.title("Fuzzy Sets A & B")
plt.xlabel("Universe (X)")
plt.ylabel("Membership Value")
plt.legend()
plt.grid(True)
plt.show()

# b. union

plt.figure(figsize=(10,6))
plt.plot(X, union, 'm', label = 'A U B', marker = 'o')
plt.title("Fuzzy Union")
plt.xlabel("Universe (X)")
plt.ylabel("Membership Value")
plt.legend()
plt.grid(True)
plt.show()

# c. intersection

plt.figure(figsize=(10,6))
plt.plot(X, intersection, 'g', label = 'A intersects B', marker = 'o')
plt.title("Fuzzy Intersection")
plt.xlabel("Universe (X)")
plt.ylabel("Membership Value")
plt.legend()
plt.grid(True)
plt.show()

# d. complement

plt.figure(figsize=(10,6))
plt.plot(X, A, 'b--', label = 'A')
plt.plot(X, complement_A, 'k', label = 'A compliment') 
plt.title("Fuzzy Complement of A")
plt.xlabel("Universe (X)")
plt.ylabel("Membership Value")
plt.legend()
plt.grid(True)
plt.show()
