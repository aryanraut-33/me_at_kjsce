def add_parity_bits(data):
    length = len(data)
    r = 0
    while 2 ** r < length + r + 1:
        r += 1

    total_len = length + r
    code = ['0'] * total_len

    k = 0
    for i in range(1, total_len + 1):
        if (i & (i - 1)) != 0:   # Not a power of 2 → place data bit
            code[i - 1] = data[k]
            k += 1

    parity_list = []
    for i in range(r):
        pos = 2 ** i
        bit = 0
        for j in range(1, total_len + 1):
            if j & pos:
                bit ^= int(code[j - 1])
        code[pos - 1] = str(bit)
        parity_list.append(str(bit))

    print("Sender parity bits:", ''.join(reversed(parity_list)))
    return ''.join(code)


def check_and_fix(received):
    size = len(received)
    arr = list(received)
    error = 0
    check_bits = []

    i = 0
    while 2 ** i <= size:
        pos = 2 ** i
        bit = 0
        for j in range(1, size + 1):
            if j & pos:
                bit ^= int(arr[j - 1])
        check_bits.append(str(bit))
        if bit != 0:
            error += pos
        i += 1

    print("Receiver parity check:", ''.join(reversed(check_bits)))

    if error == 0:
        print("No error found.")
    else:
        print("Error at position:", error)
        arr[error - 1] = '1' if arr[error - 1] == '0' else '0'
        print("Corrected position:", error)

    return ''.join(arr)


def extract_data(code):
    msg = []
    for i in range(1, len(code) + 1):
        if (i & (i - 1)) != 0:
            msg.append(code[i - 1])
    return ''.join(msg)


if __name__ == "__main__":
    user_data = input("Enter binary input data): ").strip()
    if not user_data or not all(b in '01' for b in user_data):
        print("Invalid input! Only 0 and or 1 allowed.")
        exit()

    encoded = add_parity_bits(user_data)
    print("Hamming code generated:", encoded)

    received_data = input(f"Enter received code (length {len(encoded)}): ").strip()
    if len(received_data) != len(encoded) or not all(b in '01' for b in received_data):
        print("Invalid received input!")
        exit()

    corrected = check_and_fix(received_data)
    print("Corrected code:", corrected)

    original = extract_data(corrected)
    print("Extracted original data:", original)
