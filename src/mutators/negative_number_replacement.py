#!/usr/bin/env python3

import random
import re

def replace_numbers_with_negatives(data, count=10):
    # Replace numeric values with their negative equivalents in CSV data.
    for _ in range(count):
        row = random.randint(1, len(data) - 1)
        col = random.randint(0, len(data[row]) - 1)
        if re.match(r"^[0-9]+(\.[0-9]+)?$", data[row][col]):
            data[row][col] = "-" + data[row][col]
