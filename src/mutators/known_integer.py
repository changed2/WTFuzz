import random
import sys

KNOWN_INTS = [
    0,
    -1,
    sys.maxsize if sys.maxsize <= 2147483647 else 2147483647,
    -sys.maxsize if sys.maxsize <= 2147483647 else -2147483647,
    # Probably need more
]

# Insert known integer values at random positions.
def known_integer_insertion(data) -> bytearray:
    data = bytearray(data)
    
    # Choose a random known integer and random position
    known_int = random.choice(KNOWN_INTS)
    position = random.randint(0, len(data) - 4)
    
    # Convert integer to bytes and insert
    int_bytes = known_int.to_bytes(4, 'little', signed=True)
    data[position:position+4] = int_bytes
    return data
