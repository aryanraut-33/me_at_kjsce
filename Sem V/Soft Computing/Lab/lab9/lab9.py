import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 1000)

# Triangular membership functions
def trimf(x, a, b, c):
    return np.maximum(np.minimum((x - a) / (b - a), (c - x) / (c - b)), 0)

# Example fuzzy sets
low = trimf(x, 0, 0, 5)
medium = trimf(x, 2, 5, 8)
high = trimf(x, 5, 10, 10)

# Fuzzy output after inference (example aggregated output)
aggregated = np.fmax(np.fmax(low * 0.3, medium * 0.6), high * 0.8)

# -------------------------------
# Defuzzification Methods
# -------------------------------

# 1. Center of Gravity (COG / Centroid)
def center_of_gravity(x, mf):
    return np.sum(x * mf) / np.sum(mf)

# 2. Mean of Maximum (MOM)
def mean_of_maximum(x, mf):
    max_val = np.max(mf)
    x_max = x[mf == max_val]
    return np.mean(x_max)

# 3. Center of Sum (COS)
# Here, assume we are summing individual fuzzy sets before normalization
def center_of_sum(x, mfs):
    num = 0
    den = 0
    for mf in mfs:
        area = np.trapz(mf, x)
        centroid = np.sum(x * mf) / np.sum(mf)
        num += area * centroid
        den += area
    return num / den

# Compute results
cog = center_of_gravity(x, aggregated)
mom = mean_of_maximum(x, aggregated)
cos = center_of_sum(x, [low, medium, high])

plt.figure(figsize=(10, 6))
plt.plot(x, low, 'b--', label='Low')
plt.plot(x, medium, 'g--', label='Medium')
plt.plot(x, high, 'r--', label='High')
plt.fill_between(x, aggregated, color='orange', alpha=0.5, label='Aggregated output')

# Plot defuzzified values
plt.axvline(cog, color='purple', linestyle='-', label=f'COG = {cog:.2f}')
plt.axvline(mom, color='black', linestyle='--', label=f'MOM = {mom:.2f}')
plt.axvline(cos, color='brown', linestyle=':', label=f'COS = {cos:.2f}')

plt.title("Defuzzification Methods Comparison")
plt.xlabel("Output variable (x)")
plt.ylabel("Membership degree")
plt.legend(loc='upper left')
plt.grid(True)
plt.show()

# Print results
print("Defuzzified Values:")
print(f"Center of Gravity (COG): {cog:.4f}")
print(f"Mean of Maximum (MOM): {mom:.4f}")
print(f"Center of Sum (COS): {cos:.4f}")
