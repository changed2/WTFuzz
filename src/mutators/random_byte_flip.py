import random

def flip_random_bytes(data, num_flips=1):
    byte_array = bytearray(data)
    for _ in range(num_flips):
        index = random.randint(0, len(byte_array) - 1)
        byte_array[index] ^= random.randint(0x00, 0xFF) 
    return bytes(byte_array)
