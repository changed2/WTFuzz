#!/usr/bin/env python3

import random

def append_random_characters(data, count=10, max_length=100):
    # Append random characters to various fields in the CSV data.
    for _ in range(count):
        row = random.randint(1, len(data) - 1)
        col = random.randint(0, len(data[row]) - 1)
        random_str = ''.join(chr(random.randint(ord('a'), ord('z'))) for _ in range(random.randint(1, max_length)))
        data[row][col] += random_str
