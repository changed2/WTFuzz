import random

# Flip entire bytes in the data at random positions.
def byte_flip(data: bytearray, num_flips: int = 1) -> bytearray:
    data = bytearray(data)
    for _ in range(num_flips):
        byte_index = random.randint(0, len(data) - 1)
        data[byte_index] ^= 0xFF  # Flip all bits in the byte
    return data
