# mutators/extra_comma_insert.py
import random

def insert_extra_commas(data, mutation_count=10, max_extra_commas=3):
    for _ in range(mutation_count):
        if len(data) > 0:
            row = random.randint(0, len(data) - 1)
            if len(data[row]) > 0:
                # Choose a random position
                for _ in range(random.randint(1, max_extra_commas)):
                    col = random.randint(0, len(data[row]) - 1)
                    data[row][col] += ','
