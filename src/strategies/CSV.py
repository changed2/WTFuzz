#!/usr/bin/env python3

import csv
import random
import re
from collections import UserList
from io import StringIO

from fuzzer import random_input

class CSVObject(UserList):
    def __init__(self, data=None):
        super().__init__(data or [])
    
    # MUTATION METHODS
    def append_characters(self, mutation_count=10):
        for _ in range(mutation_count):
            # get a random row and col
            row = random.randint(1, len(self.data) - 1)
            col = random.randint(0, len(self.data[row]) - 1)
            random_str = random_input(100, ord('a'), 26)
            self.data[row][col] = str(self.data[row][col]) + random_str

    # Strategy 2: replace numbers with negatives
    def replace_with_negatives(self, mutation_count=10):
        for _ in range(mutation_count):
            row = random.randint(1, len(self.data) - 1)
            col = random.randint(0, len(self.data[row]) - 1)
            if re.match(r"^[0-9]+(\.[0-9]+)?$", self.data[row][col]):
                self.data[row][col] = "-" + self.data[row][col]

    # Strategy 3: Add more rows and columns
    def add_rows_and_cols(self, mutation_count=10):
        # For each mutation, randomly add anywhere between 10-100 rows/cols.
        for _ in range(mutation_count):
            new_num_rows = random.randint(10, 100)
            new_num_cols = random.randint(10, 100)

            for _ in range(new_num_rows):
                new_row = [random.choice(self.data[random.randint(0, len(self.data) - 1)]) for _ in range(len(self.data[0]))]
                self.append(new_row)
                
            for _ in range(new_num_cols):
                new_values = [random.choice(self.data[random.randint(0, len(self.data) - 1)]) for _ in range(len(self.data))]
                for i in range(len(self.data)):
                    self.data[i].append(new_values[i])

# Read csv file contents
def read_csv(input_file):
    data = []
    with open(input_file, mode='r') as input:
        csv_reader = csv.reader(input)
        for row in csv_reader:
            data.append(row)
    return CSVObject(data)

# Helper function to read CSV data from a string and create a CSVObject
def read_csv_from_string(csv_data):
    data = []
    csv_reader = csv.reader(StringIO(csv_data))
    for row in csv_reader:
        data.append(row)
    return CSVObject(data)

# Convert back to csv from list
def list_to_csv(csv_object):
    csv_string = ""
    for row in csv_object:
        row_string = [str(item) for item in row]
        csv_row = ",".join(row_string)
        csv_string += csv_row + "\n"
    return csv_string

# main function: csv fuzzer
def mutate_csv(csv_data):
    csv_object = read_csv_from_string(csv_data)

    csv_mutator = [csv_object.append_characters, csv_object.replace_with_negatives, csv_object.add_rows_and_cols]

    mutator = random.choice(csv_mutator)
    mutator()
    
    # Convert mutated CSVObject back to CSV string format
    fuzzed_data = list_to_csv(csv_object)
    return fuzzed_data  # Return the mutated data instead of passing it to the harness

