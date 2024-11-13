#!/usr/bin/env python3
import random
from fuzzer import random_input
def append_random_characters(data, mutation_count=10):
        for _ in range(mutation_count):
            # get a random row and col
            row = random.randint(1, len(data) - 1)
            col = random.randint(0, len(data[row]) - 1)
            random_str = random_input(100, ord('a'), 26)
            data[row][col] = str(data[row][col]) + random_str
