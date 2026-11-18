def compute_checksum(data_hex: str) -> str:
    if len(data_hex) % 4 != 0:
        raise ValueError("Input must have length multiple of 4")

    total = 0
    for i in range(0, len(data_hex), 4):
        part = int(data_hex[i:i+4], 16)
        total += part
        total = (total & 0xFFFF) + (total >> 16)

    result = ~total & 0xFFFF
    return f"{result:04X}"


if __name__ == "__main__":
    try:
        inp = input("Enter hex string of length 4n: ").strip().upper()
        final_checksum = compute_checksum(inp)
        print("16-bit checksum:", final_checksum)
    except ValueError as err:
        print("Error:", err)
