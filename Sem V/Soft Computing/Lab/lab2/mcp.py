def mcp_nand(x1, x2):
    total_sum = x1 + x2
    theta = 2
    y = 0 if total_sum >= theta else 1
    return total_sum, y

def mcp_and(x1, x2):
    total_sum = x1 + x2
    theta = 2
    y = 1 if total_sum >= theta else 0
    return total_sum, y

def mcp_not(x):
    total_sum = 1 - x
    theta = 1
    y = 1 if total_sum >= theta else 0
    return total_sum, y

def print_table(title, headers, rows):
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(headers, *rows)]
    border = "+".join("-" * (w + 2) for w in col_widths)
    border = f"+{border}+"
    
    print(f"\n=== {title} ===")
    print(border)
    print("| " + " | ".join(h.ljust(w) for h, w in zip(headers, col_widths)) + " |")
    print(border)
    for row in rows:
        print("| " + " | ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths)) + " |")
    print(border)

# NAND Table
nand_rows = [(x1, x2, s, y) for x1 in [0, 1] for x2 in [0, 1] for s, y in [mcp_nand(x1, x2)]]
print_table("NAND Gate (McCulloch-Pitts Neuron)", ["X1", "X2", "Sum", "Y"], nand_rows)

# AND Table
and_rows = [(x1, x2, s, y) for x1 in [0, 1] for x2 in [0, 1] for s, y in [mcp_and(x1, x2)]]
print_table("AND Gate (McCulloch-Pitts Neuron)", ["X1", "X2", "Sum", "Y"], and_rows)

# NOT Table
not_rows = [(x, s, y) for x in [0, 1] for s, y in [mcp_not(x)]]
print_table("NOT Gate (McCulloch-Pitts Neuron)", ["X", "Sum", "Y"], not_rows)
