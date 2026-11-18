### Delta Learning Rule – Weight Update

**Given:**
- Initial weights: \( W = [0.5, -0.5] \)  
- Learning rate: \( \eta = 1 \)  
- Input patterns:  
  - \( X_1 = [1, -1], \; t_1 = 1 \)  
  - \( X_2 = [0, 1], \; t_2 = -1 \)  

**Delta Rule:**
\[
W_{new} = W_{old} + \eta (t - y)X
\]
where \( y = W \cdot X \).

---

#### Iteration Steps

| Pattern | Input \(X\) | Target \(t\) | Output \(y\) | Error \(e = t-y\) | Weight Update | New Weights |
|---------|-------------|--------------|---------------|-------------------|---------------|--------------|
| 1 | [1, -1] | 1 | \(0.5(1) + (-0.5)(-1) = 1\) | \(1 - 1 = 0\) | No change | [0.5, -0.5] |
| 2 | [0, 1] | -1 | \(0.5(0) + (-0.5)(1) = -0.5\) | \(-1 - (-0.5) = -0.5\) | \([0.5, -0.5] + (-0.5)[0,1]\) | [0.5, -1.0] |

---

### Final Weights after one iteration:
\[
W = [0.5, -1.0]
\]
