#!/usr/bin/env python3
import random

def random_input(max_length: int = 100, char_start: int = 32, char_range: int = 32) -> str:
    out = ""
    string_length = random.randrange(0, max_length + 1)
    for _ in range(0, string_length):
        out += chr(random.randrange(char_start, char_start + char_range))
    return out

def append_random_characters(data, mutation_count=10):
        for _ in range(mutation_count):
            # get a random row and col
            row = random.randint(1, len(data) - 1)
            col = random.randint(0, len(data[row]) - 1)
            random_str = random_input(10000, ord('a'), 26)
            data[row][col] = str(data[row][col]) + random_str
