#!/usr/bin/env python3

import csv
from mutators.negative_number_replacement import replace_numbers_with_negatives
from mutators.random_character_append import append_random_characters
from mutators.row_column_addition import add_rows_and_columns
from mutators.special_characters import insert_special_characters
from mutators.extra_comma_insert import insert_extra_commas
from mutators.extreme_numeric_values import insert_extreme_numeric_values
from mutators.simulate_eof import simulate_eof
from collections import UserList
from io import StringIO
import random

class CSVObject(UserList):
    def __init__(self, data=None):
        super().__init__(data or [])

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

    mutations = [
        append_random_characters,
        replace_numbers_with_negatives,
        add_rows_and_columns,
        insert_special_characters,
        insert_extra_commas,
        insert_extreme_numeric_values,
        simulate_eof
    ]

    mutator = random.choice(mutations)
    print(mutator)
    mutator(csv_object.data)
    
    # Convert mutated CSVObject back to CSV string format
    fuzzed_data = list_to_csv(csv_object)
    # print(fuzzed_data)
    return fuzzed_data  # Return the mutated data instead of passing it to the harness

