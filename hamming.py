'''
Hamming Error Correction Code
Author: David Yue

Following the intuition described here: https://www.youtube.com/watch?v=X8jsijhllIA

'''

class TwoBitError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def binstr(bits: list[bool]):
    return "".join(map(lambda b: "1" if b else "0", bits))


def xor(a, b):
    return a != b


def redundant_bit_positions(n_bits: int):
    r = 0
    positions = []

    while 2**r < n_bits + r + 1:
        positions.append(2**r)
        r += 1

    return positions


def hamming_encode(bits: list[bool]):

    pos = redundant_bit_positions(len(bits))

    total_bits = len(bits) + len(pos) + 1

    encoded_message = [False for _ in range(total_bits)]

    encoded_idx = 1
    bit_idx = 0
    j = 0
    while bit_idx < len(bits):

        if j < len(pos) and encoded_idx == pos[j]:
            encoded_message[encoded_idx] = False
            encoded_idx += 1
            j += 1
            continue

        encoded_message[encoded_idx] = bits[bit_idx]

        for k in range(total_bits.bit_length()):

            if (encoded_idx & (1 << k)) > 0:
                encoded_message[(1 << k)] = xor(
                    encoded_message[(1 << k)], bits[bit_idx])

        bit_idx += 1
        encoded_idx += 1

    for i in range(1, len(encoded_message)):
        encoded_message[0] = xor(encoded_message[i], encoded_message[0])

    return encoded_message


def hamming_decode(bits: list[bool]):
    block_parity = False

    for i in range(1, len(bits)):
        block_parity = xor(bits[i], block_parity)

    if block_parity != bits[0]:
        raise TwoBitError("A 2 bit error has been detected!")

    error_position = 0

    for i, b in enumerate(bits):

        if b:
            error_position ^= i

    if error_position != 0:

        bits[error_position] = not bits[error_position]

    positions = []
    r = 0
    while 2**r < len(bits):
        positions.append(2**r)
        r += 1

    decoded_message = []

    j = 0
    for i in range(1, len(bits)):
        if j < len(positions) and i == positions[j]:
            j += 1
            continue

        decoded_message.append(bits[i])

    return decoded_message


encoded_message = hamming_encode([True, False, False, False])
print(hamming_decode(encoded_message))
