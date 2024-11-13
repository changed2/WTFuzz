#!/usr/bin/env python3
import random

def add_rows_and_columns(data, count=10):
    # Add random rows and columns to the CSV data
    num_rows = len(data)
    num_cols = len(data[0]) if data else 0

    for _ in range(count):
        new_row = [random.choice(random.choice(data)) for _ in range(num_cols)]
        data.append(new_row)

        for row in data:
            new_value = random.choice(random.choice(data))
            row.append(new_value)
