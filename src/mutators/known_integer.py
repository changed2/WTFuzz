import random
import sys
from typing import Iterator

KNOWN_INTS = [
    0,
    -1,
    sys.maxsize,
    -sys.maxsize,
    # Probably need more
    127,
    -128,
    255,
    32767,
    -32768,
    65535, 
    2147483647,
    -2147483648,
    *((2**i) for i in range(1, 32)),
    *((2**i - 1) for i in range(1, 32))
]

# Insert known integer values at random positions.
def known_integer_insertion(data) -> Iterator[bytearray]:
    data = bytearray(data)
    
    for known_int in KNOWN_INTS:
        mutated_data = data[:]
        
        byte_length = (known_int.bit_length() + 7) // 8 or 1
        
        try:
            int_bytes = known_int.to_bytes(byte_length, 'little', signed=True)
        except OverflowError:
            continue
        
        position = random.randint(0, max(0, len(mutated_data) - byte_length))
        
        mutated_data[position:position + byte_length] = int_bytes
        yield mutated_data

def known_integer_text() -> Iterator[bytearray]:
    for i in KNOWN_INTS:
        yield f"{i}".encode()