#!/usr/bin/env python3
import random

def add_rows_and_columns(data, mutation_count=10):
        # For each mutation, randomly add anywhere between 10-100 rows/cols.
        for _ in range(mutation_count):
            new_num_rows = random.randint(10, 100)
            new_num_cols = random.randint(10, 100)

            for _ in range(new_num_rows):
                new_row = [random.choice(data[random.randint(0, len(data) - 1)]) for _ in range(len(data[0]))]
                data.append(new_row)
                
            for _ in range(new_num_cols):
                new_values = [random.choice(data[random.randint(0, len(data) - 1)]) for _ in range(len(data))]
                for i in range(len(data)):
                    data[i].append(new_values[i])