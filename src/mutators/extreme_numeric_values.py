# mutators/extreme_numeric_insert.py
import random
import sys

def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def insert_extreme_numeric_values(data, mutation_count=10):
    extreme_values = [sys.maxsize, -sys.maxsize - 1, float('inf'), float('-inf'), 1.79e308, -1.79e308]
    for _ in range(mutation_count):
        possible_locations = [(row, col) for row in range(len(data)) for col in range(len(data[row])) if is_numeric(data[row][col])]
        if possible_locations:
            row, col = random.choice(possible_locations)
            extreme_value = random.choice(extreme_values)
            # Replace or modify the existing value
            data[row][col] = str(extreme_value)
