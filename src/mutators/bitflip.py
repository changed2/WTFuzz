import random

# Flip bits in the data at random positions 
def bit_flip(data, num_flips = 1) -> bytearray:
    data = bytearray(data)
    for _ in range(num_flips):
        bit_pos = random.randint(0, len(data) * 8 - 1)
        byte_index = bit_pos // 8
        bit_index = bit_pos % 8
        data[byte_index] ^= (1 << bit_index)
    return data
