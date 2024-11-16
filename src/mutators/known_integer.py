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
]

# Insert known integer values at random positions.
def known_integer_insertion(data) -> bytearray:
    """Returns a list of mutated byte sequences with known integers inserted."""
    mutated_data_list = []
    known_int = random.choice(KNOWN_INTS)  # Random known integer from the list
    position = random.randint(0, len(data) - 4)  # Random position to insert the known integer
    
    # Convert known integer to bytes
    int_bytes = known_int.to_bytes(4, 'little', signed=True)
    
    # Create a mutated byte array with the integer inserted
    mutated_data = bytearray(data)  # Copy the original data to mutate
    mutated_data[position:position + 4] = int_bytes  # Insert the integer as bytes
    
    mutated_data_list.append(mutated_data)  # Add the mutated byte array to the list
    return mutated_data_list

def known_integer_insert() -> Iterator[bytearray]:
    return (str(i).encode() for i in KNOWN_INTS)