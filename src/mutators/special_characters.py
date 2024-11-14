#!/usr/bin/env python3
import random
import unicodedata

def is_printable(char):
    return unicodedata.category(char) not in ('Cc', 'Cf', 'Cs', 'Co', 'Cn')

def random_non_ascii_characters(start=0x0080, end=0x0370, count=100):
    printable_chars = [chr(i) for i in range(start, end) if is_printable(chr(i))]
    return ''.join(random.choice(printable_chars) for _ in range(count))

def insert_special_characters(data, mutation_count=5):
    for _ in range(mutation_count):
        row = random.randint(0, len(data) - 1)
        col = random.randint(0, len(data[row]) - 1)
        special_chars = random_non_ascii_characters()
        data[row][col] += special_chars
